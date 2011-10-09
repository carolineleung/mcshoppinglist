package com.mcshoppinglist.app.util;

import android.util.Log;

public class MCLogger {

    private static final String appName = "MCShoppingList";

    private MCLogger() {
    }

    public static <T> void d(Class<T> clazz, String message) {
        Log.d(appName, clazz.getSimpleName() + ": " + message);
    }

    public static <T> void d(Class<T> clazz, String message, Throwable e) {
        Log.d(appName, clazz.getSimpleName() + ": " + message, e);
    }

    public static <T> void i(Class<T> clazz, String message) {
        Log.i(appName, clazz.getSimpleName() + ": " + message);
    }

    public static <T> void i(Class<T> clazz, String message, Throwable e) {
        Log.i(appName, clazz.getSimpleName() + ": " + message, e);
    }

    public static <T> void w(Class<T> clazz, String message) {
        Log.w(appName, clazz.getSimpleName() + ": " + message);
    }

    public static <T> void w(Class<T> clazz, String message, Throwable e) {
        Log.w(appName, clazz.getSimpleName() + ": " + message, e);
    }

    public static <T> void e(Class<T> clazz, String message) {
        Log.e(appName, clazz.getSimpleName() + ": " + message);
    }

    public static <T> void e(Class<T> clazz, Throwable e) {
        Log.e(appName, clazz.getSimpleName(), e);
    }

    public static <T> void e(Class<T> clazz, String message, Throwable e) {
        Log.e(appName, clazz.getSimpleName() + ": " + message, e);
    }

}
