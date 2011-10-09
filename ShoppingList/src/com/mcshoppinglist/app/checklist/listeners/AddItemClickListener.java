package com.mcshoppinglist.app.checklist.listeners;

import android.net.Uri;
import android.view.View;
import android.view.View.OnClickListener;
import android.widget.Button;
import android.widget.Toast;

import com.mcshoppinglist.app.R;
import com.mcshoppinglist.app.checklist.CheckListActivity;
import com.mcshoppinglist.app.checklist.ContentManager;
import com.mcshoppinglist.app.checklist.finders.CheckListViewFinder;

public class AddItemClickListener implements OnClickListener {
    private final CheckListViewFinder viewFinder;
    private final CheckListActivity activity;

    public AddItemClickListener(CheckListViewFinder viewFinder, CheckListActivity activity) {
        this.viewFinder = viewFinder;
        this.activity = activity;

    }

    @Override
    public void onClick(View v) {
        Button addButton = viewFinder.getAddItemButton();
        addButton.setText(R.string.add_entry_text);
        String enteredText = viewFinder.getInputText().getText().toString();

        // Disabled update via Add button, since we're now using long click to open a separate update dialog.
        // // Edit existing entry
        // if (selectedEntry != null) {
        // selectedEntry.setText(enteredText);
        // String whereClause = ShoppingItems._ID + "=" + selectedItemId;
        // ContentValues values = new ContentValues();
        // values.put(ShoppingItems.ITEM, enteredText);
        // int numEntryUpdated = getContentResolver().update(ShoppingItems.CONTENT_URI, values,
        // whereClause, null);
        // Toast.makeText(getApplicationContext(),
        // "Updated " + numEntryUpdated + " entry in DB, id=" + selectedItemId,
        // Toast.LENGTH_LONG).show();
        // selectedEntry = null;
        // selectedItemId = INVALID_ID;
        //
        // } else {

        // Create new entry
        ContentManager contentManager = activity.getShoppingListApplication().getContentManager();
        Uri uri = contentManager.insertItemToDB(activity.getShoppingListId(), enteredText, null);

        // TODO Remove toast
        Toast.makeText(activity.getApplicationContext(),
                        "Added new entry to DB (total=" + contentManager.getNumItems()
                                        + ") with URI=" + uri.toString(), Toast.LENGTH_LONG).show();

        // }

        // Clear the input
        viewFinder.getInputText().setText("");
    }
}
