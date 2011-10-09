package com.michaellossos.yelp;

import junit.framework.Assert;

import org.junit.After;
import org.junit.Before;
import org.junit.Rule;
import org.junit.Test;
import org.junit.rules.TestName;

import com.michaellossos.yelp.common.TestUtil;
import com.michaellossos.yelp.data.SnippetTestData;

/**
 * Unit test the search highlighter and check snippets.
 * 
 * @author Michael Lossos <michaellossos@gmail.com>
 * 
 */
public class SearchHighlighterSnippetTest {
    private SearchHighlighterTester tester;
    @Rule
    public TestName testName = new TestName();

    @Before
    public void setUp() {
        tester = new SearchHighlighterTester(200);
        System.out.println("____________" + testName.getMethodName());
    }

    @After
    public void tearDown() {
        tester = null;
    }

    @Test
    public void codeTestDescriptionSnippet() {
        SearchHighlighterTester shortTester = new SearchHighlighterTester(50);
        shortTester.init(SnippetTestData.DEEP_DISH_PIZZA_QUERY,
            SnippetTestData.CODE_TEST_DESCRIPTION_DOC,
            SnippetTestData.CODE_TEST_SNIPPET);
        shortTester.check();
    }

    @Test
    public void yelpDocRisotto1LongQuery() {
        logYelpResult("good but not better than anywhere else I've had it.  - lobster risotto - well cooked, fresh but not any better than a local joint that does risotto in dallas - frog legs - salty - pork belly/tenderloin");
        String docStr = TestUtil
            .loadTestDoc(SnippetTestData.TEST_DOC_RISOTTO_GD1);
        tester.init(SnippetTestData.RISOTTO_LONG_QUERY, docStr,
            SnippetTestData.TEST_DOC_RISOTTO_GD1_SNIPPET);
        tester.check();
    }

    @Test
    public void yelpDocFrench1() {
        logYelpResult("de certains très bons restaurants.  Au final, même si l'addition peut paraître chère, on en a vraiment pour son argent, on sort du restaurant repu tout en ayant l'impression d'avoir mangé équilibré");
        String docStr = TestUtil
            .loadTestDoc(SnippetTestData.TEST_DOC_FRENCH_BB1);
        tester.init(SnippetTestData.FRENCH_QUERY, docStr,
            SnippetTestData.TEST_DOC_FRENCH_BB1_SNIPPET);
        tester.check();
    }

    @Test
    public void yelpDocPizzaLS2MissingSpaces() {
        String docStr = TestUtil
            .loadTestDoc(SnippetTestData.TEST_DOC_INPUT_YELP_LS_PIZZA2);
        tester.init(SnippetTestData.DEEP_DISH_PIZZA_QUERY, docStr,
            SnippetTestData.TEST_DOC_INPUT_YELP_LS_PIZZA2_SNIPPET);
        String actualSnippet = tester.check();
        Assert.assertFalse("A space is missing between sentences.",
            actualSnippet.contains("8.We"));
    }

    @Test
    public void yelpDocPizzaLS1() {
        logYelpResult("We ordered the Classic Deep Dish Pizza, and the Pesto Based Thin Crust Pizza.  The Classic Deep Dish was super super good! I had one bite of the crust, and I was in heaven. The crust was probably");
        String docStr = TestUtil
            .loadTestDoc(SnippetTestData.TEST_DOC_INPUT_YELP_LS_PIZZA1);
        tester.init(SnippetTestData.DEEP_DISH_PIZZA_QUERY, docStr,
            SnippetTestData.TEST_DOC_INPUT_YELP_LS_PIZZA1_SNIPPET);
        tester.check();
    }

    @Test
    public void yelpDocPizzaGB1() {
        logYelpResult("neither here nor there....  definitely not thin crust, or ny style pizza, but square 'deep dish' pizza, well not really deep dish either....  little star is way better for deep dish. even BJ's");
        String docStr = TestUtil
            .loadTestDoc(SnippetTestData.TEST_DOC_INPUT_YELP_GB_PIZZA1);
        tester.init(SnippetTestData.DEEP_DISH_PIZZA_QUERY, docStr,
            SnippetTestData.TEST_DOC_INPUT_YELP_GB_PIZZA1_SNIPPET);
        tester.check();
    }

    private void logYelpResult(String result) {
        System.out.println("Yelp search result snippet:");
        System.out.println("" + result);
    }

    @Test
    public void yelpDocPizzaPD1() {
        logYelpResult("the Salted Caramel ice cream at Bi-Rite Creamery, and now the best thin crust pizza at Pizzeria Delfina. I love them all!  For deep dish, I think of Little Star's classic pizza. Now for thin crust, I");

        String docStr = TestUtil
            .loadTestDoc(SnippetTestData.TEST_DOC_INPUT_YELP_PD_PIZZA1);
        tester.init(SnippetTestData.DEEP_DISH_PIZZA_QUERY, docStr,
            SnippetTestData.TEST_DOC_INPUT_YELP_PD_PIZZA1_SNIPPET);
        tester.check();
    }

}
