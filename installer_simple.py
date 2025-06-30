#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ملف تثبيت مبسط - نظام إدارة مشاكل العملاء
Simple Installer for Customer Issues Management System
"""

import os
import sys
import shutil
import tkinter as tk
from tkinter import messagebox, filedialog
from pathlib import Path

class SimpleInstaller:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("تثبيت نظام إدارة مشاكل العملاء")
        self.root.geometry("600x500")
        self.root.resizable(False, False)
        
        # متغيرات التثبيت
        self.install_path = tk.StringVar()
        self.install_path.set(os.path.join(os.path.expanduser("~"), "Desktop", "نظام_إدارة_مشاكل_العملاء"))
        
        self.create_ui()
        
    def create_ui(self):
        """إنشاء واجهة المستخدم"""
        # العنوان الرئيسي
        title_frame = tk.Frame(self.root, bg='#2c3e50', height=80)
        title_frame.pack(fill='x')
        title_frame.pack_propagate(False)
        
        title_label = tk.Label(
            title_frame,
            text="تثبيت نظام إدارة مشاكل العملاء",
            font=('Arial', 16, 'bold'),
            bg='#2c3e50',
            fg='white'
        )
        title_label.pack(expand=True)
        
        # المحتوى الرئيسي
        main_frame = tk.Frame(self.root, padx=30, pady=20)
        main_frame.pack(fill='both', expand=True)
        
        # معلومات البرنامج
        info_text = """
مرحباً بك في معالج تثبيت نظام إدارة مشاكل العملاء

هذا النظام يساعدك على:
• إدارة بيانات العملاء ومشاكلهم
• تتبع المراسلات مع شركة تاون جاس
• إنشاء التقارير والمرفقات
• البحث المتقدم في البيانات

الإصدار: 2.0.0 (النسخة المحسنة)
المطور: مساعد الذكي الاصطناعي
        """
        
        info_label = tk.Label(
            main_frame,
            text=info_text,
            font=('Arial', 10),
            justify='right',
            anchor='ne'
        )
        info_label.pack(fill='x', pady=(0, 20))
        
        # اختيار مجلد التثبيت
        path_frame = tk.Frame(main_frame)
        path_frame.pack(fill='x', pady=(0, 20))
        
        path_label = tk.Label(
            path_frame,
            text="مجلد التثبيت:",
            font=('Arial', 11, 'bold')
        )
        path_label.pack(anchor='e')
        
        path_entry_frame = tk.Frame(path_frame)
        path_entry_frame.pack(fill='x', pady=(5, 0))
        
        path_entry = tk.Entry(
            path_entry_frame,
            textvariable=self.install_path,
            font=('Arial', 10),
            state='readonly'
        )
        path_entry.pack(side='right', fill='x', expand=True, padx=(0, 10))
        
        browse_btn = tk.Button(
            path_entry_frame,
            text="استعراض...",
            command=self.browse_path,
            font=('Arial', 10),
            width=12
        )
        browse_btn.pack(side='right')
        
        # معلومات المتطلبات
        req_frame = tk.LabelFrame(main_frame, text="المتطلبات", font=('Arial', 10, 'bold'))
        req_frame.pack(fill='x', pady=(0, 20))
        
        req_text = """
