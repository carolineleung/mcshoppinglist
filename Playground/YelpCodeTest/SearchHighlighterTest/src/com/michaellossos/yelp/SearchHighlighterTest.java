package com.michaellossos.yelp;

import org.junit.After;
import org.junit.Before;
import org.junit.Test;

import com.michaellossos.yelp.common.SharedHighlighterValidator;
import com.michaellossos.yelp.data.HighlightTestData;

/**
 * Test that the search highlighter highlights. The doc strings are short and do
 * not require snippets.
 * 
 * @author Michael Lossos <michaellossos@gmail.com>
 * 
 */
public class SearchHighlighterTest {
    private SharedHighlighterValidator validator;

    @Before
    public void setUp() {
        validator = new SharedHighlighterValidator(
            new SearchHighlighterTester());
    }

    @After
    public void tearDown() {
        validator = null;
    }

    @Test
    public void termsOnly() {
        validator.checkTermsOnly();
    }

    @Test
    public void termsAtEnds() {
        validator.checkTermsAtEnds();
    }

    @Test
    public void termsAtMiddle() {
        validator.checkTermsAtMiddle();
    }

    @Test
    public void termsWithPunctuation() {
        validator.checkTermsWithPunctuation();
    }

    @Test
    public void termsWithPunctuationAndCommas() {
        validator.checkTermsWithPunctuationAndCommas();
    }

    @Test
    public void termsAtMiddleFromCodeTestDescription() {
        validator.checkTermsAtMiddleFromCodeTestDescription();
    }

    @Test
    public void termsMixedCase() {
        validator.checkTermsMixedCase();
    }

    @Test
    public void emptyDoc() {
        SearchHighlighterTester tester = new SearchHighlighterTester();
        tester.init(HighlightTestData.DEEP_DISH_PIZZA_QUERY, "", "");
        tester.check();
    }

    @Test
    public void nullDoc() {
        SearchHighlighterTester tester = new SearchHighlighterTester();
        tester.init(HighlightTestData.DEEP_DISH_PIZZA_QUERY, null, null);
        tester.check();
    }

    @Test
    public void emptyQueryNoSearchTerms() {
        SearchHighlighterTester tester = new SearchHighlighterTester();
        tester.init("", HighlightTestData.TERMS_AT_MIDDLE_DOC,
            HighlightTestData.TERMS_AT_MIDDLE_DOC);
        tester.check();
    }

    @Test
    public void termsWithNewlines() {
        SearchHighlighterTester tester = new SearchHighlighterTester();
        tester.init(HighlightTestData.DEEP_DISH_PIZZA_QUERY,
            HighlightTestData.TERMS_WITH_NEWLINES_DOC,
            HighlightTestData.TERMS_WITH_NEWLINES_HIGHLIGHTED);
        tester.check();
    }

    @Test
    public void termsWithNewlines2() {
        SearchHighlighterTester tester = new SearchHighlighterTester();
        tester.init(HighlightTestData.DEEP_DISH_PIZZA_QUERY,
            HighlightTestData.TERMS_THROUGHOUT_NEWLINES,
            HighlightTestData.TERMS_THROUGHOUT_NEWLINES_HIGHLIGHTED);
        tester.check();
    }
}
