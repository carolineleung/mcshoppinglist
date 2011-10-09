@echo off
setlocal
set MONGO_HOME=C:\opt\mongodb\mongodb-win32-i386-1.8.0-rc2
set PATH=%MONG_HOME%\bin;%PATH%
cd /d %MONGO_HOME%\bin
mongo --eval "db._adminCommand(\"shutdown\");"
