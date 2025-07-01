@echo off
chcp 65001 > nul
cd /d "%~dp0"
echo 🚀 تشغيل النظام...
python3 enhanced_main.py
if %errorlevel% neq 0 (
    echo ❌ خطأ في تشغيل النظام
    echo تأكد من تثبيت Python
    pause
)
