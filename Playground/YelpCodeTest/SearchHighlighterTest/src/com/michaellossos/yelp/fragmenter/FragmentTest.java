package com.michaellossos.yelp.fragmenter;

import junit.framework.Assert;

import org.junit.Test;

public class FragmentTest {
    @Test
    public void substring() {
        String text = "Fragment text";
        Fragment frag = new Fragment(text, text, 0);
        String actual = frag.substring(30);
        Assert.assertEquals(text, actual);
        frag.toString();
    }

    @Test
    public void exceptionTest() {
        int exceptionCount = 0;
        try {
            new Fragment("", null, 1);
        } catch (Exception ex) {
            ++exceptionCount;
        }
        try {
            new Fragment("", "", -1);
        } catch (Exception ex) {
            ++exceptionCount;
        }
        try {
            new Fragment("", "", 0).incrementScore(-1);
        } catch (Exception ex) {
            ++exceptionCount;
        }
        Assert.assertEquals(3, exceptionCount);
    }
}
