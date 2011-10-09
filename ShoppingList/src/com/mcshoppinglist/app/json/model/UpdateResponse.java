package com.mcshoppinglist.app.json.model;

import java.util.List;

import com.google.gson.annotations.SerializedName;

public class UpdateResponse implements IJsonSerializable {

    @SerializedName("update_count")
    private int updateCount;

    @SerializedName("items")
    private List<ShoppingListItem> updatedItems; // Need to use generic List not JsonList, otherwise gson would blow up

    public int getUpdateCount() {
        return updateCount;
    }

    public void setUpdateCount(int updateCount) {
        this.updateCount = updateCount;
    }

    public List<ShoppingListItem> getUpdatedItems() {
        return updatedItems;
    }

    public void setUpdatedItems(List<ShoppingListItem> updatedItems) {
        this.updatedItems = updatedItems;
    }

}
