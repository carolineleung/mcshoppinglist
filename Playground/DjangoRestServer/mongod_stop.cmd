@echo off
setlocal
set PATH=C:\opt\mongodb\mongodb-win32-i386-1.8.0-rc2\bin;%PATH%
mongo --eval "db._adminCommand(\"shutdown\");"
