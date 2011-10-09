package com.michaellossos.yelp.terms;

import org.junit.After;
import org.junit.Before;
import org.junit.Test;

import com.michaellossos.yelp.common.SharedHighlighterValidator;

/**
 * Unit test the Highlighter alone without searching or snippets.
 * 
 * @author Michael Lossos <michaellossos@gmail.com>
 * 
 */
public class TermHighlighterTest {
    private SharedHighlighterValidator validator;

    @Before
    public void setUp() {
        validator = new SharedHighlighterValidator(new TermHighlighterTester());
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
}
