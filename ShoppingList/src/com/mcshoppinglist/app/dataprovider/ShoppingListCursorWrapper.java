package com.mcshoppinglist.app.dataprovider;

import android.database.Cursor;

import com.mcshoppinglist.app.common.AppConstants;
import com.mcshoppinglist.app.dataprovider.ShoppingListData.ShoppingItems;

public class ShoppingListCursorWrapper {
    private final Cursor cursor;

    public ShoppingListCursorWrapper(Cursor shoppingListCursor) {
        this.cursor = shoppingListCursor;
    }

    public String getLabel() {
        return cursor.getString(cursor.getColumnIndex(ShoppingItems.LABELS));
    }

    public String getItem() {
        return cursor.getString(cursor.getColumnIndex(ShoppingItems.ITEM));
    }

    public int getId() {
        return cursor.getInt(cursor.getColumnIndex(ShoppingItems._ID));
    }

    public String getShoppingListId() {
        return cursor.getString(cursor.getColumnIndex(ShoppingItems.SHOPPING_LIST_ID));
    }

    public String getShoppingItemId() {
        return cursor.getString(cursor.getColumnIndex(ShoppingItems.SHOPPING_ITEM_ID));
    }

    public String getNotes() {
        return cursor.getString(cursor.getColumnIndex(ShoppingItems.ADDITIONAL_NOTES));
    }

    public int getPosition() {
        return cursor.getInt(cursor.getColumnIndex(ShoppingItems.POSITION));
    }

    public int getCheckedValue() {
        return cursor.getInt(cursor.getColumnIndex(ShoppingItems.CHECKED));
    }

    public boolean isChecked() {
        return getCheckedValue() == AppConstants.CHECKED_VALUE;
    }
}
