#!/bin/bash
# Customer Issues Management System - Linux/Mac Runner
# نظام إدارة مشاكل العملاء - مشغل لينكس/ماك

set -e

echo "================================"
echo "Customer Issues Management System"
echo "نظام إدارة مشاكل العملاء"
echo "Version 2.0.0 - Enhanced Edition"
echo "================================"
echo

echo "� Starting system... / تشغيل النظام..."

# Change to script directory
cd "$(dirname "$0")"

# Try python3 first, then python
if command -v python3 &> /dev/null; then
    PYTHON_CMD="python3"
elif command -v python &> /dev/null; then
    PYTHON_CMD="python"
else
    echo "❌ Error: Python not found"
    echo "❌ خطأ: لم يتم العثور على Python"
    echo
    echo "Please install Python 3.7+ from:"
    echo "يرجى تثبيت Python 3.7+ من:"
    echo "https://www.python.org/downloads/"
    exit 1
fi

echo "Using Python: $PYTHON_CMD"

# Run the main application
if $PYTHON_CMD customer_issues_main.py; then
    echo
    echo "✅ System started successfully / تم تشغيل النظام بنجاح"
else
    echo
    echo "❌ Error: System failed to start"
    echo "❌ خطأ: فشل تشغيل النظام"
    echo
    echo "Check the logs in the 'logs' directory for more details"
    echo "راجع ملفات السجلات في مجلد 'logs' لمزيد من التفاصيل"
    exit 1
fi