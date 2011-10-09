package com.michaellossos.yelp.common;

/**
 * Constants related to highlighting.
 * 
 * @author Michael Lossos <michaellossos@gmail.com>
 */
public class HighlighterConstants {
    /**
     * Cannot instantiate.
     */
    private HighlighterConstants() {
    }

    /**
     * Token that indicates the start of highlighting.
     */
    public static final String BEGIN_HIGHLIGHT = "[[HIGHLIGHT]]";
    /**
     * Token that indicates the end of highlighting.
     */
    public static final String END_HIGHLIGHT = "[[ENDHIGHLIGHT]]";
}
