package com.mcshoppinglist.app.checklist;

import java.util.List;

import android.app.ListActivity;
import android.content.BroadcastReceiver;
import android.content.Context;
import android.content.Intent;
import android.content.IntentFilter;
import android.database.Cursor;
import android.os.Bundle;
import android.view.Menu;
import android.view.MenuItem;
import android.widget.Button;

import com.mcshoppinglist.app.R;
import com.mcshoppinglist.app.checklist.RenderManager.ViewMode;
import com.mcshoppinglist.app.checklist.adapters.ShoppingListCursorAdapter;
import com.mcshoppinglist.app.checklist.finders.CheckListViewFinder;
import com.mcshoppinglist.app.checklist.listeners.AddItemClickListener;
import com.mcshoppinglist.app.checklist.listeners.ItemClickListener;
import com.mcshoppinglist.app.checklist.listeners.ItemLongClickListener;
import com.mcshoppinglist.app.common.AppConstants;
import com.mcshoppinglist.app.dataprovider.ShoppingListData.ShoppingItems;
import com.mcshoppinglist.app.itemsuggestion.ItemNameFilterQueryProvider;
import com.mcshoppinglist.app.itemsuggestion.ItemSuggestionCursorAdapter;
import com.mcshoppinglist.app.json.model.ShoppingListItem;
import com.mcshoppinglist.app.service.ShoppingListUpdateService;
import com.mcshoppinglist.app.util.ImportExportManager;
import com.mcshoppinglist.app.util.MCLogger;

/**
 * Checklist activity. Shopping list items can be checked off. This is the primary Activity for this app.
 * 
 * 
 */
public class CheckListActivity extends ListActivity {

	public static final String[] PROJECTION = new String[] { ShoppingItems._ID, ShoppingItems.SHOPPING_LIST_ID, ShoppingItems.SHOPPING_ITEM_ID, ShoppingItems.ITEM, ShoppingItems.CHECKED,
			ShoppingItems.LABELS, ShoppingItems.ADDITIONAL_NOTES, ShoppingItems.POSITION, ShoppingItems.MODIFIED_DATE };

	// cl: Managers resulted from refactoring
	private ImportExportManager importExportMgr;
	private RenderManager renderMgr;
	private CheckListViewFinder viewFinder;
	private String shoppingListId = AppConstants.INVALID_SHOPPING_LIST_ID;

	private ShoppingListItemDiffsReceiver diffsReceiver;

	@Override
	public void onCreate(Bundle savedInstanceState) {
		super.onCreate(savedInstanceState);
		initManagers();

		setDefaultKeyMode(DEFAULT_KEYS_SHORTCUT);
		setContentView(R.layout.checklist);

		// If no data was given in intent (as we started as a MAIN activity), use our default content provider.
		Intent intent = getIntent();
		shoppingListId = intent.getStringExtra(AppConstants.INTENT_KEY_SHOPPING_LIST_ID);
		if (AppConstants.INVALID_SHOPPING_LIST_ID.equals(shoppingListId)) {
			MCLogger.i(getClass(), "onCreate intent missing/invalid shoppingListId"); // TODO Remove this warning.
			// TODO If there's no shopping list id, then we should create a new (empty) shopping list?
		}
		// TODO mel: We're not passing data with the intent (yet)... For now just use ShoppingItems.CONTENT_URI.
		// if (intent.getData() == null) {
		// intent.setData(ShoppingItems.CONTENT_URI);

		addListItemsLabels();
		initAutoComplete();
		initListeners();

		renderMgr.refreshView(ViewMode.ViewAll, null);

		refreshCheckList();
	}

	private void initListeners() {
		Button addButton = viewFinder.getAddItemButton();
		addButton.setOnClickListener(new AddItemClickListener(viewFinder, this));
	}

	private void initManagers() {
		renderMgr = new RenderManager(this);
		viewFinder = new CheckListViewFinder(this);

		// TODO cl: ImportExportManager needs to take in ShoppingList, because we are inserting directly into the DB as
		// reading through files. This is not clean, but to preserve mem used. The alternative is to return some data
		// structure that holds all the temp entries need to be inserted, and then insert them using contentMgr
		importExportMgr = new ImportExportManager(this);
	}

