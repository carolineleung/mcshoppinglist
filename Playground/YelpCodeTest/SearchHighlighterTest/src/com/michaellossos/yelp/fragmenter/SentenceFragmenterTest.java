package com.michaellossos.yelp.fragmenter;

import java.util.List;

import junit.framework.Assert;

import org.junit.Test;

import com.michaellossos.yelp.common.TestUtil;

public class SentenceFragmenterTest {
    private SentenceFragmenter fragmenter = new SentenceFragmenter(30);

    @Test
    public void singleFragmentWithPunctuation() {
        String doc = "This is a single fragment.";
        List<Fragment> fragments = fragmenter.createFragments(doc);
        Assert.assertNotNull(fragments);
        Assert.assertEquals(doc, fragments.get(0).getFragmentText());
    }

    @Test
    public void singleFragmentNoPunctuation() {
        String doc = "This is a single fragment";
        List<Fragment> fragments = fragmenter.createFragments(doc);
        Assert.assertNotNull(fragments);
        Assert.assertEquals(doc, fragments.get(0).getFragmentText());
    }

    @Test
    public void singleFragmentOneLongWord() {
        String doc = "ThisIsAWordThatIsLongerThanTheAllowedSentenceFragmentLengthAndWillHaveToBeForceSplit";
        List<Fragment> fragments = fragmenter.createFragments(doc);
        Assert.assertNotNull(fragments);
        Assert.assertEquals(doc, fragments.get(0).getFragmentText());
    }

    @Test
    public void singleFragmentLongWordWithSpaces() {
        String docBegin = "ThisIsAWordThatIsLongerThanTheAllowedSentenceFragmentLengthAndWillHaveToBeForceSplit";
        String doc = docBegin + " Another word";
        List<Fragment> fragments = fragmenter.createFragments(doc);
        Assert.assertNotNull(fragments);
        Assert.assertEquals(docBegin, fragments.get(0).getFragmentText());
    }

    @Test
    public void multipleFragmentsNoEndPunctuation() {
        String[] expectedFragments = new String[] {
            "This is the first fragment!", " This is the second fragment, ",
            "split in two.", " This is the third and final ", "fragment", };
        validate(expectedFragments);
    }

    private void assertFragments(String[] expectedFragments,
        List<Fragment> actualFragments) {
        for (int index = 0; index < expectedFragments.length; ++index) {
            Assert.assertTrue(index < actualFragments.size());
            String expectedFrag = expectedFragments[index];
            Fragment actualFrag = actualFragments.get(index);
            Assert.assertNotNull(actualFrag);
            Assert.assertEquals(expectedFrag, actualFrag.getFragmentText());
        }
    }

    private void validate(String[] expectedFragments) {
        String doc = TestUtil.join(expectedFragments);
        List<Fragment> actualFragments = fragmenter.createFragments(doc);
        Assert.assertNotNull(actualFragments);

        //        // Uncomment to print fragments
        //        for (Fragment frag : actualFragments) {
        //            System.out.println("\"" + frag.getFragmentText() + "\",");
        //        }

        assertFragments(expectedFragments, actualFragments);
    }

    @Test
    public void longFragmentNoPunctuation() {
        fragmenter = new SentenceFragmenter(20);
        String[] expectedFragments = new String[] { "In the field of ",
            "linguistics, a ", "sentence is an ", "expression in ",
            "natural language, ", "and often defined to", " indicate a ",
            "grammatical unit ", "consisting of one or", " more words that ",
            "generally bear ", "minimal syntactic ", "relation to the ",
            "words that precede ", "or follow it  A ", "sentence can include",
            " words grouped ", "meaningfully ", };
        validate(expectedFragments);
    }

    @Test
    public void wordsAdjacentPunctuation() {
        fragmenter = new SentenceFragmenter(20);
        String[] expectedFragments = new String[] { "This is a test for ",
            "punctuation.", "There are spaces ", "missing!", "In between the ",
            "otherwise short ", "sentences...", "This helps ensure we",
            " treat punctuation ", "as a valid place to ", "split sentence ",
            "fragments?", "Even if there are ", "words adjacent to ",
            "the punctuation!!!", "Indeed...", "There is even a ",
            "fairly long ", "sentence, towards ", "the end of the doc, ",
            "that has a little ", "punctuation in it!",
            "Followed by not much.", "End...!", };
        validate(expectedFragments);
    }

    @Test
    public void yelpDocPizza1() {
        fragmenter = new SentenceFragmenter(20);
        // http://www.yelp.com/biz/little-star-pizza-san-francisco#query:deep%20dish%20pizza
        String[] expectedFragments = new String[] { "Went here for my ",
            "friend's 23rd ", "birthday, and as a ", "pizza enthusiast,  ",
            "this is one of the ", "best pizza joints I ",
            "have ever been to.", " Let me start off ", "first by saying that",
            " I gave this place 4", " stars instead of 5,",
            " only because of the", " wait.", " We got there around",
            " 6:30, and did not ", "get seated until ", "7:45 or so.",
            " But if I had read ", "the reviews, I ", "should have seen ",
            "that coming in haha.", " Plus, we had a ", "party of 8.",
            "We ordered the ", "Classic Deep Dish ", "Pizza, and the Pesto",
            " Based Thin Crust ", "Pizza.", "The Classic Deep ",
            "Dish was super super", " good!", " I had one bite of ",
            "the crust, and I was", " in heaven.", " The crust was ",
            "probably the best ", "pizza crust I had ", "ever eaten.",
            " The toppings were ", "plentiful, and fresh.", "The Pesto Based ",
            "pizza was pretty ", "good, but if I ever ", "come here again, I ",
            "would definitely ", "recommend sticking ", "to the deep dish.",
            " Man...", " I'm craving pizza ", "just thinking about ",
            "the crust....", "Oh yeah btw, the ", "crust is amazing ", "here.",
            "P.", "S.", " Oh yeah, did I ", "mention the crust?", };
        validate(expectedFragments);
    }
}
