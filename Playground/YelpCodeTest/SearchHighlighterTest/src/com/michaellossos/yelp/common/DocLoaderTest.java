package com.michaellossos.yelp.common;

import java.io.File;

import org.junit.Test;

public class DocLoaderTest {
    @Test(expected = HighlighterException.class)
    public void invalidFile() {
        DocLoader.loadDoc(new File("./invalid.file"));
    }
}
