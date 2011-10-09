@echo off
setlocal

cd /d C:\opt\apache\Apache2.2\bin
:: start "Apache2.2 httpd" C:\opt\apache\Apache2.2\bin\httpd.exe
start C:\opt\apache\Apache2.2\bin\httpd.exe %*
start "Apache2.2 tail" tail -f C:\opt\apache\Apache2.2\logs\error.log

