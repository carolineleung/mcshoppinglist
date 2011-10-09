package com.mcshoppinglist.app.dashboard;

import android.app.Activity;
import android.content.Intent;
import android.os.Bundle;
import android.view.View;
import android.view.View.OnClickListener;
import android.widget.Button;
import android.widget.EditText;
import android.widget.TextView;

import com.mcshoppinglist.app.R;
import com.mcshoppinglist.app.checklist.CheckListActivity;
import com.mcshoppinglist.app.common.AppConstants;
import com.mcshoppinglist.app.util.ViewFinderUtil;

/**
 * Dashboard for choosing a shopping list.
 */
public class ListDashboardActivity extends Activity {

    @Override
    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);

        setDefaultKeyMode(DEFAULT_KEYS_SHORTCUT);
        setContentView(R.layout.list_dashboard);

        // TODO This is all going away, so don't bother extracting the strings.
        TextView label = ViewFinderUtil.findViewByIdTyped(R.id.dashboard_label, TextView.class,
                        getWindow());
        label.setText("Choose a shopping list:");

        final EditText idText = ViewFinderUtil.findViewByIdTyped(R.id.tmp_list_id_choice,
                        EditText.class, getWindow());
        idText.setText("4d860836cb816479de000000"); // TODO Remove

        Button button = ViewFinderUtil.findViewByIdTyped(R.id.open_main_list_button, Button.class,
                        getWindow());
        button.setText("Open List By ID");
        button.setOnClickListener(new OnClickListener() {

            // TODO Remove this debug code
            private String getListChoiceId() {
                String listChoiceId = AppConstants.INVALID_SHOPPING_LIST_ID;
                try {

                    String newListChoiceId = idText.getText().toString();
                    if (AppConstants.isValidFormatShoppingListId(newListChoiceId)) {
                        listChoiceId = newListChoiceId;
                    }
                } catch (Exception ex) {
                    // Ignore
                }
                return listChoiceId;
            }

            @Override
            public void onClick(View v) {
                // TODO This should probably be via intent filters, not explicit class name.
                Intent intent = new Intent(ListDashboardActivity.this, CheckListActivity.class);

                // TODO add support for multiple shopping lists, then modify below hardcoded value
                intent.putExtra(AppConstants.INTENT_KEY_SHOPPING_LIST_ID, getListChoiceId());
                startActivity(intent);
            }
        });
    }

    @Override
    protected void onDestroy() {
        super.onDestroy();
        // Clean up listeners
        Button button = ViewFinderUtil.findViewByIdTyped(R.id.open_main_list_button, Button.class,
                        getWindow());
        button.setOnClickListener(null);
    }

}
