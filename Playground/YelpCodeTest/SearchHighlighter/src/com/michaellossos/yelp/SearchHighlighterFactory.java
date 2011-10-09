package com.michaellossos.yelp;

/**
 * Factory for ISearchHighlighter.
 * 
 * @author Michael Lossos <michaellossos@gmail.com>
 * 
 */
public class SearchHighlighterFactory {
    public ISearchHighlighter createSearchHighlighter(int maxSnippetLength) {
        return new SearchHighlighter(maxSnippetLength);
    }
}
