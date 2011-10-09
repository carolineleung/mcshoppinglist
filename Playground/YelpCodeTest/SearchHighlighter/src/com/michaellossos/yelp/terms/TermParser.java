package com.michaellossos.yelp.terms;

import java.util.LinkedHashSet;
import java.util.Set;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

import com.michaellossos.yelp.common.SharedPatterns;

/**
 * Utilities related to parsing search terms.
 * 
 * @author Michael Lossos <michaellossos@gmail.com>
 * 
 */
public class TermParser {
    // TODO This may not work with i18n UTF-8 strings. Works fine with the French language test.
    // \p{Punct} : POSIX character classes are US-ASCII only.
    // !"#$%&'()*+,-./:;<=>?@[\]^_`{|}~
    private static final Pattern NON_WORD_CHARS_PATTERN = Pattern
        .compile("[\\p{Punct}]+");

    private static Set<String> createTermsSet(String[] terms,
        Set<String> excludeTerms) {
        if (terms == null) {
            return null;
        }
        // Use a LinkedHashSet to preserve the order of the search terms.
        Set<String> searchTerms = new LinkedHashSet<String>();
        for (String term : terms) {
            term = sanitizeTerm(term);
            if (term != null && !term.isEmpty()) {
                if (excludeTerms == null || !excludeTerms.contains(term)) {
                    searchTerms.add(term);
                }
            }
        }
        return searchTerms;
    }

    public static Set<String> parseTerms(String terms, String[] excludeTermsStrs) {
        if (terms == null || terms.isEmpty()) {
            return new LinkedHashSet<String>();
        }
        Set<String> excludeTerms = createTermsSet(excludeTermsStrs, null);
        String[] splitTerms = terms
            .split(SharedPatterns.WHITESPACE_PATTERN_STR);
        Set<String> searchTerms = createTermsSet(splitTerms, excludeTerms);
        return searchTerms;
    }

    public static String sanitizeTerm(String term) {
        if (term == null || term.length() == 0) {
            return term;
        }
        String scrubbed = removeNonWordChars(term);
        scrubbed = scrubbed.toLowerCase().trim();
        return scrubbed;
    }

    private static String removeNonWordChars(String word) {
        Matcher matcher = NON_WORD_CHARS_PATTERN.matcher(word);
        return matcher.replaceAll("");
    }
}
