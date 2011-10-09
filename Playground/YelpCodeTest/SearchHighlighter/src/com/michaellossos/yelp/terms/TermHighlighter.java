package com.michaellossos.yelp.terms;

import java.util.Set;
import java.util.regex.Matcher;

import com.michaellossos.yelp.common.HighlighterConstants;
import com.michaellossos.yelp.common.HighlighterException;
import com.michaellossos.yelp.common.SharedPatterns;

/**
 * Highlight the specified terms in a (string) document.
 * 
 * @author Michael Lossos <michaellossos@gmail.com>
 * 
 */
public class TermHighlighter {

    private final Set<String> highlightTerms;

    /**
     * 
     * @param searchTerms
     *            the words to highlight.
     */
    public TermHighlighter(String searchTerms) {
        this.highlightTerms = TermParser.parseTerms(searchTerms, null);
    }

    /**
     * 
     * @param searchTerms
     *            the words to highlight. Terms must be lowercase, trimmed
     */
    public TermHighlighter(Set<String> searchTerms) {
        this.highlightTerms = searchTerms;
    }

    private WordPunctuation splitOnPunctuation(String word) {
        String returnWord = word;
        String returnPunctuation = null;
        Matcher matcher = SharedPatterns.PUNCTUATION_PATTERN.matcher(word);
        if (matcher.find()) {
            /*
             * Assumes punctuation is at the end of the word.
             */
            returnWord = word.substring(0, matcher.start());
            returnPunctuation = word.substring(matcher.start(), word.length());
        }
        return new WordPunctuation(returnWord, returnPunctuation);
    }

    private boolean isSearchTerm(String word) {
        if (word == null) {
            throw new HighlighterException("Invalid word: " + word);
        }
        String term = TermParser.sanitizeTerm(word);
        return highlightTerms.contains(term);
    }

    /**
     * @return the entire doc with all search terms highlighted.
     */
    public String getHighlightedDoc(String doc) {
        if (doc == null || doc.length() == 0) {
            return doc;
        }
        Matcher matcher = SharedPatterns.WORD_ANYWHERE_PATTERN.matcher(doc);
        StringBuilder highlighted = new StringBuilder();
        // Track where we are in the doc.
        // This will allow us to preserve whitespace between word matches.
        int currentDocPosition = 0;
        boolean highlighting = false;
        while (currentDocPosition < doc.length() && matcher.find()) {
            // We need the word start/end index, so can't use StringTokenizer.
            int wordStart = matcher.start();
            int wordEnd = matcher.end();
            if (wordStart < 0 || wordEnd <= wordStart
                || currentDocPosition >= wordEnd) {
                throw new HighlighterException("Invalid state.");
            }

            String word = doc.substring(wordStart, wordEnd);
            String scrubbedWord = TermParser.sanitizeTerm(word);
            if (isSearchTerm(scrubbedWord)) {
                //
                // The word is a search term, highlight it.
                //
                String contentSubstr = doc.substring(currentDocPosition,
                    wordStart);
                // Include the whitespace up to the word start.
                highlighted.append(contentSubstr);
                if (!highlighting) {
                    highlighting = true;
                    highlighted.append(HighlighterConstants.BEGIN_HIGHLIGHT);
                }
                // Add the highlighted word.
                // If the word includes punctuation, avoid highlighting the punctuation.
                // TODO This will also highlight commas, quotes, and other non-sentence-stop punctuation.
                WordPunctuation wordPunc = splitOnPunctuation(word);
                highlighted.append(wordPunc.getWord());

                if (wordPunc.getPunctuation() != null) {
                    // Don't higlight across sentences.
                    highlighting = false;
                    highlighted.append(HighlighterConstants.END_HIGHLIGHT);
                    highlighted.append(wordPunc.getPunctuation());
                }
            } else {
                //
                // The word is not a search term.
                //
                if (highlighting) {
                    // If highlighting started previously, end it here, 
                    // since this word is not a search term.
                    highlighting = false;
                    highlighted.append(HighlighterConstants.END_HIGHLIGHT);
                }
                // No highlight on this word.
                String contentSubstr = doc.substring(currentDocPosition,
                    wordEnd);
                highlighted.append(contentSubstr);
            }
            currentDocPosition = wordEnd;
        }
        if (highlighting) {
            // If the sentence ended with a search term and no punctuation.
            highlighted.append(HighlighterConstants.END_HIGHLIGHT);
        }
        if (currentDocPosition == 0) {
            // No matches, no highlights, just return the original.
            return doc;
        }
        return highlighted.toString();
    }

    /**
     * Store words and punctuation separately.
     */
    private static class WordPunctuation {
        private final String word;
        private final String punctuation;

        public WordPunctuation(String word, String punctuation) {
            this.word = word;
            this.punctuation = punctuation;
        }

        public String getWord() {
            return word;
        }

        public String getPunctuation() {
            return punctuation;
        }
    }
}
