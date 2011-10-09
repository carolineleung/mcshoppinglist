package com.mcshoppinglist.app.checklist.listeners;

import android.content.ContentUris;
import android.content.ContentValues;
import android.net.Uri;
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
        int itemId = finder.getItemLocalIdTag();
        String shoppingItemId = finder.getShoppingItemIdTag();
        String itemText = finder.getItemTextTag();

        // int checked = isChecked ? AppConstants.CHECKED_VALUE : AppConstants.UNCHECKED_VALUE;
        int checked = AppConstants.convertToCheckedIntValue(isChecked);
        ViewUpdateUtil.setTextBold(!isChecked, item, itemText);

        // TODO if Log.d enabled,
        MCLogger.d(getClass(), "onCheckedChanged: " + "itemId=" + itemId + ", shoppingItemId="
                        + finder.getShoppingItemIdTag() + ", isChecked=" + isChecked + ", item="
                        + itemText);

        // Update client local DB
        ContentValues values = new ContentValues();
        values.put(ShoppingItems.CHECKED, new Integer(checked));

        Uri uri = ContentUris.withAppendedId(ShoppingItems.CONTENT_URI, itemId);
        activity.getContentResolver().update(uri, values, null, null);

        // Update server if network is enabled
        boolean updateEnabled = activity.getShoppingListApplication().isNetworkEnable();
        if (!updateEnabled) {
            return;
        }

        JsonParser parser = new JsonParser();
        ShoppingListItem itemToUpdate = new ShoppingListItem();
        itemToUpdate.setId(shoppingItemId);
        itemToUpdate.setChecked(isChecked);

        String shoppingListId = finder.getShoppingListIdTag();
        String etag = activity.getShoppingListApplication().getEtag(shoppingListId);

        boolean updatedToServer = parser.updateItem(shoppingListId, itemToUpdate, etag);
        if (!updatedToServer) {
            MCLogger.d(getClass(), "Failed to update check state to server for " + itemText
                            + ", shoppingListId=" + shoppingListId);
            // CL: Do not make toast to clutter the UI
            // Toast.makeText(activity, "Failed to update check state to server for " + itemText,
            // Toast.LENGTH_LONG).show();
        }
    }

}
