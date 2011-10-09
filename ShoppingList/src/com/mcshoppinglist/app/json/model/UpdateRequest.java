package com.mcshoppinglist.app.json.model;

import java.util.List;

public class UpdateRequest implements IJsonSerializable {

    public static final String ACTION_UPDATE = "UPDATE";
    public static final String ACTION_CREATE = "CREATE";
    public static final String ACTION_DELETE = "DELETE";

    private List<ShoppingListItem> items;

    private String action;

    public UpdateRequest() {
        super();
    }

    public List<ShoppingListItem> getItems() {
        return items;
    }

    public void setItems(List<ShoppingListItem> items) {
        this.items = items;
    }

    public String getAction() {
        return action;
    }

    public void setAction(String action) {
        this.action = action;
    }

}
