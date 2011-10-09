(function(window) {

var document = window.document;

var ACTION_SAVE_NEW = 'ACTION_SAVE_NEW',
ACTION_SAVE_UPDATED = 'ACTION_SAVE_UPDATED',
ACTION_SAVE_DELETED = 'ACTION_SAVE_DELETED',
ACTION_SAVE_LIST_DETAIL = 'ACTION_SAVE_LIST_DETAIL',
ACTION_LOAD_LIST = 'ACTION_LOAD_LIST';

var INSTRUCTIONS_ENTER_TITLE = 'Click here to enter a TITLE for this shopping list.';

var REQ_CRUD_ACTION_CREATE = 'CREATE',
REQ_CRUD_ACTION_UPDATE = 'UPDATE',
REQ_CRUD_ACTION_DELETE = 'DELETE';

var _currentShoppingList = null,
_currentActionMap = {},
_editorItemDirtyMap = {},
_editorItemDeleteMap = {},
_statusMessageLog = [];

////////////////////////////////////////////////////////////////////
// Helpers
//
    
// TODO Refactor these out
var isDefined = function(obj) {
    return typeof obj != 'undefined';
};
var isUndefined = function(obj) {
    return !isDefined(obj);
};
var isEmpty = function(list) {
    return isUndefined(list) || !list || (isDefined(list.length) && list.length <= 0);
};

////////////////////////////////////////////////////////////////////
// View updates
//
var _isValidIdFormat = function(resourceId) {
//  return !isNaN(parseFloat(n)) && isFinite(n); // for integers
    // TODO Check that it's a MongoDB style ID '4d7d1c52cf660759e8000003'
    return isDefined(resourceId) && resourceId && resourceId != 'null' && resourceId != 'None';
};

var _setShoppingListTitle = function(title) {
    var elem = $("#shoppingListTitleLabel");
    var emClass = 'shoppingListTitleLabelEm';
    if(!title) {
        title = INSTRUCTIONS_ENTER_TITLE;
        elem.addClass(emClass);
    }
    else {
        elem.removeClass(emClass);
    }
    elem.html(title);
},
_getShoppingListTitle = function() {
    var html = $("#shoppingListTitleLabel").html();
    return html.replace(/(<.*?>)/ig, '');
},
_setStatusMessage = function(text) {
    if(!text) {
        text = ''
    }
    $("#statusMessageLabel").html(text);
    if(text.length > 0) {
        var now = new Date();
        var msg = '' + now.toLocaleTimeString() + ': ' + text;
        _statusMessageLog.push(msg);
        if(_statusMessageLog.length > 30) {
            _statusMessageLog.shift();
        }
    }
},
_getStatusLogHtml = function() {
    if(_statusMessageLog.length <= 0) {
        return '';
    }
    var logHtml = '';
    for(var msgIndex in _statusMessageLog) {
        var msg = _statusMessageLog[msgIndex];
        logHtml += '<div class="statusMessageLogRow">';
        logHtml += '' + msg;
        logHtml += '</div>\n';
    }
    return logHtml;
};

////////////////////////////////////////////////////////////////////
// Workarounds.
//

// Hack to allow hitting Enter to accept value
// PRE: "this" refers to the editable element.
var _registerEditableKeyHandler = function() {
    var self = $(this);
    var opts = self.data('editable.options');
    var inputElem = self.find('input').first();
    inputElem.keypress(function(event) {
        if(event.which == '13') { // Enter
            opts.toNonEditable(self, true);
        }
        // Escape '27' doesn't work properly.
        else if(event.which == '27') { // Enter
            opts.toNonEditable(self, false);
        }
    });
};

////////////////////////////////////////////////////////////////////
// Action queue
//

var _isActionRunning = function() {
    for(var action in _currentActionMap) {
        if(isDefined(action) && _currentActionMap[action]) {
            return true;
        }
    }
    return false;
},
_actionStart = function(whichAction) {
    _currentActionMap[whichAction] = true;
},
_actionComplete = function(whichAction) {
    _currentActionMap[whichAction] = false;
};

////////////////////////////////////////////////////////////////////
// Ajax callbacks
//

var _resetEditorItemDirtyMap = function() {
    _editorItemDirtyMap = {};
},
_resetEditorItemDeleteMap = function() {
    _editorItemDeleteMap = {};
},
_updateTableRowColors = function() {
    $("#editorAreaDiv").find('tr')
        .removeClass('editorItemRowOdd')
        .removeClass('editorItemRowEven');
    $("#editorAreaDiv").find('tr:odd').addClass('editorItemRowOdd');
    $("#editorAreaDiv").find('tr:even').addClass('editorItemRowEven');
},
//
// trElem: tr in the editor table.
//
_registerEditorTrEvents = function(trElem) {
    trElem.find('.editorItemCheckbox').click(function() {
        var itemId = $(this).attr('id');
        //_setStatusMessage('Clicked item id: ' + itemId + ' checked: ' + this.checked);
        _editorItemDirtyMap[itemId] = true;
    });
    trElem.find('.editorItemRemoveButton').click(function(e) {
        var itemId = $(this).attr('id');
        _editorItemDeleteMap[itemId] = true;

        $(this).parentsUntil('.editorItemRow').parent().remove();
        _updateTableRowColors();

        var itemName = $(this).parentsUntil('table').find('.editorItemName#' + itemId).html();
        _setStatusMessage('Removed ' + itemName + '.');
    });

    var editorOpts = {
//        cancel: 'X',
        editClass: 'editorItemEditing',
        onSubmit: function(content) {
            if(content.current != content.previous) {
                var itemId = this.attr('id');
                _editorItemDirtyMap[itemId] = true;
                _setStatusMessage('Edited item id: ' + itemId);
            }
        },
        onEdit: _registerEditableKeyHandler
    };
    trElem.find('.editorItemName').editable(editorOpts);
    trElem.find('.editorItemLabels').editable(editorOpts);
},
//
// item: must have properties: id, name, checked (boolean), labels
//
_addItemToEditorTable = function(item, tableElem) {
    if(isUndefined(item.id)) {
        throw 'The item must have an id.';
    }
    if(isUndefined(tableElem) || !tableElem) {
        tableElem = $("#editorAreaDiv").find('table');
    }
    _editorItemDirtyMap[item.id] = false;

    var trHtml = '<tr class="editorItemRow" id="' + item.id + '"> ';

    trHtml += '<td class="editorItemChecked"> ';
    trHtml += '<input type="checkbox" class="editorItemCheckbox" id="' + item.id + '" ';
    if(item.checked) {
        trHtml += ' checked="yes" ';
    }
    trHtml += '/>';
    trHtml += '</td>\n';
    trHtml += '<td class="editorItemName" id="' + item.id + '"> ' + item.name + '</td>\n';
    if(isDefined(item.labels)) {
        trHtml += '<td class="editorItemLabels" id="' + item.id + '"> ' + item.labels + '</td>\n';
    }
    trHtml += '<td class="editorItemRemove">';
    trHtml += '<input type="button" class="editorItemRemoveButton" id="' + item.id + '" value="X" />';
    trHtml += '</td>\n';
    trHtml += ' </tr>\n';

    tableElem.append(trHtml);

    var newTr = tableElem.find('#' + item.id + '.editorItemRow');
    _registerEditorTrEvents(newTr);
},
_createEditorTable = function() {
    $("#editorAreaDiv").html('<table class="listEditorTable">\n</table>\n');
},
_loadShoppingListFromJsonData = function(shoppingListJson) {
    _currentShoppingList = null;
    _resetEditorItemDirtyMap();
    _resetEditorItemDeleteMap();

    //$("#editorTextArea").val(data);
    if(isUndefined(shoppingListJson) || shoppingListJson == null || shoppingListJson.length <= 0) {
        _setStatusMessage('Failed to load! (Server gave us nothing!)');
        return;
    }

    _currentShoppingList = shoppingListJson;
    _setShoppingListTitle(shoppingListJson.name);

    _createEditorTable();
    var tableElem = $("#editorAreaDiv").find('table');
    var itemLen = shoppingListJson.items.length;
    for(var index = 0; index < itemLen; ++index) {
        var item = shoppingListJson.items[index];
        if(isUndefined(item) || isUndefined(item.id)) {
            throw 'ShoppingListItem/id at index ' + index + ' was undefined.';
        }
        _addItemToEditorTable(item, tableElem);
    }

    _updateTableRowColors();

    _setStatusMessage('Loaded shopping list: ' + shoppingListJson.name + ' (' + shoppingListJson.id + ')');
},
_addNewItem = function(itemName) {
    if(isUndefined(itemName)) {
        return;
    }
    var name = $.trim(itemName);
    _setStatusMessage('Adding new item: ' + name);
    var item = {
        name: name,
        id: null,
        labels: '',
        checked: false
    };
    _addItemToEditorTable(item, null);
    _updateTableRowColors();
    _setStatusMessage('Added new item: ' + name + '. Not yet saved.');
};

////////////////////////////////////////////////////////////////////
// Actions
//

//
// filterFunc: params: itemObj, returns: boolean true to accept the item
//
var _createItemsArray = function(filterFunc) {
    var itemsArray = [];

    $('.editorItemRow').each(function() {
        var itemId = $(this).attr('id');
        // TODO Strip html
        var itemText = $.trim($(this).find('.editorItemName').html());
        var itemLabels = $.trim($(this).find('.editorItemLabels').html());
        var itemChecked = $(this).find('.editorItemCheckbox').is(':checked');
        // ShoppingListItem resource
        var itemObj = {
            id: itemId,
            name: itemText,
            labels: itemLabels,
            checked: itemChecked
        };
        try {
            if(filterFunc(itemObj)) {
                itemsArray.push(itemObj);
            }
        }
        catch(ex){
            try {
                console.log('Failed to add item: id: ' + itemId + ' name: ' + itemText + '  Cause: ' + ex);
            }
            catch(ex2) {
                // ignore
            }
        }
    });

    return itemsArray;
},
_createDeletedItemsArray = function() {
    var itemsArray = [];
    for(var itemId in _editorItemDeleteMap) {
        if(_isValidIdFormat(itemId)) {
            var itemObj = {
                id: itemId
            };
            itemsArray.push(itemObj);
        }
        else {
            console.log('Invalid item id marked for deletion: ' + itemId);
        }
    }
    return itemsArray;
};

var _getShoppingListChooserEntries = function() {
    return $('#shoppingListChooserDiv > div');
},
_loadShoppingList = function(shoppingListId) {
    if(isUndefined(shoppingListId) || !shoppingListId) {
        console.log('Failed to load invalid shopping list id: ' + shoppingListId);
        return;
    }
    var uri = '/api/v1/shoppinglists/' + shoppingListId + '/'
    _setStatusMessage('Loading....');
    // TODO Switch to getJSON?
    _actionStart(ACTION_LOAD_LIST);
    $.get(uri, function(data) {
            _actionComplete(ACTION_LOAD_LIST);
            _loadShoppingListFromJsonData(data);
        })
        .error(function() {
            _actionComplete(ACTION_LOAD_LIST);
            _setStatusMessage('Failed to Load the shopping list!');
        });
},
_createActionResource = function(whichAction, items) {
    return {
        action: whichAction,
        items: items
    };
},
//
// items: ShoppingListItem array
//
_sendUpdatedItems = function(items) {
    if(!_currentShoppingList || !items || items.length <= 0) {
        return;
    }
    // Update existing ShoppingListItem(s)
    var uri = '/api/v1/shoppinglists/' + _currentShoppingList.id + '/items/';

    var actionResource = _createActionResource(REQ_CRUD_ACTION_UPDATE, items);
    var jsonData = $.toJSON(actionResource);
    _actionStart(ACTION_SAVE_UPDATED);
    $.post(uri, jsonData, function() {
            _actionComplete(ACTION_SAVE_UPDATED);
            _setStatusMessage('Saved updated items!');
            _resetEditorItemDirtyMap();
        })
        .error(function() { // params: data, jqxhr
            _actionComplete(ACTION_SAVE_UPDATED);
            _setStatusMessage('Failed to Save updated items!');
        });
},
//
// items: ShoppingListItem array
//
_sendNewItems = function(items) {
    if(!items || items.length <= 0) {
        return;
    }
    var jsonObj = null;
    var uri = '/api/v1/shoppinglists/';
    if(!_currentShoppingList) {
        // Create new ShoppingList using a ShoppingList resource
        // TODO include list name
        jsonObj = {
            'items': items
        };
    }
    else {
        // Create new ShoppingListItem(s) for an existing ShoppingList
        uri += _currentShoppingList.id + '/items/';
        jsonObj = _createActionResource(REQ_CRUD_ACTION_CREATE, items);
    }
    var jsonData = $.toJSON(jsonObj);
    _actionStart(ACTION_SAVE_NEW);
    $.post(uri, jsonData, function(data) {
            _actionComplete(ACTION_SAVE_NEW);
            _setStatusMessage('Saved new items!');
            // TODO Rather than reload the whole list, process the JSON response and assign ids to the new items.
            if(_currentShoppingList) {
                _loadShoppingList(_currentShoppingList.id);
            }
            else {
                _loadShoppingList(data.id);
            }
        })
        .error(function() { // params: data, jqxhr
            _actionComplete(ACTION_SAVE_NEW);
            _setStatusMessage('Failed to Save new items!');
        });
},
_sendDeletedItems = function(items) {
    if(!_currentShoppingList || !items || items.length <= 0) {
        return;
    }
    var uri = '/api/v1/shoppinglists/' + _currentShoppingList.id + '/items/';

    var actionResource = _createActionResource(REQ_CRUD_ACTION_DELETE, items);
    var jsonData = $.toJSON(actionResource);
    _actionStart(ACTION_SAVE_DELETED);
    $.post(uri, jsonData, function() { // params: data, jqxhr
            _actionComplete(ACTION_SAVE_DELETED);
            _setStatusMessage('Saved deleted items!');
            _resetEditorItemDeleteMap();
        })
        .error(function() {
            _actionComplete(ACTION_SAVE_DELETED);
            _setStatusMessage('Failed to Save deleted items!');
        });
},
_sendShoppingListMeta = function() {
    if(!_currentShoppingList) {
        return;
    }
    var uri = '/api/v1/shoppinglists/' + _currentShoppingList.id + '/meta/';
    var jsonData = $.toJSON({
        id: _currentShoppingList.id,
        name: _getShoppingListTitle() // TODO Strip html
    });
    _actionStart(ACTION_SAVE_LIST_DETAIL);
    $.ajax({
        type: 'PUT',
        url: uri,
        data: jsonData,
        success: function() { // params: data, jqxhr
            _actionComplete(ACTION_SAVE_LIST_DETAIL);
            _setStatusMessage('Saved Title!');
        },
        error: function() {
            _actionComplete(ACTION_SAVE_LIST_DETAIL);
            _setStatusMessage('Failed to Save Title!');
        }
    });
},
_saveShoppingList = function() {
    if(_isActionRunning()) {
        return;
    }

    // TODO Create/save new shopping list

    _setStatusMessage("Saving shopping list...");
    // Save existing items.
    var updatedItems = _createItemsArray(function(itemObj) {
        var itemId = itemObj.id;
        return _isValidIdFormat(itemId) && isDefined(_editorItemDirtyMap[itemId]) && _editorItemDirtyMap[itemId];
    });
    var newItems = _createItemsArray(function(itemObj) {
        return !_isValidIdFormat(itemObj.id);
    });
    var deletedItems = _createDeletedItemsArray();
    var shouldSaveTitle = _getShoppingListTitle() != INSTRUCTIONS_ENTER_TITLE
            && _currentShoppingList && _currentShoppingList.name != INSTRUCTIONS_ENTER_TITLE;

    if(updatedItems.length <= 0 && newItems.length <= 0 && deletedItems.length <= 0 && !shouldSaveTitle) {
        _setStatusMessage('No items modified. Skipping save.');
        return;
    }

    if(_currentShoppingList && updatedItems.length > 0) {
        _sendUpdatedItems(updatedItems);
    }
    if(newItems.length > 0) {
        _sendNewItems(newItems);
    }
    if(deletedItems.length > 0) {
        _sendDeletedItems(deletedItems);
    }
    if(shouldSaveTitle) {
        _sendShoppingListMeta();
    }
},
//
// entryElement: div for the ShoppingList nav item choice.
//
_loadShoppingListFromNav = function(entryElement) {
    if(_isActionRunning()) {
        return;
    }
    // Reset color on previous selection
    // TODO This does on all, we should just do the one.
    _getShoppingListChooserEntries().removeClass('listChoiceHighlighted');

    entryElement.addClass('listChoiceHighlighted');
    var shoppingListId = entryElement.attr('id');
    _loadShoppingList(shoppingListId);
},
_updateAddItemLabel = function() {
    $('#addItemLabel').html('Click here to add an item to your shopping list.');
},
_loadShoppingListClickHandler = function() {
    _loadShoppingListFromNav($(this));
},
_loadFirstShoppingList = function() {
    // Create an empty table.
    _createEditorTable();

    var firstListEntry = _getShoppingListChooserEntries().first();
    // TODO JQuery returns an element with nothing in it... these checks always pass.
    if(isDefined(firstListEntry) && isDefined(firstListEntry.attr)) {
        _loadShoppingListFromNav(firstListEntry);
    }
}
;


////////////////////////////////////////////////////////////////////
// Event registration
//

var _registerChooserEvents = function() {
    // TODO Is there a way to directly select all #shoppingListChooser.li ?
    var selection = _getShoppingListChooserEntries();
    if( isEmpty(selection)) {
        return;
    }
    selection.click(_loadShoppingListClickHandler);
},
_registerButtonEvents = function() {
    $('#saveButton').click(function() {
        _saveShoppingList();
    });
    $('#createButton').click(function() {
        // TODO impl
        _setStatusMessage('Sorry, use the <a href="../">other editor</a>!')
    });
},
_registerEditableEvents = function() {
    $("#shoppingListTitleLabel").editable( {
        editClass: 'editorItemEditing',
        onEdit: function() { // params: content
            $("#shoppingListTitleLabel > input").select();

            _registerEditableKeyHandler.apply(this);
        },
        onSubmit: function(content) {
            _setShoppingListTitle(content.current);
        }
    });

    $('#addItemLabel').editable( {
        editClass: 'editorItemEditing',
        onEdit: function() { // params: content
            var inputElem = $("#addItemLabel > input").first();
            inputElem.val('');

            _registerEditableKeyHandler.apply(this);
        },
        onSubmit: function(content) {
            _updateAddItemLabel();
            _addNewItem(content.current);
        },
        onCancel: function() {
            _updateAddItemLabel();
        }
    });
},
_registerStatusEvents = function() {
    var resizeStatusLogDialog = function() {
        // Workaround to ensure the status log dialog survives resize.
        // TODO If the dialog is open during resize, still need to apply width/height (e.g. by close/re-open)
        var body = $('body');
        $("#statusLogDialog").dialog('option', 'width', body.width() * 0.5);
        $("#statusLogDialog").dialog('option', 'height', body.height() * 0.9);
    };
    var logWidth = $('body').width() * 0.5;
    $('#statusLogDialog').dialog( {
        autoOpen: false,
        close: function() {
            $(this).html('');
        },
        open: function() {
            $(this).html(_getStatusLogHtml());
        },
        modal: true,
        title: 'Status Message Log'
    } );
    $(window).resize(function() {
        resizeStatusLogDialog();
    });
    resizeStatusLogDialog();
    $('#statusMessageLabel').click(function(e) {
         $('#statusLogDialog').dialog('open');
    });
};

////////////////////////////////////////////////////////////////////
// Init
//

var _init = function() {
    //$('#shoppingListChooserDiv').jScrollPane();

    _resetEditorItemDirtyMap();

    _registerChooserEvents();
    _registerButtonEvents();
    _updateAddItemLabel();
    _registerEditableEvents();
    _registerStatusEvents();
    _loadFirstShoppingList();
};

$(document).ready(function() {
    _init();
})

})(window);
