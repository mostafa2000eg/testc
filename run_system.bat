@echo off
chcp 65001 > nul
title Customer Issues Management System - نظام إدارة مشاكل العملاء

echo.
echo ================================
echo Customer Issues Management System
echo نظام إدارة مشاكل العملاء
echo Version 2.0.0 - Enhanced Edition
echo ================================
echo.

echo 🚀 Starting system... / تشغيل النظام...

cd /d "%~dp0"

REM Try python3 first, then python
python3 customer_issues_main.py
if %errorlevel% neq 0 (
    python customer_issues_main.py
    if %errorlevel% neq 0 (
        echo.
        echo ❌ Error: Python not found or system failed to start
        echo ❌ خطأ: لم يتم العثور على Python أو فشل تشغيل النظام
        echo.
        echo Please ensure Python 3.7+ is installed and added to PATH
        echo يرجى التأكد من تثبيت Python 3.7+ وإضافته للـ PATH
        echo.
        echo Download Python from: https://www.python.org/downloads/
        echo.
        pause
        exit /b 1
    )
)

echo.
echo ✅ System started successfully / تم تشغيل النظام بنجاح
echo You can close this window now / يمكنك إغلاق هذه النافذة الآن