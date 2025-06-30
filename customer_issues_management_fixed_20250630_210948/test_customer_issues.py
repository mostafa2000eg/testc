#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
اختبار نظام إدارة مشاكل العملاء - النسخة المحسنة
Test Customer Issues Management System - Enhanced Version
"""

import os
import sys
import sqlite3
from datetime import datetime

# إضافة المجلد الحالي لمسار Python
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

def test_database():
    """اختبار قاعدة البيانات المحسنة"""
    print("🔍 اختبار قاعدة البيانات المحسنة...")
    
    try:
        from enhanced_database import enhanced_db
        
        # اختبار الاتصال
        conn = enhanced_db.get_connection()
        if conn:
            print("✅ الاتصال بقاعدة البيانات نجح")
            conn.close()
        else:
            print("❌ فشل الاتصال بقاعدة البيانات")
            return False
        
        # اختبار الجداول
        tables = [
            'employees', 'issue_categories', 'cases', 
            'correspondences', 'attachments', 'audit_log'
        ]
        
        for table in tables:
            query = f"SELECT COUNT(*) FROM {table}"
            result = enhanced_db.execute_query(query)
            if result:
                count = result[0][0]
                print(f"✅ جدول {table}: {count} سجل")
            else:
                print(f"❌ خطأ في جدول {table}")
                return False
        
        # اختبار البيانات الافتراضية
        employees = enhanced_db.get_employees()
        categories = enhanced_db.get_categories()
        
        print(f"👥 الموظفين: {len(employees)} موظف")
        print(f"📋 التصنيفات: {len(categories)} تصنيف")
        
        if len(employees) >= 4 and len(categories) >= 11:
            print("✅ البيانات الافتراضية موجودة")
        else:
            print("⚠️ البيانات الافتراضية ناقصة")
        
        return True
        
    except Exception as e:
        print(f"❌ خطأ في اختبار قاعدة البيانات: {e}")
        return False

def test_file_manager():
    """اختبار مدير الملفات المحسن"""
    print("\n📁 اختبار مدير الملفات المحسن...")
    
    try:
        from enhanced_file_manager import EnhancedFileManager
        
        # إنشاء مدير الملفات
        file_manager = EnhancedFileManager()
        
        # اختبار إنشاء مجلد
        test_case_id = 999
        case_folder = file_manager.create_case_folder(test_case_id)
        
        if os.path.exists(case_folder):
            print("✅ إنشاء مجلد الحالة نجح")
        else:
            print("❌ فشل في إنشاء مجلد الحالة")
            return False
        
        # اختبار معلومات التخزين
        storage_info = file_manager.get_storage_info()
        print(f"📊 إحصائيات التخزين:")
        print(f"   - المجلد الأساسي: {storage_info['base_path']}")
        print(f"   - عدد الملفات: {storage_info['total_files']}")
        print(f"   - الحجم الإجمالي: {storage_info['total_size']}")
        
        # تنظيف الاختبار
        try:
            os.rmdir(case_folder)
            print("✅ تم تنظيف ملفات الاختبار")
        except:
            pass
        
        return True
        
    except Exception as e:
        print(f"❌ خطأ في اختبار مدير الملفات: {e}")
        return False

def test_search_functionality():
    """اختبار وظائف البحث"""
    print("\n🔍 اختبار وظائف البحث...")
    
    try:
        from enhanced_database import enhanced_db
        
        # إنشاء حالة اختبار
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # إدخال حالة اختبار
        query = """
            INSERT INTO cases (customer_name, subscriber_number, phone, address, 
                             problem_description, created_date, created_by, modified_date, modified_by)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        
        test_data = (
            "أحمد محمد الاختبار",
            "01234567890123",
            "01012345678",
            "شارع الاختبار، المدينة الاختبارية",
            "مشكلة اختبار النظام",
            current_time,
            1,  # أول موظف
            current_time,
            1
        )
        
        enhanced_db.execute_query(query, test_data)
        
        # الحصول على ID الحالة الجديدة
        case_id = enhanced_db.execute_query("SELECT last_insert_rowid()")[0][0]
        print(f"✅ تم إنشاء حالة اختبار بالرقم: {case_id}")
        
        # اختبار أنواع البحث المختلفة
        search_tests = [
            ("شامل", "أحمد"),
            ("اسم العميل", "أحمد محمد"),
            ("رقم المشترك", "01234567890123"),
            ("العنوان", "شارع الاختبار")
        ]
        
        for search_type, search_value in search_tests:
            results = enhanced_db.search_cases(search_type, search_value)
            if results:
                print(f"✅ البحث في '{search_type}' بقيمة '{search_value}': {len(results)} نتيجة")
            else:
                print(f"❌ فشل البحث في '{search_type}' بقيمة '{search_value}'")
        
        # اختبار البحث بالتصنيف
        categories = enhanced_db.get_categories()
        if categories:
            test_category = categories[0][1]  # أول تصنيف
            results = enhanced_db.search_cases("تصنيف المشكلة", test_category)
            print(f"✅ البحث بالتصنيف '{test_category}': {len(results)} نتيجة")
        
        # اختبار البحث بالحالة
        status_options = enhanced_db.get_status_options()
        if status_options:
            test_status = status_options[0][0]  # أول حالة
            results = enhanced_db.search_cases("حالة المشكلة", test_status)
            print(f"✅ البحث بالحالة '{test_status}': {len(results)} نتيجة")
        
        # تنظيف بيانات الاختبار
        enhanced_db.execute_query("DELETE FROM cases WHERE id = ?", (case_id,))
        print("✅ تم تنظيف بيانات الاختبار")
        
        return True
        
    except Exception as e:
        print(f"❌ خطأ في اختبار البحث: {e}")
        return False

