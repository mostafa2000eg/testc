#!/bin/bash
# Customer Issues Management System - Portable Package Creator
# منشئ الحزمة المحمولة لنظام إدارة مشاكل العملاء

set -e

# Configuration / الإعدادات
PACKAGE_NAME="customer_issues_management_portable"
VERSION="2.0.0"
BUILD_DATE=$(date +"%Y%m%d_%H%M%S")
PACKAGE_DIR="${PACKAGE_NAME}_${BUILD_DATE}"

echo "=================================="
echo "Customer Issues Management System"
echo "نظام إدارة مشاكل العملاء"
echo "Portable Package Creator v${VERSION}"
echo "=================================="
echo

echo "🚀 Creating portable package..."
echo "📦 Package name: ${PACKAGE_DIR}"
echo

# Create package directory / إنشاء مجلد الحزمة
echo "📁 Creating package directory..."
mkdir -p "${PACKAGE_DIR}"

# Copy Python files / نسخ ملفات Python
echo "� Copying Python files..."
PYTHON_FILES=(
    "customer_issues_main.py"
    "customer_issues_database.py"
    "customer_issues_window.py"
    "customer_issues_functions.py"
    "customer_issues_file_manager.py"
    "test_customer_issues.py"
)

for file in "${PYTHON_FILES[@]}"; do
    if [ -f "$file" ]; then
        cp "$file" "${PACKAGE_DIR}/"
        echo "  ✅ Copied: $file"
    else
        echo "  ⚠️ Not found: $file"
    fi
done

# Copy documentation / نسخ الوثائق
echo "📚 Copying documentation..."
DOC_FILES=(
    "README.md"
    "LICENSE.txt"
    "requirements.txt"
    "CHANGELOG.md"
    "docs/"
)

for item in "${DOC_FILES[@]}"; do
    if [ -e "$item" ]; then
        cp -r "$item" "${PACKAGE_DIR}/"
        echo "  ✅ Copied: $item"
    else
        echo "  ⚠️ Not found: $item"
    fi
done

# Copy run scripts / نسخ سكريبتات التشغيل
echo "⚙️ Copying run scripts..."
RUN_FILES=(
    "run_system.sh"
    "run_system.bat"
    "test_system.bat"
)

for file in "${RUN_FILES[@]}"; do
    if [ -f "$file" ]; then
        cp "$file" "${PACKAGE_DIR}/"
        chmod +x "${PACKAGE_DIR}/$file" 2>/dev/null || true
        echo "  ✅ Copied: $file"
    else
        echo "  ⚠️ Not found: $file"
    fi
done

# Create additional run scripts / إنشاء سكريبتات تشغيل إضافية
echo "🔧 Creating additional run scripts..."

# Linux/Mac run script
cat > "${PACKAGE_DIR}/run.sh" << 'EOF'
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
EOF
chmod +x "${PACKAGE_DIR}/run.sh"

# Windows batch file
cat > "${PACKAGE_DIR}/run.bat" << 'EOF'
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
EOF

echo "  ✅ Created: run.sh"
echo "  ✅ Created: run.bat"

# Create package information / إنشاء معلومات الحزمة
echo "� Creating package information..."
cat > "${PACKAGE_DIR}/PACKAGE_INFO.txt" << EOF
Customer Issues Management System - Portable Package
نظام إدارة مشاكل العملاء - الحزمة المحمولة

Version: ${VERSION}
Build Date: $(date '+%Y-%m-%d %H:%M:%S')
Package: ${PACKAGE_DIR}

=== SYSTEM REQUIREMENTS / متطلبات النظام ===
- Python 3.7 or higher / Python 3.7 أو أحدث
- Windows 7+, Linux, or macOS / ويندوز 7+ أو لينكس أو ماك
- 100MB free disk space / 100 ميجابايت مساحة فارغة

=== HOW TO RUN / كيفية التشغيل ===

Windows:
- Double-click run.bat
- Or double-click run_system.bat

Linux/Mac:
- Double-click run.sh (if GUI file manager supports it)
- Or in terminal: ./run.sh
- Or: bash run_system.sh

=== FILES INCLUDED / الملفات المرفقة ===

Python Files:
- customer_issues_main.py (Main application / التطبيق الرئيسي)
- customer_issues_database.py (Database manager / مدير قاعدة البيانات)
- customer_issues_window.py (Main window / النافذة الرئيسية)
- customer_issues_functions.py (Core functions / الوظائف الأساسية)
- customer_issues_file_manager.py (File management / إدارة الملفات)
- test_customer_issues.py (System test / اختبار النظام)

Run Scripts:
- run.sh (Quick launcher for Linux/Mac / مشغل سريع للينكس/ماك)
- run.bat (Quick launcher for Windows / مشغل سريع للويندوز)
- run_system.sh (Advanced launcher / مشغل متقدم)
- run_system.bat (Advanced launcher / مشغل متقدم)
- test_system.bat (System test / اختبار النظام)

Documentation:
- README.md (User guide / دليل المستخدم)
- LICENSE.txt (License information / معلومات الترخيص)
- requirements.txt (Python requirements / متطلبات Python)
- PACKAGE_INFO.txt (This file / هذا الملف)

