# http://developer.android.com/guide/developing/tools/adb.html#sqlite

// cmd
cd C:\opt\android\android-sdk_r09-windows\platform-tools
adb devices
adb -s emulator-5554 shell

// adb shell
cd /sdcard
sqlite3 /data/data/com.mcshoppinglist.app/databases/shopping_list.db
.output shopping_list_dump.sql
.dump shopping_list


// cmd
adb pull /sdcard/shopping_list_dump.sql shopping_list_dump.sql

adb push shopping_list_dump.sql  /sdcard/shopping_list_dump.sql


// adb shell, sqlite3
.read shopping_list_dump.sql

