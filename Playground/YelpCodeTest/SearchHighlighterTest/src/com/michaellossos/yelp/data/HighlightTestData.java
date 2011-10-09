package com.michaellossos.yelp.data;

/**
 * Shared (string) docs for highlighter unit tests.
 * 
 * @author Michael Lossos <michaellossos@gmail.com>
 * 
 */
public class HighlightTestData {
    // Cannot instantiate
    private HighlightTestData() {
    }

    public static final String DEEP_DISH_PIZZA_QUERY = "deep dish pizza";

    public static final String CODE_TEST_DESCRIPTION_HIGHLIGHTED = "I like fish.  Little star's [[HIGHLIGHT]]deep dish pizza[[ENDHIGHLIGHT]] sure is fantastic. Dogs are funny.";
    public static final String CODE_TEST_DESCRIPTION_DOC = "I like fish.  Little star's deep dish pizza sure is fantastic. Dogs are funny.";

    public static final String TERMS_PUNCTUATION_HIGHLIGHTED = "This place has great [[HIGHLIGHT]]deep dish[[ENDHIGHLIGHT]]! Best [[HIGHLIGHT]]pizza[[ENDHIGHLIGHT]]... in the world of [[HIGHLIGHT]]pizza[[ENDHIGHLIGHT]]? [[HIGHLIGHT]]Deep Dish Pizza[[ENDHIGHLIGHT]]!?!";
    public static final String TERMS_PUNCTUATION_DOC = "This place has great deep dish! Best pizza... in the world of pizza? Deep Dish Pizza!?!";

    public static final String TERMS_AT_MIDDLE_HIGHLIGHTED = "blah blah blah blah [[HIGHLIGHT]]deep[[ENDHIGHLIGHT]] blah [[HIGHLIGHT]]dish[[ENDHIGHLIGHT]] blah [[HIGHLIGHT]]pizza[[ENDHIGHLIGHT]] yum blah blah blah yummy blah blah";
    public static final String TERMS_AT_MIDDLE_DOC = "blah blah blah blah deep blah dish blah pizza yum blah blah blah yummy blah blah";

    public static final String TERMS_AT_ENDS_HIGHLIGHTED = "[[HIGHLIGHT]]deep dish[[ENDHIGHLIGHT]] blah blah blah blah blah blah yum blah blah blah yummy blah blah [[HIGHLIGHT]]pizza[[ENDHIGHLIGHT]]";
    public static final String TERMS_AT_ENDS_DOC = "deep dish blah blah blah blah blah blah yum blah blah blah yummy blah blah pizza";

    public static final String TERMS_MIXED_CASE_DOC = "Really? blah blah Deep diSh pIZZa!";
    public static final String DEEP_DISH_PIZZA_MIXED_CASE_QUERY = "Deep DISH pizzA";
    public static final String TERMS_MIXED_CASE_HIGHLIGHTED = "Really? blah blah [[HIGHLIGHT]]Deep diSh pIZZa[[ENDHIGHLIGHT]]!";

    public static final String TERMS_WITH_NEWLINES_DOC = "blah blah blah blah deep blah dish\nblah \r\npizza yum blah blah blah yummy blah blah";
    public static final String TERMS_WITH_NEWLINES_HIGHLIGHTED = "blah blah blah blah [[HIGHLIGHT]]deep[[ENDHIGHLIGHT]] blah [[HIGHLIGHT]]dish[[ENDHIGHLIGHT]] blah  [[HIGHLIGHT]]pizza[[ENDHIGHLIGHT]] yum blah blah blah yummy blah blah";

    public static final String TERMS_PUNCTUATION_COMMA_DOC = "And more Deep dish   pizza, with a comma.";
    public static final String TERMS_PUNCTUATION_COMMA_HIGHLIGHTED = "And more [[HIGHLIGHT]]Deep dish   pizza,[[ENDHIGHLIGHT]] with a comma.";

    public static final String TERMS_THROUGHOUT_NEWLINES = "Let me start off first by saying that I gave this place 4 stars instead of 5, only because of the wait. We got there around 6:30, and did not get seated until 7:45 or so. But if I had read the reviews, I should have seen that coming in haha. Plus, we had a party of 8.\r\n\r\nWe ordered the Classic Deep Dish Pizza, and the Pesto Based Thin Crust Pizza.";
    public static final String TERMS_THROUGHOUT_NEWLINES_HIGHLIGHTED = "7:45 or so. But if I had read the reviews, I should have seen that coming in haha. Plus, we had a party of 8. We ordered the Classic [[HIGHLIGHT]]Deep Dish Pizza,[[ENDHIGHLIGHT]] and the Pesto Based Thin Crust [[HIGHLIGHT]]Pizza[[ENDHIGHLIGHT]].";
}
