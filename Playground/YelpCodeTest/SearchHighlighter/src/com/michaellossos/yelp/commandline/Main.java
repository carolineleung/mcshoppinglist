package com.michaellossos.yelp.commandline;

import java.io.File;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;

import com.michaellossos.yelp.ISearchHighlighter;
import com.michaellossos.yelp.SearchHighlighterFactory;
import com.michaellossos.yelp.common.DocLoader;

/**
 * Command line interface for ISearchHighlighter.
 * 
 * @author Michael Lossos <michaellossos@gmail.com>
 * 
 */
public class Main {
    // Cannot instantiate
    private Main() {
    }

    // "..\SearchHighlighterTest\src\docs\input\Yelp Deep Dish Pizza Golden Boy 1.txt" 200 deep dish pizza
    public static final void main(String[] args) {
        if (args == null || args.length < 3) {
            System.out.println("usage: [inputDocFile] [snippetLength] "
                + " [searchTerm1] [searchTerm2] [searchTermN]");
            System.out.println("where: ");
            System.out.println("inputDocFile: Path to the \"doc\" to read.");
            System.out.println("snippetLength: Integer length of the "
                + "snippet to extract, e.g. 200.");
            return;
        }
        try {
            String inputFile = args[0];
            String snippetLengthStr = args[1];
            int maxSnippetLength = Integer.parseInt(snippetLengthStr);
            List<String> termsList = new ArrayList<String>(Arrays.asList(args));
            termsList.remove(0);
            termsList.remove(0);
            String query = join(termsList, " ");

            System.out.println("Input file: " + inputFile);
            System.out.println("Max snippet length: " + maxSnippetLength);
            System.out.println("Query: " + query);
            System.out.println();

            String doc = DocLoader.loadDoc(new File(inputFile));
            ISearchHighlighter searchHighlighter = new SearchHighlighterFactory()
                .createSearchHighlighter(maxSnippetLength);
            String snippet = searchHighlighter.highlightDoc(doc, query);

            System.out.println("Snippet:");
            System.out.println();
            System.out.println("" + snippet);
            System.out.println();
        } catch (Exception ex) {
            System.err.println("Failed to highlight a snippet.");
            ex.printStackTrace(System.err);
        }
    }

    private static String join(List<String> strs, String with) {
        if (strs == null) {
            return null;
        }
        StringBuilder sb = new StringBuilder();
        for (String s : strs) {
            if (sb.length() > 0) {
                sb.append(with);
            }
            sb.append(s);
        }
        return sb.toString();
    }
}
