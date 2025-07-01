@echo off
chcp 65001 > nul
title Customer Issues Management System v2.0.0

echo.
echo ================================
echo Customer Issues Management System
echo Version 2.0.0 - Enhanced Edition
echo ================================
echo.

echo Starting system...

cd /d "%~dp0"

REM Try python3 first, then python
python3 customer_issues_main.py
if %errorlevel% neq 0 (
    python customer_issues_main.py
    if %errorlevel% neq 0 (
        echo.
        echo Error: Python not found or system failed to start
        echo.
        echo Please ensure Python 3.7+ is installed and added to PATH
        echo Download Python from: https://www.python.org/downloads/
        echo.
        pause
        exit /b 1
    )
)

echo.
echo System started successfully
echo You can close this window now
pause