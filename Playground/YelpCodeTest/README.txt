____________________________________________________
INTRO
____________________________________________________

This is my implementation of the Yelp "Code Test.pdf" project,
to create a search result snippet extractor and search term highlighter.

Thanks for your time!
Michael Lossos <michaellossos@gmail.com>

____________________________________________________
SNIPPET RESULT QUALITY
____________________________________________________

In order to measure the quality of the snippets returned by my SearchHighlighter implementation, I did the following:
* Performed searches on Yelp.com (San Francisco). 
* Copied Yelp's search result snippet for one of the locations.
* Copied the full review that the snippet came from.
* Built tests using the full review as the "doc" input.

While my SearchHighlighter results are not identical to Yelp's, they're often quite close, as can be seen in the example below.


Query: deep dish pizza
http://www.yelp.com/search?find_desc=deep+dish+pizza&ns=1&find_loc=San+Francisco,+CA
3. Golden Boy Pizza
http://www.yelp.com/biz/golden-boy-pizza-san-francisco#query:deep%20dish%20pizza

Test document:
.\SearchHighlighterTest\src\docs\input\Yelp Deep Dish Pizza Golden Boy 1.txt


Yelp search result snippet:

neither here nor there....  definitely not thin crust, or ny style pizza, but square 'deep dish' pizza, well not really deep dish either....  little star is way better for deep dish. even BJ's


My SearchHighlighter result:

neither here nor there.... definitely not thin crust, or ny style [[HIGHLIGHT]]pizza,[[ENDHIGHLIGHT]] but square [[HIGHLIGHT]]'deep dish' pizza,[[ENDHIGHLIGHT]] well not really [[HIGHLIGHT]]deep dish[[ENDHIGHLIGHT]] either.... little star is way better for [[HIGHLIGHT]]deep dish[[ENDHIGHLIGHT]]. even BJ's is [[HIGHLIGHT]]deep[[ENDHIGHLIGHT]]


Additional results can be seen in Result Comparison.txt.

____________________________________________________
REQUIREMENTS
____________________________________________________

Java 1.6
Eclipse IDE
JUnit 4 (bundled with Eclipse IDE)

____________________________________________________
RUNNING
____________________________________________________
You can run my SearchHighlighter example using these commands, assuming java is in your path:

Windows:
run-highlighter-example.cmd

Linux/*nix/OSX:
bash run-highlighter-example.sh

____________________________________________________
BUILDING
____________________________________________________

The zip archive is pre-built with the classes in SearchHighlighter\bin.
You can rebuild by importing these projects into Eclipse:
SearchHighlighter
SearchHighlighterTest

____________________________________________________
TESTING
____________________________________________________

The unit tests and integration tests can be found in the project:
SearchHighlighterTest

____________________________________________________
TEST COVERAGE
____________________________________________________

The tests have 92% code coverage, depending on how you measure it.
Test coverage results are in:
SearchHighlighterTest\test-coverage-results

____________________________________________________
TODOs
____________________________________________________

There are a few TODOs sprinkled throughout the code, indicating areas that possibly could be improved. This is intentional: they indicate things thought of but unresolved. Most of these would be overly complicated or time consuming to resolve, and the SearchHighlighter results are good already.

