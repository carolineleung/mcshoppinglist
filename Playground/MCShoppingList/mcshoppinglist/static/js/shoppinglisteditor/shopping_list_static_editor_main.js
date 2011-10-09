(function(window) {

var document = window.document;

var ACTION_SAVE = 'save',
ACTION_LOAD = 'load';

var _currentShoppingList = null,
_currentAction = null,
_labelDetectRe = new RegExp('^\\s*__+\\s*'),
_punctuationRemovalRe = new RegExp(':+');

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
}

////////////////////////////////////////////////////////////////////
// View updates
//

var _setShoppingListTitle = function(title) {
    if(!title) {
        title = '';
    }
    $("#shoppingListTitleLabel").html(title);
},
_setStatusMessage = function(text) {
    if(!text) {
        text = ''
    }
    $("#statusMessageLabel").html(text);
};



////////////////////////////////////////////////////////////////////
// Ajax callbacks
//

var _loadShoppingListSuccessHandler = function(data_obj) {
    _currentAction = null;
    _currentShoppingList = null;

    //$("#editorTextArea").val(data);
    if(isUndefined(data_obj) || data_obj == null || data_obj.length <= 0) {
        _setStatusMessage('Failed to load! (Server gave us nothing!)');
        return;
    }

    _currentShoppingList = data_obj;
    _setShoppingListTitle(data_obj.name);

    var listContent = '';
    var itemLen = data_obj.items.length;
    var currentLabel = null;
    for(var index = 0; index < itemLen; ++index) {
        var item = data_obj.items[index];
        // For debugging, show labels in ______ LabelName sections.
        if(isDefined(item.labels) && item.labels
            && item.labels != currentLabel) {
            currentLabel = item.labels;
            listContent += '_________ ' + currentLabel + '\n';
        }
        var itemName = item.name;
        listContent += itemName + '\n';
    }
    $("#editorTextArea").val(listContent);

    _setStatusMessage('Loaded!');
},
_loadShoppingListErrorHandler = function(data) {
    _currentAction = null;
    _setStatusMessage('Failed to Load!');
},
_saveShoppingListSuccessHandler = function(data, jqxhr) {
    _currentAction = null;
//    var data_obj = $.parseJSON(data);
    _setStatusMessage('Saved!');
},
_saveShoppingListErrorHandler = function(data, jqxhr) {
    _currentAction = null;
    _setStatusMessage('Failed to Save!');
};

////////////////////////////////////////////////////////////////////
// Actions
//

var _createItemsArray = function(textData) {
    var itemsTextArray = textData.split('\n');
    var len = itemsTextArray.length;
    var itemsArray = [];
    var currentLabel = null;
    for(var index = 0; index < len; ++index) {
        var itemText = itemsTextArray[index];
        itemText = $.trim(itemText);
        if(itemText) {
            // Hack to identify our syntax of:  ________ LabelName
            if(itemText.match(_labelDetectRe)) {
                currentLabel = itemText.replace(_labelDetectRe, '');
                if(currentLabel) {
                    currentLabel = currentLabel.replace(_punctuationRemovalRe, '');
                    currentLabel = $.trim(currentLabel);

                    if(!currentLabel || currentLabel.length <= 0) {
                        currentLabel = null;
                    }
                }
            }
            else {
                // ShoppingListItem resource
                var itemObj = {
                    'name': itemText
                };
                if(currentLabel) {
                    itemObj['labels'] = currentLabel;
                }
                itemsArray.push(itemObj);
            }
        }
    }
    return itemsArray;
}

var _saveShoppingList = function() {
    if(_currentAction == ACTION_SAVE) {
        return;
    }
    _setStatusMessage("Saving shopping list...");
    var textData = $("#editorTextArea").val();
    var items = _createItemsArray(textData);
    // ShoppingList resource
    var jsonObj = {
        'items': items
    };
    _currentAction = ACTION_SAVE;
    // Create new ShoppingList
    var uri = '/api/v1/shoppinglists/';
    if(_currentShoppingList) {
        // Update (replace) existing ShoppingList
        jsonObj['id'] = _currentShoppingList.id;
        uri += _currentShoppingList.id + '/';
    }
    var jsonData = $.toJSON(jsonObj);
    if(_currentShoppingList) {
        $.ajax({
            type: 'PUT',
            url: uri,
            data: jsonData,
            success: _saveShoppingListSuccessHandler,
            error: _saveShoppingListErrorHandler
        });
    }
    else {
        $.post(uri, jsonData, _saveShoppingListSuccessHandler)
            .error(_saveShoppingListErrorHandler);
    }
},
_loadShoppingList = function() {
    if(_currentAction) {
        return;
    }
    _currentAction = ACTION_LOAD;
    // Reset color on previous selection
    $('#shoppingListChooserDiv > div').removeClass('listChoiceHighlighted');

    $(this).addClass('listChoiceHighlighted');
    var currentId = $(this).attr('id');
    var uri = '/api/v1/shoppinglists/' + currentId + '/'
    _setStatusMessage('Loading....');
    // TODO Switch to getJSON?
    $.get(uri, _loadShoppingListSuccessHandler)
        .error(_loadShoppingListErrorHandler);

};

////////////////////////////////////////////////////////////////////
// Event registration
//

var _registerChooserEvents = function() {
    // TODO Is there a way to directly select all #shoppingListChooser.li ?
    var selection = $('#shoppingListChooserDiv > div');
    if( isEmpty(selection)) {
        return;
    }
    selection.click(_loadShoppingList);
},
_registerButtonEvents = function() {
    $('#saveButton').click(function() {
        _saveShoppingList();
    })
    $('#createButton').click(function() {
        _currentShoppingList = null;
        $('#editorTextArea').text('');
    })
};

////////////////////////////////////////////////////////////////////
// Init
//

var _init = function() {
    //$('#shoppingListChooserDiv').jScrollPane();

    _registerChooserEvents();
    _registerButtonEvents();
};

$(document).ready(function() {
    _init();
})

})(window);
