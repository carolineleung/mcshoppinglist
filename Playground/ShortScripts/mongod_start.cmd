@echo off
setlocal
set MONGO_HOME=C:\opt\mongodb\mongodb-win32-i386-1.8.0-rc2
set PATH=%MONG_HOME%\bin;%PATH%
cd /d %MONGO_HOME%\bin
start mongod --dbpath C:\opt\mongodb\data1\db --journal --logpath C:\opt\mongodb\data1\logs\mongodb.log --logappend
@echo on
tail -f C:/opt/mongodb/data1/logs/mongodb.log 

