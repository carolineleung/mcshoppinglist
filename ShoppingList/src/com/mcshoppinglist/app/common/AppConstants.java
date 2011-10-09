package com.mcshoppinglist.app.common;

public class AppConstants {
    public static final int INVALID_ID = -1;
    public static final String INVALID_SHOPPING_LIST_ID = "";
    public static final int UNCHECKED_VALUE = 0;
    public static final int CHECKED_VALUE = 1;

    // TODO Move the CHECKED constants and helpers to their own class
    public static int convertToCheckedIntValue(boolean checked) {
        return checked ? CHECKED_VALUE : UNCHECKED_VALUE;
    }

    public static boolean convertToCheckedBoolValue(int checked) {
        return checked == CHECKED_VALUE ? true : false;
    }

    public static final int CONNECTION_TIMEOUT_MILLIS = 5000;
    public static final int SOCKET_TIMEOUT_MILLIS = 5000;

    public static final String RESOURCE_SHOPPING_LIST_PATH = "res/raw/shopping.txt";
    public static final String[] DROPBOX_SHOPPING_LIST_PATHS = new String[] {
                    "external_sd/dropbox/shopping/shopping.txt",
                    "external_sd/dropbox/docs/shopping/shopping.txt",
                    "sdcard/dropbox/docs/shopping/shopping.txt",
                    "/dropbox/docs/shopping/shopping.txt" };

    public static final String LABEL_PREFIX = "___";

    // public static final String PREFS_NAME = "com.mcshoppinglist.app.service.ShoppingListUpdateService";
    public static final String PREFS_SAVED_ETAG_PREFIX = "savedEtag_";
    // public static final String PREFS_ENABLE_UPDATE = "enableUpdate";
    // public static final String PREFS_UPDATE_FREQUENCY_MIN = "updateFrequencyMin";

    public static final String HTTP_HEADER_ETAG = "ETag";
    public static final String HTTP_HEADER_IF_NONE_MATCH = "If-None-Match";

    public static final int BACKGROUND_SVC_DEFAULT_DIFFS_FREQUENCY_IN_SEC = 8; // TODO 30 sec as default okay?
    public static final String INTENT_KEY_SHOPPING_LIST_ID = "ShoppingListId";
    public static final String INTENT_REFRESH_FULL_LIST_KEY = "RefreshFullList";

    public enum ETagTrigger {
        RefreshShoppingList, UiUpdateItemCheckedState, BackgroundUpdateFromDiffs
    }

    // Cannot instantiate
    private AppConstants() {

    }

    // TODO Move this method somewhere more appropriate
    /**
     * @return true if the ShoppingList or ShoppingListItem ID is in a valid format. (For now, just check non-empty.)
     */
    public static boolean isValidFormatShoppingListId(String id) {
        if (id != null && id.length() > 0) {
            return true;
        }
        return false;
    }
}
