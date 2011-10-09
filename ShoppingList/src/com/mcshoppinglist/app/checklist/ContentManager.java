package com.mcshoppinglist.app.checklist;

import java.util.HashSet;
import java.util.Set;

import android.content.ContentResolver;
import android.content.ContentValues;
import android.net.Uri;

import com.mcshoppinglist.app.common.AppConstants;
import com.mcshoppinglist.app.dataprovider.ShoppingListData.ShoppingItems;
import com.mcshoppinglist.app.json.model.ShoppingListItem;
import com.mcshoppinglist.app.util.MCLogger;

public class ContentManager {

    private int numItems = 0;
    private Set<String> labelsSet = new HashSet<String>();
    private final ContentResolver contentResolver;

    public ContentManager(ContentResolver contentResolver) {
        this.contentResolver = contentResolver;
    }

    // public Uri insertItemToDB(int shoppingListId, ShoppingListItem item) {
    // return insertItemToDB(shoppingListId, item);
    // }

    public Uri insertItemToDB(String shoppingListId, ShoppingListItem item) {
        ContentValues valuesToSaved = new ContentValues();
        // TODO Is it necessary to explicitly box primitives (int) below (Integer)?
        valuesToSaved.put(ShoppingItems.SHOPPING_LIST_ID, shoppingListId);
        valuesToSaved.put(ShoppingItems.SHOPPING_ITEM_ID, item.getId());
        valuesToSaved.put(ShoppingItems.ITEM, item.getName());
        valuesToSaved.put(ShoppingItems.CHECKED,
                        AppConstants.convertToCheckedIntValue(item.isChecked()));
        valuesToSaved.put(ShoppingItems.POSITION, new Integer(numItems));
        if (item.getLabels() != null) {
            valuesToSaved.put(ShoppingItems.LABELS, item.getLabels());
            // TODO This is not the right way to track the available labels.
            labelsSet.add(item.getLabels());
        }

        Uri uri = contentResolver.insert(ShoppingItems.CONTENT_URI, valuesToSaved);
        // TODO This way of tracking number of items may break when we have a separate server sync thread.
        numItems++;
        return uri;
    }

    public int updateItem(String shoppingListId, ShoppingListItem item) {
        String whereClause = ShoppingItems.SHOPPING_ITEM_ID + "='" + item.getId() + "'";

        ContentValues values = new ContentValues();
        values.put(ShoppingItems.SHOPPING_LIST_ID, shoppingListId);
        // values.put(ShoppingItems.SHOPPING_ITEM_ID, new Integer(item.getId()));
        values.put(ShoppingItems.ITEM, item.getName());
        values.put(ShoppingItems.CHECKED, AppConstants.convertToCheckedIntValue(item.isChecked()));
        // values.put(ShoppingItems.POSITION, new Integer(numItems));
        if (item.getLabels() != null) {
            values.put(ShoppingItems.LABELS, item.getLabels());
            labelsSet.add(item.getLabels());
        }
        // Uri uri = ContentUris.withAppendedId(ShoppingItems.CONTENT_URI, item.getId());
        int numUpdated = contentResolver.update(ShoppingItems.CONTENT_URI, values, whereClause,
                        null);
        MCLogger.d(getClass(), "Updated " + numUpdated + " item for '" + item.getName() + "'");
        return numUpdated;
    }

    public Uri insertItemToDB(String shoppingListId, String itemName, String labelsText) {
        ShoppingListItem item = new ShoppingListItem();
        item.setName(itemName);
        item.setLabels(labelsText);
        return insertItemToDB(shoppingListId, item);
    }

    public void removeAllItemsFromDB() {
        contentResolver.delete(ShoppingItems.CONTENT_URI, null, null);
        numItems = 0;
        labelsSet.clear();
    }

    public int getNumItems() {
        return numItems;
    }

    public void setNumItems(int numItems) {
        this.numItems = numItems;
    }

    public Set<String> getLabelsSet() {
        return labelsSet;
    }

    public void setLabelsSet(Set<String> labelsSet) {
        this.labelsSet = labelsSet;
    }

}
