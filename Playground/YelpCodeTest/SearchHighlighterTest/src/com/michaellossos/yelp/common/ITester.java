package com.michaellossos.yelp.common;

public interface ITester {
    void init(String searchTerms, String doc, String expectedHighlightedDoc);

    /**
     * Run the ISearchHighlighter and perform assertions.
     * 
     * @return the snippet.
     */
    String check();
}
