<%inherit file="../base/base_with_jquery.mako" />

<%def name="title_inner_html()">MC Shopping List: Editor </%def>
<%def name="css_after_reset()">
    <link rel="stylesheet" href="${static_content_path}/css/shoppinglisteditor/shopping_list_static_editor_main.css"/>
</%def>

<div id="outermostDiv">
    <div id="leftNav">
        <div id="shoppingListChooserLabel">
            <p>Shopping Lists:</p>
        </div>
        <div id="shoppingListChooserDiv">
            % for shopping_list in all_shopping_lists:
                <div id="${shopping_list.id}" title="${shopping_list.name}">
                    <!-- TODO Truncate the displayed name with "..." when too long. -->
                    ${shopping_list.name}&nbsp;(${shopping_list.id})
                </div>
            % endfor
        </div>
    </div>
    <div id="mainWindow">
        <div id="editorHeaderBarDiv">
            <div id="actionButtons">
                <input type="button" id="createButton" name="Create" value="Create New List"/>
                <input type="button" id="saveButton" name="Save" value="Save"/>
                <input type="button" id="reloadButton" name="Reload" value="Reload"/>
            </div>
            <div id="statusMessageLabel">
            </div>
            <div id="shoppingListTitleLabel">
            </div>
        </div>
        <div id="editorAreaDiv">
            <textarea id="editorTextArea" class="styledTextArea"></textarea>
        </div>
    </div>
</div>


<%def name="scripts_after_jquery()">
    <script type="application/javascript"
            src="${static_content_path}/js/shoppinglisteditor/shopping_list_static_editor_main.js">
    </script>
</%def>
