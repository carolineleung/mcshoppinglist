package com.mcshoppinglist.app.checklist.adapters;

import android.content.Context;
import android.database.Cursor;
import android.view.View;
import android.view.ViewGroup;
import android.widget.ResourceCursorAdapter;
import android.widget.TextView;

import com.mcshoppinglist.app.R;
import com.mcshoppinglist.app.checklist.CheckListActivity;
import com.mcshoppinglist.app.checklist.finders.CheckListRowViewFinder;
import com.mcshoppinglist.app.checklist.listeners.CheckboxChangeListener;
import com.mcshoppinglist.app.dataprovider.ShoppingListCursorWrapper;
import com.mcshoppinglist.app.util.ViewUpdateUtil;
import com.mcshoppinglist.app.widget.BetterCheckBox;

// TODO mel: Why are we using ResourceCursorAdapter instead of SimpleCursorAdapter (which extends it)?
/**
 * This adapter is specific to entry_item.xml.
 */
public class ShoppingListCursorAdapter extends ResourceCursorAdapter {
    private final CheckListActivity activity;

    public ShoppingListCursorAdapter(CheckListActivity activity, Cursor cur) {
        super(activity, R.layout.entry_item, cur);
        this.activity = activity;
    }

    @Override
    public View newView(Context context, Cursor cursor, ViewGroup parent) {
        View view = super.newView(context, cursor, parent);
        BetterCheckBox checkbox = (BetterCheckBox) view.findViewById(R.id.checkbox);
        checkbox.setOnCheckedChangeListener(new CheckboxChangeListener(activity));
        return view;
    }

    @Override
    public void bindView(final View view, Context context, final Cursor cur) {
        CheckListRowViewFinder finder = new CheckListRowViewFinder(view);
        BetterCheckBox checkbox = finder.getCheckbox();
        TextView text = finder.getItemTextView();
        TextView labelsTextView = finder.getLabelsTextView();

        ShoppingListCursorWrapper cursor = new ShoppingListCursorWrapper(cur);
        String itemText = cursor.getItem();
        int itemId = cursor.getId();
        String labelsValue = cursor.getLabel();

        labelsTextView.setText(labelsValue);
        boolean checked = cursor.isChecked();

        // Setting the data dynamically with the text control
        CheckListItemDynamicData dynamicData = new CheckListItemDynamicData();
        dynamicData.setItemLocalId(itemId);
        dynamicData.setItemText(itemText);
        dynamicData.setShoppingItemId(cursor.getShoppingItemId());
        dynamicData.setShoppingListId(cursor.getShoppingListId());

        // TODO Add labelsValue and notesValue to dynamicData as well?
        // dynamicData.setNotes(cursor.getNotes());
        // dynamicData.setLabels(labelsValue);
        text.setTag(R.integer.item_dynamic_data, dynamicData);

        // Log.d(getClass().getSimpleName(), "setTag with id=" + itemId + ", items=" + itemText + ", labels="
        // + labelsValue + ", notes=" + notesValue);

        checkbox.setCheckedDuringBind(checked);
        ViewUpdateUtil.setTextBold(!checked, text, itemText);
    }

}
