package com.mcshoppinglist.app.checklist.finders;

import android.app.Dialog;
import android.widget.Button;
import android.widget.EditText;

import com.mcshoppinglist.app.R;
import com.mcshoppinglist.app.util.ViewFinderUtil;

public class EditItemDialogViewFinder {
    private final Dialog dialog;
    private EditText itemEditText;
    private EditText labelEditText;
    private EditText notesEditText;
    private Button submitButton;

    private Button cancelButton;

    public EditItemDialogViewFinder(Dialog view) {
        this.dialog = view;
    }

    public Dialog getDialog() {
        return dialog;
    }

    public EditText getItemEditText() {
        if (itemEditText == null) {
            itemEditText = ViewFinderUtil.findViewByIdTyped(R.id.edit_input_item, EditText.class,
                            dialog);
        }
        return itemEditText;
    }

    public EditText getLabelEditText() {
        if (labelEditText == null) {
            labelEditText = ViewFinderUtil.findViewByIdTyped(R.id.edit_input_labels,
                            EditText.class, dialog);
        }
        return labelEditText;
    }

    public EditText getNotesEditText() {
        if (notesEditText == null) {
            notesEditText = ViewFinderUtil.findViewByIdTyped(R.id.edit_input_additional_notes,
                            EditText.class, dialog);
        }
        return notesEditText;
    }

    public Button getCancelButton() {
        if (cancelButton == null) {
            cancelButton = ViewFinderUtil.findViewByIdTyped(R.id.edit_cancel_button, Button.class,
                            dialog);
        }
        return cancelButton;
    }

    public Button getSubmitButton() {
        if (submitButton == null) {
            submitButton = ViewFinderUtil.findViewByIdTyped(R.id.edit_submit_button, Button.class,
                            dialog);
        }
        return submitButton;
    }
}
