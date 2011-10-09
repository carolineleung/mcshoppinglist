package com.michaellossos.yelp;

import java.util.List;
import java.util.Set;
import java.util.StringTokenizer;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

import com.michaellossos.yelp.common.HighlighterException;
import com.michaellossos.yelp.fragmenter.Fragment;
import com.michaellossos.yelp.fragmenter.SentenceFragmenter;
import com.michaellossos.yelp.terms.TermHighlighter;
import com.michaellossos.yelp.terms.TermParser;

/**
 * Highlight search terms in a document.
 * 
 * @author Michael Lossos <michaellossos@gmail.com>
 * 
 */
public class SearchHighlighter implements ISearchHighlighter {
    /**
     * Pattern to remove newlines and tabs.
     */
    private static final Pattern sanitizePattern = Pattern
        .compile("[\\t\\n\\r]+");
    /**
     * The length of the fragments that the document will be split into.
     */
    private static final int DEFAULT_FRAGMENT_LENGTH = 20;
    /**
     * Search query terms that add no value to search results.
     */
    private static final String[] JUNK_TERMS_TO_EXCLUDE = { "I", "me", "that",
        "this", "a", "the", "an", "you", "we", "us", "he", "she", "but", "and" };
    /**
     * Desired max length of the snippet.
     */
    private final int maxSnippetLength;

    /**
     * @param maxSnippetLength
     *            Desired max length of the snippet.
     */
    public SearchHighlighter(int maxSnippetLength) {
        this.maxSnippetLength = maxSnippetLength;
    }

    /*
     * TODO Rather than removing newlines, they could be treated like sentence
     * stops when fragmenting.
     */
    /**
     * Replace newlines and tabs and with spaces.
     */
    private String sanitize(String text) {
        Matcher matcher = sanitizePattern.matcher(text);
        return matcher.replaceAll(" ");
    }

    /**
     * Score each fragment based on how many search terms it has. Consecutive
     * search terms further increase the score of the fragment.
     * 
     * @param fragments
     *            the fragments to score.
     * @param terms
     *            search terms.
     * @return index in the fragments list of the highest scoring fragment.
     */
    private int getHighestScoreFragmentIndex(List<Fragment> fragments,
        Set<String> terms) {
        int highestScoreFragIndex = 0;
        // TODO These loops are inefficient. Measure performance on large documents with many terms.
        for (int fragIndex = 0; fragIndex < fragments.size(); ++fragIndex) {
            Fragment frag = fragments.get(fragIndex);
            // Break the fragment into words (roughly).
            StringTokenizer tokenizer = new StringTokenizer(
                frag.getFragmentText());
            // Track consecutive terms.
            int matchedLastWord = 0;
            while (tokenizer.hasMoreTokens()) {
                String word = tokenizer.nextToken();
                word = TermParser.sanitizeTerm(word);
                if (terms.contains(word)) {
                    // Increment the score when there's a matching term.
                    frag.incrementScore(1);

                    if (matchedLastWord > 0) {
                        /*
                         * Increase the score more when there are consecutive
                         * search terms.
                         */
                        frag.incrementScore(matchedLastWord);
                    }
                    ++matchedLastWord;

                    // Track the highest scoring fragment.
                    Fragment highestScoreFrag = fragments
                        .get(highestScoreFragIndex);
                    if (frag.getScore() > highestScoreFrag.getScore()
                        && fragIndex != highestScoreFragIndex) {
                        highestScoreFragIndex = fragIndex;
                    }
                } else {
                    matchedLastWord = 0;
                }
            }
        }
        return highestScoreFragIndex;
    }