	private void addListItemsLabels() {
		Cursor cur = managedQuery(ShoppingItems.CONTENT_URI, PROJECTION, null, null, ShoppingItems.DEFAULT_SORT_ORDER);
		ContentManager contentMgr = getShoppingListApplication().getContentManager();
		contentMgr.setNumItems(cur.getCount());
		if (cur.isBeforeFirst()) {
			cur.moveToFirst();
		}
		while (!cur.isAfterLast()) {
			String label = cur.getString(cur.getColumnIndex(ShoppingItems.LABELS));
			contentMgr.getLabelsSet().add(label);
			if (!cur.moveToNext()) {
				break;
			}
		}
	}

	@Override
	public boolean onCreateOptionsMenu(Menu menu) {
		renderMgr.onCreateOptionsMenu(menu);
		return super.onCreateOptionsMenu(menu);
	}

	@Override
	public boolean onPrepareOptionsMenu(Menu menu) {
		renderMgr.onPrepareOptionsMenu(menu);
		return super.onPrepareOptionsMenu(menu);
	}

	@Override
	public boolean onOptionsItemSelected(MenuItem item) {
		renderMgr.onOptionsItemSelected(item);
		return super.onOptionsItemSelected(item);
	}

	private void initAutoComplete() {
		Cursor cursor = managedQuery(ShoppingItems.CONTENT_URI, new String[] { ShoppingItems._ID, ShoppingItems.ITEM }, null, null, ShoppingItems.DEFAULT_SORT_ORDER);
		ItemSuggestionCursorAdapter adapter = new ItemSuggestionCursorAdapter(this, cursor);
		adapter.setFilterQueryProvider(new ItemNameFilterQueryProvider(this));
		viewFinder.getInputText().setAdapter(adapter);
	}

	public void updateListAdapter(Cursor cur) {
		ShoppingListCursorAdapter listAdapter = new ShoppingListCursorAdapter(this, cur);
		setListAdapter(listAdapter);
		getListView().setOnItemLongClickListener(new ItemLongClickListener(this));
		getListView().setOnItemClickListener(new ItemClickListener(this));
	}

	private void refreshCheckList(boolean fullResync) {
		Intent refreshCheckListIntent = new Intent(this, ShoppingListUpdateService.class);
		refreshCheckListIntent.putExtra(AppConstants.INTENT_KEY_SHOPPING_LIST_ID, shoppingListId);

		if (fullResync) {
			refreshCheckListIntent.putExtra(AppConstants.INTENT_REFRESH_FULL_LIST_KEY, true);
		}
		startService(refreshCheckListIntent);
	}

	public void refreshCheckList() {
		refreshCheckList(true);
	}

	@Override
	protected void onResume() {
		IntentFilter filter = new IntentFilter(ShoppingListUpdateService.INTENT_PROCESS_ITEM_DIFFS);
		diffsReceiver = new ShoppingListItemDiffsReceiver();
		registerReceiver(diffsReceiver, filter);

		// TODO refresh/load check list?
		refreshCheckList(false);
		super.onResume();
	}

	@Override
	protected void onPause() {
		unregisterReceiver(diffsReceiver);
		diffsReceiver = null;

		Intent svc = new Intent(this, ShoppingListUpdateService.class);
		stopService(svc);

		super.onPause();
	}

	@Override
	protected void onDestroy() {
		super.onDestroy();
		// Unregister listeners
		getListView().setOnItemLongClickListener(null);
		importExportMgr = null;
		renderMgr = null;
		viewFinder = null;
	}

	public ImportExportManager getImportExportManager() {
		return importExportMgr;
	}

	public ShoppingListApplication getShoppingListApplication() {
		return (ShoppingListApplication) getApplication();
	}

	public String getShoppingListId() {
		return shoppingListId;
	}

	private class ShoppingListItemDiffsReceiver extends BroadcastReceiver {

		@Override
		public void onReceive(Context context, Intent intent) {
			ShoppingListApplication shoppingListApp = getShoppingListApplication();
			List<ShoppingListItem> diffs = shoppingListApp.getMostRecentDiffs();
			if (diffs != null && !diffs.isEmpty()) {
				ContentManager contentMgr = getShoppingListApplication().getContentManager();
				for (ShoppingListItem updatedItem : diffs) {
					contentMgr.updateItem(shoppingListId, updatedItem);
				}
			}
			// Reset diffs to null
			shoppingListApp.setMostRecentDiffs(null);

		}
	}
}