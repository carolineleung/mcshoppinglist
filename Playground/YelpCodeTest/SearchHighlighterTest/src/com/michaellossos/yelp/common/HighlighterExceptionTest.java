package com.michaellossos.yelp.common;

import org.junit.Test;

public class HighlighterExceptionTest {
    @Test
    public void increaseHighlighterExceptionCoverage() {
        new HighlighterException();
        new HighlighterException("");
        new HighlighterException("", new HighlighterException());
        new HighlighterException(new HighlighterException());
    }
}
