package com.mcshoppinglist.app.checklist;

import java.util.List;

import android.app.Application;
import android.content.SharedPreferences;
import android.content.SharedPreferences.Editor;
import android.preference.PreferenceManager;

import com.mcshoppinglist.app.R;
import com.mcshoppinglist.app.common.AppConstants;
import com.mcshoppinglist.app.common.AppConstants.ETagTrigger;
import com.mcshoppinglist.app.json.model.ShoppingListItem;
import com.mcshoppinglist.app.util.MCLogger;

public class ShoppingListApplication extends Application {

    // TODO deal with multiple shopping list? May be change to hashmap?
    private List<ShoppingListItem> mostRecentDiffs;

    private ContentManager contentMgr;

    // private final Map<String, String> savedEtags = new HashMap<String, String>(5);

    @Override
    public void onCreate() {
        super.onCreate();
        contentMgr = new ContentManager(getContentResolver());

        // No need to save etag to memory
        // SharedPreferences sharedPrefs = getSharedPreferences(AppConstants.PREFS_NAME, MODE_PRIVATE);
        // Set<String> prefsKeys = sharedPrefs.getAll().keySet();
        // for (String key : prefsKeys) {
        // if (key.startsWith(AppConstants.PREFS_SAVED_ETAG)) {
        // savedEtags.put(key, sharedPrefs.getString(AppConstants.PREFS_SAVED_ETAG, null);
        //
        // }
    }

    public List<ShoppingListItem> getMostRecentDiffs() {
        return mostRecentDiffs;
    }

    public void setMostRecentDiffs(List<ShoppingListItem> mostRecentDiffs) {
        this.mostRecentDiffs = mostRecentDiffs;
    }

    public ContentManager getContentManager() {
        return contentMgr;
    }

    public String getEtag(String shoppingListId) {
        SharedPreferences sharedPrefs = getShoppingListSharedPrefs();
        String savedEtag = sharedPrefs.getString(AppConstants.PREFS_SAVED_ETAG_PREFIX
                        + shoppingListId, null);
        return savedEtag;
    }

    public boolean saveEtag(String shoppingListId, String etag, ETagTrigger trigger) {
        boolean updated = false;
        String triggerString = "[ETagUpdateTrigger=" + trigger + "] for shoppingListId="
                        + shoppingListId + " - ";
        if (etag == null || etag.length() <= 0) {
            MCLogger.w(getClass(), triggerString
                            + "Etag is empty, not updating existing saved etag for shoppingList="
                            + shoppingListId);
        } else {
            SharedPreferences sharedPrefs = getShoppingListSharedPrefs();
            Editor prefsEditor = sharedPrefs.edit();
            prefsEditor.putString(AppConstants.PREFS_SAVED_ETAG_PREFIX + shoppingListId, etag);
            updated = prefsEditor.commit();
            if (updated) {
                MCLogger.i(getClass(), triggerString + "Updated etag to " + etag);
            } else {
                MCLogger.i(getClass(), triggerString + "Failed to update etag to " + etag);
            }
        }
        return updated;
    }

    public SharedPreferences getShoppingListSharedPrefs() {
        SharedPreferences prefs = PreferenceManager.getDefaultSharedPreferences(this);
        return prefs;
    }

    public boolean isNetworkEnable() {
        SharedPreferences prefs = getShoppingListSharedPrefs();
        boolean updateEnabled = prefs.getBoolean(getString(R.string.prefs_network_enable), true);
        return updateEnabled;
    }

}
