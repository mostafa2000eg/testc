#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
نظام إدارة مشاكل العملاء - النسخة المحسنة
Customer Issues Management System - Enhanced Version

تطوير: مساعد الذكي الاصطناعي
Development: AI Assistant

هذا النظام مصمم لإدارة مشاكل العملاء في شركات الغاز بشكل إلكتروني
بدلاً من الملفات التقليدية
"""

import os
import sys
import tkinter as tk
from tkinter import messagebox
import traceback
from datetime import datetime

# إضافة المجلد الحالي لمسار Python
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

def check_requirements():
    """فحص المتطلبات الأساسية"""
    missing_modules = []
    
    # فحص tkinter
    try:
        import tkinter
        import tkinter.ttk
        print("✓ tkinter متوفر")
    except ImportError:
        missing_modules.append("tkinter")
        print("✗ tkinter غير متوفر")
    
    # فحص sqlite3
    try:
        import sqlite3
        print("✓ sqlite3 متوفر")
    except ImportError:
        missing_modules.append("sqlite3")
        print("✗ sqlite3 غير متوفر")
    
    # فحص المكتبات الأخرى
    optional_modules = {
        'reportlab': 'تقارير PDF',
        'PIL': 'معالجة الصور',
        'win32api': 'وظائف ويندوز (اختياري)'
    }
    
    for module, description in optional_modules.items():
        try:
            __import__(module)
            print(f"✓ {module} متوفر - {description}")
        except ImportError:
            print(f"⚠ {module} غير متوفر - {description} (اختياري)")
    
    if missing_modules:
        error_msg = f"المكتبات التالية مطلوبة ولكنها غير متوفرة:\n{', '.join(missing_modules)}"
        print(f"\n❌ خطأ: {error_msg}")
        return False
    
    print("\n✅ جميع المتطلبات الأساسية متوفرة")
    return True

def create_backup():
    """إنشاء نسخة احتياطية من قاعدة البيانات"""
    try:
        # إنشاء مجلد النسخ الاحتياطية
        backup_dir = os.path.join(current_dir, "backups")
        if not os.path.exists(backup_dir):
            os.makedirs(backup_dir)
        
        # إنشاء النسخة الاحتياطية
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # نسخ قاعدة البيانات الرئيسية
        import shutil
        source_db = os.path.join(current_dir, "customer_issues_enhanced.db")
        if os.path.exists(source_db):
            backup_db = os.path.join(backup_dir, f"backup_{timestamp}.db")
            shutil.copy2(source_db, backup_db)
            print(f"✓ تم إنشاء نسخة احتياطية: {backup_db}")
        
        # تنظيف النسخ القديمة (الاحتفاظ بآخر 10 نسخ)
        cleanup_old_backups(backup_dir)
        
    except Exception as e:
        print(f"⚠ تحذير: فشل في إنشاء نسخة احتياطية - {e}")

def cleanup_old_backups(backup_dir, keep_count=10):
    """تنظيف النسخ الاحتياطية القديمة"""
    try:
        backup_files = []
        for file in os.listdir(backup_dir):
            if file.startswith("backup_") and file.endswith(".db"):
                file_path = os.path.join(backup_dir, file)
                backup_files.append((file_path, os.path.getmtime(file_path)))
        
        # ترتيب حسب التاريخ
        backup_files.sort(key=lambda x: x[1], reverse=True)
        
        # حذف النسخ الزائدة
        for file_path, _ in backup_files[keep_count:]:
            os.remove(file_path)
            print(f"✓ تم حذف نسخة احتياطية قديمة: {os.path.basename(file_path)}")
            
    except Exception as e:
        print(f"⚠ تحذير: فشل في تنظيف النسخ الاحتياطية - {e}")

def setup_logging():
    """إعداد نظام السجلات"""
    try:
        import logging
        
        # إنشاء مجلد السجلات
        logs_dir = os.path.join(current_dir, "logs")
        if not os.path.exists(logs_dir):
            os.makedirs(logs_dir)
        
        # إعداد ملف السجل
        log_file = os.path.join(logs_dir, f"system_{datetime.now().strftime('%Y%m%d')}.log")
        
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_file, encoding='utf-8'),
                logging.StreamHandler(sys.stdout)
            ]
        )
        
        return logging.getLogger(__name__)
        
    except Exception as e:
        print(f"⚠ تحذير: فشل في إعداد السجلات - {e}")
        return None

def handle_exception(exc_type, exc_value, exc_traceback):
    """معالج الأخطاء العام"""
    if issubclass(exc_type, KeyboardInterrupt):
        sys.__excepthook__(exc_type, exc_value, exc_traceback)
        return
    
    # تسجيل الخطأ
    error_msg = "".join(traceback.format_exception(exc_type, exc_value, exc_traceback))
    print(f"❌ خطأ غير متوقع:\n{error_msg}")
    
    # عرض رسالة للمستخدم
    try:
        root = tk.Tk()
        root.withdraw()
        messagebox.showerror(
            "خطأ في النظام",
            f"حدث خطأ غير متوقع في النظام:\n\n{str(exc_value)}\n\nسيتم إغلاق التطبيق الآن."
        )
        root.destroy()
    except:
        pass

def main():
    """الوظيفة الرئيسية"""
    print("=" * 60)
    print("نظام إدارة مشاكل العملاء - النسخة المحسنة")
    print("Customer Issues Management System - Enhanced Version")
    print("=" * 60)
    
    # إعداد معالج الأخطاء
    sys.excepthook = handle_exception
    
    # إعداد السجلات
    logger = setup_logging()
    if logger:
        logger.info("بدء تشغيل النظام")
    
    # فحص المتطلبات
    print("\n🔍 فحص المتطلبات...")
    if not check_requirements():
        input("\nاضغط Enter للخروج...")
        return 1
    
    # إنشاء نسخة احتياطية
    print("\n💾 إنشاء نسخة احتياطية...")
    create_backup()
    
    try:
        # تشغيل النظام
        print("\n🚀 تشغيل النظام...")
        
        # استيراد الواجهة الرئيسية
        from enhanced_main_window import EnhancedMainWindow
        from enhanced_functions import EnhancedFunctions
        
        # إنشاء الواجهة الرئيسية
        app = EnhancedMainWindow()
        
        # ربط الوظائف
        functions = EnhancedFunctions(app)
        app.functions = functions
        
        # ربط الوظائف بالواجهة
        app.load_initial_data = functions.load_initial_data
        app.filter_by_year = functions.filter_by_year
        app.on_search_type_change = functions.on_search_type_change
        app.perform_search = functions.perform_search
        app.add_new_case = functions.add_new_case
        app.select_case = functions.select_case
        
        # تحميل البيانات الأولية
        functions.load_initial_data()
        
        if logger:
            logger.info("تم تشغيل النظام بنجاح")
        
        print("✅ تم تشغيل النظام بنجاح!")
        print("📝 يمكنك الآن استخدام النظام...")
        
        # تشغيل الواجهة
        app.run()
        
        if logger:
            logger.info("تم إغلاق النظام بنجاح")
        
        print("\n👋 تم إغلاق النظام بنجاح")
        return 0
        
    except ImportError as e:
        error_msg = f"فشل في استيراد الملفات المطلوبة: {e}"
        print(f"\n❌ خطأ: {error_msg}")
        if logger:
            logger.error(error_msg)
        
        try:
            root = tk.Tk()
            root.withdraw()
            messagebox.showerror("خطأ في التشغيل", error_msg)
            root.destroy()
        except:
            pass
        
        input("\nاضغط Enter للخروج...")
        return 1
        
    except Exception as e:
        error_msg = f"خطأ في تشغيل النظام: {e}"
        print(f"\n❌ خطأ: {error_msg}")
        if logger:
            logger.error(error_msg)
        
        try:
            root = tk.Tk()
            root.withdraw()
            messagebox.showerror("خطأ في التشغيل", error_msg)
            root.destroy()
        except:
            pass
        
        input("\nاضغط Enter للخروج...")
        return 1

def on_closing():
    """معالج إغلاق التطبيق"""
    try:
        # حفظ البيانات المهمة
        print("\n💾 حفظ البيانات...")
        
        # إنشاء نسخة احتياطية أخيرة
        create_backup()
        
        print("✅ تم حفظ البيانات بنجاح")
        
    except Exception as e:
        print(f"⚠ تحذير: فشل في حفظ البيانات - {e}")

if __name__ == "__main__":
    # تسجيل معالج الإغلاق
    import atexit
    atexit.register(on_closing)
    
    # تشغيل النظام
    exit_code = main()
    sys.exit(exit_code)