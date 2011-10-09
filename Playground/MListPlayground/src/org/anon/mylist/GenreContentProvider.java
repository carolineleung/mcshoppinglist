package org.anon.mylist;

import android.content.ContentProvider;
import android.content.ContentValues;
import android.database.AbstractCursor;
import android.database.Cursor;
import android.net.Uri;
import android.provider.BaseColumns;

public class GenreContentProvider extends ContentProvider {
    // TODO How can we set underlying data outside of the ContentProvider? How to configure dynamically in onCreate()?
    private static final String[] GENRES = new String[] { "Action", "Adventure", "Animation", "Children", "Comedy",
            "Documentary", "Drama", "Foreign", "History", "Independent", "Romance", "Sci-Fi", "Television", "Thriller",

            "Action2", "Adventure2", "Animation2", "Children2", "Comedy2", "Documentary2", "Drama2", "Foreign2",
            "History2", "Independent2", "Romance2", "Sci-Fi2", "Television2", "Thriller2", };
    private final Object[] underlyingData = GENRES;

    public static final Uri CONTENT_URI = Uri.parse("content://org.anon.mylist.genrecontentprovider");

    public static class ColumnNames {
        public static final String Genre = "Genre";
    }

    @Override
    public boolean onCreate() {
        return true;
    }

    @Override
    public Cursor query(Uri uri, String[] projection, String selection, String[] selectionArgs, String sortOrder) {
        if (!CONTENT_URI.equals(uri)) {
            throw new MyException("Invalid URI: " + (uri != null ? uri.toString() : null));
        }
        // Unused irrelevant params:
        // projection: columns to return
        // selection: rows to return
        // selectionArgs: for '?' in selection query
        // sortOrder: e.g. COL_NAME ASC

        return new GenreCursor();
    }

    @Override
    public String getType(Uri uri) {
        // This "MIME type" is constant and irrelevant in this case.
        // http://developer.android.com/guide/topics/providers/content-providers.html
        return "vnd.android.cursor.item/vnd.org.anon.mylist.arraydata";
    }

    @Override
    public Uri insert(Uri uri, ContentValues values) {
        // TODO Auto-generated method stub
        return null;
    }

    @Override
    public int delete(Uri uri, String selection, String[] selectionArgs) {
        // TODO Auto-generated method stub
        return 0;
    }

    @Override
    public int update(Uri uri, ContentValues values, String selection, String[] selectionArgs) {
        // TODO Auto-generated method stub
        return 0;
    }

    private class GenreCursor extends AbstractCursor {

        @Override
        public int getCount() {
            return underlyingData.length;
        }

        @Override
        public String[] getColumnNames() {
            return new String[] { BaseColumns._ID, ColumnNames.Genre };
        }

        @Override
        public String getString(int column) {
            if (getPosition() < 0 || getPosition() > underlyingData.length) {
                throw new MyException("Invalid cursor position: " + getPosition());
            }
            if (column == 0) {
                // _ID
                return new Integer(getPosition()).toString();
            }
            // column 1
            Object obj = underlyingData[getPosition()];
            return (obj != null ? obj.toString() : "");
        }

        @Override
        public short getShort(int column) {
            return 0;
        }

        @Override
        public int getInt(int column) {
            return 0;
        }

        @Override
        public long getLong(int column) {
            return 0;
        }

        @Override
        public float getFloat(int column) {
            return 0;
        }

        @Override
        public double getDouble(int column) {
            return 0;
        }

        @Override
        public boolean isNull(int column) {
            return false;
        }

        @Override
        public String toString() {
            try {
                return getString(0);
            } catch (Exception ex) {
                return "";
            }
        }
    }
}
