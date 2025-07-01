@echo off
chcp 65001 > nul
title Test Customer Issues Management System - اختبار نظام إدارة مشاكل العملاء

echo.
echo ================================
echo System Test / اختبار النظام
echo Customer Issues Management System
echo نظام إدارة مشاكل العملاء
echo ================================
echo.

echo 🧪 Running system tests... / تشغيل اختبارات النظام...

cd /d "%~dp0"

REM Try python3 first, then python
python3 test_customer_issues.py
if %errorlevel% neq 0 (
    python test_customer_issues.py
    if %errorlevel% neq 0 (
        echo.
        echo ❌ Error: Python not found or test failed
        echo ❌ خطأ: لم يتم العثور على Python أو فشل الاختبار
        echo.
        echo Please ensure Python 3.7+ is installed
        echo يرجى التأكد من تثبيت Python 3.7+
        pause
        exit /b 1
    )
)

echo.
echo ✅ Test completed / اكتمل الاختبار
pause