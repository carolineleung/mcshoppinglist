package com.mcshoppinglist.app.itemsuggestion;

import android.database.Cursor;
import android.widget.SimpleCursorAdapter;

import com.mcshoppinglist.app.dataprovider.ShoppingListData.ShoppingItems;

/**
 * Convert a ShoppingItems cursor to the item name string.
 */
public class ItemCursorToStringConverter implements SimpleCursorAdapter.CursorToStringConverter {
	@Override
	public CharSequence convertToString(Cursor cursor) {
		String entryText = cursor.getString(cursor.getColumnIndex(ShoppingItems.ITEM));
		return entryText;
	}
}
