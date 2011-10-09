<%inherit file="../base/base_with_jquery.mako" />

<%def name="title_inner_html()">MC Shopping List: Editor </%def>
<%def name="css_after_reset()">
    <link rel="stylesheet" href="${static_content_path}/css/shoppinglisteditor/shopping_list_entry_editor_main.css"/>
    <link rel="stylesheet" href="${static_content_path}/lib/css/jquery/ui/redmond/jquery-ui-1.8.10.custom.css"/>
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
                <div id="statusMessageLabel">
                </div>
            </div>
            <div id="shoppingListTitleLabel">
            </div>
        </div>
        <div id="addItemDiv">
            + <div id="addItemLabel"></div>
        </div>
        <div id="editorAreaDiv">
        </div>
        <div id="statusLogDialog">
        </div>
    </div>
</div>

<%def name="scripts_after_jquery()">
    <!-- http://www.arashkarimzadeh.com/jquery/7-editable-jquery-plugin.html -->
    <script type="application/javascript"
            src="${static_content_path}/lib/js/jquery/editable/jquery.editable-1.3.3.js"></script>
    <script type="application/javascript"
            src="${static_content_path}/lib/js/jquery/ui/jquery-ui-1.8.10.custom.min.js"></script>
    <script type="application/javascript"
            src="${static_content_path}/js/shoppinglisteditor/shopping_list_entry_editor_main.js">
    </script>
</%def>