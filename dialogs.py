import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from datetime import datetime
from database import db
from file_manager import FileManager

class CustomerDialog:
    def __init__(self, parent, customer_data=None):
        self.parent = parent
        self.customer_data = customer_data
        self.result = None
        
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("إضافة عميل جديد" if not customer_data else "تحرير بيانات العميل")
        self.dialog.geometry("400x500")
        self.dialog.resizable(False, False)
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        self.create_widgets()
        if customer_data:
            self.load_data()
        
        # توسيط النافذة
        self.dialog.geometry("+%d+%d" % (parent.winfo_rootx() + 50, parent.winfo_rooty() + 50))
    
    def create_widgets(self):
        """إنشاء عناصر النافذة"""
        main_frame = tk.Frame(self.dialog, bg='white', padx=20, pady=20)
        main_frame.pack(fill='both', expand=True)
        
        # العنوان
        title = "إضافة عميل جديد" if not self.customer_data else "تحرير بيانات العميل"
        tk.Label(main_frame, text=title, font=('Arial', 16, 'bold'), bg='white').pack(pady=(0, 20))
        
        # حقول البيانات
        fields = [
            ("رقم المشترك:", "subscriber_number"),
            ("اسم العميل:", "name"),
            ("العنوان:", "address"),
            ("رقم الهاتف:", "phone"),
            ("آخر قراءة:", "last_reading"),
            ("تاريخ آخر قراءة:", "last_reading_date"),
            ("المديونية:", "debt_amount")
        ]
        
        self.entries = {}
        
        for label_text, field_name in fields:
            frame = tk.Frame(main_frame, bg='white')
            frame.pack(fill='x', pady=5)
            
            tk.Label(frame, text=label_text, font=('Arial', 12), bg='white', width=15, anchor='e').pack(side='right')
            
            if field_name == "address":
                entry = tk.Text(frame, height=3, width=25, font=('Arial', 10))
            elif field_name == "last_reading_date":
                entry = tk.Entry(frame, font=('Arial', 10), width=25)
                # إضافة تلميح للتاريخ
                tk.Label(frame, text="(YYYY-MM-DD)", font=('Arial', 8), fg='gray', bg='white').pack(side='left')
            else:
                entry = tk.Entry(frame, font=('Arial', 10), width=25)
            
            entry.pack(side='right', padx=(5, 0))
            self.entries[field_name] = entry
        
        # أزرار العمليات
        buttons_frame = tk.Frame(main_frame, bg='white')
        buttons_frame.pack(pady=20)
        
        tk.Button(buttons_frame, text="حفظ", command=self.save, 
                 font=('Arial', 12), width=10, bg='#27ae60', fg='white').pack(side='right', padx=5)
        tk.Button(buttons_frame, text="إلغاء", command=self.cancel, 
                 font=('Arial', 12), width=10, bg='#e74c3c', fg='white').pack(side='right')
    
    def load_data(self):
        """تحميل البيانات للتحرير"""
        if self.customer_data:
            for i, value in enumerate(self.customer_data):
                field_names = ["id", "subscriber_number", "name", "address", "phone", 
                              "last_reading", "last_reading_date", "debt_amount"]
                if i < len(field_names) and field_names[i] in self.entries:
                    field_name = field_names[i]
                    if field_name == "address":
                        self.entries[field_name].insert('1.0', str(value) if value else "")
                    else:
                        self.entries[field_name].insert(0, str(value) if value else "")
    
    def save(self):
        """حفظ البيانات"""
        # التحقق من صحة البيانات
        subscriber_number = self.entries['subscriber_number'].get().strip()
        name = self.entries['name'].get().strip()
        
        if not subscriber_number or not name:
            messagebox.showerror("خطأ", "رقم المشترك واسم العميل مطلوبان")
            return
        
        # جمع البيانات
        data = {
            'subscriber_number': subscriber_number,
            'name': name,
            'address': self.entries['address'].get('1.0', 'end-1c').strip(),
            'phone': self.entries['phone'].get().strip(),
            'last_reading': self.entries['last_reading'].get().strip() or 0,
            'last_reading_date': self.entries['last_reading_date'].get().strip(),
            'debt_amount': self.entries['debt_amount'].get().strip() or 0
        }
        
        try:
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            if self.customer_data:  # تحديث
                query = """
                    UPDATE customers SET subscriber_number=?, name=?, address=?, phone=?, 
                           last_reading=?, last_reading_date=?, debt_amount=?, 
                           modified_date=?, modified_by=?
                    WHERE id=?
                """
                params = (data['subscriber_number'], data['name'], data['address'], 
                         data['phone'], data['last_reading'], data['last_reading_date'],
                         data['debt_amount'], current_time, "المدير", self.customer_data[0])
            else:  # إضافة جديد
                query = """
                    INSERT INTO customers (subscriber_number, name, address, phone, 
                                         last_reading, last_reading_date, debt_amount, 
                                         created_date, created_by)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """
                params = (data['subscriber_number'], data['name'], data['address'], 
                         data['phone'], data['last_reading'], data['last_reading_date'],
                         data['debt_amount'], current_time, "المدير")
            
            db.execute_query(query, params)
            
            # تسجيل في سجل التدقيق
            action = "تحديث" if self.customer_data else "إضافة"
            db.log_audit("customers", self.customer_data[0] if self.customer_data else None, 
                        action, self.customer_data, data, "المدير")
            
            self.result = "success"
            self.dialog.destroy()
            
        except Exception as e:
            messagebox.showerror("خطأ", f"فشل في حفظ البيانات: {str(e)}")
    
    def cancel(self):
        """إلغاء العملية"""
        self.dialog.destroy()

