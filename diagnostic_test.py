#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Customer Issues Management System - Diagnostic Test
فحص تشخيصي لنظام إدارة مشاكل العملاء

Version: 2.0.0
"""

import os
import sys
import importlib.util

def test_database_import():
    """فحص استيراد قاعدة البيانات"""
    print("🔍 فحص استيراد قاعدة البيانات...")
    
    try:
        from customer_issues_database import DatabaseManager
        print("  ✅ تم استيراد DatabaseManager بنجاح")
        
        # إنشاء مثيل للاختبار
        db = DatabaseManager("test_diagnostic.db")
        print("  ✅ تم إنشاء مثيل قاعدة البيانات بنجاح")
        
        # اختبار الدوال الأساسية
        categories = db.get_categories()
        print(f"  ✅ تم جلب التصنيفات: {len(categories)} تصنيف")
        
        employees = db.get_employees()
        print(f"  ✅ تم جلب الموظفين: {len(employees)} موظف")
        
        # تنظيف ملف الاختبار
        if os.path.exists("test_diagnostic.db"):
            os.remove("test_diagnostic.db")
        
        return True
        
    except ImportError as e:
        print(f"  ❌ خطأ في الاستيراد: {e}")
        return False
    except Exception as e:
        print(f"  ❌ خطأ في التشغيل: {e}")
        return False

def test_main_import():
    """فحص استيراد الملف الرئيسي"""
    print("\n🔍 فحص استيراد الملف الرئيسي...")
    
    try:
        spec = importlib.util.spec_from_file_location("customer_issues_main", "customer_issues_main.py")
        module = importlib.util.module_from_spec(spec)
        
        print("  ✅ تم تحميل الملف الرئيسي بنجاح")
        
        # فحص المتغيرات المطلوبة
        if hasattr(module, 'VERSION'):
            print(f"  ✅ الإصدار موجود: VERSION")
        else:
            print("  ⚠️ متغير VERSION غير موجود")
        
        return True
        
    except Exception as e:
        print(f"  ❌ خطأ في تحميل الملف الرئيسي: {e}")
        return False

def test_window_import():
    """فحص استيراد نافذة الواجهة"""
    print("\n🔍 فحص استيراد نافذة الواجهة...")
    
    try:
        from customer_issues_window import CustomerIssuesWindow
        print("  ✅ تم استيراد CustomerIssuesWindow بنجاح")
        return True
        
    except ImportError as e:
        print(f"  ❌ خطأ في الاستيراد: {e}")
        return False
    except Exception as e:
        print(f"  ❌ خطأ في التشغيل: {e}")
        return False

def test_functions_import():
    """فحص استيراد الوظائف الأساسية"""
    print("\n🔍 فحص استيراد الوظائف الأساسية...")
    
    try:
        from customer_issues_functions import CustomerIssuesFunctions
        print("  ✅ تم استيراد CustomerIssuesFunctions بنجاح")
        return True
        
    except ImportError as e:
        print(f"  ❌ خطأ في الاستيراد: {e}")
        return False
    except Exception as e:
        print(f"  ❌ خطأ في التشغيل: {e}")
        return False

def test_file_manager_import():
    """فحص استيراد مدير الملفات"""
    print("\n🔍 فحص استيراد مدير الملفات...")
    
    try:
        from customer_issues_file_manager import FileManager
        print("  ✅ تم استيراد FileManager بنجاح")
        return True
        
    except ImportError as e:
        print(f"  ❌ خطأ في الاستيراد: {e}")
        return False
    except Exception as e:
        print(f"  ❌ خطأ في التشغيل: {e}")
        return False

def test_file_syntax():
    """فحص صحة التركيب النحوي للملفات"""
    print("\n🔍 فحص صحة التركيب النحوي...")
    
    python_files = [
        'customer_issues_main.py',
        'customer_issues_database.py',
        'customer_issues_window.py',
        'customer_issues_functions.py',
        'customer_issues_file_manager.py',
        'test_customer_issues.py'
    ]
    
    syntax_errors = 0
    
    for file in python_files:
        if os.path.exists(file):
            try:
                with open(file, 'r', encoding='utf-8') as f:
                    code = f.read()
                compile(code, file, 'exec')
                print(f"  ✅ {file}")
            except SyntaxError as e:
                print(f"  ❌ {file}: خطأ نحوي في السطر {e.lineno}")
                syntax_errors += 1
            except Exception as e:
                print(f"  ⚠️ {file}: {e}")
        else:
            print(f"  ❌ {file}: الملف غير موجود")
            syntax_errors += 1
    
    return syntax_errors == 0

def main():
    """الوظيفة الرئيسية للفحص التشخيصي"""
    print("=" * 60)
    print("🔧 فحص تشخيصي شامل - نظام إدارة مشاكل العملاء")
    print("Customer Issues Management System - Diagnostic Test")
    print("=" * 60)
    
    tests = [
        ("فحص التركيب النحوي", test_file_syntax),
        ("فحص قاعدة البيانات", test_database_import),
        ("فحص الملف الرئيسي", test_main_import),
        ("فحص نافذة الواجهة", test_window_import),
        ("فحص الوظائف الأساسية", test_functions_import),
        ("فحص مدير الملفات", test_file_manager_import)
    ]
    
    passed_tests = 0
    total_tests = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n{'='*20} {test_name} {'='*20}")
        try:
            if test_func():
                passed_tests += 1
                print(f"✅ {test_name}: نجح")
            else:
                print(f"❌ {test_name}: فشل")
        except Exception as e:
            print(f"❌ {test_name}: خطأ غير متوقع - {e}")
    
    print("\n" + "="*60)
    print("📊 ملخص نتائج الفحص التشخيصي:")
    print(f"✅ الاختبارات الناجحة: {passed_tests}/{total_tests}")
    print(f"❌ الاختبارات الفاشلة: {total_tests - passed_tests}/{total_tests}")
    print(f"📈 معدل النجاح: {(passed_tests/total_tests)*100:.1f}%")
    
    if passed_tests == total_tests:
        print("\n🎉 جميع الاختبارات نجحت! النظام جاهز للاستخدام.")
        return 0
    else:
        print(f"\n⚠️ {total_tests - passed_tests} اختبار(ات) فشل. يرجى مراجعة المشاكل المذكورة أعلاه.")
        return 1

if __name__ == "__main__":
    sys.exit(main())