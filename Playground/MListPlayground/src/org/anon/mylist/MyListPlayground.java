package org.anon.mylist;

import android.app.ListActivity;
import android.content.Context;
import android.database.Cursor;
import android.graphics.Color;
import android.os.Bundle;
import android.view.View;
import android.view.View.OnClickListener;
import android.widget.CheckBox;
import android.widget.CompoundButton;
import android.widget.CompoundButton.OnCheckedChangeListener;
import android.widget.ListView;
import android.widget.SimpleCursorAdapter;
import android.widget.TextView;

public class MyListPlayground extends ListActivity {
    /** Called when the activity is first created. */
    @Override
    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.main);

        Cursor cursor = managedQuery(GenreContentProvider.CONTENT_URI, null, null, null, null);
        GenreCursorAdapter adapter = new GenreCursorAdapter(this, cursor);
        setListAdapter(adapter);

        final ListView listView = getListView();

        listView.setItemsCanFocus(true);
        listView.setChoiceMode(ListView.CHOICE_MODE_MULTIPLE);
    }

    private static class GenreCursorAdapter extends SimpleCursorAdapter {

        public GenreCursorAdapter(Context context, Cursor c) {
            // "layout" is the outer layout (in our case for the row)
            // "to" has the id of the view within the "layout" (in our case, the item description)
            super(context, R.layout.item_row, c, new String[] { GenreContentProvider.ColumnNames.Genre },
                    new int[] { R.id.item_short_description });

            // setViewBinder(new GenreViewBinder());
        }

        @Override
        public void bindView(View view, Context context, Cursor cursor) {
            // TODO Auto-generated method stub
            super.bindView(view, context, cursor);

            View itemDescView = view.findViewById(R.id.item_short_description);
            View checkBoxView = view.findViewById(R.id.item_checkbox);
            if (itemDescView instanceof TextView && checkBoxView instanceof CheckBox) {
                final TextView tv = (TextView) itemDescView;
                final CheckBox cb = (CheckBox) checkBoxView;

                tv.setOnClickListener(new OnClickListener() {
                    @Override
                    public void onClick(View v) {
                        cb.setChecked(!cb.isChecked());
                    }
                });
                cb.setOnCheckedChangeListener(new OnCheckedChangeListener() {
                    @Override
                    public void onCheckedChanged(CompoundButton buttonView, boolean isChecked) {
                        if (isChecked) {
                            tv.setBackgroundColor(Color.GREEN);
                        } else {
                            tv.setBackgroundColor(Color.RED);
                        }
                    }
                });
            }
        }
    }

}