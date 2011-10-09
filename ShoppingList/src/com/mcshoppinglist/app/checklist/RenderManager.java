package com.mcshoppinglist.app.checklist;

import java.util.ArrayList;
import java.util.List;
import java.util.Set;

import android.app.Dialog;
import android.content.Intent;
import android.database.Cursor;
import android.util.SparseBooleanArray;
import android.view.Menu;
import android.view.MenuItem;
import android.view.View;
import android.view.View.OnClickListener;
import android.widget.ArrayAdapter;
import android.widget.Button;
import android.widget.ListView;
import android.widget.Toast;

import com.mcshoppinglist.app.R;
import com.mcshoppinglist.app.common.AppConstants;
import com.mcshoppinglist.app.dataprovider.ShoppingListData.ShoppingItems;
import com.mcshoppinglist.app.service.ShoppingListPreferenceActivity;

public class RenderManager {

    private final CheckListActivity shoppingListActivity;
    private ViewMode currentMode = ViewMode.ViewAll;

    public enum ViewMode {
        ViewAll, ViewChecked, ViewUnchecked;
    }

    public enum ViewMenuItem {
        ImportFromTxtFile(Menu.FIRST), FilterByLabels(Menu.FIRST + 1), CheckedStateFilter1(
                        Menu.FIRST + 2), CheckedStateFilter2(Menu.FIRST + 3), SyncList(
                        Menu.FIRST + 5), Prefs(Menu.FIRST + 6);
        // ClearItems(Menu.FIRST + 4),

        private ViewMenuItem(int index) {
            this.index = index;
        }

        private final int index;

        public int getIndex() {
            return index;
        }

    };

    private MenuItem menuItem1;
    private MenuItem menuItem2;

    public RenderManager(CheckListActivity shoppingList) {
        shoppingListActivity = shoppingList;
    }

    public void onCreateOptionsMenu(Menu menu) {
        menu.add(Menu.NONE, ViewMenuItem.Prefs.getIndex(), Menu.NONE, R.string.menu_prefs);
        menu.add(Menu.NONE, ViewMenuItem.FilterByLabels.getIndex(), Menu.NONE,
                        R.string.menu_filter_by_labels);
        menuItem1 = menu.add(Menu.NONE, ViewMenuItem.CheckedStateFilter1.getIndex(), Menu.NONE,
                        R.string.menu_view_checked);
        menuItem2 = menu.add(Menu.NONE, ViewMenuItem.CheckedStateFilter2.getIndex(), Menu.NONE,
                        R.string.menu_view_unchecked);
        menu.add(Menu.NONE, ViewMenuItem.SyncList.getIndex(), Menu.NONE, R.string.menu_sync_list);
        menu.add(Menu.NONE, ViewMenuItem.ImportFromTxtFile.getIndex(), Menu.NONE,
                        R.string.menu_import_from_txt_file);
        // menu.add(Menu.NONE, ViewMenuItem.ClearItems.getIndex(), Menu.NONE,
        // R.string.menu_clear_items);
    }

    public void onPrepareOptionsMenu(Menu menu) {
        switch (currentMode) {
        case ViewAll:
            menuItem1.setTitle(R.string.menu_view_checked);
            menuItem2.setTitle(R.string.menu_view_unchecked);
            break;
        case ViewChecked:
            menuItem1.setTitle(R.string.menu_view_all);
            menuItem2.setTitle(R.string.menu_view_unchecked);
            break;
        case ViewUnchecked:
            menuItem1.setTitle(R.string.menu_view_all);
            menuItem2.setTitle(R.string.menu_view_checked);
            break;
        }
    }

    public void onOptionsItemSelected(MenuItem item) {
        int menuItemId = item.getItemId();
        // if (menuItemId == ViewMenuItem.ClearItems.getIndex()) {
        // shoppingListActivity.getShoppingListApplication().getContentManager()
        // .removeAllItemsFromDB();
        //
        // } else
        if (menuItemId == ViewMenuItem.SyncList.getIndex()) {
            shoppingListActivity.refreshCheckList();
        } else if (menuItemId == ViewMenuItem.ImportFromTxtFile.getIndex()) {
            shoppingListActivity.getImportExportManager().importFromTextFile();
        } else if (menuItemId == ViewMenuItem.FilterByLabels.getIndex()) {
            filterByLabels();
        } else if (menuItemId == ViewMenuItem.Prefs.getIndex()) {
            Intent intent = new Intent(shoppingListActivity, ShoppingListPreferenceActivity.class);
            shoppingListActivity.startActivity(intent);
        } else {
            filterItemsByCheckedState(menuItemId);
        }
    }

