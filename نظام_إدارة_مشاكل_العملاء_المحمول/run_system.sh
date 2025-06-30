#!/bin/bash
cd "$(dirname "$0")"
echo "🚀 تشغيل النظام..."
python3 enhanced_main.py
if [ $? -ne 0 ]; then
    echo "❌ خطأ في تشغيل النظام"
    echo "تأكد من تثبيت Python"
    read -p "اضغط Enter للمتابعة..."
fi
