package com.michaellossos.yelp.common;

/**
 * <p>
 * A RuntimeException for the search highlighter Code Test.
 * </p>
 * 
 * @author Michael Lossos <michaellossos@gmail.com>
 * 
 */
public class HighlighterException extends RuntimeException {
    private static final long serialVersionUID = 5262453065463215149L;

    public HighlighterException() {
        super();
    }

    public HighlighterException(String message, Throwable cause) {
        super(message, cause);
    }

    public HighlighterException(String message) {
        super(message);
    }

    public HighlighterException(Throwable cause) {
        super(cause);
    }

}
