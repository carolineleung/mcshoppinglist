package com.mcshoppinglist.app.widget;

import android.content.Context;
import android.util.AttributeSet;
import android.widget.CheckBox;

/**
 * A CheckBox that allows you to programmatically update setChecked() without triggering the OnCheckedChangeListener.
 */
public class BetterCheckBox extends CheckBox {
	protected OnCheckedChangeListener checkedChangeListener;

	public BetterCheckBox(Context context, AttributeSet attrs, int defStyle) {
		super(context, attrs, defStyle);
	}

	public BetterCheckBox(Context context, AttributeSet attrs) {
		super(context, attrs);
	}

	public BetterCheckBox(Context context) {
		super(context);
	}

	public OnCheckedChangeListener getOnCheckedChangeListener() {
		return checkedChangeListener;
	}

	// Ensure we always know what the listener is. Workaround for there not being a getOnCheckedChangeListener()
	@Override
	public void setOnCheckedChangeListener(OnCheckedChangeListener listener) {
		checkedChangeListener = listener;
		super.setOnCheckedChangeListener(listener);
	}

	/**
	 * Workaround for the OnCheckedChangeListener being called from setChecked() during bind. This allows you to avoid
	 * having your change listener called when programmatically changing the checked state.
	 * 
	 * @param checked
	 *            new checked state
	 */
	public void setCheckedDuringBind(boolean checked) {
		OnCheckedChangeListener oldListener = getOnCheckedChangeListener();
		try {
			// Turn off listeners
			setOnCheckedChangeListener(null);

			setChecked(checked);
		} finally {
			setOnCheckedChangeListener(oldListener);
		}
	}

	// TODO Remove this debug code
	// @Override
	// public void setChecked(boolean checked) {
	// Log.d(this.toString(),
	// "setChecked " + checked + "  current mChecked " + super.isChecked() + " " + this.toString() + "");
	// try {
	// throw new Exception("IGNORE. For stack trace.");
	// } catch (Exception ex) {
	// ByteArrayOutputStream baos = new ByteArrayOutputStream();
	// PrintStream ps = new PrintStream(baos);
	// ex.printStackTrace(ps);
	// String content = baos.toString(); // e.g. ISO-8859-1
	// Log.d(this.toString(), "setChecked stack trace: " + content);
	// }
	// // TODO Auto-generated method stub
	// super.setChecked(checked);
	// }

}
