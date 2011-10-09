package com.mcshoppinglist.app.itemsuggestion;

import android.content.Context;
import android.database.Cursor;
import android.widget.SimpleCursorAdapter;

import com.mcshoppinglist.app.dataprovider.ShoppingListData;
import com.mcshoppinglist.app.R;

/**
 * Adapt a ShoppingItems cursor to item_suggestion (entry in AutoCompleteTextView).
 */
public class ItemSuggestionCursorAdapter extends SimpleCursorAdapter {
	public ItemSuggestionCursorAdapter(Context context, Cursor cur) {
		super(context, R.layout.item_suggestion, cur, new String[] { ShoppingListData.ShoppingItems.ITEM },
				new int[] { R.id.item_suggestion });

		setCursorToStringConverter(new ItemCursorToStringConverter());
	}
}
