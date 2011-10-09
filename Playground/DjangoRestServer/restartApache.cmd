@echo off
setlocal


cd /d C:\opt\apache\Apache2.2\bin
:: start "Apache2.2 httpd" C:\opt\apache\Apache2.2\bin\httpd.exe
C:\opt\apache\Apache2.2\bin\httpd.exe -k restart

