package com.michaellossos.yelp.terms;

import junit.framework.Assert;

import org.junit.Test;

import com.michaellossos.yelp.terms.TermParser;

public class TermParserTest {
    @Test
    public void sanitizePizzaCommas() {
        String actual = TermParser.sanitizeTerm("pizza,");
        Assert.assertEquals("pizza", actual);
    }
}
