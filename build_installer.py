#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Customer Issues Management System - Build Installer
بناء مثبت نظام إدارة مشاكل العملاء

This script builds executable files using PyInstaller.
يقوم هذا السكريبت ببناء ملفات تنفيذية باستخدام PyInstaller.
"""

import os
import sys
import subprocess
import shutil
import platform
from datetime import datetime

def ensure_pyinstaller():
    """التأكد من تثبيت PyInstaller"""
    try:
        import PyInstaller
        print("✅ PyInstaller is available")
        return True
    except ImportError:
        print("❌ PyInstaller not found")
        print("Installing PyInstaller...")
        try:
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'pyinstaller'])
            print("✅ PyInstaller installed successfully")
            return True
        except subprocess.CalledProcessError:
            print("❌ Failed to install PyInstaller")
            return False

def clean_build_dirs():
    """تنظيف مجلدات البناء"""
    dirs_to_clean = ['build', 'dist', '__pycache__']
    for dir_name in dirs_to_clean:
        if os.path.exists(dir_name):
            shutil.rmtree(dir_name)
            print(f"🧹 Cleaned {dir_name}")

def build_windows_executable():
    """بناء ملف تنفيذي للويندوز"""
    print("\n🏗️ Building Windows executable...")
    
    cmd = [
        'pyinstaller',
        '--onefile',                    # ملف واحد
        '--windowed',                   # بدون نافذة terminal
        '--name', 'CustomerIssuesManagement',  # اسم الملف التنفيذي
        '--distpath', 'dist',           # مجلد الإخراج
        '--workpath', 'build',          # مجلد العمل المؤقت
        '--specpath', '.',              # مجلد ملف .spec
        '--clean',                      # تنظيف قبل البناء
        'customer_issues_main.py'       # الملف الرئيسي
    ]
    
    # إضافة أيقونة إذا كانت متوفرة
    if os.path.exists('app.ico'):
        cmd.extend(['--icon', 'app.ico'])
    
    try:
        subprocess.check_call(cmd)
        print("✅ Windows executable built successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to build Windows executable: {e}")
        return False

def build_linux_executable():
    """بناء ملف تنفيذي للينكس"""
    print("\n🏗️ Building Linux executable...")
    
    cmd = [
        'pyinstaller',
        '--onefile',                    # ملف واحد
        '--name', 'customer-issues-management',  # اسم الملف التنفيذي
        '--distpath', 'dist',           # مجلد الإخراج
        '--workpath', 'build',          # مجلد العمل المؤقت
        '--specpath', '.',              # مجلد ملف .spec
        '--clean',                      # تنظيف قبل البناء
        'customer_issues_main.py'       # الملف الرئيسي
    ]
    
    try:
        subprocess.check_call(cmd)
        print("✅ Linux executable built successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to build Linux executable: {e}")
        return False

def create_portable_package():
    """إنشاء حزمة محمولة"""
    print("\n📦 Creating portable package...")
    
    package_name = f"customer_issues_portable_{datetime.now().strftime('%Y%m%d')}"
    package_dir = os.path.join('dist', package_name)
    
    # إنشاء مجلد الحزمة
    os.makedirs(package_dir, exist_ok=True)
    
    # نسخ الملفات الأساسية
    files_to_copy = [
        'customer_issues_main.py',
        'customer_issues_database.py',
        'customer_issues_window.py',
        'customer_issues_functions.py',
        'customer_issues_file_manager.py',
        'requirements.txt',
        'README.md',
        'LICENSE.txt'
    ]
    
    for file_name in files_to_copy:
        if os.path.exists(file_name):
            shutil.copy2(file_name, package_dir)
            print(f"📄 Copied {file_name}")
    
    # نسخ الملف التنفيذي إذا كان موجوداً
    system = platform.system().lower()
    if system == 'windows':
        exe_name = 'CustomerIssuesManagement.exe'
        run_script = 'run.bat'
        run_content = '''@echo off
chcp 65001 > nul
cd /d "%~dp0"
if exist CustomerIssuesManagement.exe (
    CustomerIssuesManagement.exe
) else (
    python customer_issues_main.py
)
pause'''
    else:
        exe_name = 'customer-issues-management'
        run_script = 'run.sh'
        run_content = '''#!/bin/bash
cd "$(dirname "$0")"
if [ -f "./customer-issues-management" ]; then
    ./customer-issues-management
else
    python3 customer_issues_main.py
fi'''
    
    exe_path = os.path.join('dist', exe_name)
    if os.path.exists(exe_path):
        shutil.copy2(exe_path, package_dir)
        print(f"🚀 Copied executable: {exe_name}")
    
    # إنشاء سكريبت التشغيل
    script_path = os.path.join(package_dir, run_script)
    with open(script_path, 'w', encoding='utf-8') as f:
        f.write(run_content)
    
    if system != 'windows':
        os.chmod(script_path, 0o755)
    
    print(f"� Created run script: {run_script}")
    
    # إنشاء ملف معلومات
    info_content = f"""Customer Issues Management System - Portable Package
