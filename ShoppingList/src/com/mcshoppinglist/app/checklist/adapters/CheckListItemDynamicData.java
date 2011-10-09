package com.mcshoppinglist.app.checklist.adapters;

public class CheckListItemDynamicData {

    private String shoppingItemId;
    private String shoppingListId;
    private int itemLocalId;
    private String itemText;

    public String getShoppingItemId() {
        return shoppingItemId;
    }

    public void setShoppingItemId(String shoppingItemId) {
        this.shoppingItemId = shoppingItemId;
    }

    public String getShoppingListId() {
        return shoppingListId;
    }

    public void setShoppingListId(String shoppingListId) {
        this.shoppingListId = shoppingListId;
    }

    public int getItemLocalId() {
        return itemLocalId;
    }

    public void setItemLocalId(int itemLocalId) {
        this.itemLocalId = itemLocalId;
    }

    public String getItemText() {
        return itemText;
    }

    public void setItemText(String itemText) {
        this.itemText = itemText;
    }

}
