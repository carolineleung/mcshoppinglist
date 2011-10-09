package com.mcshoppinglist.app.checklist.listeners;

import android.view.View;
import android.widget.CompoundButton;
import android.widget.CompoundButton.OnCheckedChangeListener;

import com.mcshoppinglist.app.checklist.CheckListActivity;
import com.mcshoppinglist.app.util.ViewFinderUtil;

public class CheckboxChangeListener extends CheckedStateUpdater implements OnCheckedChangeListener {

	public CheckboxChangeListener(CheckListActivity activity) {
		super(activity);
	}

	@Override
	public void onCheckedChanged(CompoundButton buttonView, boolean isChecked) {
		View parentView = ViewFinderUtil.getParentView(buttonView);
		if (parentView == null) {
			return;
		}
		onCheckedChangedImpl(isChecked, parentView);
	}

}