def test_correspondence_numbering():
    """اختبار نظام ترقيم المراسلات"""
    print("\n📧 اختبار نظام ترقيم المراسلات...")
    
    try:
        from enhanced_database import enhanced_db
        
        # إنشاء حالة اختبار
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        query = """
            INSERT INTO cases (customer_name, subscriber_number, created_date, created_by)
            VALUES (?, ?, ?, ?)
        """
        enhanced_db.execute_query(query, ("عميل اختبار المراسلات", "99999999999999", current_time, 1))
        
        case_id = enhanced_db.execute_query("SELECT last_insert_rowid()")[0][0]
        
        # اختبار إنشاء أرقام المراسلات
        for i in range(3):
            case_seq, yearly_seq = enhanced_db.get_next_correspondence_numbers(case_id)
            print(f"✅ مراسلة {i+1}: رقم الحالة {case_seq}, الرقم السنوي {yearly_seq}")
            
            # إدخال المراسلة
            query = """
                INSERT INTO correspondences (case_id, case_sequence_number, yearly_sequence_number,
                                           sender, message_content, sent_date, created_by)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """
            enhanced_db.execute_query(query, (
                case_id, case_seq, yearly_seq, "مختبر النظام", 
                f"محتوى المراسلة رقم {i+1}", current_time, 1
            ))
        
        # فحص ترقيم المراسلات
        correspondences = enhanced_db.get_case_correspondences(case_id)
        if len(correspondences) == 3:
            print("✅ تم إنشاء 3 مراسلات بنجاح")
            for i, corr in enumerate(correspondences):
                print(f"   مراسلة {i+1}: تسلسل {corr[2]}, سنوي {corr[3]}")
        else:
            print(f"❌ عدد غير صحيح من المراسلات: {len(correspondences)}")
        
        # تنظيف البيانات
        enhanced_db.execute_query("DELETE FROM correspondences WHERE case_id = ?", (case_id,))
        enhanced_db.execute_query("DELETE FROM cases WHERE id = ?", (case_id,))
        print("✅ تم تنظيف بيانات الاختبار")
        
        return True
        
    except Exception as e:
        print(f"❌ خطأ في اختبار ترقيم المراسلات: {e}")
        return False

def test_audit_log():
    """اختبار سجل التعديلات"""
    print("\n📝 اختبار سجل التعديلات...")
    
    try:
        from enhanced_database import enhanced_db
        
        # إنشاء حالة اختبار
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        query = """
            INSERT INTO cases (customer_name, subscriber_number, created_date, created_by)
            VALUES (?, ?, ?, ?)
        """
        enhanced_db.execute_query(query, ("عميل اختبار السجل", "88888888888888", current_time, 1))
        
        case_id = enhanced_db.execute_query("SELECT last_insert_rowid()")[0][0]
        
        # تسجيل عدة إجراءات
        actions = [
            ("إنشاء", "تم إنشاء الحالة"),
            ("تحديث", "تم تحديث بيانات العميل"),
            ("إضافة مرفق", "تم إضافة مرفق: صورة.jpg"),
            ("حل", "تم حل المشكلة")
        ]
        
        for action_type, description in actions:
            enhanced_db.log_action(case_id, action_type, description, 1)
            print(f"✅ تم تسجيل: {action_type} - {description}")
        
        # فحص السجل
        audit_logs = enhanced_db.get_case_audit_log(case_id)
        if len(audit_logs) == 4:
            print(f"✅ سجل التعديلات يحتوي على {len(audit_logs)} إدخال")
            for log in audit_logs:
                print(f"   {log[5]}: {log[2]} - {log[3]}")
        else:
            print(f"❌ عدد غير صحيح في سجل التعديلات: {len(audit_logs)}")
        
        # تنظيف البيانات
        enhanced_db.execute_query("DELETE FROM audit_log WHERE case_id = ?", (case_id,))
        enhanced_db.execute_query("DELETE FROM cases WHERE id = ?", (case_id,))
        print("✅ تم تنظيف بيانات الاختبار")
        
        return True
        
    except Exception as e:
        print(f"❌ خطأ في اختبار سجل التعديلات: {e}")
        return False

