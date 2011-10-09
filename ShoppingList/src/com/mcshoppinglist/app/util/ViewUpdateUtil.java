package com.mcshoppinglist.app.util;

import android.graphics.Color;
import android.graphics.Typeface;
import android.text.SpannableString;
import android.text.Spanned;
import android.text.style.StyleSpan;
import android.widget.TextView;

public class ViewUpdateUtil {

    /**
     * Bold/unbold the TextView based on the boolean value.
     * 
     * @param notBold
     * @param textView
     * @param textViewStr
     */
    public static void setTextBold(boolean bold, TextView textView, String textViewStr) {
        if (bold) {
            textView.setTextColor(Color.WHITE);
            SpannableString spannableStr = new SpannableString(textViewStr);
            spannableStr.setSpan(new StyleSpan(Typeface.BOLD), 0, textViewStr.length(),
                            Spanned.SPAN_EXCLUSIVE_EXCLUSIVE);
            textView.setText(spannableStr);
        } else {
            textView.setTextColor(Color.GRAY);
            textView.setText(textViewStr);
        }
    }

}
