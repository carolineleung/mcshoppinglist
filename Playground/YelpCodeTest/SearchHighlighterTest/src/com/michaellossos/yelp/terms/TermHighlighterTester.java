package com.michaellossos.yelp.terms;

import org.junit.Assert;

import com.michaellossos.yelp.common.HighlightTestPatterns;
import com.michaellossos.yelp.common.TesterBase;

/**
 * Performs a check against a TermHighlighter.
 * 
 * @author Michael Lossos <michaellossos@gmail.com>
 * 
 */
public class TermHighlighterTester extends TesterBase {

    @Override
    public String check() {
        TermHighlighter highlighter = new TermHighlighter(searchTerms);
        String actualSnippet = highlighter.getHighlightedDoc(doc);
        Assert.assertEquals(expectedHighlightedDoc, actualSnippet);
        Assert.assertFalse(HighlightTestPatterns
            .hasConsecutiveHighlights(actualSnippet));
        return actualSnippet;
    }
}
