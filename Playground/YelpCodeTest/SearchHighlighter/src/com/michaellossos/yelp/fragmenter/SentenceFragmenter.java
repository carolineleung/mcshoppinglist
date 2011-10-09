package com.michaellossos.yelp.fragmenter;

import java.util.ArrayList;
import java.util.List;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

import com.michaellossos.yelp.common.HighlighterException;
import com.michaellossos.yelp.common.SharedPatterns;

/**
 * Split text into fragments by length or by sentence stop punctuation
 * characters (.!?).
 * 
 * @author Michael Lossos <michaellossos@gmail.com>
 * 
 */
public class SentenceFragmenter {
    private static final Pattern END_WORD_PATTERN = Pattern.compile("\\S+$");
    private final int fragmentLength;

    public SentenceFragmenter(int fragmentLength) {
        this.fragmentLength = fragmentLength;
    }

    private class SentenceFragmenterImpl {
        private final String doc;
        private int currentDocIndex = 0;
        private List<Fragment> fragments = new ArrayList<Fragment>();
        private final Matcher punctMatcher;

        public SentenceFragmenterImpl(String doc) {
            this.doc = doc;
            punctMatcher = SharedPatterns.PUNCTUATION_PATTERN.matcher(doc);
        }

        private int getSafeFragmentEndIndex(int targetEndIndex) {
            int endIndex = targetEndIndex;
            // There's no need for additional checks if we're at the end of the doc.
            if (endIndex + 1 <= doc.length()) {
                /*
                 * Detect if we're splitting the fragment in the middle of the
                 * word by sampling the two characters at the end of this
                 * fragment and the beginning of the next.
                 */
                String endChars = doc.substring(endIndex - 1, endIndex + 1);
                Matcher wordMatcher = SharedPatterns.WORD_ONLY_PATTERN
                    .matcher(endChars);
                if (wordMatcher.matches()) {
                    // Prevent splitting in the middle of a word.
                    Matcher endCharsPunctMatcher = SharedPatterns.PUNCTUATION_PATTERN
                        .matcher(endChars);
                    if (endCharsPunctMatcher.find()) {
                        /*
                         * If the end chars include punctuation, we can split
                         * after that. The start index of the punctuation will
                         * often be 0 (have no effect on endIndex), but this
                         * handles the odd case of endChars "x."
                         */
                        // TODO Handle contiguous punctuation, such as "..."
                        endIndex += endCharsPunctMatcher.start();
                    } else {
                        // Otherwise, split before the last word in the fragment.
                        String invalidFragment = doc.substring(currentDocIndex,
                            endIndex);
                        // Match all the word characters up until whitespace or non-terminating punctuation.
                        Matcher m = END_WORD_PATTERN.matcher(invalidFragment);
                        if (!m.find()) {
                            throw new HighlighterException(
                                "Expected a word character at "
                                    + "the end of the fragment.");
                        }
                        // The new endIndex for this fragment comes before the word that spans two fragments.
                        endIndex = m.start() + currentDocIndex;

                        if (endIndex == currentDocIndex) {
                            /*
                             * Handle the unusual case of one long single word
                             * longer than the max fragment length. Find the
                             * next whitespace or punctuation and keep the long
                             * word as a single fragment.
                             */
                            String docRemaining = doc
                                .substring(currentDocIndex);
                            Matcher whitespaceMatcher = SharedPatterns.WHITESPACE_PATTERN
                                .matcher(docRemaining);
                            if (whitespaceMatcher.find()) {
                                endIndex = whitespaceMatcher.start();
                            } else {
                                /*
                                 * If there's no whitespace in the rest of the
                                 * doc, the fragment ends at the end of the doc.
                                 */
                                endIndex = doc.length();
                            }
                        }
                    }
                }
            }
            if (endIndex <= currentDocIndex || endIndex > doc.length()) {
                throw new HighlighterException("Invalid endIndex " + endIndex
                    + " for currentDocIndex " + currentDocIndex
                    + " doc length " + doc.length());
            }
            return endIndex;
        }

        private void addFragment(int targetEndIndex) {
            int endIndex = getSafeFragmentEndIndex(targetEndIndex);
            // Add the fragment.
            String fragmentText = doc.substring(currentDocIndex, endIndex);
            fragments.add(new Fragment(fragmentText, doc, currentDocIndex));
            currentDocIndex += fragmentText.length();
        }

        public List<Fragment> createFragments() {
            fragments = new ArrayList<Fragment>();

            /*
             * Find the first sentence terminating punctuation, or get the
             * substring up to the fragmentLength.
             */
            while (punctMatcher.find()) {
                /*
                 * If the punctuation ends beyond the fragment length, add
                 * fragments until we get near the punctuation.
                 */
                while (punctMatcher.end() - currentDocIndex > fragmentLength) {
                    if (currentDocIndex + fragmentLength > doc.length()) {
                        throw new HighlighterException(
                            "The punctuation matcher returned a "
                                + "position beyond the end of the document.");
                    }
                    int endIndex = currentDocIndex + fragmentLength;
                    // Add a fragment without punctuation.
                    addFragment(endIndex);
                }
                /*
                 * If there is a remaining fragment between the currentDocIndex
                 * and the punctuation.
                 */
                // TODO This can result in shorter than requested fragments.  
                if (punctMatcher.end() > currentDocIndex) {
                    // Add a fragment with punctuation.
                    addFragment(punctMatcher.end());
                }
            }
            // No punctuation found if currentDocPosition == 0.
            // No ending punctuation found if currentDocPosition < doc.length().
            if (currentDocIndex == 0 || currentDocIndex < doc.length()) {
                // Split by fragment lengths.
                while (currentDocIndex < doc.length()) {
                    int endIndex = currentDocIndex + fragmentLength;
                    if (endIndex > doc.length()) {
                        endIndex = doc.length();
                    }
                    // Add a fragment without punctuation.
                    addFragment(endIndex);
                }
            }
            return fragments;
        }
    }

    /**
     * Splits the doc string into individual fragments by sentence stop
     * punctuation (.?!) and by limiting the length of the fragments.
     */
    public List<Fragment> createFragments(String doc) {
        SentenceFragmenterImpl fragmenter = new SentenceFragmenterImpl(doc);
        return fragmenter.createFragments();
    }
}