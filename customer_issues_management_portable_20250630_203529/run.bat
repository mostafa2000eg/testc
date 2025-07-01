@echo off
chcp 65001 > nul
title Customer Issues Management System

echo � Starting Customer Issues Management System...
echo تشغيل نظام إدارة مشاكل العملاء...

cd /d "%~dp0"

python customer_issues_main.py
if %errorlevel% neq 0 (
    python3 customer_issues_main.py
    if %errorlevel% neq 0 (
        echo ❌ Python not found. Please install Python 3.7+
        echo ❌ لم يتم العثور على Python. يرجى تثبيت Python 3.7+
        pause
        exit /b 1
    )
)
