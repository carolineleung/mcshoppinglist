package com.mcshoppinglist.app.dataprovider;

import java.util.HashMap;
import java.util.Map;

import android.content.ContentProvider;
import android.content.ContentUris;
import android.content.ContentValues;
import android.content.UriMatcher;
import android.database.Cursor;
import android.database.SQLException;
import android.database.sqlite.SQLiteDatabase;
import android.database.sqlite.SQLiteQueryBuilder;
import android.net.Uri;
import android.text.TextUtils;

import com.mcshoppinglist.app.common.AppConstants;
import com.mcshoppinglist.app.dataprovider.ShoppingListData.ShoppingItems;

public class ShoppingListDataProvider extends ContentProvider {

    public static final String SHOPPING_LIST_TABLE_NAME = "shopping_list";

    private static final int ITEMS_MULTI = 1;
    private static final int ITEM_SINGLE_ID = 2;
    // private static final int LIVE_FOLDER_NOTES = 3;

    private static final UriMatcher uriMatcher;
    private static Map<String, String> projectionMap;

    private ShoppingListDatabaseHelper dbHelper;

    static {
        uriMatcher = new UriMatcher(UriMatcher.NO_MATCH);
        uriMatcher.addURI(ShoppingListData.AUTHORITY, SHOPPING_LIST_TABLE_NAME, ITEMS_MULTI);
        uriMatcher.addURI(ShoppingListData.AUTHORITY, SHOPPING_LIST_TABLE_NAME + "/#",
                        ITEM_SINGLE_ID);
        // uriMatcher.addURI(ShoppingListData.AUTHORITY, "live_folders/notes", LIVE_FOLDER_NOTES);

        projectionMap = new HashMap<String, String>();
        projectionMap.put(ShoppingItems._ID, ShoppingItems._ID);
        projectionMap.put(ShoppingItems.SHOPPING_LIST_ID, ShoppingItems.SHOPPING_LIST_ID);
        projectionMap.put(ShoppingItems.SHOPPING_ITEM_ID, ShoppingItems.SHOPPING_ITEM_ID);
        projectionMap.put(ShoppingItems.ITEM, ShoppingItems.ITEM);
        projectionMap.put(ShoppingItems.CHECKED, ShoppingItems.CHECKED);
        projectionMap.put(ShoppingItems.POSITION, ShoppingItems.POSITION);
        projectionMap.put(ShoppingItems.LABELS, ShoppingItems.LABELS);
        projectionMap.put(ShoppingItems.ADDITIONAL_NOTES, ShoppingItems.ADDITIONAL_NOTES);
        projectionMap.put(ShoppingItems.MODIFIED_DATE, ShoppingItems.MODIFIED_DATE);

        // Support for Live Folders.
        // sLiveFolderProjectionMap = new HashMap<String, String>();
        // sLiveFolderProjectionMap.put(LiveFolders._ID, Notes._ID + " AS " + LiveFolders._ID);
        // sLiveFolderProjectionMap.put(LiveFolders.NAME, Notes.TITLE + " AS " + LiveFolders.NAME);
    }

    @Override
    public boolean onCreate() {
        dbHelper = new ShoppingListDatabaseHelper(getContext());
        return false;
    }

    @Override
    public int delete(Uri uri, String where, String[] whereArgs) {
        SQLiteDatabase db = dbHelper.getWritableDatabase();
        int count;
        switch (uriMatcher.match(uri)) {
        case ITEMS_MULTI:
            count = db.delete(SHOPPING_LIST_TABLE_NAME, where, whereArgs);
            break;

        case ITEM_SINGLE_ID:
            String itemId = uri.getPathSegments().get(1);
            count = db.delete(SHOPPING_LIST_TABLE_NAME, ShoppingItems._ID + "=" + itemId
                            + (!TextUtils.isEmpty(where) ? " AND (" + where + ')' : ""), whereArgs);
            break;

        default:
            throw new IllegalArgumentException("Unknown URI " + uri);
        }

        getContext().getContentResolver().notifyChange(uri, null);
        return count;
    }

    @Override
    public String getType(Uri uri) {
        switch (uriMatcher.match(uri)) {
        case ITEMS_MULTI:
            // case LIVE_FOLDER_NOTES:
            return ShoppingItems.CONTENT_TYPE_MULTI;

        case ITEM_SINGLE_ID:
            return ShoppingItems.CONTENT_TYPE_SINGLE;

        default:
            throw new IllegalArgumentException("Unknown URI " + uri);
        }
    }

