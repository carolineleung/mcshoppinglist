package com.mcshoppinglist.app.service;

import java.util.List;
import java.util.Timer;
import java.util.TimerTask;

import android.app.Service;
import android.content.ContentResolver;
import android.content.Intent;
import android.content.SharedPreferences;
import android.os.IBinder;
import android.widget.Toast;

import com.mcshoppinglist.app.R;
import com.mcshoppinglist.app.checklist.ContentManager;
import com.mcshoppinglist.app.checklist.ShoppingListApplication;
import com.mcshoppinglist.app.common.AppConstants;
import com.mcshoppinglist.app.common.AppConstants.ETagTrigger;
import com.mcshoppinglist.app.json.JsonParser;
import com.mcshoppinglist.app.json.model.ErrorResponse;
import com.mcshoppinglist.app.json.model.ResponseContainer;
import com.mcshoppinglist.app.json.model.ShoppingList;
import com.mcshoppinglist.app.json.model.ShoppingListItem;
import com.mcshoppinglist.app.util.MCLogger;

public class ShoppingListUpdateService extends Service {

    // private static final int MS_IN_ONE_MIN = 60 * 1000;
    private static final long TIMER_DELAY_SEC = 10;

    private static final String TIMER_SHOPPING_LIST_UPDATE = "ShoppingListUpdates";

    public static final String INTENT_PROCESS_ITEM_DIFFS = "com.mcshoppinglist.app.service.PROCESS_ITEM_DIFFS";

    private JsonParser parser;

    private Timer updateTimer;

    private String shoppingListId = AppConstants.INVALID_SHOPPING_LIST_ID;

    private TimerTask doRefreshTask;

    @Override
    public void onCreate() {
        super.onCreate();
        if (parser == null) {
            parser = new JsonParser();
        }
        // TODO Getting an IllegalStateException: TimerTask started already.
        // The second time this is hit.
        // Added this updateTimer guard to ensure we don't
        if (updateTimer == null) {
            scheduleUpdateTimer();
        }
    }

    @Override
    public void onDestroy() {
        // TODO Review this timer destruction.
        if (updateTimer != null) {
            if (doRefreshTask != null) {
                doRefreshTask.cancel();
            }
            updateTimer.cancel();
            updateTimer.purge();
            updateTimer = null;
        }
        doRefreshTask = null;
        super.onDestroy();
    }

    @Override
    public void onLowMemory() {
        // TODO We should stop the current update (if any) and schedule the timer in the distant future (minutes away),
        // to free up memory.
        // TODO Anything else we can do here to free up mem?
        super.onLowMemory();
    }

    @Override
    public IBinder onBind(Intent intent) {
        // Unused. (Per the docs, binding is for "complex services".)
        return null;
    }

    // TODO Remove these if "binding" is only for complex services as doc'd in onBind
    // @Override
    // public boolean onUnbind(Intent intent) {
    // // TODO If unbind, then our shoppinglist activity has closed? We should disable all timers, but allow current
    // // updates to complete.
    // return super.onUnbind(intent);
    // }
    //
    // @Override
    // public void onRebind(Intent intent) {
    // // TODO Do the opposite of onUnbind. (Start timers up again.)
    // super.onRebind(intent);
    // }

    @Override
    public int onStartCommand(Intent intent, int flags, int startId) {
        try {
            return onStartCommandImpl(intent, flags, startId);
        } catch (Exception ex) {
            // Ensure we don't force close on failure to start update.
            MCLogger.e(getClass(), "Failed to start background sync service. " + ex.getMessage(),
                            ex);
            // TODO We should do a UI callback to notify the user that server sync is unavailable.
            // TODO Review this return value:
            return Service.START_NOT_STICKY;
        }
    }

    private int onStartCommandImpl(Intent intent, int flags, int startId) {
        MCLogger.d(getClass(), "onStartCommand with intent=" + intent.toString());

        shoppingListId = intent.getStringExtra(AppConstants.INTENT_KEY_SHOPPING_LIST_ID);
        if (!AppConstants.isValidFormatShoppingListId(shoppingListId)) {
            shoppingListId = AppConstants.INVALID_SHOPPING_LIST_ID;
        }

        setRefreshTimerTask(); // Need to reset the timerTask, otherwise will get TimerTask already scheduled error

        updateTimer.cancel();
        // TODO Review this purge, is it correct?
        updateTimer.purge();

        // TODO This should be done differently!

        if (AppConstants.isValidFormatShoppingListId(shoppingListId)
                        && intent.getBooleanExtra(AppConstants.INTENT_REFRESH_FULL_LIST_KEY, false)) {
            refreshShoppingList();
        }

        scheduleUpdateTimer();

        return Service.START_STICKY; // TODO check if this return value is okay
    }

