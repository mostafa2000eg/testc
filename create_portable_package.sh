#!/bin/bash
# -*- coding: utf-8 -*-
# ملف إنشاء الحزمة المحمولة - نظام إدارة مشاكل العملاء
# Create Portable Package Script for Customer Issues Management System

set -e  # خروج عند أول خطأ

echo "🏗️ إنشاء الحزمة المحمولة - نظام إدارة مشاكل العملاء"
echo "=================================================="
echo

# تحديد أمر Python
PYTHON_CMD=""
if command -v python3 &> /dev/null; then
    PYTHON_CMD="python3"
elif command -v python &> /dev/null; then
    PYTHON_CMD="python"
else
    echo "❌ Python غير متوفر"
    echo "يرجى تثبيت Python من: https://www.python.org/downloads/"
    exit 1
fi

echo "🔍 فحص Python..."
$PYTHON_CMD --version
echo "✅ Python متوفر"
echo

echo "🔧 فحص pip..."
if ! $PYTHON_CMD -m pip --version &> /dev/null; then
    echo "❌ pip غير متوفر"
    exit 1
fi
echo "✅ pip متوفر"
echo

echo "📦 تثبيت PyInstaller..."
if ! $PYTHON_CMD -m pip install pyinstaller; then
    echo "⚠️ فشل في تثبيت PyInstaller، جاري إنشاء حزمة Python..."
    CREATE_EXE=false
else
    echo "✅ تم تثبيت PyInstaller"
    CREATE_EXE=true
fi
echo

# إنشاء الحزمة
PACKAGE_DIR="نظام_إدارة_مشاكل_العملاء_المحمول"

if [ "$CREATE_EXE" = true ]; then
    echo "🔨 تجميع البرنامج..."
    if $PYTHON_CMD -m PyInstaller --onefile --windowed --name "نظام_إدارة_مشاكل_العملاء" enhanced_main.py; then
        echo "✅ تم تجميع البرنامج بنجاح"
        HAS_EXE=true
    else
        echo "❌ فشل في تجميع البرنامج، جاري إنشاء حزمة Python..."
        HAS_EXE=false
    fi
else
    HAS_EXE=false
fi

echo
echo "📁 إنشاء الحزمة المحمولة..."

# حذف المجلد إذا كان موجوداً
if [ -d "$PACKAGE_DIR" ]; then
    rm -rf "$PACKAGE_DIR"
fi

# إنشاء مجلد الحزمة
mkdir -p "$PACKAGE_DIR"

# نسخ الملف المجمع إذا وجد
if [ "$HAS_EXE" = true ] && [ -f "dist/نظام_إدارة_مشاكل_العملاء" ]; then
    cp "dist/نظام_إدارة_مشاكل_العملاء" "$PACKAGE_DIR/"
    echo "✅ تم نسخ الملف المجمع"
elif [ "$HAS_EXE" = true ] && [ -f "dist/نظام_إدارة_مشاكل_العملاء.exe" ]; then
    cp "dist/نظام_إدارة_مشاكل_العملاء.exe" "$PACKAGE_DIR/"
    echo "✅ تم نسخ الملف المجمع"
else
    echo "📋 إنشاء حزمة Python..."
fi

# نسخ ملفات Python
echo "📋 نسخ ملفات Python..."
for file in enhanced_main.py enhanced_database.py enhanced_main_window.py enhanced_functions.py enhanced_file_manager.py test_enhanced_system.py; do
    if [ -f "$file" ]; then
        cp "$file" "$PACKAGE_DIR/"
        echo "✅ تم نسخ $file"
    fi
done

# نسخ الملفات المساعدة
echo "📄 نسخ الملفات المساعدة..."
for file in "دليل_النظام_المحسن.md" "ملخص_النظام_المحسن.md" "README_Enhanced.md" "enhanced_requirements.txt" "دليل_إنشاء_الحزمة.md"; do
    if [ -f "$file" ]; then
        cp "$file" "$PACKAGE_DIR/"
        echo "✅ تم نسخ $file"
    fi
done

# إنشاء ملفات التشغيل
echo "🛠️ إنشاء ملفات التشغيل..."

# ملف تشغيل Unix
if [ -f "$PACKAGE_DIR/نظام_إدارة_مشاكل_العملاء" ]; then
    cat > "$PACKAGE_DIR/run_system.sh" << 'EOF'
