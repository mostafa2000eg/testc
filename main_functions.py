import tkinter as tk
from tkinter import messagebox, filedialog
from datetime import datetime
from database import db
from file_manager import FileManager
from report_generator import ReportGenerator
from dialogs import CustomerDialog, IssueDialog, CorrespondenceDialog, AttachmentDialog

class MainFunctions:
    def __init__(self, main_window):
        self.main_window = main_window
        self.file_manager = FileManager()
        self.report_generator = ReportGenerator()
    
    def add_customer(self):
        """إضافة عميل جديد"""
        dialog = CustomerDialog(self.main_window.root)
        self.main_window.root.wait_window(dialog.dialog)
        
        if dialog.result == "success":
            messagebox.showinfo("نجح", "تم إضافة العميل بنجاح")
            self.main_window.refresh_data()
    
    def add_issue(self):
        """إضافة مشكلة جديدة"""
        dialog = IssueDialog(self.main_window.root)
        self.main_window.root.wait_window(dialog.dialog)
        
        if dialog.result == "success":
            messagebox.showinfo("نجح", "تم إضافة المشكلة بنجاح")
            self.main_window.refresh_data()
    
    def add_correspondence(self):
        """إضافة مراسلة جديدة"""
        dialog = CorrespondenceDialog(self.main_window.root)
        self.main_window.root.wait_window(dialog.dialog)
        
        if dialog.result == "success":
            messagebox.showinfo("نجح", "تم إضافة المراسلة بنجاح")
            self.main_window.refresh_data()
    
    def add_attachment(self):
        """إضافة مرفق جديد"""
        dialog = AttachmentDialog(self.main_window.root)
        self.main_window.root.wait_window(dialog.dialog)
        
        if dialog.result == "success":
            self.main_window.refresh_data()
    
    def edit_customer(self, event):
        """تحرير بيانات العميل"""
        selection = self.main_window.customers_tree.selection()
        if not selection:
            return
        
        item = self.main_window.customers_tree.item(selection[0])
        customer_data = item['values']
        
        dialog = CustomerDialog(self.main_window.root, customer_data)
        self.main_window.root.wait_window(dialog.dialog)
        
        if dialog.result == "success":
            messagebox.showinfo("نجح", "تم تحديث بيانات العميل بنجاح")
            self.main_window.refresh_data()
    
    def edit_issue(self, event):
        """تحرير المشكلة"""
        selection = self.main_window.issues_tree.selection()
        if not selection:
            return
        
        item = self.main_window.issues_tree.item(selection[0])
        issue_data = item['values']
        
        # الحصول على بيانات المشكلة الكاملة
        query = """
            SELECT i.id, i.customer_id, i.category_id, i.title, i.description, 
                   i.status, i.priority, i.responsible_employee
            FROM issues i WHERE i.id = ?
        """
        full_issue_data = db.execute_query(query, (issue_data[0],))
        
        if full_issue_data:
            dialog = IssueDialog(self.main_window.root, full_issue_data[0])
            self.main_window.root.wait_window(dialog.dialog)
            
            if dialog.result == "success":
                messagebox.showinfo("نجح", "تم تحديث المشكلة بنجاح")
                self.main_window.refresh_data()
    
    def edit_correspondence(self, event):
        """تحرير المراسلة"""
        selection = self.main_window.corr_tree.selection()
        if not selection:
            return
        
        item = self.main_window.corr_tree.item(selection[0])
        corr_data = item['values']
        
        # الحصول على بيانات المراسلة الكاملة
        query = """
            SELECT id, issue_id, correspondence_number, sender, receiver, subject, 
                   date_sent, date_received, content, response_content, response_date
            FROM correspondences WHERE id = ?
        """
        full_corr_data = db.execute_query(query, (corr_data[0],))
        
        if full_corr_data:
            dialog = CorrespondenceDialog(self.main_window.root, full_corr_data[0])
            self.main_window.root.wait_window(dialog.dialog)
            
            if dialog.result == "success":
                messagebox.showinfo("نجح", "تم تحديث المراسلة بنجاح")
                self.main_window.refresh_data()
    
    def open_attachment(self, event):
        """فتح المرفق"""
        selection = self.main_window.attach_tree.selection()
        if not selection:
            return
        
        item = self.main_window.attach_tree.item(selection[0])
        attach_data = item['values']
        
        # الحصول على مسار الملف
        query = "SELECT file_path FROM attachments WHERE id = ?"
        result = db.execute_query(query, (attach_data[0],))
        
        if result:
            file_path = result[0][0]
            self.file_manager.open_file(file_path)
    
    def open_attachments_folder(self):
        """فتح مجلد المرفقات للعميل المختار"""
        # الحصول على العميل المختار
        selection = self.main_window.customers_tree.selection()
        if not selection:
            messagebox.showwarning("تحذير", "يرجى اختيار عميل أولاً")
            return
        
        item = self.main_window.customers_tree.item(selection[0])
        customer_data = item['values']
        subscriber_number = customer_data[1]
        
        self.file_manager.open_customer_folder(subscriber_number)
    
    def generate_report(self):
        """إنتاج التقارير"""
        # نافذة اختيار نوع التقرير
        report_window = tk.Toplevel(self.main_window.root)
        report_window.title("إنتاج التقارير")
        report_window.geometry("300x200")
        report_window.transient(self.main_window.root)
        report_window.grab_set()
        
        tk.Label(report_window, text="اختر نوع التقرير", font=('Arial', 14, 'bold')).pack(pady=20)
        
        tk.Button(report_window, text="تقرير عميل محدد", 
                 command=lambda: self.customer_report(report_window),
                 font=('Arial', 12), width=20, bg='#27ae60', fg='white').pack(pady=5)
        
        tk.Button(report_window, text="تقرير ملخص المشاكل", 
                 command=lambda: self.issues_summary_report(report_window),
                 font=('Arial', 12), width=20, bg='#e74c3c', fg='white').pack(pady=5)
        
        tk.Button(report_window, text="تقرير المراسلات", 
                 command=lambda: self.correspondence_report(report_window),
                 font=('Arial', 12), width=20, bg='#f39c12', fg='white').pack(pady=5)
    
    def customer_report(self, parent_window=None):
        """إنتاج تقرير عميل محدد"""
        if parent_window:
            parent_window.destroy()
        
        # اختيار العميل
        customers_query = "SELECT id, subscriber_number, name FROM customers ORDER BY name"
        customers = db.execute_query(customers_query)
        
        if not customers:
            messagebox.showwarning("تحذير", "لا توجد عملاء في النظام")
            return
        
        # نافذة اختيار العميل
        customer_window = tk.Toplevel(self.main_window.root)
        customer_window.title("اختيار العميل")
        customer_window.geometry("400x300")
        customer_window.transient(self.main_window.root)
        customer_window.grab_set()
        
        tk.Label(customer_window, text="اختر العميل", font=('Arial', 14, 'bold')).pack(pady=10)
        
        from tkinter import ttk
        customer_var = tk.StringVar()
        customer_combo = ttk.Combobox(customer_window, textvariable=customer_var, width=40, state='readonly')
        
        customer_list = [f"{customer[1]} - {customer[2]}" for customer in customers]
        customer_combo['values'] = customer_list
        customer_combo.pack(pady=10)
        
        customers_data = {f"{customer[1]} - {customer[2]}": customer for customer in customers}
        
        def generate_customer_report():
            if not customer_var.get():
                messagebox.showerror("خطأ", "يرجى اختيار عميل")
                return
            
            selected_customer = customers_data[customer_var.get()]
            customer_id = selected_customer[0]
            
            # الحصول على بيانات العميل
            customer_query = """
                SELECT id, subscriber_number, name, address, phone, 
                       last_reading, last_reading_date, debt_amount
                FROM customers WHERE id = ?
            """
            customer_data = db.execute_query(customer_query, (customer_id,))
            
            if not customer_data:
                messagebox.showerror("خطأ", "لم يتم العثور على بيانات العميل")
                return
            
            customer_info = {
                'id': customer_data[0][0],
                'subscriber_number': customer_data[0][1],
                'name': customer_data[0][2],
                'address': customer_data[0][3],
                'phone': customer_data[0][4],
                'last_reading': customer_data[0][5],
                'last_reading_date': customer_data[0][6],
                'debt_amount': customer_data[0][7]
            }
            
            # الحصول على مشاكل العميل
            issues_query = """
                SELECT i.id, ic.category_name, i.title, i.description, i.status, 
                       i.priority, i.responsible_employee, i.created_date
                FROM issues i
                LEFT JOIN issue_categories ic ON i.category_id = ic.id
                WHERE i.customer_id = ?
                ORDER BY i.created_date DESC
            """
            issues_data = db.execute_query(issues_query, (customer_id,))
            
            issues_list = []
            for issue in issues_data:
                issues_list.append({
                    'id': issue[0],
                    'category': issue[1],
                    'title': issue[2],
                    'description': issue[3],
                    'status': issue[4],
                    'priority': issue[5],
                    'responsible_employee': issue[6],
                    'created_date': issue[7]
                })
            
            # اختيار مكان الحفظ
            output_path = filedialog.asksaveasfilename(
                title="حفظ التقرير",
                defaultextension=".pdf",
                filetypes=[("ملفات PDF", "*.pdf")]
            )
            
            if output_path:
                try:
                    self.report_generator.generate_customer_report(customer_info, issues_list, output_path)
                    messagebox.showinfo("نجح", f"تم إنتاج التقرير بنجاح: {output_path}")
                    customer_window.destroy()
                except Exception as e:
                    messagebox.showerror("خطأ", f"فشل في إنتاج التقرير: {str(e)}")
        
        tk.Button(customer_window, text="إنتاج التقرير", command=generate_customer_report,
                 font=('Arial', 12), bg='#3498db', fg='white').pack(pady=20)
        tk.Button(customer_window, text="إلغاء", command=customer_window.destroy,
                 font=('Arial', 12), bg='#e74c3c', fg='white').pack()
    
    def issues_summary_report(self, parent_window=None):
        """إنتاج تقرير ملخص المشاكل"""
        if parent_window:
            parent_window.destroy()
        
        # الحصول على جميع المشاكل
        issues_query = """
            SELECT i.id, c.name, ic.category_name, i.title, i.status, 
                   i.priority, i.responsible_employee, i.created_date
            FROM issues i
            LEFT JOIN customers c ON i.customer_id = c.id
            LEFT JOIN issue_categories ic ON i.category_id = ic.id
            ORDER BY i.created_date DESC
        """
        issues_data = db.execute_query(issues_query)
        
        issues_list = []
        for issue in issues_data:
            issues_list.append({
                'id': issue[0],
                'customer_name': issue[1],
                'category': issue[2],
                'title': issue[3],
                'status': issue[4],
                'priority': issue[5],
                'responsible_employee': issue[6],
                'created_date': issue[7]
            })
        
        # اختيار مكان الحفظ
        output_path = filedialog.asksaveasfilename(
            title="حفظ تقرير ملخص المشاكل",
            defaultextension=".pdf",
            filetypes=[("ملفات PDF", "*.pdf")]
        )
        
        if output_path:
            try:
                self.report_generator.generate_issues_summary_report(issues_list, output_path)
                messagebox.showinfo("نجح", f"تم إنتاج التقرير بنجاح: {output_path}")
            except Exception as e:
                messagebox.showerror("خطأ", f"فشل في إنتاج التقرير: {str(e)}")
    
    def correspondence_report(self, parent_window=None):
        """إنتاج تقرير المراسلات"""
        if parent_window:
            parent_window.destroy()
        
        # الحصول على جميع المراسلات
        corr_query = """
            SELECT cor.id, cor.correspondence_number, cor.sender, cor.receiver, 
                   cor.subject, cor.date_sent, cor.date_received, cor.content, 
                   cor.response_content, cor.response_date
            FROM correspondences cor
            ORDER BY cor.created_date DESC
        """
        corr_data = db.execute_query(corr_query)
        
        corr_list = []
        for corr in corr_data:
            corr_list.append({
                'id': corr[0],
                'correspondence_number': corr[1],
                'sender': corr[2],
                'receiver': corr[3],
                'subject': corr[4],
                'date_sent': corr[5],
                'date_received': corr[6],
                'content': corr[7],
                'response_content': corr[8],
                'response_date': corr[9]
            })
        
        # اختيار مكان الحفظ
        output_path = filedialog.asksaveasfilename(
            title="حفظ تقرير المراسلات",
            defaultextension=".pdf",
            filetypes=[("ملفات PDF", "*.pdf")]
        )
        
        if output_path:
            try:
                self.report_generator.generate_correspondence_report(corr_list, output_path)
                messagebox.showinfo("نجح", f"تم إنتاج التقرير بنجاح: {output_path}")
            except Exception as e:
                messagebox.showerror("خطأ", f"فشل في إنتاج التقرير: {str(e)}")
    
    def advanced_search(self):
        """البحث المتقدم"""
        search_window = tk.Toplevel(self.main_window.root)
        search_window.title("البحث المتقدم")
        search_window.geometry("500x400")
        search_window.transient(self.main_window.root)
        search_window.grab_set()
        
        main_frame = tk.Frame(search_window, bg='white', padx=20, pady=20)
        main_frame.pack(fill='both', expand=True)
        
        tk.Label(main_frame, text="البحث المتقدم", font=('Arial', 16, 'bold'), bg='white').pack(pady=(0, 20))
        
        # خيارات البحث
        search_options = tk.Frame(main_frame, bg='white')
        search_options.pack(fill='x', pady=10)
        
        # نوع البحث
        search_type_frame = tk.Frame(search_options, bg='white')
        search_type_frame.pack(fill='x', pady=5)
        tk.Label(search_type_frame, text="البحث في:", font=('Arial', 12), bg='white', width=15, anchor='e').pack(side='right')
        
        search_type_var = tk.StringVar(value="العملاء")
        from tkinter import ttk
        search_type_combo = ttk.Combobox(search_type_frame, textvariable=search_type_var, width=20,
                                        values=["العملاء", "المشاكل", "المراسلات"], state='readonly')
        search_type_combo.pack(side='right', padx=(5, 0))
        
        # معايير البحث
        criteria_frame = tk.Frame(search_options, bg='white')
        criteria_frame.pack(fill='x', pady=5)
        tk.Label(criteria_frame, text="كلمة البحث:", font=('Arial', 12), bg='white', width=15, anchor='e').pack(side='right')
        search_term_entry = tk.Entry(criteria_frame, font=('Arial', 10), width=30)
        search_term_entry.pack(side='right', padx=(5, 0))
        
        # فترة زمنية
        date_frame = tk.Frame(search_options, bg='white')
        date_frame.pack(fill='x', pady=5)
        tk.Label(date_frame, text="من تاريخ:", font=('Arial', 12), bg='white', width=15, anchor='e').pack(side='right')
        date_from_entry = tk.Entry(date_frame, font=('Arial', 10), width=15)
        date_from_entry.pack(side='right', padx=(5, 0))
        
        tk.Label(date_frame, text="إلى تاريخ:", font=('Arial', 12), bg='white', width=10, anchor='e').pack(side='right')
        date_to_entry = tk.Entry(date_frame, font=('Arial', 10), width=15)
        date_to_entry.pack(side='right', padx=(5, 0))
        
        # نتائج البحث
        results_frame = tk.Frame(main_frame, bg='white')
        results_frame.pack(fill='both', expand=True, pady=10)
        
        tk.Label(results_frame, text="نتائج البحث:", font=('Arial', 12), bg='white', anchor='e').pack(anchor='e')
        
        # جدول النتائج
        columns = ('ID', 'النوع', 'التفاصيل', 'التاريخ')
        results_tree = ttk.Treeview(results_frame, columns=columns, show='headings', height=10)
        
        for col in columns:
            results_tree.heading(col, text=col)
            results_tree.column(col, width=100)
        
        results_scrollbar = ttk.Scrollbar(results_frame, orient='vertical', command=results_tree.yview)
        results_tree.configure(yscrollcommand=results_scrollbar.set)
        
        results_tree.pack(side='left', fill='both', expand=True)
        results_scrollbar.pack(side='right', fill='y')
        
        def perform_search():
            """تنفيذ البحث"""
            search_type = search_type_var.get()
            search_term = search_term_entry.get().strip()
            date_from = date_from_entry.get().strip()
            date_to = date_to_entry.get().strip()
            
            # مسح النتائج السابقة
            for item in results_tree.get_children():
                results_tree.delete(item)
            
            if not search_term:
                messagebox.showwarning("تحذير", "يرجى إدخال كلمة البحث")
                return
            
            try:
                if search_type == "العملاء":
                    query = """
                        SELECT id, subscriber_number, name, created_date, 'عميل' as type
                        FROM customers 
                        WHERE (subscriber_number LIKE ? OR name LIKE ? OR address LIKE ?)
                    """
                    params = [f"%{search_term}%", f"%{search_term}%", f"%{search_term}%"]
                    
                    if date_from:
                        query += " AND created_date >= ?"
                        params.append(date_from)
                    if date_to:
                        query += " AND created_date <= ?"
                        params.append(date_to + " 23:59:59")
                    
                    results = db.execute_query(query, params)
                    
                    for result in results:
                        details = f"{result[1]} - {result[2]}"
                        results_tree.insert('', 'end', values=(result[0], result[4], details, result[3].split(' ')[0] if result[3] else ''))
                
                elif search_type == "المشاكل":
                    query = """
                        SELECT i.id, i.title, c.name, i.created_date, 'مشكلة' as type
                        FROM issues i
                        LEFT JOIN customers c ON i.customer_id = c.id
                        WHERE (i.title LIKE ? OR i.description LIKE ? OR c.name LIKE ?)
                    """
                    params = [f"%{search_term}%", f"%{search_term}%", f"%{search_term}%"]
                    
                    if date_from:
                        query += " AND i.created_date >= ?"
                        params.append(date_from)
                    if date_to:
                        query += " AND i.created_date <= ?"
                        params.append(date_to + " 23:59:59")
                    
                    results = db.execute_query(query, params)
                    
                    for result in results:
                        details = f"{result[1]} ({result[2]})"
                        results_tree.insert('', 'end', values=(result[0], result[4], details, result[3].split(' ')[0] if result[3] else ''))
                
                elif search_type == "المراسلات":
                    query = """
                        SELECT cor.id, cor.subject, cor.sender, cor.created_date, 'مراسلة' as type
                        FROM correspondences cor
                        WHERE (cor.subject LIKE ? OR cor.content LIKE ? OR cor.sender LIKE ?)
                    """
                    params = [f"%{search_term}%", f"%{search_term}%", f"%{search_term}%"]
                    
                    if date_from:
                        query += " AND cor.created_date >= ?"
                        params.append(date_from)
                    if date_to:
                        query += " AND cor.created_date <= ?"
                        params.append(date_to + " 23:59:59")
                    
                    results = db.execute_query(query, params)
                    
                    for result in results:
                        details = f"{result[1]} من {result[2]}"
                        results_tree.insert('', 'end', values=(result[0], result[4], details, result[3].split(' ')[0] if result[3] else ''))
                
                messagebox.showinfo("نتائج البحث", f"تم العثور على {len(results_tree.get_children())} نتيجة")
                
            except Exception as e:
                messagebox.showerror("خطأ", f"فشل في البحث: {str(e)}")
        
        # أزرار العمليات
        buttons_frame = tk.Frame(main_frame, bg='white')
        buttons_frame.pack(pady=10)
        
        tk.Button(buttons_frame, text="بحث", command=perform_search,
                 font=('Arial', 12), width=10, bg='#3498db', fg='white').pack(side='right', padx=5)
        tk.Button(buttons_frame, text="إغلاق", command=search_window.destroy,
                 font=('Arial', 12), width=10, bg='#e74c3c', fg='white').pack(side='right')