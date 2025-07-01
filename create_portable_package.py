#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Customer Issues Management System - Portable Package Creator (Fixed)
منشئ الحزمة المحمولة - نظام إدارة مشاكل العملاء (مصحح)

Version: 2.0.0
"""

import os
import shutil
import zipfile
from datetime import datetime

def create_portable_package():
    """إنشاء حزمة محمولة للنظام"""
    
    # تحديد ملفات النظام الأساسية
    system_files = [
        'customer_issues_main.py',
        'customer_issues_database.py', 
        'customer_issues_window.py',
        'customer_issues_functions.py',
        'customer_issues_file_manager.py',
        'test_customer_issues.py'
    ]
    
    # ملفات التشغيل والتوثيق
    additional_files = [
        'requirements.txt',
        'README.md',
        'CHANGELOG.md',
        'LICENSE.txt',
        'run_system_fixed.bat',
        'run_system.sh'
    ]
    
    # التحقق من وجود الملفات
    missing_files = []
    for file in system_files + additional_files:
        if not os.path.exists(file):
            missing_files.append(file)
    
    if missing_files:
        print("❌ الملفات التالية مفقودة:")
        for file in missing_files:
            print(f"  - {file}")
        return False
    
    # إنشاء اسم المجلد
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    package_name = f"customer_issues_management_fixed_{timestamp}"
    
    print(f"📦 إنشاء الحزمة المحمولة: {package_name}")
    
    # إنشاء مجلد الحزمة
    if os.path.exists(package_name):
        shutil.rmtree(package_name)
    
    os.makedirs(package_name)
    
    # نسخ الملفات الأساسية
    print("📋 نسخ الملفات الأساسية...")
    files_copied = 0
    
    for file in system_files + additional_files:
        try:
            shutil.copy2(file, package_name)
            files_copied += 1
            print(f"  ✓ {file}")
        except Exception as e:
            print(f"  ❌ خطأ في نسخ {file}: {e}")
    
    # إنشاء المجلدات الفرعية
    print("📁 إنشاء المجلدات الفرعية...")
    subdirs = ['files', 'backups', 'reports', 'logs', 'temp']
    
    for subdir in subdirs:
        subdir_path = os.path.join(package_name, subdir)
        os.makedirs(subdir_path, exist_ok=True)
        print(f"  ✓ {subdir}/")
    
    # إنشاء ملف README للحزمة
    readme_content = """# Customer Issues Management System - Portable Package (Fixed)
## نظام إدارة مشاكل العملاء - الحزمة المحمولة (مصححة)

### How to Run / طريقة التشغيل:

**Windows:**
- Double-click `run_system_fixed.bat`

**Linux/Mac:**
- Run `bash run_system.sh`

### Requirements / المتطلبات:
- Python 3.7 or higher
- tkinter (usually included with Python)

### Files Included / الملفات المضمنة:
- customer_issues_main.py (Main application)
- customer_issues_database.py (Database manager - FIXED)
- customer_issues_window.py (User interface)
- customer_issues_functions.py (Core functions)
- customer_issues_file_manager.py (File management)
- test_customer_issues.py (System tests)
- requirements.txt (Dependencies)
- README.md (Documentation)
- CHANGELOG.md (Version history)
- LICENSE.txt (License information)

### What's Fixed / ما تم إصلاحه:
✅ Class name fixed: EnhancedDatabase → DatabaseManager
✅ Import statements corrected
✅ Batch file encoding issues resolved
✅ Function name corrected: initialize_database → init_database
✅ Removed Arabic characters from batch file

### Version: 2.0.0 (Fixed)
### Date: {}

For support, please check the README.md file.
""".format(datetime.now().strftime("%Y-%m-%d"))
    
    readme_path = os.path.join(package_name, "PORTABLE_README.txt")
    with open(readme_path, 'w', encoding='utf-8') as f:
        f.write(readme_content)
    
    print(f"  ✓ PORTABLE_README.txt")
    
    # إحصائيات الحزمة
    total_files = len(os.listdir(package_name))
    package_size = sum(os.path.getsize(os.path.join(package_name, f)) 
                      for f in os.listdir(package_name) 
                      if os.path.isfile(os.path.join(package_name, f)))
    
    print(f"\n📊 إحصائيات الحزمة:")
    print(f"  📁 المجلد: {package_name}")
    print(f"  📄 عدد الملفات: {total_files}")
    print(f"  📏 الحجم: {package_size / 1024:.1f} KB")
    
    # إنشاء ملف ZIP
    zip_name = f"{package_name}.zip"
    print(f"\n🗜️ إنشاء ملف مضغوط: {zip_name}")
    
    with zipfile.ZipFile(zip_name, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(package_name):
            for file in files:
                file_path = os.path.join(root, file)
                arc_path = os.path.relpath(file_path, os.path.dirname(package_name))
                zipf.write(file_path, arc_path)
    
    zip_size = os.path.getsize(zip_name)
    print(f"  ✓ حجم الملف المضغوط: {zip_size / 1024:.1f} KB")
    
    print(f"\n🎉 تم إنشاء الحزمة المحمولة بنجاح!")
    print(f"📦 المجلد: {package_name}")
    print(f"🗜️ الملف المضغوط: {zip_name}")
    print(f"\n🚀 لتشغيل النظام:")
    print(f"  1. استخراج الملف المضغوط")
    print(f"  2. تشغيل run_system_fixed.bat (Windows)")
    print(f"  3. أو تشغيل run_system.sh (Linux/Mac)")
    
    return True

if __name__ == "__main__":
    print("=" * 60)
    print("🔧 منشئ الحزمة المحمولة المصححة")
    print("Customer Issues Management System - Fixed Package Creator")
    print("=" * 60)
    print()
    
    if create_portable_package():
        print("\n✅ تمت العملية بنجاح!")
    else:
        print("\n❌ فشلت العملية!")
        exit(1)