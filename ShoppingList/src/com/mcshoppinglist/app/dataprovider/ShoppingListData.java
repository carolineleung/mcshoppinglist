package com.mcshoppinglist.app.dataprovider;

import android.net.Uri;
import android.provider.BaseColumns;

/**
 * Convenience definitions for ShoppingListDataProvider
 */
public final class ShoppingListData {

    public static final String AUTHORITY = "com.mcshoppinglist.app.shoppinglistdataprovider";

    // This class cannot be instantiated
    private ShoppingListData() {
    }

    /**
     * Notes table
     */
    public static final class ShoppingItems implements BaseColumns {
        // This class cannot be instantiated
        private ShoppingItems() {
        }

        // TODO We have column names lumped together with URIs, separate them so that ONLY column names appear in X, and
        // other stuff in Y.
        /**
         * The content:// style URL for this table
         */
        public static final Uri CONTENT_URI = Uri.parse("content://" + AUTHORITY + "/"
                        + ShoppingListDataProvider.SHOPPING_LIST_TABLE_NAME);
        /**
         * The MIME type of {@link #CONTENT_URI} providing a directory of items.
         */
        public static final String CONTENT_TYPE_MULTI = "vnd.mcshoppinglist.cursor.dir/vnd.mcshoppinglist.item";

        /**
         * The MIME type of a {@link #CONTENT_URI} sub-directory of a single item.
         */
        public static final String CONTENT_TYPE_SINGLE = "vnd.mcshoppinglist.cursor.item/vnd.mcshoppinglist.item";

        /**
         * ID of the ShoppingList from the server.
         */
        public static final String SHOPPING_LIST_ID = "shopping_list_id";

        /**
         * ID of the ShoppingListItem from the server.
         */
        public static final String SHOPPING_ITEM_ID = "shopping_item_id";

        /**
         * The content of the item <P>Type: TEXT</P>
         */
        public static final String ITEM = "item";

        /**
         * Whether the item is checked <P>Type: INTEGER (translate to Boolean)</P>
         */
        public static final String CHECKED = "checked";

        /**
         * The position of the item <P>Type: INTEGER</P>
         */
        public static final String POSITION = "position";

        /**
         * The label(s) of the item <P>Type: TEXT</P>
         */
        public static final String LABELS = "labels";

        /**
         * Additional notes of the item (optional) <P>Type: TEXT</P>
         */
        public static final String ADDITIONAL_NOTES = "notes";

        /**
         * The timestamp for when the item was last modified
         * 
         * <P>Type: INTEGER (long from System.curentTimeMillis())</P>
         */
        // TODO Rename to LAST_MODIFIED_DATE
        public static final String MODIFIED_DATE = "last_modified";

        /**
         * The default sort order for this table, position ascending
         */
        public static final String DEFAULT_SORT_ORDER = POSITION + " ASC";

    }
}