    private void scheduleUpdateTimer() {
        SharedPreferences prefs = getShoppingListApplication().getShoppingListSharedPrefs();
        boolean updateEnabled = prefs.getBoolean(getString(R.string.prefs_network_enable), true);
        if (!updateEnabled) {
            return;
        }
        String updateFrequencySecStr = prefs.getString(getString(R.string.prefs_network_frequency),
                        "" + AppConstants.BACKGROUND_SVC_DEFAULT_DIFFS_FREQUENCY_IN_SEC);
        int updateFrequencySec = Integer.parseInt(updateFrequencySecStr.length() == 0 ? "0"
                        : updateFrequencySecStr);

        updateTimer = new Timer(TIMER_SHOPPING_LIST_UPDATE);
        setRefreshTimerTask();
        updateTimer.scheduleAtFixedRate(doRefreshTask, TIMER_DELAY_SEC * 1000,
                        updateFrequencySec * 1000);

        MCLogger.d(getClass(), "Scheduled updateItemDiffs timer to run every " + updateFrequencySec
                        + " sec with delay of " + TIMER_DELAY_SEC + " sec");
    }

    private boolean refreshShoppingList() {
        MCLogger.d(getClass(), "Refreshing full shopping list.");
        boolean refreshed = false;
        // For testing
        // InputStream testContent = getResources().openRawResource(R.raw.test_json);
        // ShoppingList shoppingList = parser.getShoppingList(testContent);

        ResponseContainer<ShoppingList> responseContainer = parser.getShoppingList(shoppingListId);
        ShoppingList shoppingList = responseContainer.getObject();
        if (shoppingList != null) {
            List<ShoppingListItem> items = shoppingList.getItems();
            if (items != null && !items.isEmpty()) {
                ShoppingListApplication shoppingListApp = getShoppingListApplication();
                ContentManager contentMgr = shoppingListApp.getContentManager();
                contentMgr.removeAllItemsFromDB();
                // TODO improve to do bulk insert
                for (ShoppingListItem item : items) {
                    contentMgr.insertItemToDB(shoppingList.getId(), item);
                }
                refreshed = true;
                updateETagPrefs(responseContainer, ETagTrigger.RefreshShoppingList);
                Toast.makeText(this, "Sync'ed " + items.size() + " items from server",
                                Toast.LENGTH_LONG).show();

            }
        } else {
            ErrorResponse errorResponse = responseContainer.getErrorResponse();
            String errorMsg = "Failed to refresh shopping list due to "
                            + errorResponse.getErrorCode() + ": " + errorResponse.getErrorMessage();
            MCLogger.w(getClass(), errorMsg);
            Toast.makeText(this, errorMsg, Toast.LENGTH_LONG).show();
        }
        return refreshed;
    }

    private boolean getItemDiffs() {
        boolean updateEnabled = getShoppingListApplication().isNetworkEnable();
        if (!updateEnabled) {
            return false;
        }

        boolean updated = false;
        String etag = getShoppingListApplication().getEtag(shoppingListId);
        ResponseContainer<ShoppingList> responseContainer = parser.getItemDiffs(shoppingListId,
                        etag);
        ShoppingList shoppingListDiffs = responseContainer.getObject();
        if (shoppingListDiffs != null) {
            List<ShoppingListItem> updatedItems = shoppingListDiffs.getItems();
            if (updatedItems != null && !updatedItems.isEmpty()) {
                MCLogger.d(getClass(), "Retrieved " + updatedItems.size() + " itemDiffs, etag1="
                                + etag + ", etag2=" + responseContainer.getETag() + ", list="
                                + shoppingListId);
                updateETagPrefs(responseContainer, ETagTrigger.BackgroundUpdateFromDiffs);
                updated = true;
                broadcastItemDiffs(updatedItems);
            } else {
                MCLogger.d(getClass(), "No updated items found for shoppingListId="
                                + shoppingListId);
            }
        }
        return updated;
    }

    private void addItem(ShoppingListItem item) {
        ContentResolver provider = getContentResolver();
        // TODO implement
    }

    private void updateItem(String shoppingListId, ShoppingListItem item, String currEtag) {
        parser.updateItem(shoppingListId, item, currEtag);
    }

    private void broadcastItemDiffs(List<ShoppingListItem> diffs) {
        Intent intentProcessItemDiffs = new Intent(INTENT_PROCESS_ITEM_DIFFS);
        getShoppingListApplication().setMostRecentDiffs(diffs);
        sendBroadcast(intentProcessItemDiffs);
    }

    private <T> void updateETagPrefs(ResponseContainer<T> responseContainer,
                    ETagTrigger updateTrigger) {
        String etag = responseContainer.getETag();
        getShoppingListApplication().saveEtag(shoppingListId, etag, updateTrigger);
    }

    private void updateItemCheckState(ShoppingListItem item) {

        // TODO implement
    }

    private void setRefreshTimerTask() {
        if (doRefreshTask != null) {
            doRefreshTask.cancel();
        }
        doRefreshTask = new TimerTask() {
            @Override
            public void run() {
                try {
                    getItemDiffs();
                } catch (Exception ex) {
                    // Prevent force close on service error.
                    MCLogger.e(getClass(), "Failed to retrieve/update item diffs.", ex);
                    // TODO Should we do a UI callback to notify the user that server sync is unavailable?
                }
            }
        };
    }

    private ShoppingListApplication getShoppingListApplication() {
        return (ShoppingListApplication) getApplication();
    }

}
