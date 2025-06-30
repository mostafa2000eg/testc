#!/bin/bash
# Customer Issues Management System - Quick Launcher
# نظام إدارة مشاكل العملاء - مشغل سريع

echo "🚀 Starting Customer Issues Management System..."
echo "تشغيل نظام إدارة مشاكل العملاء..."

cd "$(dirname "$0")"

# Try different Python commands
if command -v python3 &> /dev/null; then
    python3 customer_issues_main.py
elif command -v python &> /dev/null; then
    python customer_issues_main.py
else
    echo "❌ Python not found. Please install Python 3.7+"
    echo "❌ لم يتم العثور على Python. يرجى تثبيت Python 3.7+"
    exit 1
fi
