@echo off
chcp 65001 > nul
title نظام إدارة مشاكل العملاء - النسخة المحسنة

echo.
echo ================================
echo نظام إدارة مشاكل العملاء
echo النسخة المحسنة
echo ================================
echo.

echo 🔍 فحص Python...
python --version > nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python غير مثبت أو غير موجود في PATH
    echo يرجى تثبيت Python من: https://www.python.org/downloads/
    pause
    exit /b 1
)

python --version
echo ✅ Python متوفر
echo.

echo 🚀 تشغيل النظام...
python enhanced_main.py

if %errorlevel% neq 0 (
    echo.
    echo ❌ حدث خطأ في تشغيل النظام
    echo جرب تشغيل الاختبار أولاً: python test_enhanced_system.py
    echo.
    pause
    exit /b 1
)

echo.
echo ✅ تم إغلاق النظام بنجاح
pause