    /**
     * Create a snippet from the highest scoring fragment and, when length
     * permits, adjacent fragments.
     * 
     * @param fragments
     *            fragments to use for the snippet.
     * @param highestScoreFragIndex
     *            the index in the fragments list of the highest score.
     * @return a snippet comprised of one or more fragments.
     */
    private String createSnippetWithAdjacentFragments(List<Fragment> fragments,
        int highestScoreFragIndex) {
        // TODO We could improve the snippet quality by checking the score of adjacent fragments before adding them.
        // Track a decreasing index (fragments before high score frag).
        int prevIndex = highestScoreFragIndex - 1;
        // Track a increasing index (fragments after high score frag).
        int nextIndex = highestScoreFragIndex + 1;
        Fragment highestScoreFrag = fragments.get(highestScoreFragIndex);
        // The snippet must include the highest scoring fragment.
        String snippet = highestScoreFrag.getFragmentText();
        while (snippet.length() < maxSnippetLength
            && (prevIndex >= 0 || nextIndex < fragments.size())) {
            if (prevIndex >= 0) {
                // Attempt to add the earlier fragment. 
                Fragment frag = fragments.get(prevIndex);
                if (snippet.length() + frag.length() > maxSnippetLength) {
                    // Stop looking at previous fragments.
                    prevIndex = -1;
                } else {
                    // Add the fragment before the snippet.
                    snippet = frag.getFragmentText() + snippet;
                    --prevIndex;
                }
            }
            if (nextIndex < fragments.size()
                && snippet.length() < maxSnippetLength) {
                // Attempt to add the later fragment.
                Fragment frag = fragments.get(nextIndex);
                if (snippet.length() + frag.length() > maxSnippetLength) {
                    // Stop looking at next fragments.
                    nextIndex = fragments.size() + 1;
                } else {
                    // Add the fragment after the snippet.
                    snippet = snippet + frag.getFragmentText();
                    ++nextIndex;
                }
            }
        }
        return snippet;
    }

    /**
     * Create a snippet from doc fragments.
     */
    private String createSnippet(List<Fragment> fragments,
        int highestScoreFragIndex) {
        Fragment highestScoreFrag = fragments.get(highestScoreFragIndex);
        String snippet = "";
        if (highestScoreFrag.length() >= maxSnippetLength) {
            // The fragment is larger than the snippet that we can return.
            /*
             * TODO Ensure that the fragment we return here contains the search
             * terms, i.e. that the search terms are not truncated by the
             * substring. This check is not really needed when the fragment
             * length is less than the snippet length.
             */
            snippet = highestScoreFrag.substring(maxSnippetLength);
        } else {
            /*
             * The high scoring fragment is smaller than the snippet length, so
             * we can return more fragments. Add adjacent fragments for context.
             */
            snippet = createSnippetWithAdjacentFragments(fragments,
                highestScoreFragIndex);
        }
        return snippet;
    }

    private int getFragmentLength(String query) {
        int fragmentLength = DEFAULT_FRAGMENT_LENGTH;
        if (query != null && query.length() > fragmentLength) {
            /*
             * Try for better results by increasing the fragment length when
             * there are many search terms.
             */
            int multiple = (int) Math.ceil((double) query.length()
                / fragmentLength);
            fragmentLength = multiple * fragmentLength;
        }
        return fragmentLength;
    }

    /**
     * 
     * @param doc
     *            the sanitized doc.
     * @param query
     *            the original query (not sanitized).
     * @param terms
     *            the sanitized search terms from the query.
     * @return the highlighted document snippet.
     */
    private String highlightDoc(String doc, String query, Set<String> terms) {
        int fragmentLength = getFragmentLength(query);
        SentenceFragmenter fragmenter = new SentenceFragmenter(fragmentLength);
        // Split the doc into fragments by sentences or fragment length.
        List<Fragment> fragments = fragmenter.createFragments(doc);
        if (fragments == null || fragments.size() < 1) {
            throw new HighlighterException(
                "Failed to create document fragments. "
                    + "There must be at least one fragment.");
        }
        int highestScoreFragIndex = getHighestScoreFragmentIndex(fragments,
            terms);

        String snippet = createSnippet(fragments, highestScoreFragIndex);
        TermHighlighter highlighter = new TermHighlighter(terms);
        snippet = snippet.trim();
        snippet = highlighter.getHighlightedDoc(snippet);
        return snippet;
    }

    @Override
    public String highlightDoc(String doc, String query) {
        if (doc == null || doc.length() == 0) {
            return doc;
        }
        String scrubbedQuery = sanitize(query);
        /*
         * TODO Sanitizing the entire doc is potentially expensive for large
         * docs. We could instead fold sanitizing into the fragment analysis.
         */
        String scrubbedDoc = sanitize(doc);
        Set<String> terms = TermParser.parseTerms(scrubbedQuery,
            JUNK_TERMS_TO_EXCLUDE);
        return highlightDoc(scrubbedDoc, query, terms);
    }
}
