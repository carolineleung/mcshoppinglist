package com.mcshoppinglist.app.dataprovider;

import android.content.Context;
import android.database.sqlite.SQLiteDatabase;
import android.database.sqlite.SQLiteDatabase.CursorFactory;
import android.database.sqlite.SQLiteOpenHelper;

import com.mcshoppinglist.app.dataprovider.ShoppingListData.ShoppingItems;
import com.mcshoppinglist.app.util.MCLogger;

/**
 * This class helps open, create, and upgrade the ShoppingList database file.
 */
public class ShoppingListDatabaseHelper extends SQLiteOpenHelper {

    private static final int SHOPPING_LIST_DB_VERSION = 1;
    private static final String SHOPPING_LIST_DB_NAME = "shopping_list.db";;

    public ShoppingListDatabaseHelper(Context context) {
        this(context, SHOPPING_LIST_DB_NAME, null, SHOPPING_LIST_DB_VERSION);
    }

    public ShoppingListDatabaseHelper(Context context, String name, CursorFactory factory,
                    int version) {
        super(context, name, factory, version);
    }

    @Override
    public void onCreate(SQLiteDatabase db) {
        db.execSQL("CREATE TABLE " + ShoppingListDataProvider.SHOPPING_LIST_TABLE_NAME + " ("
                        + ShoppingItems._ID + " INTEGER PRIMARY KEY AUTOINCREMENT,"
                        + ShoppingItems.SHOPPING_LIST_ID + " TEXT, "
                        + ShoppingItems.SHOPPING_ITEM_ID + " TEXT, " + ShoppingItems.ITEM
                        + " TEXT," + ShoppingItems.CHECKED + " INTEGER," + ShoppingItems.POSITION
                        + " INTEGER," + ShoppingItems.LABELS + " TEXT,"
                        + ShoppingItems.ADDITIONAL_NOTES + " TEXT," + ShoppingItems.MODIFIED_DATE
                        + " INTEGER" + ");");
    }

    @Override
    public void onUpgrade(SQLiteDatabase db, int oldVersion, int newVersion) {
        MCLogger.w(getClass(), "Upgrading database from version " + oldVersion + " to "
                        + newVersion + ", which will destroy all old data");
        db.execSQL("DROP TABLE IF EXISTS notes");
        onCreate(db);
    }

}
