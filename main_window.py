import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from datetime import datetime
import sqlite3
from database import db
from file_manager import FileManager
from report_generator import ReportGenerator
from main_functions import MainFunctions

class MainWindow:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("نظام إدارة مشاكل العملاء")
        self.root.geometry("1200x800")
        self.root.configure(bg='#f0f0f0')
        
        self.file_manager = FileManager()
        self.report_generator = ReportGenerator()
        self.current_user = "المدير"  # يمكن تطويره لإدارة المستخدمين
        
        # إنشاء مثيل للوظائف
        self.functions = MainFunctions(self)
        
        self.create_widgets()
        self.refresh_data()
    
    def create_widgets(self):
        """إنشاء عناصر الواجهة"""
        # إطار العنوان
        title_frame = tk.Frame(self.root, bg='#2c3e50', height=60)
        title_frame.pack(fill='x', pady=(0, 10))
        title_frame.pack_propagate(False)
        
        title_label = tk.Label(title_frame, text="نظام إدارة مشاكل العملاء", 
                              font=('Arial', 18, 'bold'), fg='white', bg='#2c3e50')
        title_label.pack(expand=True)
        
        # إطار الأزرار الرئيسية
        buttons_frame = tk.Frame(self.root, bg='#f0f0f0')
        buttons_frame.pack(fill='x', padx=10, pady=5)
        
        # أزرار العمليات الأساسية
        self.create_button(buttons_frame, "إضافة عميل جديد", self.functions.add_customer, 0, 0)
        self.create_button(buttons_frame, "إضافة مشكلة جديدة", self.functions.add_issue, 0, 1)
        self.create_button(buttons_frame, "إضافة مراسلة", self.functions.add_correspondence, 0, 2)
        self.create_button(buttons_frame, "إضافة مرفق", self.functions.add_attachment, 0, 3)
        
        # صف ثاني من الأزرار
        self.create_button(buttons_frame, "تحديث البيانات", self.refresh_data, 1, 0)
        self.create_button(buttons_frame, "فتح مجلد المرفقات", self.functions.open_attachments_folder, 1, 1)
        self.create_button(buttons_frame, "إنتاج تقرير", self.functions.generate_report, 1, 2)
        self.create_button(buttons_frame, "البحث المتقدم", self.functions.advanced_search, 1, 3)
        
        # إطار البحث
        search_frame = tk.Frame(self.root, bg='#f0f0f0')
        search_frame.pack(fill='x', padx=10, pady=5)
        
        tk.Label(search_frame, text="البحث:", font=('Arial', 12), bg='#f0f0f0').pack(side='right')
        self.search_var = tk.StringVar()
        self.search_var.trace('w', self.search_data)
        search_entry = tk.Entry(search_frame, textvariable=self.search_var, font=('Arial', 12), width=30)
        search_entry.pack(side='right', padx=(5, 0))
        
        # إطار علامات التبويب
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill='both', expand=True, padx=10, pady=5)
        
        # إنشاء علامات التبويب
        self.create_customers_tab()
        self.create_issues_tab()
        self.create_correspondences_tab()
        self.create_attachments_tab()
        self.create_reports_tab()
    
    def create_button(self, parent, text, command, row, col):
        """إنشاء زر بتنسيق موحد"""
        btn = tk.Button(parent, text=text, command=command, 
                       font=('Arial', 10), width=15, height=2,
                       bg='#3498db', fg='white', relief='raised')
        btn.grid(row=row, column=col, padx=5, pady=2, sticky='ew')
        parent.grid_columnconfigure(col, weight=1)
    
    def create_customers_tab(self):
        """إنشاء تبويب العملاء"""
        customers_frame = ttk.Frame(self.notebook)
        self.notebook.add(customers_frame, text="العملاء")
        
        # جدول العملاء
        columns = ('ID', 'رقم المشترك', 'الاسم', 'العنوان', 'الهاتف', 'آخر قراءة', 'المديونية')
        self.customers_tree = ttk.Treeview(customers_frame, columns=columns, show='headings', height=20)
        
        for col in columns:
            self.customers_tree.heading(col, text=col)
            self.customers_tree.column(col, width=120)
        
        # شريط التمرير
        customers_scrollbar = ttk.Scrollbar(customers_frame, orient='vertical', command=self.customers_tree.yview)
        self.customers_tree.configure(yscrollcommand=customers_scrollbar.set)
        
        self.customers_tree.pack(side='left', fill='both', expand=True)
        customers_scrollbar.pack(side='right', fill='y')
        
        # ربط النقر المزدوج
        self.customers_tree.bind('<Double-1>', self.functions.edit_customer)
    
    def create_issues_tab(self):
        """إنشاء تبويب المشاكل"""
        issues_frame = ttk.Frame(self.notebook)
        self.notebook.add(issues_frame, text="المشاكل")
        
        columns = ('ID', 'العميل', 'التصنيف', 'العنوان', 'الحالة', 'الأولوية', 'المسؤول', 'التاريخ')
        self.issues_tree = ttk.Treeview(issues_frame, columns=columns, show='headings', height=20)
        
        for col in columns:
            self.issues_tree.heading(col, text=col)
            self.issues_tree.column(col, width=120)
        
        issues_scrollbar = ttk.Scrollbar(issues_frame, orient='vertical', command=self.issues_tree.yview)
        self.issues_tree.configure(yscrollcommand=issues_scrollbar.set)
        
        self.issues_tree.pack(side='left', fill='both', expand=True)
        issues_scrollbar.pack(side='right', fill='y')
        
        self.issues_tree.bind('<Double-1>', self.functions.edit_issue)
    
    def create_correspondences_tab(self):
        """إنشاء تبويب المراسلات"""
        corr_frame = ttk.Frame(self.notebook)
        self.notebook.add(corr_frame, text="المراسلات")
        
        columns = ('ID', 'رقم المراسلة', 'المشكلة', 'المرسل', 'المستقبل', 'الموضوع', 'تاريخ الإرسال')
        self.corr_tree = ttk.Treeview(corr_frame, columns=columns, show='headings', height=20)
        
        for col in columns:
            self.corr_tree.heading(col, text=col)
            self.corr_tree.column(col, width=120)
        
        corr_scrollbar = ttk.Scrollbar(corr_frame, orient='vertical', command=self.corr_tree.yview)
        self.corr_tree.configure(yscrollcommand=corr_scrollbar.set)
        
        self.corr_tree.pack(side='left', fill='both', expand=True)
        corr_scrollbar.pack(side='right', fill='y')
        
        self.corr_tree.bind('<Double-1>', self.functions.edit_correspondence)
    
    def create_attachments_tab(self):
        """إنشاء تبويب المرفقات"""
        attach_frame = ttk.Frame(self.notebook)
        self.notebook.add(attach_frame, text="المرفقات")
        
        columns = ('ID', 'المشكلة', 'اسم الملف', 'النوع', 'الوصف', 'تاريخ الرفع', 'المستخدم')
        self.attach_tree = ttk.Treeview(attach_frame, columns=columns, show='headings', height=20)
        
        for col in columns:
            self.attach_tree.heading(col, text=col)
            self.attach_tree.column(col, width=120)
        
        attach_scrollbar = ttk.Scrollbar(attach_frame, orient='vertical', command=self.attach_tree.yview)
        self.attach_tree.configure(yscrollcommand=attach_scrollbar.set)
        
        self.attach_tree.pack(side='left', fill='both', expand=True)
        attach_scrollbar.pack(side='right', fill='y')
        
        self.attach_tree.bind('<Double-1>', self.functions.open_attachment)
    
    def create_reports_tab(self):
        """إنشاء تبويب التقارير"""
        reports_frame = ttk.Frame(self.notebook)
        self.notebook.add(reports_frame, text="التقارير")
        
        # إطار خيارات التقارير
        options_frame = tk.Frame(reports_frame, bg='white', relief='ridge', bd=2)
        options_frame.pack(fill='x', padx=10, pady=10)
        
        tk.Label(options_frame, text="خيارات التقارير", font=('Arial', 14, 'bold'), bg='white').pack(pady=10)
        
        # أزرار التقارير
        reports_buttons_frame = tk.Frame(options_frame, bg='white')
        reports_buttons_frame.pack(pady=10)
        
        tk.Button(reports_buttons_frame, text="تقرير عميل محدد", command=self.functions.customer_report,
                 font=('Arial', 12), width=20, bg='#27ae60', fg='white').pack(pady=5)
        
        tk.Button(reports_buttons_frame, text="تقرير ملخص المشاكل", command=self.functions.issues_summary_report,
                 font=('Arial', 12), width=20, bg='#e74c3c', fg='white').pack(pady=5)
        
        tk.Button(reports_buttons_frame, text="تقرير المراسلات", command=self.functions.correspondence_report,
                 font=('Arial', 12), width=20, bg='#f39c12', fg='white').pack(pady=5)
    
    def refresh_data(self):
        """تحديث البيانات في جميع الجداول"""
        self.load_customers()
        self.load_issues()
        self.load_correspondences()
        self.load_attachments()
    
    def load_customers(self):
        """تحميل بيانات العملاء"""
        for item in self.customers_tree.get_children():
            self.customers_tree.delete(item)
        
        query = """
            SELECT id, subscriber_number, name, address, phone, last_reading, debt_amount
            FROM customers ORDER BY created_date DESC
        """
        customers = db.execute_query(query)
        
        for customer in customers:
            self.customers_tree.insert('', 'end', values=customer)
    
    def load_issues(self):
        """تحميل بيانات المشاكل"""
        for item in self.issues_tree.get_children():
            self.issues_tree.delete(item)
        
        query = """
            SELECT i.id, c.name, ic.category_name, i.title, i.status, 
                   i.priority, i.responsible_employee, i.created_date
            FROM issues i
            LEFT JOIN customers c ON i.customer_id = c.id
            LEFT JOIN issue_categories ic ON i.category_id = ic.id
            ORDER BY i.created_date DESC
        """
        issues = db.execute_query(query)
        
        for issue in issues:
            # تنسيق التاريخ
            formatted_date = issue[7].split(' ')[0] if issue[7] else ''
            formatted_issue = list(issue)
            formatted_issue[7] = formatted_date
            self.issues_tree.insert('', 'end', values=formatted_issue)
    
    def load_correspondences(self):
        """تحميل بيانات المراسلات"""
        for item in self.corr_tree.get_children():
            self.corr_tree.delete(item)
        
        query = """
            SELECT cor.id, cor.correspondence_number, i.title, cor.sender, 
                   cor.receiver, cor.subject, cor.date_sent
            FROM correspondences cor
            LEFT JOIN issues i ON cor.issue_id = i.id
            ORDER BY cor.created_date DESC
        """
        correspondences = db.execute_query(query)
        
        for corr in correspondences:
            self.corr_tree.insert('', 'end', values=corr)
    
    def load_attachments(self):
        """تحميل بيانات المرفقات"""
        for item in self.attach_tree.get_children():
            self.attach_tree.delete(item)
        
        query = """
            SELECT a.id, i.title, a.file_name, a.file_type, 
                   a.description, a.upload_date, a.uploaded_by
            FROM attachments a
            LEFT JOIN issues i ON a.issue_id = i.id
            ORDER BY a.upload_date DESC
        """
        attachments = db.execute_query(query)
        
        for attach in attachments:
            self.attach_tree.insert('', 'end', values=attach)
    
    def search_data(self, *args):
        """البحث في البيانات"""
        search_term = self.search_var.get().strip()
        if not search_term:
            self.refresh_data()
            return
        
        # البحث في العملاء
        self.search_customers(search_term)
        self.search_issues(search_term)
    
    def search_customers(self, term):
        """البحث في العملاء"""
        for item in self.customers_tree.get_children():
            self.customers_tree.delete(item)
        
        query = """
            SELECT id, subscriber_number, name, address, phone, last_reading, debt_amount
            FROM customers 
            WHERE subscriber_number LIKE ? OR name LIKE ? OR address LIKE ? OR phone LIKE ?
            ORDER BY created_date DESC
        """
        term_pattern = f"%{term}%"
        customers = db.execute_query(query, (term_pattern, term_pattern, term_pattern, term_pattern))
        
        for customer in customers:
            self.customers_tree.insert('', 'end', values=customer)
    
    def search_issues(self, term):
        """البحث في المشاكل"""
        for item in self.issues_tree.get_children():
            self.issues_tree.delete(item)
        
        query = """
            SELECT i.id, c.name, ic.category_name, i.title, i.status, 
                   i.priority, i.responsible_employee, i.created_date
            FROM issues i
            LEFT JOIN customers c ON i.customer_id = c.id
            LEFT JOIN issue_categories ic ON i.category_id = ic.id
            WHERE c.name LIKE ? OR i.title LIKE ? OR i.description LIKE ? OR ic.category_name LIKE ?
            ORDER BY i.created_date DESC
        """
        term_pattern = f"%{term}%"
        issues = db.execute_query(query, (term_pattern, term_pattern, term_pattern, term_pattern))
        
        for issue in issues:
            formatted_date = issue[7].split(' ')[0] if issue[7] else ''
            formatted_issue = list(issue)
            formatted_issue[7] = formatted_date
            self.issues_tree.insert('', 'end', values=formatted_issue)
    
    # يتم إضافة باقي الوظائف في الجزء التالي...
    
    def run(self):
        """تشغيل التطبيق"""
        self.root.mainloop()

if __name__ == "__main__":
    app = MainWindow()
    app.run()