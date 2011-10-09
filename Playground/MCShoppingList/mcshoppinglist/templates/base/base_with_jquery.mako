<!DOCTYPE HTML>
<html lang="en" xml:lang="en">
<head>
    <meta charset="utf-8" />
    <title>${self.title_inner_html()}</title>
    <link rel="stylesheet" href="${static_content_path}/lib/css/yui/build/reset/reset-min.css"/>
    ${self.css_after_reset()}
</head>
<body>
    <noscript><p>Please enable JavaScript.</p></noscript>
    ${self.body()}

    <!--
    <script type="application/javascript"
            src="{{ STATIC_DOC_ROOT }}/lib/js/jquery/jquery-1.5.min.js"></script>
            -->
    <script type="application/javascript"
            src="${static_content_path}/lib/js/jquery/jquery-1.5.js"></script>
    <script type="application/javascript"
            src="${static_content_path}/lib/js/jquery/jquery.json-2.2.js"></script>
    ${self.scripts_after_jquery()}
</body>
</html>