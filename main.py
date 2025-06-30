#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
نظام إدارة مشاكل العملاء
Customer Issues Management System

تطبيق شامل لإدارة مشاكل وشكاوى العملاء مع إمكانيات متقدمة للبحث والتقارير
"""

import sys
import os
import tkinter as tk
from tkinter import messagebox

# إضافة المجلد الحالي إلى مسار Python
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from main_window import MainWindow
    from database import db
    import sqlite3
except ImportError as e:
    print(f"خطأ في استيراد المكتبات: {e}")
    sys.exit(1)

def check_dependencies():
    """فحص المتطلبات والمكتبات المطلوبة"""
    missing_modules = []
    
    try:
        import tkinter
    except ImportError:
        missing_modules.append("tkinter")
    
    try:
        import sqlite3
    except ImportError:
        missing_modules.append("sqlite3")
    
    try:
        from reportlab.lib.pagesizes import A4
        from reportlab.platypus import SimpleDocTemplate
    except ImportError:
        missing_modules.append("reportlab")
    
    if missing_modules:
        error_msg = f"المكتبات التالية مفقودة: {', '.join(missing_modules)}\n"
        error_msg += "يرجى تثبيتها باستخدام pip install"
        print(error_msg)
        return False
    
    return True

def create_directories():
    """إنشاء المجلدات المطلوبة"""
    directories = [
        "d:/test",  # مجلد المرفقات الافتراضي
        "reports",  # مجلد التقارير
        "backups"   # مجلد النسخ الاحتياطية
    ]
    
    for directory in directories:
        try:
            if not os.path.exists(directory):
                os.makedirs(directory)
                print(f"تم إنشاء المجلد: {directory}")
        except Exception as e:
            print(f"فشل في إنشاء المجلد {directory}: {e}")

def initialize_database():
    """تهيئة قاعدة البيانات"""
    try:
        # إنشاء قاعدة البيانات والجداول
        print("جارٍ تهيئة قاعدة البيانات...")
        
        # التحقق من وجود الجداول
        conn = sqlite3.connect("customer_issues.db")
        cursor = conn.cursor()
        
        # فحص وجود الجداول
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = cursor.fetchall()
        table_names = [table[0] for table in tables]
        
        expected_tables = ['customers', 'issue_categories', 'issues', 'correspondences', 'attachments', 'audit_log']
        
        if all(table in table_names for table in expected_tables):
            print("قاعدة البيانات جاهزة")
        else:
            print("جارٍ إنشاء الجداول...")
            # سيتم إنشاء الجداول تلقائياً عند استيراد database.py
        
        conn.close()
        return True
        
    except Exception as e:
        print(f"خطأ في تهيئة قاعدة البيانات: {e}")
        return False

def show_welcome_message():
    """عرض رسالة الترحيب"""
    welcome_text = """
    مرحباً بك في نظام إدارة مشاكل العملاء
    
    الميزات المتاحة:
    • إدارة بيانات العملاء
    • تسجيل ومتابعة المشاكل
    • إدارة المراسلات
    • رفع وإدارة المرفقات
    • إنتاج التقارير PDF
    • البحث المتقدم
    • تتبع التعديلات
    
    للبدء، استخدم الأزرار في الأعلى لإضافة البيانات
    """
    
    root = tk.Tk()
    root.withdraw()  # إخفاء النافذة الرئيسية مؤقتاً
    
    messagebox.showinfo("نظام إدارة مشاكل العملاء", welcome_text)
    root.destroy()

def backup_database():
    """إنشاء نسخة احتياطية من قاعدة البيانات"""
    try:
        import shutil
        from datetime import datetime
        
        if os.path.exists("customer_issues.db"):
            backup_name = f"backups/customer_issues_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.db"
            shutil.copy2("customer_issues.db", backup_name)
            print(f"تم إنشاء نسخة احتياطية: {backup_name}")
    except Exception as e:
        print(f"فشل في إنشاء النسخة الاحتياطية: {e}")

def main():
    """الدالة الرئيسية لتشغيل التطبيق"""
    print("=" * 50)
    print("نظام إدارة مشاكل العملاء")
    print("Customer Issues Management System")
    print("=" * 50)
    
    # فحص المتطلبات
    print("جارٍ فحص المتطلبات...")
    if not check_dependencies():
        return
    
    # إنشاء المجلدات المطلوبة
    print("جارٍ إنشاء المجلدات...")
    create_directories()
    
    # تهيئة قاعدة البيانات
    if not initialize_database():
        print("فشل في تهيئة قاعدة البيانات")
        return
    
    # إنشاء نسخة احتياطية
    backup_database()
    
    try:
        # عرض رسالة الترحيب
        show_welcome_message()
        
        # تشغيل التطبيق
        print("جارٍ تشغيل التطبيق...")
        app = MainWindow()
        
        # إعداد معالج إغلاق التطبيق
        def on_closing():
            if messagebox.askokcancel("إغلاق", "هل تريد إغلاق التطبيق؟"):
                backup_database()  # نسخة احتياطية عند الإغلاق
                app.root.destroy()
        
        app.root.protocol("WM_DELETE_WINDOW", on_closing)
        
        # تشغيل التطبيق
        app.run()
        
    except Exception as e:
        error_msg = f"خطأ في تشغيل التطبيق: {e}"
        print(error_msg)
        
        # محاولة عرض الخطأ في نافذة منبثقة
        try:
            root = tk.Tk()
            root.withdraw()
            messagebox.showerror("خطأ", error_msg)
            root.destroy()
        except:
            pass
        
        sys.exit(1)

if __name__ == "__main__":
    main()