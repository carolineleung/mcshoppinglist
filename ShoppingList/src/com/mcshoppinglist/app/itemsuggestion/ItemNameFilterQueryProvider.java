package com.mcshoppinglist.app.itemsuggestion;

import android.app.Activity;
import android.database.Cursor;
import android.widget.FilterQueryProvider;

import com.mcshoppinglist.app.dataprovider.ShoppingListData;
import com.mcshoppinglist.app.dataprovider.ShoppingListData.ShoppingItems;

public class ItemNameFilterQueryProvider implements FilterQueryProvider {
	private Activity activity;

	// TODO Is passing in an Activity (to use managedQuery) an improper use of Activity?
	public ItemNameFilterQueryProvider(Activity activity) {
		this.activity = activity;
	}

	@Override
	public Cursor runQuery(CharSequence constraint) {
		String whereClause = null;
		if (constraint != null) {
			String constraintStr = constraint.toString();
			// TODO tolower(ITEM)
			// Where the item name starts with constraint
			whereClause = ShoppingListData.ShoppingItems.ITEM + " LIKE '" + constraintStr.toLowerCase() + "%'";
		}
		Cursor cursor = activity.managedQuery(ShoppingItems.CONTENT_URI, new String[] { ShoppingItems._ID,
				ShoppingItems.ITEM }, whereClause, null, ShoppingItems.DEFAULT_SORT_ORDER);
		return cursor;
	}
}
