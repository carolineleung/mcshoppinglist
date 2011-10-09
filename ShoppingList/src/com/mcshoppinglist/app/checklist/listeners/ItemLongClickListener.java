package com.mcshoppinglist.app.checklist.listeners;

import android.app.Dialog;
import android.content.ContentUris;
import android.content.ContentValues;
import android.database.Cursor;
import android.net.Uri;
import android.view.View;
import android.view.View.OnClickListener;
import android.widget.AdapterView;
import android.widget.AdapterView.OnItemLongClickListener;
import android.widget.Button;

import com.mcshoppinglist.app.R;
import com.mcshoppinglist.app.checklist.CheckListActivity;
import com.mcshoppinglist.app.checklist.ContentManager;
import com.mcshoppinglist.app.checklist.finders.EditItemDialogViewFinder;
import com.mcshoppinglist.app.dataprovider.ShoppingListCursorWrapper;
import com.mcshoppinglist.app.dataprovider.ShoppingListData.ShoppingItems;
import com.mcshoppinglist.app.util.MCLogger;

public class ItemLongClickListener implements OnItemLongClickListener {
    private final CheckListActivity activity;

    public ItemLongClickListener(CheckListActivity activity) {
        this.activity = activity;
    }

    @Override
    public boolean onItemLongClick(AdapterView<?> parent, View view, int position, long id) {
        MCLogger.d(getClass(), "OnItemClick: position=" + position + ", id=" + id + ", view="
                        + view.getClass());

        ShoppingListCursorWrapper cursor = new ShoppingListCursorWrapper(
                        (Cursor) parent.getItemAtPosition(position));
        ItemData itemData = new ItemData(cursor.getId(), cursor.getLabel());

        final Dialog editEntryDialog = new Dialog(activity);
        editEntryDialog.setContentView(R.layout.edit_item);
        EditItemDialogViewFinder finder = new EditItemDialogViewFinder(editEntryDialog);

        String itemFromCursor = cursor.getItem();
        String notesFromCursor = cursor.getNotes();
        finder.getLabelEditText().setText(itemData.getLabels() == null ? "" : itemData.getLabels());
        finder.getItemEditText().setText(itemFromCursor);
        finder.getNotesEditText().setText(notesFromCursor == null ? "" : notesFromCursor);

        MCLogger.d(getClass(), "onItemClick with id=" + itemData.getId() + ", items="
                        + itemFromCursor + ", labels=" + itemData.getId() + ", notes="
                        + notesFromCursor);

        Button submitButton = finder.getSubmitButton();
        Button cancelButton = finder.getCancelButton();

        submitButton.setOnClickListener(new SubmitClickListener(finder, itemData));

        cancelButton.setOnClickListener(new OnClickListener() {

            @Override
            public void onClick(View v) {
                editEntryDialog.cancel();
            }
        });

        editEntryDialog.show();
        return true;
    }

    private static class ItemData {
        private final int id;
        private final String labels;

        public ItemData(int id, String labels) {
            this.id = id;
            this.labels = labels;
        }

        public int getId() {
            return id;
        }

        public String getLabels() {
            return labels;
        }

    }

    private class SubmitClickListener implements OnClickListener {
        private final EditItemDialogViewFinder finder;
        private final ItemData itemData;

        public SubmitClickListener(EditItemDialogViewFinder finder, ItemData itemData) {
            this.finder = finder;
            this.itemData = itemData;
        }

        @Override
        public void onClick(View button) {
            String newItem = finder.getItemEditText().getText().toString();
            String newLabels = finder.getLabelEditText().getText().toString();
            String newNotes = finder.getNotesEditText().getText().toString();

            // Update labelsSet if labels is updated
            if (newLabels != null && !newLabels.equals(itemData.getLabels())) {
                ContentManager contentManager = activity.getShoppingListApplication()
                                .getContentManager();
                contentManager.getLabelsSet().add(newLabels);
            }

            ContentValues values = new ContentValues();
            values.put(ShoppingItems.ITEM, newItem);
            values.put(ShoppingItems.LABELS, newLabels);
            values.put(ShoppingItems.ADDITIONAL_NOTES, newNotes);
            Uri uri = ContentUris.withAppendedId(ShoppingItems.CONTENT_URI, itemData.getId());
            activity.getContentResolver().update(uri, values, null, null);
            finder.getDialog().cancel();

            // Toast.makeText( getApplicationContext(),
            // "Updated id=" + idFromCursor + ", labels='" + newLabels + "', item='" + newItem
            // + "', notes='" + newNotes + "'", Toast.LENGTH_LONG).show();
        }
    }
}
