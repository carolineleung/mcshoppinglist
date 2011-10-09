package com.mcshoppinglist.app.util;

import android.app.Dialog;
import android.view.View;
import android.view.ViewParent;
import android.view.Window;

import com.mcshoppinglist.app.common.AppConstants;

/**
 * Assist finding views (wrap findViewById) and (view) tags (wrap getTag).
 */
public class ViewFinderUtil {
    // TODO Does the Android API already have a method like this?
    @SuppressWarnings("unchecked")
    public static <T extends View> T findViewByIdTyped(int id, Class<T> expectedType,
                    View parentView) {
        View view = parentView.findViewById(id);
        checkView(view, id, expectedType);
        return (T) view;
    }

    // TODO Does the Android API already have a method like this?
    @SuppressWarnings("unchecked")
    public static <T extends View> T findViewByIdTyped(int id, Class<T> expectedType,
                    Dialog parentDialog) {
        View view = parentDialog.findViewById(id);
        checkView(view, id, expectedType);
        return (T) view;
    }

    private static <T> void checkView(View view, int id, Class<T> expectedType) {
        if (view == null || !expectedType.isAssignableFrom(view.getClass())) {
            MCLogger.e(ViewFinderUtil.class, "Failed to convert view: " + view
                            + " to expected type: " + expectedType + " for ID " + id);
        }
    }

    // TODO Does the Android API already have a method like this?
    @SuppressWarnings("unchecked")
    public static <T extends View> T findViewByIdTyped(int id, Class<T> expectedType, Window window) {
        View view = window.findViewById(id); // In 2.1, calls getDecorView().findViewById()
        checkView(view, id, expectedType);
        return (T) view;
    }

    // TODO Does the Android API already have a method like this?
    @SuppressWarnings("unchecked")
    public static <T> T getTagTyped(int tagId, Class<T> expectedType, View view) {
        Object obj = view.getTag(tagId);
        if (obj == null || !expectedType.isAssignableFrom(expectedType)) {
            MCLogger.e(ViewFinderUtil.class, "Failed to get tag ID: " + tagId
                            + " with expected type: " + expectedType);
        }
        return (T) obj;
    }

    public static int getTagInt(int tagId, View view) {
        Integer itemIdObj = getTagTyped(tagId, Integer.class, view);
        int itemId = AppConstants.INVALID_ID;
        if (itemIdObj != null) {
            itemId = itemIdObj;
        }
        return itemId;
    }

    public static View getParentView(View childView) {
        ViewParent parent = childView.getParent();
        if (parent instanceof View) {
            return (View) parent;
        }
        return null;
    }
}
