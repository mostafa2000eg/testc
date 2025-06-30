#!/bin/bash

echo "================================"
echo "نظام إدارة مشاكل العملاء"
echo "النسخة المحسنة"
echo "Customer Issues Management System"
echo "Enhanced Version"
echo "================================"
echo

echo "🔍 فحص Python..."
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 غير مثبت"
    echo "يرجى تثبيت Python3 أولاً"
    exit 1
fi

python3 --version
echo "✅ Python3 متوفر"
echo

echo "🚀 تشغيل النظام..."
python3 enhanced_main.py

if [ $? -ne 0 ]; then
    echo
    echo "❌ حدث خطأ في تشغيل النظام"
    echo "جرب تشغيل الاختبار أولاً:"
    echo "python3 test_enhanced_system.py"
    echo
    read -p "اضغط Enter للمتابعة..."
    exit 1
fi

echo
echo "✅ تم إغلاق النظام بنجاح"