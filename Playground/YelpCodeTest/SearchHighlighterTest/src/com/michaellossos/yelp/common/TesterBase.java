package com.michaellossos.yelp.common;

public abstract class TesterBase implements ITester {
    protected String searchTerms;
    protected String doc;
    protected String expectedHighlightedDoc;

    @Override
    public abstract String check();

    @Override
    public void init(String searchTerms, String doc,
        String expectedHighlightedDoc) {
        this.searchTerms = searchTerms;
        this.doc = doc;
        this.expectedHighlightedDoc = expectedHighlightedDoc;
    }
}
