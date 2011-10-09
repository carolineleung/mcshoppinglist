package com.michaellossos.yelp.common;

import java.io.File;
import java.io.FileReader;

public class DocLoader {
    /**
     * Load a file as a single string.
     */
    public static String loadDoc(File docFile) {
        try {
            StringBuilder doc = new StringBuilder();
            FileReader fileReader = new FileReader(docFile);
            String line = null;
            do {
                // Ineffecient but simple.
                char[] cbuf = new char[1024 * 64];
                int charsRead = 0;
                do {
                    charsRead = fileReader.read(cbuf);
                    if (charsRead > 0) {
                        doc.append(cbuf, 0, charsRead);
                    }
                } while (charsRead > 0);
            } while (line != null);
            return doc.toString();
        } catch (Exception ex) {
            throw new HighlighterException("Failed to load file: "
                + docFile.getAbsolutePath(), ex);
        }
    }
}
