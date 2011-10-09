package com.mcshoppinglist.app.checklist.listeners;

import android.content.ContentUris;
import android.content.ContentValues;
import android.net.Uri;
import android.os.AsyncTask;
import android.view.View;
import android.widget.CompoundButton;
import android.widget.CompoundButton.OnCheckedChangeListener;
import android.widget.TextView;

import com.mcshoppinglist.app.checklist.CheckListActivity;
import com.mcshoppinglist.app.checklist.finders.CheckListRowViewFinder;
import com.mcshoppinglist.app.common.AppConstants;
import com.mcshoppinglist.app.dataprovider.ShoppingListData.ShoppingItems;
import com.mcshoppinglist.app.json.JsonParser;
import com.mcshoppinglist.app.json.model.ShoppingListItem;
import com.mcshoppinglist.app.util.MCLogger;
import com.mcshoppinglist.app.util.ViewFinderUtil;
import com.mcshoppinglist.app.util.ViewUpdateUtil;

public class CheckboxChangeListener implements OnCheckedChangeListener {
	private final CheckListActivity activity;

	public CheckboxChangeListener(CheckListActivity activity) {
		this.activity = activity;
	}

	@Override
	public void onCheckedChanged(CompoundButton buttonView, boolean isChecked) {
		View parentView = ViewFinderUtil.getParentView(buttonView);
		if (parentView == null) {
			return;
		}
		CheckListRowViewFinder finder = new CheckListRowViewFinder(parentView);
		TextView item = finder.getItemTextView();
		String itemText = finder.getItemTextTag();
		ViewUpdateUtil.setTextBold(!isChecked, item, itemText);

		new HandleCheckboxChangesTask(isChecked, finder, itemText).execute();
	}

	private boolean updateChangesToDBAndServer(boolean isChecked, CheckListRowViewFinder finder, String itemText) {
		int itemId = finder.getItemLocalIdTag();
		// TODO if Log.d enabled,
		MCLogger.d(getClass(), "onCheckedChanged: " + "itemId=" + itemId + ", shoppingItemId=" + finder.getShoppingItemIdTag() + ", isChecked=" + isChecked + ", item=" + itemText);

		// Update client local DB
		// int checked = isChecked ? AppConstants.CHECKED_VALUE : AppConstants.UNCHECKED_VALUE;
		int checked = AppConstants.convertToCheckedIntValue(isChecked);

		ContentValues values = new ContentValues();
		values.put(ShoppingItems.CHECKED, new Integer(checked));

		Uri uri = ContentUris.withAppendedId(ShoppingItems.CONTENT_URI, itemId);
		activity.getContentResolver().update(uri, values, null, null);

		// Update server if network is enabled
		boolean updateEnabled = activity.getShoppingListApplication().isNetworkEnable();
		if (!updateEnabled) {
			return false;
		}

		JsonParser parser = new JsonParser();
		String shoppingItemId = finder.getShoppingItemIdTag();
		ShoppingListItem itemToUpdate = new ShoppingListItem();
		itemToUpdate.setId(shoppingItemId);
		itemToUpdate.setChecked(isChecked);

		String shoppingListId = finder.getShoppingListIdTag();
		String etag = activity.getShoppingListApplication().getEtag(shoppingListId);

		boolean updatedToServer = parser.updateItem(shoppingListId, itemToUpdate, etag);
		if (!updatedToServer) {
			MCLogger.d(getClass(), "Failed to update check state to server for " + itemText + ", shoppingListId=" + shoppingListId);
			// CL: Do not make toast to clutter the UI
			// Toast.makeText(activity, "Failed to update check state to server for " + itemText,
			// Toast.LENGTH_LONG).show();
		}
		return updatedToServer;
	}

	private class HandleCheckboxChangesTask extends AsyncTask<Void, Void, Boolean> {

		private String itemText;
		private boolean isChecked;
		private CheckListRowViewFinder finder;

		public HandleCheckboxChangesTask(boolean isChecked, CheckListRowViewFinder finder, String itemText) {
			super();
			this.isChecked = isChecked;
			this.finder = finder;
			this.itemText = itemText;
		}

		@Override
		protected Boolean doInBackground(Void... params) {
			updateChangesToDBAndServer(isChecked, finder, itemText);
			return null;
		}

	}

}
