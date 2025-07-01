#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Pre-Release Quality Check Script
سكريبت فحص الجودة قبل الإصدار

This script performs comprehensive checks before releasing the Customer Issues Management System.
يقوم هذا السكريبت بفحوصات شاملة قبل إصدار نظام إدارة مشاكل العملاء.
"""

import os
import sys
import subprocess
import ast
import re
from pathlib import Path
from typing import List, Dict, Tuple

class PreReleaseChecker:
    """فاحص ما قبل الإصدار"""
    
    def __init__(self):
        self.project_root = Path.cwd()
        self.errors = []
        self.warnings = []
        self.info = []
        
        # الملفات المطلوبة
        self.required_files = [
            'customer_issues_main.py',
            'customer_issues_database.py',
            'customer_issues_window.py',
            'customer_issues_functions.py',
            'customer_issues_file_manager.py',
            'test_customer_issues.py',
            'README.md',
            'LICENSE.txt',
            'requirements.txt',
            'CHANGELOG.md',
            'setup.py',
            '.github/workflows/release.yml'
        ]
        
        # الإصدار المتوقع
        self.expected_version = "2.0.0"
    
    def log_error(self, message: str):
        """تسجيل خطأ"""
        self.errors.append(f"❌ ERROR: {message}")
        print(f"❌ ERROR: {message}")
    
    def log_warning(self, message: str):
        """تسجيل تحذير"""
        self.warnings.append(f"⚠️ WARNING: {message}")
        print(f"⚠️ WARNING: {message}")
    
    def log_info(self, message: str):
        """تسجيل معلومة"""
        self.info.append(f"ℹ️ INFO: {message}")
        print(f"ℹ️ INFO: {message}")
    
    def log_success(self, message: str):
        """تسجيل نجاح"""
        print(f"✅ SUCCESS: {message}")
    
    def check_required_files(self) -> bool:
        """فحص الملفات المطلوبة"""
        print("\n📁 Checking required files...")
        all_present = True
        
        for file_path in self.required_files:
            if os.path.exists(file_path):
                self.log_success(f"Found: {file_path}")
            else:
                self.log_error(f"Missing required file: {file_path}")
                all_present = False
        
        return all_present
    
    def check_python_syntax(self) -> bool:
        """فحص صحة بناء جملة Python"""
        print("\n🐍 Checking Python syntax...")
        all_valid = True
        
        python_files = [f for f in self.required_files if f.endswith('.py')]
        
        for file_path in python_files:
            if os.path.exists(file_path):
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    # فحص صحة البناء
                    ast.parse(content)
                    self.log_success(f"Valid syntax: {file_path}")
                    
                except SyntaxError as e:
                    self.log_error(f"Syntax error in {file_path}: {e}")
                    all_valid = False
                except Exception as e:
                    self.log_error(f"Error reading {file_path}: {e}")
                    all_valid = False
        
        return all_valid
    
    def check_imports(self) -> bool:
        """فحص الاستيرادات"""
        print("\n📦 Checking imports...")
        all_valid = True
        
        python_files = [f for f in self.required_files if f.endswith('.py')]
        
        for file_path in python_files:
            if os.path.exists(file_path):
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    # البحث عن الاستيرادات
                    import_lines = re.findall(r'^(?:from|import)\s+([^\s#]+)', content, re.MULTILINE)
                    
                    for import_name in import_lines:
                        # تنظيف اسم الاستيراد
                        import_name = import_name.split('.')[0]
                        
                        # فحص الاستيرادات المحلية
                        if import_name.startswith('customer_issues_'):
                            expected_file = f"{import_name}.py"
                            if not os.path.exists(expected_file):
                                self.log_error(f"Missing imported file: {expected_file} (imported in {file_path})")
                                all_valid = False
                    
                    self.log_success(f"Imports checked: {file_path}")
                    
                except Exception as e:
                    self.log_error(f"Error checking imports in {file_path}: {e}")
                    all_valid = False
        
        return all_valid
    
    def check_version_consistency(self) -> bool:
        """فحص تطابق الإصدارات"""
        print("\n🔢 Checking version consistency...")
        version_files = {
            'customer_issues_main.py': r'VERSION\s*=\s*[\'"]([^\'"]+)[\'"]',
            'setup.py': r'[\'"]version[\'"]\s*:\s*[\'"]([^\'"]+)[\'"]',
            'README.md': r'version-([^-]+)-blue',
            'CHANGELOG.md': r'##\s*\[([^\]]+)\]'
        }
        
        found_versions = {}
        
        for file_path, pattern in version_files.items():
            if os.path.exists(file_path):
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    matches = re.findall(pattern, content)
                    if matches:
                        version = matches[0]
                        found_versions[file_path] = version
                        self.log_info(f"Version in {file_path}: {version}")
                    else:
                        self.log_warning(f"No version found in {file_path}")
                        
                except Exception as e:
                    self.log_error(f"Error reading {file_path}: {e}")
        
        # فحص تطابق الإصدارات
        all_consistent = True
        for file_path, version in found_versions.items():
            if version != self.expected_version:
                self.log_error(f"Version mismatch in {file_path}: expected {self.expected_version}, found {version}")
                all_consistent = False
        
        if all_consistent and found_versions:
            self.log_success(f"All versions consistent: {self.expected_version}")
        
        return all_consistent
    
    def check_documentation(self) -> bool:
        """فحص الوثائق"""
        print("\n📚 Checking documentation...")
        all_good = True
        
        # فحص README.md
        if os.path.exists('README.md'):
            with open('README.md', 'r', encoding='utf-8') as f:
                readme_content = f.read()
            
            required_sections = [
                'Features', 'Installation', 'Usage', 'Requirements'
            ]
            
            for section in required_sections:
                if section.lower() not in readme_content.lower():
                    self.log_warning(f"Missing section in README.md: {section}")
                    all_good = False
            
            if len(readme_content) < 1000:
                self.log_warning("README.md seems too short (less than 1000 characters)")
                all_good = False
            else:
                self.log_success("README.md looks comprehensive")
        
        # فحص CHANGELOG.md
        if os.path.exists('CHANGELOG.md'):
            with open('CHANGELOG.md', 'r', encoding='utf-8') as f:
                changelog_content = f.read()
            
            if self.expected_version not in changelog_content:
                self.log_error(f"CHANGELOG.md doesn't contain version {self.expected_version}")
                all_good = False
            else:
                self.log_success(f"CHANGELOG.md contains version {self.expected_version}")
        
        return all_good
    
    def check_test_coverage(self) -> bool:
        """فحص تغطية الاختبارات"""
        print("\n🧪 Checking test coverage...")
        
        if not os.path.exists('test_customer_issues.py'):
            self.log_error("Test file missing: test_customer_issues.py")
            return False
        
        try:
            with open('test_customer_issues.py', 'r', encoding='utf-8') as f:
                test_content = f.read()
            
            # عد وظائف الاختبار
            test_functions = re.findall(r'def\s+(test_\w+)', test_content)
            test_count = len(test_functions)
            
            if test_count < 5:
                self.log_warning(f"Only {test_count} test functions found. Consider adding more tests.")
            else:
                self.log_success(f"Found {test_count} test functions")
            
            # فحص الاختبارات المهمة
            important_tests = [
                'test_database', 'test_window', 'test_functions'
            ]
            
            for test_type in important_tests:
                if any(test_type in func for func in test_functions):
                    self.log_success(f"Found {test_type} tests")
                else:
                    self.log_warning(f"Missing {test_type} tests")
            
            return True
            
        except Exception as e:
            self.log_error(f"Error reading test file: {e}")
            return False
    
    def check_github_workflow(self) -> bool:
        """فحص GitHub workflow"""
        print("\n⚙️ Checking GitHub workflow...")
        
        workflow_path = '.github/workflows/release.yml'
        if not os.path.exists(workflow_path):
            self.log_error(f"Missing GitHub workflow: {workflow_path}")
            return False
        
        try:
            with open(workflow_path, 'r', encoding='utf-8') as f:
                workflow_content = f.read()
            
            # فحص المكونات المهمة
            required_components = [
                'customer_issues_main.py', 'build-windows', 'build-linux', 
                'create-release', 'PyInstaller'
            ]
            
            all_present = True
            for component in required_components:
                if component in workflow_content:
                    self.log_success(f"Workflow contains: {component}")
                else:
                    self.log_warning(f"Workflow missing: {component}")
                    all_present = False
            
            return all_present
            
        except Exception as e:
            self.log_error(f"Error reading workflow file: {e}")
            return False
    
    def check_file_encoding(self) -> bool:
        """فحص ترميز الملفات"""
        print("\n🔤 Checking file encoding...")
        all_good = True
        
        text_files = [f for f in self.required_files if f.endswith(('.py', '.md', '.txt', '.yml'))]
        
        for file_path in text_files:
            if os.path.exists(file_path):
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    # فحص وجود نص عربي
                    has_arabic = bool(re.search(r'[\u0600-\u06FF]', content))
                    if has_arabic:
                        self.log_success(f"UTF-8 encoding with Arabic text: {file_path}")
                    else:
                        self.log_info(f"UTF-8 encoding (no Arabic): {file_path}")
                        
                except UnicodeDecodeError:
                    self.log_error(f"File not UTF-8 encoded: {file_path}")
                    all_good = False
                except Exception as e:
                    self.log_error(f"Error reading {file_path}: {e}")
                    all_good = False
        
        return all_good
    
    def run_tests(self) -> bool:
        """تشغيل الاختبارات"""
        print("\n🏃 Running tests...")
        
        if not os.path.exists('test_customer_issues.py'):
            self.log_error("Cannot run tests: test file missing")
            return False
        
        try:
            # تشغيل الاختبارات
            result = subprocess.run([
                sys.executable, 'test_customer_issues.py'
            ], capture_output=True, text=True, timeout=60)
            
            if result.returncode == 0:
                self.log_success("All tests passed!")
                return True
            else:
                self.log_error(f"Tests failed with exit code {result.returncode}")
                if result.stderr:
                    self.log_error(f"Test errors: {result.stderr}")
                return False
                
        except subprocess.TimeoutExpired:
            self.log_error("Tests timed out after 60 seconds")
            return False
        except Exception as e:
            self.log_error(f"Error running tests: {e}")
            return False
    
    def generate_report(self) -> Dict:
        """إنشاء تقرير شامل"""
        print("\n📊 Generating report...")
        
        total_checks = 8  # عدد الفحوصات الرئيسية
        passed_checks = 0
        
        # تشغيل جميع الفحوصات
        checks = [
            ("Required Files", self.check_required_files()),
            ("Python Syntax", self.check_python_syntax()),
            ("Imports", self.check_imports()),
            ("Version Consistency", self.check_version_consistency()),
            ("Documentation", self.check_documentation()),
            ("Test Coverage", self.check_test_coverage()),
            ("GitHub Workflow", self.check_github_workflow()),
            ("File Encoding", self.check_file_encoding())
        ]
        
        # تشغيل الاختبارات (اختياري)
        if '--skip-tests' not in sys.argv:
            test_result = self.run_tests()
            checks.append(("Tests Execution", test_result))
            total_checks += 1
        
        # حساب النتائج
        for check_name, result in checks:
            if result:
                passed_checks += 1
        
        # إنشاء التقرير
        report = {
            'total_checks': total_checks,
            'passed_checks': passed_checks,
            'success_rate': (passed_checks / total_checks) * 100,
            'errors': self.errors,
            'warnings': self.warnings,
            'info': self.info,
            'checks': checks
        }
        
        return report
    
    def print_summary(self, report: Dict):
        """طباعة ملخص التقرير"""
        print("\n" + "="*60)
        print("🏁 PRE-RELEASE CHECK SUMMARY | ملخص فحص ما قبل الإصدار")
        print("="*60)
        
        print(f"\n📊 Overall Results:")
        print(f"   ✅ Passed: {report['passed_checks']}/{report['total_checks']} checks")
        print(f"   📈 Success Rate: {report['success_rate']:.1f}%")
        
        if report['errors']:
            print(f"\n❌ Errors ({len(report['errors'])}):")
            for error in report['errors']:
                print(f"   {error}")
        
        if report['warnings']:
            print(f"\n⚠️ Warnings ({len(report['warnings'])}):")
            for warning in report['warnings']:
                print(f"   {warning}")
        
        print(f"\n📋 Check Details:")
        for check_name, result in report['checks']:
            status = "✅ PASS" if result else "❌ FAIL"
            print(f"   {status} - {check_name}")
        
        print("\n" + "="*60)
        
        # تقييم الجاهزية للإصدار
        if report['success_rate'] >= 90 and not report['errors']:
            print("🎉 READY FOR RELEASE! | جاهز للإصدار!")
            print("   All critical checks passed. You can proceed with the release.")
            return True
        elif report['success_rate'] >= 80:
            print("⚠️ MOSTLY READY | جاهز تقريباً")
            print("   Most checks passed, but review warnings before releasing.")
            return False
        else:
            print("❌ NOT READY FOR RELEASE | غير جاهز للإصدار")
            print("   Critical issues found. Fix errors before releasing.")
            return False

def main():
    """الوظيفة الرئيسية"""
    print("🔍 Customer Issues Management System - Pre-Release Checker")
    print("   فاحص ما قبل الإصدار - نظام إدارة مشاكل العملاء")
    print("   Version 2.0.0")
    print()
    
    checker = PreReleaseChecker()
    report = checker.generate_report()
    ready = checker.print_summary(report)
    
         # حفظ التقرير
     try:
         import json
         from datetime import datetime
         report_file = f"pre_release_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        print(f"\n📄 Report saved to: {report_file}")
    except Exception as e:
        print(f"\n⚠️ Could not save report: {e}")
    
    # كود الخروج
    if ready:
        print("\n🚀 You can now proceed with creating the GitHub release!")
        sys.exit(0)
    else:
        print("\n🛠️ Please fix the issues above before releasing.")
        sys.exit(1)

if __name__ == "__main__":
    main()