package com.michaellossos.yelp.common;

import java.util.regex.Pattern;

public class HighlightTestPatterns {
    private static final Pattern CONSECUTIVE_HIGHLIGHTS_BEGIN_FIRST;
    private static final Pattern CONSECUTIVE_HIGHLIGHTS_END_FIRST;

    static {
        String s1 = Pattern.quote(HighlighterConstants.BEGIN_HIGHLIGHT) + "\\s"
            + Pattern.quote(HighlighterConstants.END_HIGHLIGHT);
        CONSECUTIVE_HIGHLIGHTS_BEGIN_FIRST = Pattern.compile(s1);
        String s2 = Pattern.quote(HighlighterConstants.END_HIGHLIGHT) + "\\s"
            + Pattern.quote(HighlighterConstants.BEGIN_HIGHLIGHT);
        CONSECUTIVE_HIGHLIGHTS_END_FIRST = Pattern.compile(s2);
    }

    /**
     * @return true if begin [[HIGHLIGHT]] [[ENDHIGHLIGHT]] with only whitespace
     *         between (or end..begin).
     */
    public static boolean hasConsecutiveHighlights(String highlightedDoc) {
        if (highlightedDoc == null) {
            return false;
        }
        return CONSECUTIVE_HIGHLIGHTS_BEGIN_FIRST.matcher(highlightedDoc)
            .find()
            || CONSECUTIVE_HIGHLIGHTS_END_FIRST.matcher(highlightedDoc).find();
    }
}
