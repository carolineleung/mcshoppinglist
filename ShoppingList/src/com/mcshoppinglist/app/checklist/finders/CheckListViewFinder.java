package com.mcshoppinglist.app.checklist.finders;

import android.app.Activity;
import android.widget.AutoCompleteTextView;
import android.widget.Button;

import com.mcshoppinglist.app.R;
import com.mcshoppinglist.app.util.ViewFinderUtil;

public class CheckListViewFinder {
    private final Activity activity;
    private Button addItemButton;
    private AutoCompleteTextView inputText;

    // TODO mel: Should we pass in the Window instead? When does the Window change within an Activity?
    public CheckListViewFinder(Activity activity) {
        this.activity = activity;
    }

    public Button getAddItemButton() {
        if (addItemButton == null) {
            addItemButton = ViewFinderUtil.findViewByIdTyped(R.id.add_button, Button.class,
                            activity.getWindow());
        }
        return addItemButton;
    }

    public AutoCompleteTextView getInputText() {
        if (inputText == null) {
            inputText = ViewFinderUtil.findViewByIdTyped(R.id.autocomplete_item,
                            AutoCompleteTextView.class, activity.getWindow());
        }
        return inputText;
    }
}
