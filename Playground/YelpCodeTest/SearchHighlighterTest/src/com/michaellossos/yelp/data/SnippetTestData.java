package com.michaellossos.yelp.data;

/**
 * Shared (string) docs for highlighted snippet unit tests.
 * 
 * @author Michael Lossos <michaellossos@gmail.com>
 * 
 */
public class SnippetTestData {
    public static final String DEEP_DISH_PIZZA_QUERY = "deep dish pizza";
    public static final String CODE_TEST_DESCRIPTION_DOC = "I like fish.  Little star's deep dish pizza sure is fantastic. Dogs are funny.";
    public static final String CODE_TEST_SNIPPET = "Little star's [[HIGHLIGHT]]deep dish pizza[[ENDHIGHLIGHT]] sure is fantastic.";

    /**
     * Relative to the current working directory when running the tests. By
     * default in Eclipse, this is the top level project directory
     * (SearchHighlights).
     */
    public static final String TEST_DOCS_INPUT_FILE_PATH = "./src/docs/input/";
    public static final String TEST_DOC_INPUT_YELP_LS_PIZZA1 = "Yelp Deep Dish Pizza Little Star 1.txt";
    public static final String TEST_DOC_INPUT_YELP_LS_PIZZA1_SNIPPET = "the reviews, I should have seen that coming in haha. Plus, we had a party of 8. We ordered the Classic [[HIGHLIGHT]]Deep Dish Pizza,[[ENDHIGHLIGHT]] and the Pesto Based Thin Crust [[HIGHLIGHT]]Pizza[[ENDHIGHLIGHT]]. The Classic [[HIGHLIGHT]]Deep Dish[[ENDHIGHLIGHT]] was super super";
    public static final String TEST_DOC_INPUT_YELP_LS_PIZZA2 = "Yelp Deep Dish Pizza Little Star 2.txt";
    public static final String TEST_DOC_INPUT_YELP_LS_PIZZA2_SNIPPET = "7:45 or so. But if I had read the reviews, I should have seen that coming in haha. Plus, we had a party of 8. We ordered the Classic [[HIGHLIGHT]]Deep Dish Pizza,[[ENDHIGHLIGHT]] and the Pesto Based Thin Crust [[HIGHLIGHT]]Pizza[[ENDHIGHLIGHT]].";
    public static final String TEST_DOC_INPUT_YELP_GB_PIZZA1 = "Yelp Deep Dish Pizza Golden Boy 1.txt";
    public static final String TEST_DOC_INPUT_YELP_GB_PIZZA1_SNIPPET = "neither here nor there.... definitely not thin crust, or ny style [[HIGHLIGHT]]pizza,[[ENDHIGHLIGHT]] but square [[HIGHLIGHT]]'deep dish' pizza,[[ENDHIGHLIGHT]] well not really [[HIGHLIGHT]]deep dish[[ENDHIGHLIGHT]] either.... little star is way better for [[HIGHLIGHT]]deep dish[[ENDHIGHLIGHT]]. even BJ's is [[HIGHLIGHT]]deep[[ENDHIGHLIGHT]]";
    public static final String TEST_DOC_INPUT_YELP_PD_PIZZA1 = "Yelp Deep Dish Pizza Delfina 1.txt";
    public static final String TEST_DOC_INPUT_YELP_PD_PIZZA1_SNIPPET = "Creamery, and now the best thin crust [[HIGHLIGHT]]pizza[[ENDHIGHLIGHT]] at Pizzeria Delfina. I love them all! For [[HIGHLIGHT]]deep dish,[[ENDHIGHLIGHT]] I think of Little Star's classic [[HIGHLIGHT]]pizza[[ENDHIGHLIGHT]]. Now for thin crust, I immediately think of Pizzeria Delfina.";

    public static final String RISOTTO_LONG_QUERY = "risotto my we how good better this than that I ate food";
    public static final String TEST_DOC_RISOTTO_GD1 = "Yelp Risotto Danko 1.txt";
    public static final String TEST_DOC_RISOTTO_GD1_SNIPPET = "memorable. Don't get me wrong. I love [[HIGHLIGHT]]food[[ENDHIGHLIGHT]] and I wanted more [[HIGHLIGHT]]than[[ENDHIGHLIGHT]] anything else to LOVE Danko, but I didn't. I had: - foie gras - [[HIGHLIGHT]]good[[ENDHIGHLIGHT]] but not [[HIGHLIGHT]]better than[[ENDHIGHLIGHT]] anywhere else I've had it.";

    public static final String FRENCH_QUERY = "très paraître";
    public static final String TEST_DOC_FRENCH_BB1 = "Yelp France Bo Bun 1.txt";
    public static final String TEST_DOC_FRENCH_BB1_SNIPPET = "pour déjeuner. C'est un peu la version 2.0 du Bobun traditionnel, avec un décor moderne [[HIGHLIGHT]]très[[ENDHIGHLIGHT]] propre, et surtout on peut décider de tous les ingrédients qu'on veut. (j'aime pas le coriandre par";
}
