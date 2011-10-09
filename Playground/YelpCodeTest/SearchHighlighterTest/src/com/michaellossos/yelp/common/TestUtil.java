package com.michaellossos.yelp.common;

import java.io.File;

import com.michaellossos.yelp.data.SnippetTestData;

public class TestUtil {
    public static String join(String[] strs) {
        if (strs == null) {
            return null;
        }
        StringBuilder sb = new StringBuilder();
        for (String s : strs) {
            sb.append(s);
        }
        return sb.toString();
    }

    public static String loadTestDoc(String testDocFilename) {
        File docFile = new File(SnippetTestData.TEST_DOCS_INPUT_FILE_PATH
            + testDocFilename);
        return DocLoader.loadDoc(docFile);
    }
}
