#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ملف تجميع نظام إدارة مشاكل العملاء
Build script for Customer Issues Management System
"""

import os
import sys
import shutil
import subprocess
from pathlib import Path

def check_pyinstaller():
    """فحص وجود PyInstaller"""
    try:
        import PyInstaller
        print("✅ PyInstaller متوفر")
        return True
    except ImportError:
        print("❌ PyInstaller غير متوفر")
        print("جاري تثبيت PyInstaller...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])
            print("✅ تم تثبيت PyInstaller بنجاح")
            return True
        except:
            print("❌ فشل في تثبيت PyInstaller")
            return False

def create_spec_file():
    """إنشاء ملف .spec للتجميع"""
    spec_content = '''# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

# الملفات الإضافية المطلوبة
added_files = [
    ('دليل_النظام_المحسن.md', '.'),
    ('ملخص_النظام_المحسن.md', '.'),
    ('README_Enhanced.md', '.'),
    ('enhanced_requirements.txt', '.'),
]

a = Analysis(
    ['enhanced_main.py'],
    pathex=[],
    binaries=[],
    datas=added_files,
    hiddenimports=[
        'tkinter',
        'tkinter.ttk',
        'tkinter.messagebox',
        'tkinter.filedialog',
        'tkinter.simpledialog',
        'sqlite3',
        'datetime',
        'os',
        'sys',
        'shutil',
        'platform'
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='نظام_إدارة_مشاكل_العملاء',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='icon.ico' if os.path.exists('icon.ico') else None,
)
'''
    
    with open('customer_issues.spec', 'w', encoding='utf-8') as f:
        f.write(spec_content)
    
    print("✅ تم إنشاء ملف customer_issues.spec")

def create_icon():
    """إنشاء أيقونة بسيطة للبرنامج"""
    # إذا لم تكن الأيقونة موجودة، ننشئ ملف نصي يوضح ذلك
    if not os.path.exists('icon.ico'):
        print("⚠️ لا توجد أيقونة - سيتم استخدام الأيقونة الافتراضية")
        # يمكن إضافة كود لإنشاء أيقونة بسيطة هنا إذا أردت

def build_executable():
    """تجميع البرنامج إلى ملف .exe"""
    print("\n🔨 بدء تجميع البرنامج...")
    
    try:
        # تشغيل PyInstaller
        cmd = [
            sys.executable, "-m", "PyInstaller",
            "--clean",
            "--noconfirm", 
            "customer_issues.spec"
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ تم تجميع البرنامج بنجاح!")
            return True
        else:
            print(f"❌ خطأ في التجميع:\n{result.stderr}")
            return False
            
    except Exception as e:
        print(f"❌ خطأ في تشغيل PyInstaller: {e}")
        return False

def create_portable_package():
    """إنشاء حزمة محمولة كاملة"""
    print("\n📦 إنشاء الحزمة المحمولة...")
    
    # إنشاء مجلد الحزمة
    package_dir = "نظام_إدارة_مشاكل_العملاء_المحمول"
    if os.path.exists(package_dir):
        shutil.rmtree(package_dir)
    
    os.makedirs(package_dir)
    
    # نسخ الملف المجمع
    exe_source = os.path.join("dist", "نظام_إدارة_مشاكل_العملاء.exe")
    if os.path.exists(exe_source):
        shutil.copy2(exe_source, os.path.join(package_dir, "نظام_إدارة_مشاكل_العملاء.exe"))
        print("✅ تم نسخ الملف المجمع")
    else:
        print("❌ لم يتم العثور على الملف المجمع")
        return False
    
    # نسخ الملفات المهمة
    important_files = [
        "دليل_النظام_المحسن.md",
        "ملخص_النظام_المحسن.md", 
        "README_Enhanced.md",
        "enhanced_requirements.txt"
    ]
    
    for file in important_files:
        if os.path.exists(file):
            shutil.copy2(file, package_dir)
            print(f"✅ تم نسخ {file}")
    
    # إنشاء ملف تشغيل سريع
    batch_content = '''@echo off
chcp 65001 > nul
title نظام إدارة مشاكل العملاء - النسخة المحمولة

echo.
echo ================================
echo نظام إدارة مشاكل العملاء
echo النسخة المحمولة
echo ================================
echo.

echo 🚀 تشغيل النظام...
start "" "نظام_إدارة_مشاكل_العملاء.exe"

echo ✅ تم تشغيل النظام
echo يمكنك إغلاق هذه النافذة الآن
pause > nul
'''
    
    with open(os.path.join(package_dir, "تشغيل_النظام.bat"), 'w', encoding='utf-8') as f:
        f.write(batch_content)
    
    # إنشاء ملف معلومات
    info_content = '''# نظام إدارة مشاكل العملاء - النسخة المحمولة

## كيفية التشغيل:
1. انقر نقراً مزدوجاً على "تشغيل_النظام.bat"
2. أو انقر نقراً مزدوجاً على "نظام_إدارة_مشاكل_العملاء.exe"

## الملفات المرفقة:
- نظام_إدارة_مشاكل_العملاء.exe: البرنامج الرئيسي
- تشغيل_النظام.bat: ملف تشغيل سريع
- دليل_النظام_المحسن.md: دليل الاستخدام المفصل
- ملخص_النظام_المحسن.md: ملخص تقني
- README_Enhanced.md: معلومات البداية السريعة

## متطلبات التشغيل:
- ويندوز 7 أو أحدث
- لا يحتاج Python أو أي برامج إضافية
- يعمل بدون إنترنت

## المطور:
مساعد الذكي الاصطناعي - 2024

جميع الحقوق محفوظة
'''
    
    with open(os.path.join(package_dir, "معلومات_التشغيل.txt"), 'w', encoding='utf-8') as f:
        f.write(info_content)
    
    print(f"✅ تم إنشاء الحزمة المحمولة في: {package_dir}")
    return True

def create_installer():
    """إنشاء ملف تثبيت NSIS (اختياري)"""
    print("\n💿 إنشاء ملف الإعداد...")
    
    nsis_script = '''# نص NSIS لإنشاء ملف تثبيت
# يحتاج NSIS مثبت على الجهاز

!define APP_NAME "نظام إدارة مشاكل العملاء"
!define APP_VERSION "2.0.0"
!define APP_PUBLISHER "AI Assistant"
!define APP_EXE "نظام_إدارة_مشاكل_العملاء.exe"

Name "${APP_NAME}"
OutFile "تثبيت_نظام_إدارة_مشاكل_العملاء.exe"
InstallDir "$PROGRAMFILES\\${APP_NAME}"
RequestExecutionLevel admin

Page directory
Page instfiles

Section "الملفات الرئيسية"
    SetOutPath "$INSTDIR"
    File "نظام_إدارة_مشاكل_العملاء_المحمول\\${APP_EXE}"
    File "نظام_إدارة_مشاكل_العملاء_المحمول\\*.md"
    File "نظام_إدارة_مشاكل_العملاء_المحمول\\*.txt"
    File "نظام_إدارة_مشاكل_العملاء_المحمول\\*.bat"
    
    # إنشاء اختصار في قائمة ابدأ
    CreateDirectory "$SMPROGRAMS\\${APP_NAME}"
    CreateShortcut "$SMPROGRAMS\\${APP_NAME}\\${APP_NAME}.lnk" "$INSTDIR\\${APP_EXE}"
    
    # إنشاء اختصار على سطح المكتب
    CreateShortcut "$DESKTOP\\${APP_NAME}.lnk" "$INSTDIR\\${APP_EXE}"
    
    # تسجيل في إضافة/إزالة البرامج
    WriteRegStr HKLM "Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\${APP_NAME}" "DisplayName" "${APP_NAME}"
    WriteRegStr HKLM "Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\${APP_NAME}" "UninstallString" "$INSTDIR\\uninstall.exe"
    WriteRegStr HKLM "Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\${APP_NAME}" "Publisher" "${APP_PUBLISHER}"
    WriteRegStr HKLM "Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\${APP_NAME}" "DisplayVersion" "${APP_VERSION}"
    
    WriteUninstaller "$INSTDIR\\uninstall.exe"
SectionEnd

Section "Uninstall"
    Delete "$INSTDIR\\${APP_EXE}"
    Delete "$INSTDIR\\*.md"
    Delete "$INSTDIR\\*.txt"
    Delete "$INSTDIR\\*.bat"
    Delete "$INSTDIR\\uninstall.exe"
    
    Delete "$SMPROGRAMS\\${APP_NAME}\\${APP_NAME}.lnk"
    RMDir "$SMPROGRAMS\\${APP_NAME}"
    
    Delete "$DESKTOP\\${APP_NAME}.lnk"
    
    DeleteRegKey HKLM "Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\${APP_NAME}"
    
    RMDir "$INSTDIR"
SectionEnd
'''
    
    with open("installer.nsi", 'w', encoding='utf-8') as f:
        f.write(nsis_script)
    
    print("✅ تم إنشاء ملف installer.nsi")
    print("💡 لإنشاء ملف التثبيت، شغل: makensis installer.nsi")

def cleanup():
    """تنظيف الملفات المؤقتة"""
    print("\n🧹 تنظيف الملفات المؤقتة...")
    
    dirs_to_remove = ["build", "dist", "__pycache__"]
    files_to_remove = ["customer_issues.spec"]
    
    for dir_name in dirs_to_remove:
        if os.path.exists(dir_name):
            try:
                shutil.rmtree(dir_name)
                print(f"✅ تم حذف مجلد {dir_name}")
            except:
                print(f"⚠️ لم يتم حذف مجلد {dir_name}")
    
    for file_name in files_to_remove:
        if os.path.exists(file_name):
            try:
                os.remove(file_name)
                print(f"✅ تم حذف ملف {file_name}")
            except:
                print(f"⚠️ لم يتم حذف ملف {file_name}")

def main():
    """الوظيفة الرئيسية للتجميع"""
    print("🏗️ بناء حزمة نظام إدارة مشاكل العملاء")
    print("=" * 50)
    
    # فحص PyInstaller
    if not check_pyinstaller():
        print("❌ لا يمكن المتابعة بدون PyInstaller")
        return False
    
    # إنشاء الأيقونة
    create_icon()
    
    # إنشاء ملف .spec
    create_spec_file()
    
    # تجميع البرنامج
    if not build_executable():
        print("❌ فشل في تجميع البرنامج")
        return False
    
    # إنشاء الحزمة المحمولة
    if not create_portable_package():
        print("❌ فشل في إنشاء الحزمة المحمولة")
        return False
    
    # إنشاء ملف التثبيت (اختياري)
    create_installer()
    
    # تنظيف الملفات المؤقتة
    cleanup()
    
    print("\n🎉 تم إنجاز التجميع بنجاح!")
    print("📦 الحزمة المحمولة جاهزة في: نظام_إدارة_مشاكل_العملاء_المحمول")
    print("💡 يمكنك نسخ هذا المجلد لأي جهاز وتشغيله بدون تثبيت")
    
    return True

if __name__ == "__main__":
    success = main()
    input("\n👋 اضغط Enter للخروج...")
    sys.exit(0 if success else 1)