    private void filterByLabels() {
        final Dialog filterSelectionDialog = new Dialog(shoppingListActivity);
        filterSelectionDialog.setContentView(R.layout.choose_labels_filter_dialog);

        Set<String> labelsSet = shoppingListActivity.getShoppingListApplication()
                        .getContentManager().getLabelsSet();
        final String[] labelsAsArray = new String[labelsSet.size()];
        int i = 0;
        for (String label : labelsSet) {
            labelsAsArray[i++] = label;
        }
        final ListView labelsList = (ListView) filterSelectionDialog.findViewById(R.id.labels_list);
        labelsList.setAdapter(new ArrayAdapter<String>(shoppingListActivity,
                        android.R.layout.simple_list_item_multiple_choice, labelsAsArray));
        labelsList.setItemsCanFocus(false);

        Button okButton = (Button) filterSelectionDialog.findViewById(R.id.labels_chose_button);
        okButton.setOnClickListener(new OnClickListener() {

            @Override
            public void onClick(View v) {
                SparseBooleanArray checkedPositions = labelsList.getCheckedItemPositions();
                List<String> checked = new ArrayList<String>();
                int i = 0;
                for (String label : labelsAsArray) {
                    if (checkedPositions.get(i++)) {
                        checked.add(label);
                    }
                }
                filterSelectionDialog.dismiss();
                Toast.makeText(shoppingListActivity, "Selected labels " + checked,
                                Toast.LENGTH_LONG).show();

                if (checked.size() > 0) {
                    // TODO fix get(0) - only the
                    String labelsFilterClause = ShoppingItems.LABELS + "='" + checked.get(0) + "'";
                    refreshView(currentMode, labelsFilterClause);
                }
            }
        });

        filterSelectionDialog.show();
    }

    private void filterItemsByCheckedState(int menuItemId) {
        ViewMode renderedViewMode = ViewMode.ViewAll;

        switch (currentMode) {
        case ViewAll:
            if (menuItemId == ViewMenuItem.CheckedStateFilter1.getIndex()) {
                renderedViewMode = ViewMode.ViewChecked;
            } else if (menuItemId == ViewMenuItem.CheckedStateFilter2.getIndex()) {
                renderedViewMode = ViewMode.ViewUnchecked;
            }
            break;
        case ViewChecked:
            if (menuItemId == ViewMenuItem.CheckedStateFilter1.getIndex()) {
                renderedViewMode = ViewMode.ViewAll;
            } else if (menuItemId == ViewMenuItem.CheckedStateFilter2.getIndex()) {
                renderedViewMode = ViewMode.ViewUnchecked;
            }
            break;
        case ViewUnchecked:
            if (menuItemId == ViewMenuItem.CheckedStateFilter1.getIndex()) {
                renderedViewMode = ViewMode.ViewAll;
            } else if (menuItemId == ViewMenuItem.CheckedStateFilter2.getIndex()) {
                renderedViewMode = ViewMode.ViewChecked;
            }
            break;
        }

        refreshView(renderedViewMode, null);
    }

    /**
     * Refresh the view of the shopping list based on view mode (All, Checked or Unchecked).
     * 
     * @param viewMode
     * @return
     */
    public void refreshView(ViewMode viewMode, String labelsFilterClause) {
        currentMode = viewMode;

        String whereClause = labelsFilterClause == null ? null : "(" + labelsFilterClause + ")";
        switch (viewMode) {

        case ViewChecked:
            String checkedFilter = ShoppingItems.CHECKED + "=" + AppConstants.CHECKED_VALUE;
            if (labelsFilterClause == null) {
                whereClause = checkedFilter;
            } else {
                whereClause += " AND (" + checkedFilter + ")";
            }
            break;
        case ViewUnchecked:
            String uncheckedFilter = ShoppingItems.CHECKED + "=" + AppConstants.UNCHECKED_VALUE;
            if (labelsFilterClause == null) {
                whereClause = uncheckedFilter;
            } else {
                whereClause += " AND (" + uncheckedFilter + ")";
            }
            break;
        }
        Cursor cur = shoppingListActivity.managedQuery(ShoppingItems.CONTENT_URI,
                        CheckListActivity.PROJECTION, whereClause, null,
                        ShoppingItems.DEFAULT_SORT_ORDER);
        shoppingListActivity.updateListAdapter(cur);
    }

}
