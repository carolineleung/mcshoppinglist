package com.michaellossos.yelp.fragmenter;

import com.michaellossos.yelp.common.HighlighterException;

/**
 * Represents a fragment of a document. This may be a sentence, or part of a
 * sentence.
 * 
 * @author Michael Lossos <michaellossos@gmail.com>
 * 
 */
public class Fragment {
    private int score;
    private final String fragmentText;
    private final String docFullText;
    private final int fragmentStartIndex;

    /**
     * @param fragmentText
     *            the text of the fragment.
     * @param docFullText
     *            the full text of the document.
     * @param fragmentStartIndex
     *            the start of the fragment text in the document.
     */
    public Fragment(String fragmentText, String docFullText,
        int fragmentStartIndex) {
        if (docFullText == null) {
            throw new HighlighterException("Invalid docFullText");
        }
        if (fragmentStartIndex < 0) {
            throw new HighlighterException("Invalid fragmentStartPosition");
        }
        this.fragmentText = fragmentText;
        this.docFullText = docFullText;
        this.fragmentStartIndex = fragmentStartIndex;
    }

    /**
     * @param amount
     *            increases the score by the amount, must be > 0.
     */
    public void incrementScore(int amount) {
        if (amount <= 0) {
            throw new HighlighterException("Invalid score amount.");
        }
        score += amount;
    }

    public int getScore() {
        return score;
    }

    /**
     * @return a substring of the fragment text.
     */
    public String substring(int length) {
        int endIndex = fragmentStartIndex + length;
        if (endIndex > docFullText.length()) {
            endIndex = docFullText.length();
        }
        return docFullText.substring(fragmentStartIndex, endIndex);
    }

    /**
     * @return the fragment text.
     */
    public String getFragmentText() {
        return fragmentText;
    }

    public int length() {
        return fragmentText.length();
    }

    @Override
    public String toString() {
        return getFragmentText();
    }
}