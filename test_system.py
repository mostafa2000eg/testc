#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
اختبار نظام إدارة مشاكل العملاء بدون واجهة رسومية
لاختبار وظائف قاعدة البيانات والمكونات الأساسية
"""

import sys
import os
from datetime import datetime

# إضافة المجلد الحالي إلى مسار Python
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_database():
    """اختبار قاعدة البيانات"""
    print("=" * 50)
    print("اختبار قاعدة البيانات")
    print("=" * 50)
    
    try:
        from database import db
        print("✓ تم تحميل قاعدة البيانات بنجاح")
        
        # اختبار الاتصال
        result = db.execute_query("SELECT COUNT(*) FROM customers")
        print(f"✓ عدد العملاء الحالي: {result[0][0]}")
        
        result = db.execute_query("SELECT COUNT(*) FROM issues")
        print(f"✓ عدد المشاكل الحالية: {result[0][0]}")
        
        result = db.execute_query("SELECT COUNT(*) FROM issue_categories")
        print(f"✓ عدد تصنيفات المشاكل: {result[0][0]}")
        
        return True
    except Exception as e:
        print(f"✗ خطأ في قاعدة البيانات: {e}")
        return False

def test_file_manager():
    """اختبار إدارة الملفات"""
    print("\n" + "=" * 50)
    print("اختبار إدارة الملفات")
    print("=" * 50)
    
    try:
        from file_manager import FileManager
        file_manager = FileManager()
        print("✓ تم تحميل مدير الملفات بنجاح")
        
        # اختبار إنشاء مجلد
        test_folder = file_manager.create_customer_folder("01091818010100")
        print(f"✓ تم إنشاء مجلد العميل: {test_folder}")
        
        return True
    except Exception as e:
        print(f"✗ خطأ في إدارة الملفات: {e}")
        return False

def test_report_generator():
    """اختبار مولد التقارير"""
    print("\n" + "=" * 50)
    print("اختبار مولد التقارير")
    print("=" * 50)
    
    try:
        from report_generator import ReportGenerator
        report_gen = ReportGenerator()
        print("✓ تم تحميل مولد التقارير بنجاح")
        return True
    except Exception as e:
        print(f"✗ خطأ في مولد التقارير: {e}")
        print("تحقق من تثبيت reportlab: pip install reportlab")
        return False

def add_sample_data():
    """إضافة بيانات تجريبية"""
    print("\n" + "=" * 50)
    print("إضافة بيانات تجريبية")
    print("=" * 50)
    
    try:
        from database import db
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # إضافة عميل تجريبي
        customer_query = """
            INSERT OR REPLACE INTO customers 
            (subscriber_number, name, address, phone, last_reading, last_reading_date, 
             debt_amount, created_date, created_by)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        customer_params = (
            "01091818010100", "أحمد محمد علي", "شارع 15 مايو، الدقي، الجيزة",
            "01012345678", 150.5, "2024-01-15", 250.75, current_time, "النظام"
        )
        
        db.execute_query(customer_query, customer_params)
        print("✓ تم إضافة عميل تجريبي")
        
        # إضافة مشكلة تجريبية
        issue_query = """
            INSERT OR REPLACE INTO issues 
            (customer_id, category_id, title, description, status, priority, 
             responsible_employee, created_date, created_by)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        issue_params = (
            1, 1, "مشكلة في قراءة العداد", 
            "العداد لا يعطي قراءة صحيحة ويحتاج لفحص فني",
            "مفتوحة", "عالية", "مهندس الصيانة", current_time, "النظام"
        )
        
        db.execute_query(issue_query, issue_params)
        print("✓ تم إضافة مشكلة تجريبية")
        
        # إضافة مراسلة تجريبية
        corr_query = """
            INSERT OR REPLACE INTO correspondences 
            (issue_id, correspondence_number, sender, receiver, subject, 
             date_sent, content, created_date, created_by)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        corr_params = (
            1, "CORR-2024-001", "قسم خدمة العملاء", "شركة تاون جاس",
            "شكوى بخصوص قراءة العداد", "2024-01-16",
            "نرجو التكرم بالنظر في شكوى العميل وإجراء اللازم",
            current_time, "النظام"
        )
        
        db.execute_query(corr_query, corr_params)
        print("✓ تم إضافة مراسلة تجريبية")
        
        return True
        
    except Exception as e:
        print(f"✗ خطأ في إضافة البيانات التجريبية: {e}")
        return False

def show_sample_data():
    """عرض البيانات التجريبية"""
    print("\n" + "=" * 50)
    print("البيانات المحفوظة في النظام")
    print("=" * 50)
    
    try:
        from database import db
        
        # عرض العملاء
        print("\nالعملاء:")
        customers = db.execute_query("SELECT subscriber_number, name, phone FROM customers")
        for customer in customers:
            print(f"  - {customer[0]}: {customer[1]} ({customer[2]})")
        
        # عرض المشاكل
        print("\nالمشاكل:")
        issues = db.execute_query("""
            SELECT i.title, i.status, c.name, ic.category_name 
            FROM issues i
            LEFT JOIN customers c ON i.customer_id = c.id
            LEFT JOIN issue_categories ic ON i.category_id = ic.id
        """)
        for issue in issues:
            print(f"  - {issue[0]} ({issue[1]}) - {issue[2]} - {issue[3]}")
        
        # عرض المراسلات
        print("\nالمراسلات:")
        correspondences = db.execute_query("""
            SELECT correspondence_number, sender, receiver, subject 
            FROM correspondences
        """)
        for corr in correspondences:
            print(f"  - {corr[0]}: {corr[3]} (من {corr[1]} إلى {corr[2]})")
        
        return True
        
    except Exception as e:
        print(f"✗ خطأ في عرض البيانات: {e}")
        return False

def main():
    """الدالة الرئيسية للاختبار"""
    print("نظام إدارة مشاكل العملاء - وضع الاختبار")
    print("Customer Issues Management System - Test Mode")
    
    # قائمة الاختبارات
    tests = [
        ("قاعدة البيانات", test_database),
        ("إدارة الملفات", test_file_manager),
        ("مولد التقارير", test_report_generator),
    ]
    
    results = {}
    
    # تشغيل الاختبارات
    for test_name, test_func in tests:
        results[test_name] = test_func()
    
    # إضافة البيانات التجريبية
    if results.get("قاعدة البيانات", False):
        add_sample_data()
        show_sample_data()
    
    # عرض النتائج النهائية
    print("\n" + "=" * 50)
    print("نتائج الاختبارات")
    print("=" * 50)
    
    passed = 0
    total = len(results)
    
    for test_name, passed_test in results.items():
        status = "✓ نجح" if passed_test else "✗ فشل"
        print(f"{test_name}: {status}")
        if passed_test:
            passed += 1
    
    print(f"\nالنتيجة النهائية: {passed}/{total} اختبارات نجحت")
    
    if passed == total:
        print("\n🎉 جميع الاختبارات نجحت! النظام جاهز للاستخدام")
        print("\nلتشغيل التطبيق الكامل (إذا كان tkinter متوفراً):")
        print("python main.py")
    else:
        print("\n⚠️  بعض الاختبارات فشلت. تحقق من المتطلبات")
        print("pip install -r requirements.txt")
    
    return passed == total

if __name__ == "__main__":
    main()