#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Customer Issues Management System - Setup Script
سكريبت إعداد نظام إدارة مشاكل العملاء

This script sets up the Customer Issues Management System for distribution.
يقوم هذا السكريبت بإعداد نظام إدارة مشاكل العملاء للتوزيع.
"""

from setuptools import setup, find_packages
import os
import sys

# Read README
def read_readme():
    """قراءة ملف README"""
    if os.path.exists('README.md'):
        with open('README.md', 'r', encoding='utf-8') as f:
            return f.read()
    return "Customer Issues Management System - نظام إدارة مشاكل العملاء"

# Read requirements
def read_requirements():
    """قراءة ملف requirements"""
    try:
        with open('requirements.txt', 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        # Filter out comments and empty lines
        requirements = []
        for line in lines:
            line = line.strip()
            if line and not line.startswith('#'):
                requirements.append(line)
        
        return requirements
    except FileNotFoundError:
        return []

# Package information
PACKAGE_INFO = {
    'name': 'customer-issues-management',
    'version': '2.0.0',
    'description': 'Customer Issues Management System for Gas Companies / نظام إدارة مشاكل العملاء لشركات الغاز',
    'long_description': read_readme(),
    'long_description_content_type': 'text/markdown',
    'author': 'AI Assistant',
    'author_email': 'ai.assistant@example.com',
    'url': 'https://github.com/yourusername/customer-issues-management',
    'license': 'MIT',
    'classifiers': [
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Topic :: Office/Business',
        'Topic :: Database :: Front-Ends',
        'Natural Language :: Arabic',
        'Natural Language :: English',
    ],
    'keywords': 'customer management, issues tracking, gas company, database, GUI, Arabic',
    'python_requires': '>=3.7',
    'install_requires': read_requirements(),
    'entry_points': {
        'console_scripts': [
            'customer-issues=customer_issues_main:main',
        ],
        'gui_scripts': [
            'customer-issues-gui=customer_issues_main:main',
        ],
    },
    'include_package_data': True,
    'zip_safe': False,
}

# Package data
PACKAGE_DATA = {
    '': [
        '*.md',
        '*.txt',
        '*.rst',
        '*.yml',
        '*.yaml',
        '*.json',
        '*.cfg',
        '*.ini',
        'LICENSE*',
        'README*',
        'CHANGELOG*',
        'requirements*.txt',
    ]
}

# Data files (installed outside the package)
DATA_FILES = [
    ('share/customer-issues-management/docs', [
        'README.md',
        'LICENSE.txt',
    ]),
    ('share/customer-issues-management/scripts', [
        'run_system.sh',
        'run_system.bat',
        'test_system.bat',
    ]),
]

def check_python_version():
    """فحص إصدار Python"""
    if sys.version_info < (3, 7):
        print("❌ Error: Python 3.7 or higher is required")
        print("❌ خطأ: يتطلب Python 3.7 أو أحدث")
        print(f"Current version: {sys.version}")
        sys.exit(1)
    else:
        print(f"✅ Python version check passed: {sys.version}")

def main():
    """الوظيفة الرئيسية للإعداد"""
    print("=" * 60)
    print("🏗️ Customer Issues Management System - Setup")
    print("   إعداد نظام إدارة مشاكل العملاء")
    print("=" * 60)
    
    # فحص إصدار Python
    check_python_version()
    
    # إنشاء المجلدات المطلوبة
    dirs_to_create = ['files', 'reports', 'backups', 'logs']
    for dir_name in dirs_to_create:
        if not os.path.exists(dir_name):
            os.makedirs(dir_name, exist_ok=True)
            print(f"📁 Created directory: {dir_name}")
    
    # تشغيل setup
    try:
        setup(
            packages=find_packages(),
            package_data=PACKAGE_DATA,
            data_files=DATA_FILES,
            **PACKAGE_INFO
        )
        
        print("\n✅ Setup completed successfully!")
        print("✅ اكتمل الإعداد بنجاح!")
        
    except Exception as e:
        print(f"\n❌ Setup failed: {e}")
        print(f"❌ فشل الإعداد: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()