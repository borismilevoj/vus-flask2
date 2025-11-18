@echo off
powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0stop-vus.ps1" %*
pause