    @Override
    public Uri insert(Uri uri, ContentValues initialValues) {
        // Validate the requested uri
        if (uriMatcher.match(uri) != ITEMS_MULTI) {
            throw new IllegalArgumentException("Unknown URI " + uri);
        }

        ContentValues values;
        if (initialValues != null) {
            values = new ContentValues(initialValues);
        } else {
            values = new ContentValues();
        }

        Long now = Long.valueOf(System.currentTimeMillis());

        // Make sure that the fields are all set
        if (!values.containsKey(ShoppingItems.ITEM)) {
            values.put(ShoppingItems.ITEM, "");
        }

        if (!values.containsKey(ShoppingItems.LABELS)) {
            values.put(ShoppingItems.LABELS, "");
        }

        if (!values.containsKey(ShoppingItems.ADDITIONAL_NOTES)) {
            values.put(ShoppingItems.ADDITIONAL_NOTES, "");
        }

        // TODO handle incrementing position

        if (!values.containsKey(ShoppingItems.SHOPPING_LIST_ID)) {
            values.put(ShoppingItems.SHOPPING_LIST_ID, AppConstants.INVALID_SHOPPING_LIST_ID);
        }

        if (!values.containsKey(ShoppingItems.SHOPPING_ITEM_ID)) {
            values.put(ShoppingItems.SHOPPING_ITEM_ID, AppConstants.INVALID_SHOPPING_LIST_ID);
        }

        if (!values.containsKey(ShoppingItems.MODIFIED_DATE)) {
            values.put(ShoppingItems.MODIFIED_DATE, now);
        }

        SQLiteDatabase db = dbHelper.getWritableDatabase();

        long rowId = db.insert(SHOPPING_LIST_TABLE_NAME, ShoppingItems.ITEM, values);

        if (rowId > 0) {
            Uri noteUri = ContentUris.withAppendedId(ShoppingItems.CONTENT_URI, rowId);
            getContext().getContentResolver().notifyChange(noteUri, null);
            return noteUri;
        }

        throw new SQLException("Failed to insert row into " + uri);
    }

    @Override
    public Cursor query(Uri uri, String[] projection, String selection, String[] selectionArgs,
                    String sortOrder) {
        SQLiteQueryBuilder qb = new SQLiteQueryBuilder();
        qb.setTables(SHOPPING_LIST_TABLE_NAME);

        int matchResult = uriMatcher.match(uri);
        switch (matchResult) {
        case ITEMS_MULTI:
            qb.setProjectionMap(projectionMap);
            break;

        case ITEM_SINGLE_ID:
            qb.setProjectionMap(projectionMap);
            qb.appendWhere(ShoppingItems._ID + "=" + uri.getPathSegments().get(1));
            break;

        // case LIVE_FOLDER_NOTES:
        // qb.setProjectionMap(sLiveFolderProjectionMap);
        // break;

        default:
            throw new IllegalArgumentException("Unknown URI " + uri);
        }

        // If no sort order is specified, use the default
        String orderBy;
        if (TextUtils.isEmpty(sortOrder)) {
            orderBy = ShoppingItems.DEFAULT_SORT_ORDER;
        } else {
            orderBy = sortOrder;
        }

        // Get the database and run the query
        SQLiteDatabase db = dbHelper.getReadableDatabase();
        Cursor c = qb.query(db, projection, selection, selectionArgs, null, null, orderBy);

        // Tell the cursor what uri to watch, so it knows when its source data changes
        c.setNotificationUri(getContext().getContentResolver(), uri);
        return c;
    }

    @Override
    public int update(Uri uri, ContentValues values, String where, String[] whereArgs) {
        SQLiteDatabase db = dbHelper.getWritableDatabase();
        int count;
        switch (uriMatcher.match(uri)) {
        case ITEMS_MULTI:
            count = db.update(SHOPPING_LIST_TABLE_NAME, values, where, whereArgs);
            break;

        case ITEM_SINGLE_ID:
            String itemId = uri.getPathSegments().get(1);
            count = db.update(SHOPPING_LIST_TABLE_NAME, values, ShoppingItems._ID + "=" + itemId
                            + (!TextUtils.isEmpty(where) ? " AND (" + where + ')' : ""), whereArgs);
            break;

        default:
            throw new IllegalArgumentException("Unknown URI " + uri);
        }

        getContext().getContentResolver().notifyChange(uri, null);
        return count;
    }

}
