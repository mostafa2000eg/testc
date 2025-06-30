#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ملف إعداد تجميع نظام إدارة مشاكل العملاء
Setup file for Customer Issues Management System
"""

from setuptools import setup, find_packages
import os

# قراءة محتويات README
def read_file(filename):
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            return f.read()
    except:
        return ""

# معلومات المشروع
PACKAGE_NAME = "customer_issues_system"
VERSION = "2.0.0"
DESCRIPTION = "نظام إدارة مشاكل العملاء - النسخة المحسنة"
LONG_DESCRIPTION = read_file("README_Enhanced.md")

# الملفات المطلوبة
REQUIRED_FILES = [
    "enhanced_main.py",
    "enhanced_database.py", 
    "enhanced_main_window.py",
    "enhanced_functions.py",
    "enhanced_file_manager.py",
    "test_enhanced_system.py",
    "enhanced_requirements.txt",
    "دليل_النظام_المحسن.md",
    "ملخص_النظام_المحسن.md",
    "README_Enhanced.md"
]

# إعداد المشروع
setup(
    name=PACKAGE_NAME,
    version=VERSION,
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    
    # معلومات المطور
    author="AI Assistant",
    author_email="ai.assistant@example.com",
    
    # معلومات المشروع
    url="https://github.com/example/customer-issues-system",
    project_urls={
        "Documentation": "https://github.com/example/customer-issues-system/docs",
        "Source": "https://github.com/example/customer-issues-system",
        "Tracker": "https://github.com/example/customer-issues-system/issues",
    },
    
    # التصنيفات
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: End Users/Desktop",
        "Topic :: Office/Business :: Financial :: Accounting",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: MacOS",
        "Operating System :: POSIX :: Linux",
        "Natural Language :: Arabic",
    ],
    
    # الكلمات المفتاحية
    keywords="customer management, issues tracking, gas company, database, tkinter",
    
    # المتطلبات
    python_requires=">=3.7",
    install_requires=[
        # لا توجد متطلبات إضافية - كلها مدمجة مع Python
    ],
    
    # المتطلبات الاختيارية
    extras_require={
        "full": [
            "reportlab>=3.6.0",
            "Pillow>=8.0.0",
            "python-dateutil>=2.8.0",
            "openpyxl>=3.0.0",
        ],
        "windows": [
            "pywin32>=301; sys_platform=='win32'",
        ],
        "dev": [
            "pytest>=6.0",
            "black>=21.0",
            "flake8>=3.9",
        ],
    },
    
    # الحزم
    packages=find_packages(),
    py_modules=[
        "enhanced_main",
        "enhanced_database", 
        "enhanced_main_window",
        "enhanced_functions",
        "enhanced_file_manager",
        "test_enhanced_system"
    ],
    
    # ملفات البيانات
    package_data={
        "": [
            "*.md",
            "*.txt",
            "*.bat",
            "*.sh",
            "*.ico",
        ],
    },
    include_package_data=True,
    
    # نقطة الدخول
    entry_points={
        "console_scripts": [
            "customer-issues=enhanced_main:main",
            "customer-issues-test=test_enhanced_system:main",
        ],
        "gui_scripts": [
            "customer-issues-gui=enhanced_main:main",
        ],
    },
    
    # إعدادات ZIP
    zip_safe=False,
)