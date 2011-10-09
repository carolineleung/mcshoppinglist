package com.michaellossos.yelp.commandline;

import org.junit.Test;

import com.michaellossos.yelp.data.SnippetTestData;

public class MainTest {
    @Test
    public void runMainNull() {
        Main.main(null);
    }

    @Test
    public void runMainWithDoc() {
        Main.main(new String[] {
            SnippetTestData.TEST_DOCS_INPUT_FILE_PATH
                + SnippetTestData.TEST_DOC_INPUT_YELP_GB_PIZZA1, "200", "deep",
            "dish", "pizza" });
    }
}
