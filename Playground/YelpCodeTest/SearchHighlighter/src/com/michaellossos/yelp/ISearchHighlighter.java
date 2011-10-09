package com.michaellossos.yelp;

/**
 * Highlight search terms in a document. This is the main interface for the Yelp
 * Code Test implementation.
 * 
 * @author Michael Lossos <michaellossos@gmail.com>
 */
public interface ISearchHighlighter {
    /**
     * 
     * @param doc
     *            The "document to be highlighted."
     * @param query
     *            "Contains the search query."
     * @return "The the most relevant snippet with the query terms highlighted."
     */
    String highlightDoc(String doc, String query);
}

// From Yelp's Code Test.pdf:
// def highlight_doc(doc, query):
// """
// Args:
// doc - String that is a document to be highlighted
// query - String that contains the search query
//
// Returns:
// The the most relevant snippet with the query terms highlighted.
// """!
