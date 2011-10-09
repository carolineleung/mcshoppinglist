package com.mcshoppinglist.app.util;

import java.io.BufferedReader;
import java.io.File;
import java.io.FileReader;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;

import android.os.Environment;
import android.widget.Toast;

import com.mcshoppinglist.app.R;
import com.mcshoppinglist.app.checklist.CheckListActivity;
import com.mcshoppinglist.app.common.AppConstants;

public class ImportExportManager {

    private final CheckListActivity shoppingListActivity;

    public ImportExportManager(CheckListActivity shoppingList) {
        shoppingListActivity = shoppingList;
    }

    public void importFromTextFile() {
        int numImported = 0;
        File sdcard = Environment.getExternalStorageDirectory();
        String whichFileMessage = "";
        for (String fileName : AppConstants.DROPBOX_SHOPPING_LIST_PATHS) {
            File textFile = new File(sdcard, fileName);
            if (textFile.exists() && textFile.canRead()) {
                Toast.makeText(shoppingListActivity.getApplicationContext(),
                                "Dropbox shopping list found.  Loading from " + textFile.getPath(),
                                Toast.LENGTH_LONG).show();
                numImported = importItemsFromTextFile(textFile);
                if (numImported > 0) {
                    whichFileMessage = fileName;
                    break;
                }
            }
        }
        if (numImported == 0) {
            Toast.makeText(shoppingListActivity.getApplicationContext(),
                            "Loading list from embedded resource now...", Toast.LENGTH_LONG).show();
            InputStream inputStream = shoppingListActivity.getResources().openRawResource(
                            R.raw.shopping);
            numImported = importItemsFromFile(inputStream);
            if (numImported > 0) {
                whichFileMessage = "embedded text file";
            }
        }

        if (numImported == 0) {
            Toast.makeText(shoppingListActivity.getApplicationContext(),
                            "Cannot import from text file", Toast.LENGTH_LONG).show();
            return;
        }
        Toast.makeText(shoppingListActivity.getApplicationContext(),
                        "Imported " + numImported + " items from: " + whichFileMessage,
                        Toast.LENGTH_LONG).show();
    }

    private int importItemsFromTextFile(File textFile) {
        int numImported = 0;
        try {
            BufferedReader br = new BufferedReader(new FileReader(textFile));
            numImported = importItemsImpl(br);
        } catch (IOException e) {
            MCLogger.e(getClass(), "Error importing items from file:" + textFile.getName(), e);
        }
        return numImported;
    }

    private int importItemsImpl(BufferedReader br) throws IOException {
        int numInserted = 0;
        String line;
        String labels = "";
        while ((line = br.readLine()) != null) {
            line = line.trim();
            if (line.length() == 0) {
                continue;
            }
            if (line.startsWith(AppConstants.LABEL_PREFIX)) {
                labels = line;
                continue;
            }
            shoppingListActivity.getShoppingListApplication().getContentManager()
                            .insertItemToDB(shoppingListActivity.getShoppingListId(), line, labels);
            numInserted++;
        }
        return numInserted;
    }

    public int importItemsFromFile(InputStream aFile) {
        int numImported = 0;
        try {
            BufferedReader br = new BufferedReader(new InputStreamReader(aFile));
            numImported = importItemsImpl(br);
        } catch (IOException e) {
            MCLogger.e(getClass(), "Error importing items from inputStream", e);
        }
        return numImported;
    }

}