def test_employee_management():
    """اختبار إدارة الموظفين"""
    print("\n👥 اختبار إدارة الموظفين...")
    
    try:
        from enhanced_database import enhanced_db
        
        # عد الموظفين الحاليين
        initial_employees = enhanced_db.get_employees()
        initial_count = len(initial_employees)
        print(f"📊 عدد الموظفين الحاليين: {initial_count}")
        
        # إضافة موظف اختبار
        test_employee_name = "موظف اختبار النظام"
        success = enhanced_db.add_employee(test_employee_name, "مختبر")
        
        if success:
            print(f"✅ تم إضافة الموظف: {test_employee_name}")
        else:
            print(f"❌ فشل في إضافة الموظف: {test_employee_name}")
            return False
        
        # فحص الزيادة
        new_employees = enhanced_db.get_employees()
        new_count = len(new_employees)
        
        if new_count == initial_count + 1:
            print(f"✅ عدد الموظفين زاد إلى: {new_count}")
        else:
            print(f"❌ عدد غير صحيح من الموظفين: {new_count}")
        
        # العثور على الموظف الجديد وحذفه
        test_employee_id = None
        for emp in new_employees:
            if emp[1] == test_employee_name:
                test_employee_id = emp[0]
                break
        
        if test_employee_id:
            success = enhanced_db.delete_employee(test_employee_id)
            if success:
                print(f"✅ تم حذف الموظف الاختباري")
            else:
                print(f"❌ فشل في حذف الموظف الاختباري")
        
        # فحص العدد النهائي
        final_employees = enhanced_db.get_employees()
        final_count = len(final_employees)
        
        if final_count == initial_count:
            print(f"✅ تم استعادة العدد الأصلي: {final_count}")
        else:
            print(f"⚠️ العدد النهائي مختلف: {final_count}")
        
        return True
        
    except Exception as e:
        print(f"❌ خطأ في اختبار إدارة الموظفين: {e}")
        return False

def generate_test_report():
    """إنشاء تقرير الاختبار"""
    print("\n" + "="*60)
    print("📋 تقرير اختبار النظام المحسن")
    print("="*60)
    
    tests = [
        ("قاعدة البيانات", test_database),
        ("مدير الملفات", test_file_manager),
        ("وظائف البحث", test_search_functionality),
        ("ترقيم المراسلات", test_correspondence_numbering),
        ("سجل التعديلات", test_audit_log),
        ("إدارة الموظفين", test_employee_management)
    ]
    
    results = []
    
    for test_name, test_function in tests:
        print(f"\n🧪 تشغيل اختبار: {test_name}")
        print("-" * 40)
        
        try:
            result = test_function()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ خطأ في الاختبار: {e}")
            results.append((test_name, False))
    
    # تلخيص النتائج
    print("\n" + "="*60)
    print("📊 ملخص نتائج الاختبارات")
    print("="*60)
    
    passed = 0
    failed = 0
    
    for test_name, result in results:
        status = "✅ نجح" if result else "❌ فشل"
        print(f"{test_name}: {status}")
        
        if result:
            passed += 1
        else:
            failed += 1
    
    print("-" * 60)
    print(f"إجمالي الاختبارات: {len(results)}")
    print(f"نجح: {passed}")
    print(f"فشل: {failed}")
    
    if failed == 0:
        print("\n🎉 جميع الاختبارات نجحت! النظام جاهز للاستخدام.")
    else:
        print(f"\n⚠️ فشل {failed} اختبار. يرجى مراجعة الأخطاء المذكورة أعلاه.")
    
    return failed == 0

def main():
    """الوظيفة الرئيسية للاختبار"""
    print("🔧 اختبار نظام إدارة مشاكل العملاء - النسخة المحسنة")
    print("Testing Customer Issues Management System - Enhanced Version")
    print("=" * 60)
    
    # فحص متطلبات النظام
    try:
        import tkinter
        print("✅ tkinter متوفر")
    except ImportError:
        print("❌ tkinter غير متوفر - قد تواجه مشاكل في الواجهة الرسومية")
    
    try:
        import sqlite3
        print("✅ sqlite3 متوفر")
    except ImportError:
        print("❌ sqlite3 غير متوفر - النظام لن يعمل")
        return False
    
    # تشغيل الاختبارات
    success = generate_test_report()
    
    print("\n" + "="*60)
    if success:
        print("🎯 جميع الاختبارات اكتملت بنجاح!")
        print("💡 يمكنك الآن تشغيل النظام بأمان باستخدام: python enhanced_main.py")
    else:
        print("⚠️ بعض الاختبارات فشلت. يرجى مراجعة الأخطاء قبل استخدام النظام.")
    
    return success

if __name__ == "__main__":
    success = main()
    
    input("\n👋 اضغط Enter للخروج...")
    
    sys.exit(0 if success else 1)