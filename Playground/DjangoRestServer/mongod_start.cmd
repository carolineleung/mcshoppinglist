@echo off
setlocal
set PATH=C:\opt\mongodb\mongodb-win32-i386-1.8.0-rc2\bin;%PATH%
start mongod --dbpath C:\opt\mongodb\data1\db --dur --logpath C:\opt\mongodb\data1\logs\mongodb.log --logappend
@echo on
tail -f C:/opt/mongodb/data1/logs/mongodb.log 