class IssueDialog:
    def __init__(self, parent, issue_data=None):
        self.parent = parent
        self.issue_data = issue_data
        self.result = None
        
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("إضافة مشكلة جديدة" if not issue_data else "تحرير المشكلة")
        self.dialog.geometry("500x600")
        self.dialog.resizable(False, False)
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        self.create_widgets()
        if issue_data:
            self.load_data()
        
        self.dialog.geometry("+%d+%d" % (parent.winfo_rootx() + 50, parent.winfo_rooty() + 50))
    
    def create_widgets(self):
        """إنشاء عناصر النافذة"""
        main_frame = tk.Frame(self.dialog, bg='white', padx=20, pady=20)
        main_frame.pack(fill='both', expand=True)
        
        title = "إضافة مشكلة جديدة" if not self.issue_data else "تحرير المشكلة"
        tk.Label(main_frame, text=title, font=('Arial', 16, 'bold'), bg='white').pack(pady=(0, 20))
        
        # اختيار العميل
        customer_frame = tk.Frame(main_frame, bg='white')
        customer_frame.pack(fill='x', pady=5)
        tk.Label(customer_frame, text="العميل:", font=('Arial', 12), bg='white', width=15, anchor='e').pack(side='right')
        
        self.customer_var = tk.StringVar()
        self.customer_combo = ttk.Combobox(customer_frame, textvariable=self.customer_var, width=30, state='readonly')
        self.customer_combo.pack(side='right', padx=(5, 0))
        self.load_customers()
        
        # تصنيف المشكلة
        category_frame = tk.Frame(main_frame, bg='white')
        category_frame.pack(fill='x', pady=5)
        tk.Label(category_frame, text="تصنيف المشكلة:", font=('Arial', 12), bg='white', width=15, anchor='e').pack(side='right')
        
        self.category_var = tk.StringVar()
        self.category_combo = ttk.Combobox(category_frame, textvariable=self.category_var, width=30, state='readonly')
        self.category_combo.pack(side='right', padx=(5, 0))
        self.load_categories()
        
        # عنوان المشكلة
        title_frame = tk.Frame(main_frame, bg='white')
        title_frame.pack(fill='x', pady=5)
        tk.Label(title_frame, text="عنوان المشكلة:", font=('Arial', 12), bg='white', width=15, anchor='e').pack(side='right')
        self.title_entry = tk.Entry(title_frame, font=('Arial', 10), width=35)
        self.title_entry.pack(side='right', padx=(5, 0))
        
        # وصف المشكلة
        desc_frame = tk.Frame(main_frame, bg='white')
        desc_frame.pack(fill='x', pady=5)
        tk.Label(desc_frame, text="وصف المشكلة:", font=('Arial', 12), bg='white', width=15, anchor='e').pack(side='right')
        self.desc_text = tk.Text(main_frame, height=5, width=40, font=('Arial', 10))
        self.desc_text.pack(pady=5)
        
        # الحالة
        status_frame = tk.Frame(main_frame, bg='white')
        status_frame.pack(fill='x', pady=5)
        tk.Label(status_frame, text="الحالة:", font=('Arial', 12), bg='white', width=15, anchor='e').pack(side='right')
        
        self.status_var = tk.StringVar(value="مفتوحة")
        status_combo = ttk.Combobox(status_frame, textvariable=self.status_var, width=30, 
                                   values=["مفتوحة", "قيد المعالجة", "مغلقة", "مؤجلة"], state='readonly')
        status_combo.pack(side='right', padx=(5, 0))
        
        # الأولوية
        priority_frame = tk.Frame(main_frame, bg='white')
        priority_frame.pack(fill='x', pady=5)
        tk.Label(priority_frame, text="الأولوية:", font=('Arial', 12), bg='white', width=15, anchor='e').pack(side='right')
        
        self.priority_var = tk.StringVar(value="متوسطة")
        priority_combo = ttk.Combobox(priority_frame, textvariable=self.priority_var, width=30,
                                     values=["منخفضة", "متوسطة", "عالية", "عاجلة"], state='readonly')
        priority_combo.pack(side='right', padx=(5, 0))
        
        # الموظف المسؤول
        employee_frame = tk.Frame(main_frame, bg='white')
        employee_frame.pack(fill='x', pady=5)
        tk.Label(employee_frame, text="الموظف المسؤول:", font=('Arial', 12), bg='white', width=15, anchor='e').pack(side='right')
        self.employee_entry = tk.Entry(employee_frame, font=('Arial', 10), width=35)
        self.employee_entry.pack(side='right', padx=(5, 0))
        
        # أزرار العمليات
        buttons_frame = tk.Frame(main_frame, bg='white')
        buttons_frame.pack(pady=20)
        
        tk.Button(buttons_frame, text="حفظ", command=self.save,
                 font=('Arial', 12), width=10, bg='#27ae60', fg='white').pack(side='right', padx=5)
        tk.Button(buttons_frame, text="إلغاء", command=self.cancel,
                 font=('Arial', 12), width=10, bg='#e74c3c', fg='white').pack(side='right')
    
    def load_customers(self):
        """تحميل قائمة العملاء"""
        query = "SELECT id, subscriber_number, name FROM customers ORDER BY name"
        customers = db.execute_query(query)
        
        customer_list = [f"{customer[1]} - {customer[2]}" for customer in customers]
        self.customer_combo['values'] = customer_list
        self.customers_data = {f"{customer[1]} - {customer[2]}": customer[0] for customer in customers}
    
    def load_categories(self):
        """تحميل تصنيفات المشاكل"""
        query = "SELECT id, category_name FROM issue_categories ORDER BY category_name"
        categories = db.execute_query(query)
        
        category_list = [category[1] for category in categories]
        self.category_combo['values'] = category_list
        self.categories_data = {category[1]: category[0] for category in categories}
    
    def save(self):
        """حفظ البيانات"""
        # التحقق من صحة البيانات
        if not self.customer_var.get() or not self.category_var.get() or not self.title_entry.get().strip():
            messagebox.showerror("خطأ", "يجب ملء جميع الحقول المطلوبة")
            return
        
        try:
            customer_id = self.customers_data[self.customer_var.get()]
            category_id = self.categories_data[self.category_var.get()]
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            data = {
                'customer_id': customer_id,
                'category_id': category_id,
                'title': self.title_entry.get().strip(),
                'description': self.desc_text.get('1.0', 'end-1c').strip(),
                'status': self.status_var.get(),
                'priority': self.priority_var.get(),
                'responsible_employee': self.employee_entry.get().strip()
            }
            
            if self.issue_data:  # تحديث
                query = """
                    UPDATE issues SET customer_id=?, category_id=?, title=?, description=?, 
                           status=?, priority=?, responsible_employee=?, modified_date=?, modified_by=?
                    WHERE id=?
                """
                params = (data['customer_id'], data['category_id'], data['title'], 
                         data['description'], data['status'], data['priority'],
                         data['responsible_employee'], current_time, "المدير", self.issue_data[0])
            else:  # إضافة جديد
                query = """
                    INSERT INTO issues (customer_id, category_id, title, description, status, 
                                      priority, responsible_employee, created_date, created_by)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """
                params = (data['customer_id'], data['category_id'], data['title'], 
                         data['description'], data['status'], data['priority'],
                         data['responsible_employee'], current_time, "المدير")
            
            db.execute_query(query, params)
            
            action = "تحديث" if self.issue_data else "إضافة"
            db.log_audit("issues", self.issue_data[0] if self.issue_data else None,
                        action, self.issue_data, data, "المدير")
            
            self.result = "success"
            self.dialog.destroy()
            
        except Exception as e:
            messagebox.showerror("خطأ", f"فشل في حفظ البيانات: {str(e)}")
    
    def cancel(self):
        """إلغاء العملية"""
        self.dialog.destroy()