#!/bin/bash
cd "$(dirname "$0")"
echo "🚀 تشغيل النظام..."
./نظام_إدارة_مشاكل_العملاء
EOF
else
    cat > "$PACKAGE_DIR/run_system.sh" << EOF
#!/bin/bash
cd "\$(dirname "\$0")"
echo "🚀 تشغيل النظام..."
$PYTHON_CMD enhanced_main.py
if [ \$? -ne 0 ]; then
    echo "❌ خطأ في تشغيل النظام"
    echo "تأكد من تثبيت Python"
    read -p "اضغط Enter للمتابعة..."
fi
EOF
fi

chmod +x "$PACKAGE_DIR/run_system.sh"

# ملف اختبار Unix
cat > "$PACKAGE_DIR/test_system.sh" << EOF
#!/bin/bash
cd "\$(dirname "\$0")"
echo "🧪 اختبار النظام..."
$PYTHON_CMD test_enhanced_system.py
read -p "اضغط Enter للمتابعة..."
EOF

chmod +x "$PACKAGE_DIR/test_system.sh"

# ملف تشغيل Windows (إذا كان النظام يدعم Windows)
if [ -f "$PACKAGE_DIR/نظام_إدارة_مشاكل_العملاء.exe" ]; then
    cat > "$PACKAGE_DIR/تشغيل_النظام.bat" << 'EOF'
@echo off
chcp 65001 > nul
cd /d "%~dp0"
echo 🚀 تشغيل النظام...
start "" "نظام_إدارة_مشاكل_العملاء.exe"
EOF
else
    cat > "$PACKAGE_DIR/تشغيل_النظام.bat" << EOF
@echo off
chcp 65001 > nul
cd /d "%~dp0"
echo 🚀 تشغيل النظام...
$PYTHON_CMD enhanced_main.py
if %errorlevel% neq 0 (
    echo ❌ خطأ في تشغيل النظام
    echo تأكد من تثبيت Python
    pause
)
EOF
fi

# ملف اختبار Windows
cat > "$PACKAGE_DIR/اختبار_النظام.bat" << EOF
@echo off
chcp 65001 > nul
cd /d "%~dp0"
echo 🧪 اختبار النظام...
$PYTHON_CMD test_enhanced_system.py
pause
EOF

echo "✅ تم إنشاء ملفات التشغيل"
echo

# إنشاء ملف معلومات
echo "📝 إنشاء ملف المعلومات..."
cat > "$PACKAGE_DIR/معلومات_التشغيل.txt" << 'EOF'
# نظام إدارة مشاكل العملاء - الحزمة المحمولة

## كيفية التشغيل:

### على ويندوز:
1. انقر نقراً مزدوجاً على "تشغيل_النظام.bat"
2. أو انقر نقراً مزدوجاً على الملف المجمع (إن وجد)

### على لينكس/ماك:
1. افتح Terminal في مجلد البرنامج
2. شغل: ./run_system.sh
3. أو: chmod +x run_system.sh && ./run_system.sh

## للاختبار:
- ويندوز: انقر على "اختبار_النظام.bat"
- لينكس/ماك: شغل ./test_system.sh

## المطور:
مساعد الذكي الاصطناعي - 2024

جميع الحقوق محفوظة
EOF

echo "✅ تم إنشاء ملف المعلومات"
echo

# تنظيف الملفات المؤقتة
echo "🧹 تنظيف الملفات المؤقتة..."
rm -rf build dist *.spec __pycache__ 2>/dev/null || true
echo "✅ تم التنظيف"
echo

echo "🎉 تم إنجاز الحزمة المحمولة بنجاح!"
echo
echo "📦 الحزمة جاهزة في: $PACKAGE_DIR"
echo
echo "💡 يمكنك نسخ هذا المجلد لأي جهاز وتشغيله"
echo

if [ -f "$PACKAGE_DIR/نظام_إدارة_مشاكل_العملاء.exe" ] || [ -f "$PACKAGE_DIR/نظام_إدارة_مشاكل_العملاء" ]; then
    echo "✅ الحزمة تحتوي على ملف مجمع - لا تحتاج Python على الجهاز الهدف"
else
    echo "⚠️ الحزمة تحتاج Python مثبت على الجهاز الهدف"
fi

echo
echo "👋 اكتمل!"