✅ ويندوز 7 أو أحدث
✅ مساحة فارغة: 100 ميجابايت
✅ صلاحيات الكتابة في مجلد التثبيت
⚠️ Python 3.7+ (إذا لم يكن البرنامج مجمعاً)
        """
        
        req_label = tk.Label(
            req_frame,
            text=req_text,
            font=('Arial', 9),
            justify='right',
            anchor='ne'
        )
        req_label.pack(fill='x', padx=10, pady=10)
        
        # أزرار التحكم
        btn_frame = tk.Frame(main_frame)
        btn_frame.pack(fill='x', pady=(20, 0))
        
        self.install_btn = tk.Button(
            btn_frame,
            text="تثبيت",
            command=self.install,
            font=('Arial', 12, 'bold'),
            bg='#27ae60',
            fg='white',
            width=15,
            height=2
        )
        self.install_btn.pack(side='left')
        
        cancel_btn = tk.Button(
            btn_frame,
            text="إلغاء",
            command=self.root.quit,
            font=('Arial', 12),
            bg='#e74c3c',
            fg='white',
            width=15,
            height=2
        )
        cancel_btn.pack(side='right')
        
        # شريط التقدم (مخفي في البداية)
        self.progress_frame = tk.Frame(main_frame)
        self.progress_label = tk.Label(
            self.progress_frame,
            text="جاري التثبيت...",
            font=('Arial', 10)
        )
        self.progress_label.pack()
        
    def browse_path(self):
        """استعراض مجلد التثبيت"""
        path = filedialog.askdirectory(
            title="اختر مجلد التثبيت",
            initialdir=os.path.dirname(self.install_path.get())
        )
        if path:
            self.install_path.set(os.path.join(path, "نظام_إدارة_مشاكل_العملاء"))
    
    def install(self):
        """تنفيذ عملية التثبيت"""
        install_dir = self.install_path.get()
        
        # فحص المجلد
        if not install_dir or install_dir.strip() == "":
            messagebox.showerror("خطأ", "يرجى اختيار مجلد التثبيت")
            return
        
        # تأكيد التثبيت
        if os.path.exists(install_dir):
            result = messagebox.askyesno(
                "تأكيد",
                f"المجلد موجود بالفعل:\n{install_dir}\n\nهل تريد المتابعة؟"
            )
            if not result:
                return
        
        # بدء التثبيت
        self.install_btn.config(state='disabled')
        self.progress_frame.pack(fill='x', pady=(10, 0))
        self.root.update()
        
        try:
            self.copy_files(install_dir)
            self.create_shortcuts(install_dir)
            
            messagebox.showinfo(
                "نجح التثبيت",
                f"تم تثبيت النظام بنجاح في:\n{install_dir}\n\n"
                "يمكنك الآن تشغيله من:\n"
                "• قائمة ابدأ\n"
                "• سطح المكتب\n"
                "• مجلد التثبيت"
            )
            
            # فتح مجلد التثبيت
            os.startfile(install_dir)
            self.root.quit()
            
        except Exception as e:
            messagebox.showerror("خطأ في التثبيت", f"حدث خطأ أثناء التثبيت:\n{str(e)}")
            self.install_btn.config(state='normal')
            self.progress_frame.pack_forget()
    
    def copy_files(self, install_dir):
        """نسخ الملفات"""
        self.progress_label.config(text="إنشاء مجلد التثبيت...")
        self.root.update()
        
        # إنشاء مجلد التثبيت
        os.makedirs(install_dir, exist_ok=True)
        
        # قائمة الملفات للنسخ
        files_to_copy = [
            "enhanced_main.py",
            "enhanced_database.py",
            "enhanced_main_window.py",
            "enhanced_functions.py",
            "enhanced_file_manager.py",
            "test_enhanced_system.py",
            "enhanced_requirements.txt",
            "دليل_النظام_المحسن.md",
            "ملخص_النظام_المحسن.md",
            "README_Enhanced.md",
            "دليل_إنشاء_الحزمة.md"
        ]
        
        # البحث عن الملف المجمع
        exe_file = None
        for possible_exe in ["نظام_إدارة_مشاكل_العملاء.exe", "customer_issues.exe"]:
            if os.path.exists(possible_exe):
                exe_file = possible_exe
                break
        
        if exe_file:
            files_to_copy.append(exe_file)
        
        # نسخ الملفات
        for i, file_name in enumerate(files_to_copy):
            self.progress_label.config(text=f"نسخ: {file_name}")
            self.root.update()
            
            if os.path.exists(file_name):
                target_path = os.path.join(install_dir, file_name)
                shutil.copy2(file_name, target_path)
        
        # إنشاء ملفات التشغيل
        self.progress_label.config(text="إنشاء ملفات التشغيل...")
        self.root.update()
        
        # ملف تشغيل
        if exe_file:
            run_content = f'''@echo off
chcp 65001 > nul
cd /d "%~dp0"
start "" "{exe_file}"
'''
        else:
            run_content = '''@echo off
chcp 65001 > nul
cd /d "%~dp0"
python enhanced_main.py
if %errorlevel% neq 0 (
    echo خطأ: تأكد من تثبيت Python
    pause
)
'''
        
        with open(os.path.join(install_dir, "تشغيل_النظام.bat"), 'w', encoding='utf-8') as f:
            f.write(run_content)
        
        # ملف اختبار
        test_content = '''@echo off
chcp 65001 > nul
cd /d "%~dp0"
python test_enhanced_system.py
pause
'''
        
        with open(os.path.join(install_dir, "اختبار_النظام.bat"), 'w', encoding='utf-8') as f:
            f.write(test_content)
    
    def create_shortcuts(self, install_dir):
        """إنشاء الاختصارات"""
        self.progress_label.config(text="إنشاء الاختصارات...")
        self.root.update()
        
        try:
            import winshell
            from win32com.client import Dispatch
            
            # اختصار سطح المكتب
            desktop = winshell.desktop()
            shortcut_path = os.path.join(desktop, "نظام إدارة مشاكل العملاء.lnk")
            
            shell = Dispatch('WScript.Shell')
            shortcut = shell.CreateShortCut(shortcut_path)
            shortcut.Targetpath = os.path.join(install_dir, "تشغيل_النظام.bat")
            shortcut.WorkingDirectory = install_dir
            shortcut.IconLocation = os.path.join(install_dir, "تشغيل_النظام.bat")
            shortcut.save()
            
        except ImportError:
            # إذا لم تكن المكتبات متوفرة، تجاهل إنشاء الاختصارات
            pass
    
    def run(self):
        """تشغيل المثبت"""
        self.root.mainloop()

def main():
    """تشغيل المثبت"""
    # تحقق من كون البرنامج يعمل على ويندوز
    if os.name != 'nt':
        print("هذا المثبت يعمل على ويندوز فقط")
        sys.exit(1)
    
    # إنشاء وتشغيل المثبت
    installer = SimpleInstaller()
    installer.run()

if __name__ == "__main__":
    main()