class CorrespondenceDialog:
    def __init__(self, parent, correspondence_data=None):
        self.parent = parent
        self.correspondence_data = correspondence_data
        self.result = None
        
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("إضافة مراسلة جديدة" if not correspondence_data else "تحرير المراسلة")
        self.dialog.geometry("600x700")
        self.dialog.resizable(False, False)
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        self.create_widgets()
        if correspondence_data:
            self.load_data()
        
        self.dialog.geometry("+%d+%d" % (parent.winfo_rootx() + 50, parent.winfo_rooty() + 50))
    
    def create_widgets(self):
        """إنشاء عناصر النافذة"""
        main_frame = tk.Frame(self.dialog, bg='white', padx=20, pady=20)
        main_frame.pack(fill='both', expand=True)
        
        title = "إضافة مراسلة جديدة" if not self.correspondence_data else "تحرير المراسلة"
        tk.Label(main_frame, text=title, font=('Arial', 16, 'bold'), bg='white').pack(pady=(0, 20))
        
        # اختيار المشكلة
        issue_frame = tk.Frame(main_frame, bg='white')
        issue_frame.pack(fill='x', pady=5)
        tk.Label(issue_frame, text="المشكلة:", font=('Arial', 12), bg='white', width=15, anchor='e').pack(side='right')
        
        self.issue_var = tk.StringVar()
        self.issue_combo = ttk.Combobox(issue_frame, textvariable=self.issue_var, width=40, state='readonly')
        self.issue_combo.pack(side='right', padx=(5, 0))
        self.load_issues()
        
        # رقم المراسلة
        corr_num_frame = tk.Frame(main_frame, bg='white')
        corr_num_frame.pack(fill='x', pady=5)
        tk.Label(corr_num_frame, text="رقم المراسلة:", font=('Arial', 12), bg='white', width=15, anchor='e').pack(side='right')
        self.corr_num_entry = tk.Entry(corr_num_frame, font=('Arial', 10), width=40)
        self.corr_num_entry.pack(side='right', padx=(5, 0))
        
        # المرسل والمستقبل
        sender_frame = tk.Frame(main_frame, bg='white')
        sender_frame.pack(fill='x', pady=5)
        tk.Label(sender_frame, text="المرسل:", font=('Arial', 12), bg='white', width=15, anchor='e').pack(side='right')
        self.sender_entry = tk.Entry(sender_frame, font=('Arial', 10), width=40)
        self.sender_entry.pack(side='right', padx=(5, 0))
        
        receiver_frame = tk.Frame(main_frame, bg='white')
        receiver_frame.pack(fill='x', pady=5)
        tk.Label(receiver_frame, text="المستقبل:", font=('Arial', 12), bg='white', width=15, anchor='e').pack(side='right')
        self.receiver_entry = tk.Entry(receiver_frame, font=('Arial', 10), width=40)
        self.receiver_entry.pack(side='right', padx=(5, 0))
        
        # الموضوع
        subject_frame = tk.Frame(main_frame, bg='white')
        subject_frame.pack(fill='x', pady=5)
        tk.Label(subject_frame, text="الموضوع:", font=('Arial', 12), bg='white', width=15, anchor='e').pack(side='right')
        self.subject_entry = tk.Entry(subject_frame, font=('Arial', 10), width=40)
        self.subject_entry.pack(side='right', padx=(5, 0))
        
        # تواريخ الإرسال والاستلام
        date_sent_frame = tk.Frame(main_frame, bg='white')
        date_sent_frame.pack(fill='x', pady=5)
        tk.Label(date_sent_frame, text="تاريخ الإرسال:", font=('Arial', 12), bg='white', width=15, anchor='e').pack(side='right')
        self.date_sent_entry = tk.Entry(date_sent_frame, font=('Arial', 10), width=40)
        self.date_sent_entry.pack(side='right', padx=(5, 0))
        
        date_received_frame = tk.Frame(main_frame, bg='white')
        date_received_frame.pack(fill='x', pady=5)
        tk.Label(date_received_frame, text="تاريخ الاستلام:", font=('Arial', 12), bg='white', width=15, anchor='e').pack(side='right')
        self.date_received_entry = tk.Entry(date_received_frame, font=('Arial', 10), width=40)
        self.date_received_entry.pack(side='right', padx=(5, 0))
        
        # محتوى المراسلة
        tk.Label(main_frame, text="محتوى المراسلة:", font=('Arial', 12), bg='white', anchor='e').pack(anchor='e', pady=(10, 5))
        self.content_text = tk.Text(main_frame, height=6, width=50, font=('Arial', 10))
        self.content_text.pack(pady=5)
        
        # الرد
        tk.Label(main_frame, text="الرد:", font=('Arial', 12), bg='white', anchor='e').pack(anchor='e', pady=(10, 5))
        self.response_text = tk.Text(main_frame, height=4, width=50, font=('Arial', 10))
        self.response_text.pack(pady=5)
        
        # تاريخ الرد
        response_date_frame = tk.Frame(main_frame, bg='white')
        response_date_frame.pack(fill='x', pady=5)
        tk.Label(response_date_frame, text="تاريخ الرد:", font=('Arial', 12), bg='white', width=15, anchor='e').pack(side='right')
        self.response_date_entry = tk.Entry(response_date_frame, font=('Arial', 10), width=40)
        self.response_date_entry.pack(side='right', padx=(5, 0))
        
        # أزرار العمليات
        buttons_frame = tk.Frame(main_frame, bg='white')
        buttons_frame.pack(pady=20)
        
        tk.Button(buttons_frame, text="حفظ", command=self.save,
                 font=('Arial', 12), width=10, bg='#27ae60', fg='white').pack(side='right', padx=5)
        tk.Button(buttons_frame, text="إلغاء", command=self.cancel,
                 font=('Arial', 12), width=10, bg='#e74c3c', fg='white').pack(side='right')
    
    def load_issues(self):
        """تحميل قائمة المشاكل"""
        query = """
            SELECT i.id, i.title, c.name 
            FROM issues i 
            LEFT JOIN customers c ON i.customer_id = c.id 
            ORDER BY i.created_date DESC
        """
        issues = db.execute_query(query)
        
        issue_list = [f"{issue[0]} - {issue[1]} ({issue[2]})" for issue in issues]
        self.issue_combo['values'] = issue_list
        self.issues_data = {f"{issue[0]} - {issue[1]} ({issue[2]})": issue[0] for issue in issues}
    
    def save(self):
        """حفظ البيانات"""
        if not self.issue_var.get() or not self.corr_num_entry.get().strip():
            messagebox.showerror("خطأ", "يجب اختيار المشكلة وإدخال رقم المراسلة")
            return
        
        try:
            issue_id = self.issues_data[self.issue_var.get()]
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            data = {
                'issue_id': issue_id,
                'correspondence_number': self.corr_num_entry.get().strip(),
                'sender': self.sender_entry.get().strip(),
                'receiver': self.receiver_entry.get().strip(),
                'subject': self.subject_entry.get().strip(),
                'date_sent': self.date_sent_entry.get().strip(),
                'date_received': self.date_received_entry.get().strip(),
                'content': self.content_text.get('1.0', 'end-1c').strip(),
                'response_content': self.response_text.get('1.0', 'end-1c').strip(),
                'response_date': self.response_date_entry.get().strip()
            }
            
            if self.correspondence_data:  # تحديث
                query = """
                    UPDATE correspondences SET issue_id=?, correspondence_number=?, sender=?, 
                           receiver=?, subject=?, date_sent=?, date_received=?, content=?, 
                           response_content=?, response_date=?
                    WHERE id=?
                """
                params = tuple(data.values()) + (self.correspondence_data[0],)
            else:  # إضافة جديد
                query = """
                    INSERT INTO correspondences (issue_id, correspondence_number, sender, receiver, 
                                               subject, date_sent, date_received, content, 
                                               response_content, response_date, created_date, created_by)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """
                params = tuple(data.values()) + (current_time, "المدير")
            
            db.execute_query(query, params)
            
            action = "تحديث" if self.correspondence_data else "إضافة"
            db.log_audit("correspondences", self.correspondence_data[0] if self.correspondence_data else None,
                        action, self.correspondence_data, data, "المدير")
            
            self.result = "success"
            self.dialog.destroy()
            
        except Exception as e:
            messagebox.showerror("خطأ", f"فشل في حفظ البيانات: {str(e)}")
    
    def cancel(self):
        """إلغاء العملية"""
        self.dialog.destroy()

