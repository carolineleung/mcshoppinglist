package com.mcshoppinglist.app.checklist.listeners;

import android.view.View;
import android.widget.AdapterView;
import android.widget.AdapterView.OnItemClickListener;

import com.mcshoppinglist.app.checklist.CheckListActivity;
import com.mcshoppinglist.app.checklist.finders.CheckListRowViewFinder;

public class ItemClickListener extends CheckedStateUpdater implements OnItemClickListener {

	public ItemClickListener(CheckListActivity activity) {
		super(activity);
	}

	@Override
	public void onItemClick(AdapterView<?> parent, View view, int position, long id) {
		CheckListRowViewFinder finder = new CheckListRowViewFinder(view);
		boolean originalCheckedState = finder.getCheckbox().isChecked();
		onCheckedChangedImpl(!originalCheckedState, view);

	}

}
