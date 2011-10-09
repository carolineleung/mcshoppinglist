package com.mcshoppinglist.app.checklist.finders;

import android.view.View;
import android.widget.TextView;

import com.mcshoppinglist.app.R;
import com.mcshoppinglist.app.checklist.adapters.CheckListItemDynamicData;
import com.mcshoppinglist.app.util.ViewFinderUtil;
import com.mcshoppinglist.app.widget.BetterCheckBox;

public class CheckListRowViewFinder {
    private TextView item;
    private CheckListItemDynamicData dynamicData;
    private final View rowParentView;
    private BetterCheckBox checkbox;
    private TextView labelsTextView;

    /**
     * 
     * @param rowParentView
     *            parent view of the entire row (e.g. the LinearLayout comprising the checkbox, item text, etc.)
     */
    public CheckListRowViewFinder(View rowParentView) {
        this.rowParentView = rowParentView;
    }

    public TextView getItemTextView() {
        if (item == null) {
            item = ViewFinderUtil.findViewByIdTyped(R.id.entry, TextView.class, rowParentView);
        }
        return item;
    }

    private CheckListItemDynamicData getData() {
        if (dynamicData == null) {
            dynamicData = ViewFinderUtil.getTagTyped(R.integer.item_dynamic_data,
                            CheckListItemDynamicData.class, getItemTextView());
        }
        return dynamicData;
    }

    public int getItemLocalIdTag() {
        return getData().getItemLocalId();
    }

    public String getShoppingListIdTag() {
        return getData().getShoppingListId();
    }

    public String getShoppingItemIdTag() {
        return getData().getShoppingItemId();
    }

    public String getItemTextTag() {
        return getData().getItemText();
    }

    public BetterCheckBox getCheckbox() {
        if (checkbox == null) {
            checkbox = ViewFinderUtil.findViewByIdTyped(R.id.checkbox, BetterCheckBox.class,
                            rowParentView);
        }
        return checkbox;
    }

    public TextView getLabelsTextView() {
        if (labelsTextView == null) {
            labelsTextView = ViewFinderUtil.findViewByIdTyped(R.id.labels, TextView.class,
                            rowParentView);
        }
        return labelsTextView;
    }
}
