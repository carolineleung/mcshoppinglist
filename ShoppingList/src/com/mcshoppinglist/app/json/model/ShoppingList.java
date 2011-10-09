package com.mcshoppinglist.app.json.model;

import java.util.List;

public class ShoppingList implements IJsonSerializable {

    private List<ShoppingListItem> items;

    private String id;
    private String name;

    public List<ShoppingListItem> getItems() {
        return items;
    }

    public void setItems(List<ShoppingListItem> items) {
        this.items = items;
    }

    public String getId() {
        return id;
    }

    public void setId(String id) {
        this.id = id;
    }

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

}