نظام إدارة مشاكل العملاء - الحزمة المحمولة

Version: 2.0.0
Build Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
Platform: {platform.system()} {platform.machine()}

Files included:
- Executable (if available)
- Python source files
- Run script
- Documentation

To run the system:
- Double-click {run_script}
- Or run: python customer_issues_main.py

للتشغيل:
- انقر مرتين على {run_script}
- أو شغل: python customer_issues_main.py
"""
    
    with open(os.path.join(package_dir, 'INFO.txt'), 'w', encoding='utf-8') as f:
        f.write(info_content)
    
    print(f"📋 Created info file")
    print(f"✅ Portable package created: {package_dir}")
    
    return package_dir

def create_archive(package_dir):
    """إنشاء أرشيف مضغوط"""
    print("\n🗜️ Creating archive...")
    
    base_name = os.path.basename(package_dir)
    system = platform.system().lower()
    
    if system == 'windows':
        # إنشاء ZIP
        archive_name = f"{base_name}.zip"
        try:
            shutil.make_archive(
                os.path.join('dist', base_name),
                'zip',
                os.path.dirname(package_dir),
                base_name
            )
            print(f"✅ ZIP archive created: {archive_name}")
        except Exception as e:
            print(f"❌ Failed to create ZIP: {e}")
    else:
        # إنشاء TAR.GZ
        archive_name = f"{base_name}.tar.gz"
        try:
            shutil.make_archive(
                os.path.join('dist', base_name),
                'gztar',
                os.path.dirname(package_dir),
                base_name
            )
            print(f"✅ TAR.GZ archive created: {archive_name}")
        except Exception as e:
            print(f"❌ Failed to create TAR.GZ: {e}")

def main():
    """الوظيفة الرئيسية"""
    print("=" * 60)
    print("🏗️ Customer Issues Management System - Build Installer")
    print("   بناء مثبت نظام إدارة مشاكل العملاء")
    print("=" * 60)
    
    # فحص النظام
    system = platform.system()
    print(f"🖥️ Platform: {system}")
    print(f"🐍 Python: {sys.version}")
    
    # التأكد من PyInstaller
    if not ensure_pyinstaller():
        return 1
    
    # تنظيف المجلدات القديمة
    clean_build_dirs()
    
    # بناء الملف التنفيذي
    success = False
    if system == "Windows":
        success = build_windows_executable()
    else:
        success = build_linux_executable()
    
    if not success:
        print("\n❌ Build failed!")
        return 1
    
    # إنشاء الحزمة المحمولة
    package_dir = create_portable_package()
    
    # إنشاء الأرشيف
    create_archive(package_dir)
    
    print("\n" + "=" * 60)
    print("✅ Build completed successfully!")
    print("✅ اكتمل البناء بنجاح!")
    print("\nBuilt files are in the 'dist' directory")
    print("الملفات المبنية موجودة في مجلد 'dist'")
    print("=" * 60)
    
    return 0

if __name__ == "__main__":
    sys.exit(main())