class AttachmentDialog:
    def __init__(self, parent, issue_id=None):
        self.parent = parent
        self.issue_id = issue_id
        self.result = None
        self.file_manager = FileManager()
        
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("إضافة مرفق جديد")
        self.dialog.geometry("400x300")
        self.dialog.resizable(False, False)
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        self.create_widgets()
        self.dialog.geometry("+%d+%d" % (parent.winfo_rootx() + 50, parent.winfo_rooty() + 50))
    
    def create_widgets(self):
        """إنشاء عناصر النافذة"""
        main_frame = tk.Frame(self.dialog, bg='white', padx=20, pady=20)
        main_frame.pack(fill='both', expand=True)
        
        tk.Label(main_frame, text="إضافة مرفق جديد", font=('Arial', 16, 'bold'), bg='white').pack(pady=(0, 20))
        
        # اختيار المشكلة
        issue_frame = tk.Frame(main_frame, bg='white')
        issue_frame.pack(fill='x', pady=5)
        tk.Label(issue_frame, text="المشكلة:", font=('Arial', 12), bg='white', width=15, anchor='e').pack(side='right')
        
        self.issue_var = tk.StringVar()
        self.issue_combo = ttk.Combobox(issue_frame, textvariable=self.issue_var, width=30, state='readonly')
        self.issue_combo.pack(side='right', padx=(5, 0))
        self.load_issues()
        
        if self.issue_id:
            # تحديد المشكلة المختارة مسبقاً
            for item in self.issue_combo['values']:
                if item.startswith(str(self.issue_id)):
                    self.issue_var.set(item)
                    break
        
        # وصف المرفق
        desc_frame = tk.Frame(main_frame, bg='white')
        desc_frame.pack(fill='x', pady=5)
        tk.Label(desc_frame, text="وصف المرفق:", font=('Arial', 12), bg='white', width=15, anchor='e').pack(side='right')
        self.desc_entry = tk.Entry(desc_frame, font=('Arial', 10), width=30)
        self.desc_entry.pack(side='right', padx=(5, 0))
        
        # معلومات الملف المختار
        self.file_info_frame = tk.Frame(main_frame, bg='white')
        self.file_info_frame.pack(fill='x', pady=10)
        
        self.file_label = tk.Label(self.file_info_frame, text="لم يتم اختيار ملف", 
                                  font=('Arial', 10), bg='white', fg='gray')
        self.file_label.pack()
        
        # زر اختيار الملف
        tk.Button(main_frame, text="اختيار ملف", command=self.choose_file,
                 font=('Arial', 12), width=15, bg='#3498db', fg='white').pack(pady=10)
        
        # أزرار العمليات
        buttons_frame = tk.Frame(main_frame, bg='white')
        buttons_frame.pack(pady=20)
        
        self.save_button = tk.Button(buttons_frame, text="حفظ", command=self.save,
                                    font=('Arial', 12), width=10, bg='#27ae60', fg='white', state='disabled')
        self.save_button.pack(side='right', padx=5)
        
        tk.Button(buttons_frame, text="إلغاء", command=self.cancel,
                 font=('Arial', 12), width=10, bg='#e74c3c', fg='white').pack(side='right')
        
        self.selected_file = None
    
    def load_issues(self):
        """تحميل قائمة المشاكل"""
        query = """
            SELECT i.id, i.title, c.name, c.subscriber_number
            FROM issues i 
            LEFT JOIN customers c ON i.customer_id = c.id 
            ORDER BY i.created_date DESC
        """
        issues = db.execute_query(query)
        
        issue_list = [f"{issue[0]} - {issue[1]} ({issue[3]})" for issue in issues]
        self.issue_combo['values'] = issue_list
        self.issues_data = {f"{issue[0]} - {issue[1]} ({issue[3]})": (issue[0], issue[3]) for issue in issues}
    
    def choose_file(self):
        """اختيار ملف"""
        file_path = filedialog.askopenfilename(
            title="اختر الملف",
            filetypes=[
                ("ملفات الصور", "*.jpg *.jpeg *.png *.gif *.bmp"),
                ("ملفات PDF", "*.pdf"),
                ("جميع الملفات", "*.*")
            ]
        )
        
        if file_path:
            self.selected_file = file_path
            file_name = file_path.split('/')[-1]
            self.file_label.config(text=f"الملف المختار: {file_name}", fg='green')
            self.save_button.config(state='normal')
    
    def save(self):
        """حفظ المرفق"""
        if not self.issue_var.get() or not self.selected_file:
            messagebox.showerror("خطأ", "يجب اختيار المشكلة والملف")
            return
        
        try:
            issue_id, subscriber_number = self.issues_data[self.issue_var.get()]
            
            # نسخ الملف
            file_info = self.file_manager.copy_file_to_customer_folder(self.selected_file, subscriber_number, self.desc_entry.get().strip())
            
            if not file_info:
                return
            
            # حفظ في قاعدة البيانات
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            query = """
                INSERT INTO attachments (issue_id, file_name, file_path, file_type, 
                                       description, upload_date, uploaded_by)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """
            params = (issue_id, file_info['original_name'], file_info['path'], 
                     file_info['type'], file_info['description'], current_time, "المدير")
            
            db.execute_query(query, params)
            
            db.log_audit("attachments", None, "إضافة", None, file_info, "المدير")
            
            self.result = "success"
            messagebox.showinfo("نجح", "تم إضافة المرفق بنجاح")
            self.dialog.destroy()
            
        except Exception as e:
            messagebox.showerror("خطأ", f"فشل في حفظ المرفق: {str(e)}")
    
    def cancel(self):
        """إلغاء العملية"""
        self.dialog.destroy()