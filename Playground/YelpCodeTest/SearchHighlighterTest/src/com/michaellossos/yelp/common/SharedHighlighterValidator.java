package com.michaellossos.yelp.common;

import com.michaellossos.yelp.common.HighlighterConstants;
import com.michaellossos.yelp.data.HighlightTestData;

/**
 * Reuseable tests for the TermHighlighter and the SearchHighlighter.
 * 
 * @author Michael Lossos <michaellossos@gmail.com>
 * 
 */
public class SharedHighlighterValidator {
    private final ITester tester;

    public SharedHighlighterValidator(ITester tester) {
        this.tester = tester;
    }

    /**
     * The document is comprised of only the query terms.
     */
    public void checkTermsOnly() {
        tester.init(HighlightTestData.DEEP_DISH_PIZZA_QUERY,
            HighlightTestData.DEEP_DISH_PIZZA_QUERY,
            HighlighterConstants.BEGIN_HIGHLIGHT
                + HighlightTestData.DEEP_DISH_PIZZA_QUERY
                + HighlighterConstants.END_HIGHLIGHT);
        tester.check();
    }

    public void checkTermsAtEnds() {
        tester.init(HighlightTestData.DEEP_DISH_PIZZA_QUERY,
            HighlightTestData.TERMS_AT_ENDS_DOC,
            HighlightTestData.TERMS_AT_ENDS_HIGHLIGHTED);
        tester.check();
    }

    public void checkTermsAtMiddle() {
        tester.init(HighlightTestData.DEEP_DISH_PIZZA_QUERY,
            HighlightTestData.TERMS_AT_MIDDLE_DOC,
            HighlightTestData.TERMS_AT_MIDDLE_HIGHLIGHTED);
        tester.check();
    }

    public void checkTermsWithPunctuation() {
        tester.init(HighlightTestData.DEEP_DISH_PIZZA_QUERY,
            HighlightTestData.TERMS_PUNCTUATION_DOC,
            HighlightTestData.TERMS_PUNCTUATION_HIGHLIGHTED);
        tester.check();
    }

    public void checkTermsWithPunctuationAndCommas() {
        tester.init(HighlightTestData.DEEP_DISH_PIZZA_QUERY,
            HighlightTestData.TERMS_PUNCTUATION_COMMA_DOC,
            HighlightTestData.TERMS_PUNCTUATION_COMMA_HIGHLIGHTED);
        tester.check();
    }

    public void checkTermsAtMiddleFromCodeTestDescription() {
        tester.init(HighlightTestData.DEEP_DISH_PIZZA_QUERY,
            HighlightTestData.CODE_TEST_DESCRIPTION_DOC,
            HighlightTestData.CODE_TEST_DESCRIPTION_HIGHLIGHTED);
        tester.check();
    }

    public void checkTermsMixedCase() {
        tester.init(HighlightTestData.DEEP_DISH_PIZZA_MIXED_CASE_QUERY,
            HighlightTestData.TERMS_MIXED_CASE_DOC,
            HighlightTestData.TERMS_MIXED_CASE_HIGHLIGHTED);
        tester.check();
    }

}
