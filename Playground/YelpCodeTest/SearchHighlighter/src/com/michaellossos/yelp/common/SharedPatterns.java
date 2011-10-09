package com.michaellossos.yelp.common;

import java.util.regex.Pattern;

/**
 * Regex patterns used throughout the search highlighter.
 * 
 * @author Michael Lossos <michaellossos@gmail.com>
 * 
 */
public class SharedPatterns {
    /*
     * We use "non-whitespace" patterns here and avoid US-ASCII/English specific
     * character patterns to allow for internationalized (I18N/Culture specific)
     * searches.
     */
    public static final Pattern WORD_ANYWHERE_PATTERN = Pattern.compile("\\S+");
    public static final Pattern WORD_ONLY_PATTERN = Pattern.compile("^\\S+$");
    /**
     * Pattern for punctuation that terminates a sentence.
     */
    public static final Pattern PUNCTUATION_PATTERN = Pattern
        .compile(SharedPatterns.PUNCTUATION_PATTERN_STR);
    /**
     * Pattern string for punctuation that terminates a sentence.
     */
    public static final String PUNCTUATION_PATTERN_STR = "[\\!\\.\\?]+";

    public static final String WHITESPACE_PATTERN_STR = "\\s";
    public static final Pattern WHITESPACE_PATTERN = Pattern.compile("\\s+");
}
