package com.michaellossos.yelp;

import org.junit.Assert;

import com.michaellossos.yelp.common.HighlightTestPatterns;
import com.michaellossos.yelp.common.TesterBase;

/**
 * Performs a check against an ISearchHighlighter.
 * 
 * @author Michael Lossos <michaellossos@gmail.com>
 * 
 */
public class SearchHighlighterTester extends TesterBase {
    private int maxSnippetLength = 200;

    public SearchHighlighterTester() {
    }

    public SearchHighlighterTester(int maxSnippetLength) {
        this.maxSnippetLength = maxSnippetLength;
    }

    @Override
    public String check() {
        ISearchHighlighter highlighter = new SearchHighlighterFactory()
            .createSearchHighlighter(maxSnippetLength);
        String actualSnippet = highlighter.highlightDoc(doc, searchTerms);
        System.out.println("SearchHighlighter result:");
        System.out.println("" + actualSnippet);
        System.out.println();
        Assert.assertEquals(expectedHighlightedDoc, actualSnippet);
        Assert.assertFalse(HighlightTestPatterns
            .hasConsecutiveHighlights(actualSnippet));
        return actualSnippet;
    }
}