=== FEATURES / المميزات ===
✅ Enhanced UI with split layout / واجهة محسنة مع تخطيط مقسم
✅ Advanced search with 7 types / بحث متقدم بـ 7 أنواع
✅ Dual numbering for correspondence / ترقيم مزدوج للمراسلات
✅ 11 issue categories / 11 تصنيف للمشاكل
✅ Staff management / إدارة الموظفين
✅ Auto backups / نسخ احتياطية تلقائية
✅ Arabic and English support / دعم العربية والإنجليزية

=== FIRST TIME SETUP / إعداد المرة الأولى ===
1. Extract all files to a folder / استخرج جميع الملفات لمجلد
2. Run the system using one of the run scripts / شغل النظام باستخدام أحد سكريبتات التشغيل
3. The system will create necessary folders automatically / سينشئ النظام المجلدات المطلوبة تلقائياً

=== TROUBLESHOOTING / حل المشاكل ===
- If Python is not found, install Python 3.7+ from python.org
- If you get permission errors, run as administrator
- Check the logs folder for detailed error information

- إذا لم يتم العثور على Python، ثبت Python 3.7+ من python.org
- إذا حصلت على أخطاء صلاحيات، شغل كمدير
- راجع مجلد logs للحصول على معلومات مفصلة عن الأخطاء

=== SUPPORT / الدعم ===
For technical support, check the documentation or contact the development team.
للدعم التقني، راجع الوثائق أو اتصل بفريق التطوير.

Developed specifically for gas companies by AI Assistant.
تم تطويره خصيصاً لشركات الغاز بواسطة المساعد الذكي.
EOF

# Create directory structure / إنشاء هيكل المجلدات
echo "🗂️ Creating directory structure..."
mkdir -p "${PACKAGE_DIR}/files"
mkdir -p "${PACKAGE_DIR}/reports"
mkdir -p "${PACKAGE_DIR}/backups"
mkdir -p "${PACKAGE_DIR}/logs"

echo "  ✅ Created: files/ (for attachments)"
echo "  ✅ Created: reports/ (for generated reports)"
echo "  ✅ Created: backups/ (for database backups)"
echo "  ✅ Created: logs/ (for system logs)"

# Create sample data (optional) / إنشاء بيانات نموذجية (اختياري)
echo "� Creating sample configuration..."
cat > "${PACKAGE_DIR}/sample_config.txt" << 'EOF'
# Sample Configuration for Customer Issues Management System
# إعدادات نموذجية لنظام إدارة مشاكل العملاء

# Database will be created automatically on first run
# ستُنشأ قاعدة البيانات تلقائياً عند التشغيل الأول

# Default file storage path: ./files/
# مسار تخزين الملفات الافتراضي: ./files/

# Reports output path: ./reports/
# مسار تقارير الإخراج: ./reports/

# Backup path: ./backups/
# مسار النسخ الاحتياطية: ./backups/

# Log files path: ./logs/
# مسار ملفات السجلات: ./logs/
EOF

# Count files / عد الملفات
FILE_COUNT=$(find "${PACKAGE_DIR}" -type f | wc -l)
DIR_COUNT=$(find "${PACKAGE_DIR}" -type d | wc -l)

echo
echo "📊 Package Statistics:"
echo "  📄 Files: ${FILE_COUNT}"
echo "  📁 Directories: ${DIR_COUNT}"

# Calculate size / حساب الحجم
PACKAGE_SIZE=$(du -sh "${PACKAGE_DIR}" | cut -f1)
echo "  💾 Size: ${PACKAGE_SIZE}"

# Create compressed archive / إنشاء أرشيف مضغوط
echo
echo "🗜️ Creating compressed archive..."
if command -v zip &> /dev/null; then
    zip -r "${PACKAGE_DIR}.zip" "${PACKAGE_DIR}" >/dev/null 2>&1
    ZIP_SIZE=$(du -sh "${PACKAGE_DIR}.zip" | cut -f1)
    echo "  ✅ Created: ${PACKAGE_DIR}.zip (${ZIP_SIZE})"
else
    tar -czf "${PACKAGE_DIR}.tar.gz" "${PACKAGE_DIR}"
    TAR_SIZE=$(du -sh "${PACKAGE_DIR}.tar.gz" | cut -f1)
    echo "  ✅ Created: ${PACKAGE_DIR}.tar.gz (${TAR_SIZE})"
fi

echo
echo "=================================="
echo "✅ Portable package created successfully!"
echo "✅ تم إنشاء الحزمة المحمولة بنجاح!"
echo
echo "📦 Package directory: ${PACKAGE_DIR}"
echo "📋 Information file: ${PACKAGE_DIR}/PACKAGE_INFO.txt"
echo
echo "� To run the system:"
echo "   Windows: Double-click ${PACKAGE_DIR}/run.bat"
echo "   Linux/Mac: ./${PACKAGE_DIR}/run.sh"
echo
echo "للتشغيل:"
echo "   ويندوز: انقر مرتين على ${PACKAGE_DIR}/run.bat"
echo "   لينكس/ماك: ./${PACKAGE_DIR}/run.sh"
echo "=================================="