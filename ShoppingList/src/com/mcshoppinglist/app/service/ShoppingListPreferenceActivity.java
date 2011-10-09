package com.mcshoppinglist.app.service;

import android.os.Bundle;
import android.preference.PreferenceActivity;

import com.mcshoppinglist.app.R;

public class ShoppingListPreferenceActivity extends PreferenceActivity {
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);

        addPreferencesFromResource(R.xml.shoppinglist_preferences);
    }

}