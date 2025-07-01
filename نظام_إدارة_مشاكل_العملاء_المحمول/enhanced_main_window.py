import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from datetime import datetime
import os
from enhanced_database import enhanced_db
from enhanced_file_manager import EnhancedFileManager

class EnhancedMainWindow:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("نظام إدارة مشاكل العملاء - النسخة المحسنة")
        self.root.geometry("1400x900")
        self.root.configure(bg='#f8f9fa')
        
        # إعداد الخطوط
        self.setup_fonts()
        
        # المتغيرات
        self.file_manager = EnhancedFileManager()
        self.current_case_id = None
        self.cases_data = []
        self.filtered_cases = []
        
        # إنشاء الواجهة
        self.create_main_layout()
        self.load_initial_data()
        
        # ربط أحداث الإغلاق
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
    
    def setup_fonts(self):
        """إعداد الخطوط"""
        self.fonts = {
            'header': ('Arial', 16, 'bold'),
            'subheader': ('Arial', 12, 'bold'),
            'normal': ('Arial', 10),
            'small': ('Arial', 9),
            'button': ('Arial', 10, 'bold')
        }
    
    def create_main_layout(self):
        """إنشاء التخطيط الرئيسي"""
        # الإطار الرئيسي
        main_frame = tk.Frame(self.root, bg='#f8f9fa')
        main_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # اللوحة الجانبية (يمين)
        self.create_sidebar(main_frame)
        
        # فاصل
        separator = ttk.Separator(main_frame, orient='vertical')
        separator.pack(side='right', fill='y', padx=5)
        
        # منطقة العرض الرئيسية (يسار)
        self.create_main_display(main_frame)
    
    def create_sidebar(self, parent):
        """إنشاء اللوحة الجانبية"""
        # الإطار الجانبي
        sidebar_frame = tk.Frame(parent, bg='#ffffff', width=400, relief='raised', bd=1)
        sidebar_frame.pack(side='right', fill='y', padx=(0, 5))
        sidebar_frame.pack_propagate(False)
        
        # عنوان اللوحة الجانبية
        header_frame = tk.Frame(sidebar_frame, bg='#2c3e50', height=50)
        header_frame.pack(fill='x')
        header_frame.pack_propagate(False)
        
        header_label = tk.Label(header_frame, text="قائمة الحالات", 
                               font=self.fonts['header'], fg='white', bg='#2c3e50')
        header_label.pack(expand=True)
        
        # أزرار الإجراءات
        self.create_action_buttons(sidebar_frame)
        
        # أدوات البحث والفلترة
        self.create_search_filters(sidebar_frame)
        
        # قائمة الحالات
        self.create_cases_list(sidebar_frame)
    
    def create_action_buttons(self, parent):
        """إنشاء أزرار الإجراءات"""
        buttons_frame = tk.Frame(parent, bg='#ffffff')
        buttons_frame.pack(fill='x', padx=10, pady=10)
        
        # زر إضافة حالة جديدة
        add_case_btn = tk.Button(buttons_frame, text="+ إضافة حالة جديدة",
                                command=self.add_new_case,
                                font=self.fonts['button'], bg='#27ae60', fg='white',
                                relief='flat', padx=20, pady=10)
        add_case_btn.pack(fill='x', pady=(0, 5))
        
        # زر إدارة الموظفين
        manage_emp_btn = tk.Button(buttons_frame, text="👥 إدارة الموظفين",
                                  command=self.manage_employees,
                                  font=self.fonts['button'], bg='#3498db', fg='white',
                                  relief='flat', padx=20, pady=10)
        manage_emp_btn.pack(fill='x')
    
    def create_search_filters(self, parent):
        """إنشاء أدوات البحث والفلترة"""
        filters_frame = tk.Frame(parent, bg='#ffffff')
        filters_frame.pack(fill='x', padx=10, pady=10)
        
        # فلترة السنة
        year_frame = tk.Frame(filters_frame, bg='#ffffff')
        year_frame.pack(fill='x', pady=(0, 10))
        
        tk.Label(year_frame, text="السنة:", font=self.fonts['normal'], bg='#ffffff').pack(side='right')
        
        self.year_var = tk.StringVar(value="الكل")
        self.year_combo = ttk.Combobox(year_frame, textvariable=self.year_var, 
                                      state='readonly', width=15)
        self.year_combo.pack(side='right', padx=(5, 0))
        self.year_combo.bind('<<ComboboxSelected>>', self.filter_by_year)
        
        # البحث المتقدم
        search_frame = tk.Frame(filters_frame, bg='#ffffff')
        search_frame.pack(fill='x')
        
        tk.Label(search_frame, text="البحث:", font=self.fonts['normal'], bg='#ffffff').pack(anchor='e')
        
        # نوع البحث
        search_type_frame = tk.Frame(search_frame, bg='#ffffff')
        search_type_frame.pack(fill='x', pady=(5, 0))
        
        self.search_type_var = tk.StringVar(value="شامل")
        self.search_type_combo = ttk.Combobox(search_type_frame, textvariable=self.search_type_var,
                                             state='readonly', width=18)
        self.search_type_combo['values'] = [
            "شامل", "اسم العميل", "رقم المشترك", "العنوان", 
            "تصنيف المشكلة", "حالة المشكلة", "اسم الموظف"
        ]
        self.search_type_combo.pack(fill='x')
        self.search_type_combo.bind('<<ComboboxSelected>>', self.on_search_type_change)
        
        # حقل البحث
        search_input_frame = tk.Frame(search_frame, bg='#ffffff')
        search_input_frame.pack(fill='x', pady=(5, 0))
        
        self.search_value_var = tk.StringVar()
        self.search_entry = tk.Entry(search_input_frame, textvariable=self.search_value_var,
                                    font=self.fonts['normal'])
        self.search_entry.pack(fill='x')
        self.search_entry.bind('<KeyRelease>', self.perform_search)
        
        # سيتم إنشاء الكومبو بوكس ديناميكياً حسب نوع البحث
        self.search_combo = None
    
    def create_cases_list(self, parent):
        """إنشاء قائمة الحالات"""
        list_frame = tk.Frame(parent, bg='#ffffff')
        list_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # إطار القائمة مع سكرول
        list_canvas = tk.Canvas(list_frame, bg='#ffffff', highlightthickness=0)
        scrollbar = ttk.Scrollbar(list_frame, orient="vertical", command=list_canvas.yview)
        self.scrollable_frame = tk.Frame(list_canvas, bg='#ffffff')
        
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: list_canvas.configure(scrollregion=list_canvas.bbox("all"))
        )
        
        list_canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        list_canvas.configure(yscrollcommand=scrollbar.set)
        
        list_canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # حفظ المراجع
        self.cases_canvas = list_canvas
        self.cases_scrollbar = scrollbar
    
    def create_main_display(self, parent):
        """إنشاء منطقة العرض الرئيسية"""
        # الإطار الرئيسي للعرض
        display_frame = tk.Frame(parent, bg='#ffffff', relief='raised', bd=1)
        display_frame.pack(side='left', fill='both', expand=True)
        
        # رأس العرض
        self.create_display_header(display_frame)
        
        # أزرار العمليات
        self.create_display_buttons(display_frame)
        
        # نظام التبويبات
        self.create_tabs(display_frame)
    
    def create_display_header(self, parent):
        """إنشاء رأس العرض"""
        header_frame = tk.Frame(parent, bg='#34495e', height=80)
        header_frame.pack(fill='x')
        header_frame.pack_propagate(False)
        
        # اسم العميل
        self.customer_name_label = tk.Label(header_frame, text="اختر حالة من القائمة",
                                           font=('Arial', 18, 'bold'), fg='white', bg='#34495e')
        self.customer_name_label.pack(expand=True, pady=(10, 0))
        
        # الموظف المسؤول عن الحل
        self.solved_by_label = tk.Label(header_frame, text="",
                                       font=self.fonts['normal'], fg='#bdc3c7', bg='#34495e')
        self.solved_by_label.pack(pady=(0, 10))
    
    def create_display_buttons(self, parent):
        """إنشاء أزرار العمليات"""
        buttons_frame = tk.Frame(parent, bg='#ecf0f1', height=60)
        buttons_frame.pack(fill='x')
        buttons_frame.pack_propagate(False)
        
        # زر حفظ التغييرات
        self.save_btn = tk.Button(buttons_frame, text="💾 حفظ التغييرات",
                                 command=self.save_changes,
                                 font=self.fonts['button'], bg='#27ae60', fg='white',
                                 relief='flat', padx=20, pady=8, state='disabled')
        self.save_btn.pack(side='right', padx=10, pady=10)
        
        # زر طباعة
        self.print_btn = tk.Button(buttons_frame, text="🖨️ طباعة",
                                  command=self.print_case,
                                  font=self.fonts['button'], bg='#3498db', fg='white',
                                  relief='flat', padx=20, pady=8, state='disabled')
        self.print_btn.pack(side='right', padx=(0, 10), pady=10)
    
    def create_tabs(self, parent):
        """إنشاء نظام التبويبات"""
        # إطار التبويبات
        tabs_frame = tk.Frame(parent, bg='#ffffff')
        tabs_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # نوت بوك التبويبات
        self.notebook = ttk.Notebook(tabs_frame)
        self.notebook.pack(fill='both', expand=True)
        
        # التبويبات
        self.create_basic_data_tab()
        self.create_attachments_tab()
        self.create_correspondences_tab()
        self.create_audit_log_tab()
    
    def create_basic_data_tab(self):
        """إنشاء تبويب البيانات الأساسية"""
        basic_frame = ttk.Frame(self.notebook)
        self.notebook.add(basic_frame, text="البيانات الأساسية")
        
        # إطار للمحتوى مع سكرول
        canvas = tk.Canvas(basic_frame, bg='#ffffff')
        scrollbar = ttk.Scrollbar(basic_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg='#ffffff')
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # الحقول
        fields_frame = tk.Frame(scrollable_frame, bg='#ffffff')
        fields_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # بيانات العميل
        customer_section = tk.LabelFrame(fields_frame, text="بيانات العميل", 
                                        font=self.fonts['subheader'], bg='#ffffff')
        customer_section.pack(fill='x', pady=(0, 20))
        
        # اسم العميل
        self.create_field(customer_section, "اسم العميل:", "customer_name", row=0)
        
        # رقم المشترك
        self.create_field(customer_section, "رقم المشترك:", "subscriber_number", row=1)
        
        # رقم الهاتف
        self.create_field(customer_section, "رقم الهاتف:", "phone", row=2)
        
        # العنوان
        self.create_text_field(customer_section, "العنوان:", "address", row=3, height=3)
        
        # بيانات المشكلة
        problem_section = tk.LabelFrame(fields_frame, text="بيانات المشكلة", 
                                       font=self.fonts['subheader'], bg='#ffffff')
        problem_section.pack(fill='x', pady=(0, 20))
        
        # تصنيف المشكلة
        self.create_combo_field(problem_section, "تصنيف المشكلة:", "category", row=0)
        
        # حالة المشكلة
        self.create_combo_field(problem_section, "حالة المشكلة:", "status", row=1)
        
        # وصف المشكلة
        self.create_text_field(problem_section, "وصف المشكلة:", "problem_description", row=2, height=4)
        
        # ما تم تنفيذه
        self.create_text_field(problem_section, "ما تم تنفيذه:", "actions_taken", row=3, height=4)
        
        # بيانات العداد والمديونية
        meter_section = tk.LabelFrame(fields_frame, text="بيانات العداد والمديونية", 
                                     font=self.fonts['subheader'], bg='#ffffff')
        meter_section.pack(fill='x')
        
        # آخر قراءة
        self.create_field(meter_section, "آخر قراءة للعداد:", "last_meter_reading", row=0)
        
        # تاريخ آخر قراءة
        self.create_field(meter_section, "تاريخ آخر قراءة:", "last_reading_date", row=1)
        
        # المديونية
        self.create_field(meter_section, "المديونية:", "debt_amount", row=2)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # حفظ المراجع
        self.basic_data_widgets = {}
    
    def create_field(self, parent, label_text, field_name, row, column=0, width=30):
        """إنشاء حقل إدخال عادي"""
        label = tk.Label(parent, text=label_text, font=self.fonts['normal'], bg='#ffffff')
        label.grid(row=row, column=column*2, sticky='e', padx=(10, 5), pady=5)
        
        entry = tk.Entry(parent, font=self.fonts['normal'], width=width)
        entry.grid(row=row, column=column*2+1, sticky='w', padx=(0, 10), pady=5)
        
        self.basic_data_widgets[field_name] = entry
        return entry
    
    def create_text_field(self, parent, label_text, field_name, row, height=3, width=40):
        """إنشاء حقل نص متعدد الأسطر"""
        label = tk.Label(parent, text=label_text, font=self.fonts['normal'], bg='#ffffff')
        label.grid(row=row, column=0, sticky='ne', padx=(10, 5), pady=5)
        
        text_frame = tk.Frame(parent, bg='#ffffff')
        text_frame.grid(row=row, column=1, sticky='w', padx=(0, 10), pady=5)
        
        text_widget = tk.Text(text_frame, font=self.fonts['normal'], width=width, height=height)
        text_scrollbar = ttk.Scrollbar(text_frame, orient="vertical", command=text_widget.yview)
        text_widget.configure(yscrollcommand=text_scrollbar.set)
        
        text_widget.pack(side="left", fill="both", expand=True)
        text_scrollbar.pack(side="right", fill="y")
        
        self.basic_data_widgets[field_name] = text_widget
        return text_widget
    
    def create_combo_field(self, parent, label_text, field_name, row, width=30):
        """إنشاء حقل قائمة منسدلة"""
        label = tk.Label(parent, text=label_text, font=self.fonts['normal'], bg='#ffffff')
        label.grid(row=row, column=0, sticky='e', padx=(10, 5), pady=5)
        
        combo = ttk.Combobox(parent, font=self.fonts['normal'], width=width-3, state='readonly')
        combo.grid(row=row, column=1, sticky='w', padx=(0, 10), pady=5)
        
        self.basic_data_widgets[field_name] = combo
        return combo
    
    def create_attachments_tab(self):
        """إنشاء تبويب المرفقات"""
        attachments_frame = ttk.Frame(self.notebook)
        self.notebook.add(attachments_frame, text="المرفقات")
        
        # أزرار المرفقات
        buttons_frame = tk.Frame(attachments_frame, bg='#ffffff')
        buttons_frame.pack(fill='x', padx=10, pady=10)
        
        add_attachment_btn = tk.Button(buttons_frame, text="📎 إضافة مرفق",
                                      command=self.add_attachment,
                                      font=self.fonts['button'], bg='#3498db', fg='white',
                                      relief='flat', padx=15, pady=8)
        add_attachment_btn.pack(side='right')
        
        # جدول المرفقات
        columns = ('ID', 'نوع الملف', 'اسم الملف', 'الوصف', 'تاريخ الرفع', 'الموظف')
        self.attachments_tree = ttk.Treeview(attachments_frame, columns=columns, show='headings', height=15)
        
        for col in columns:
            self.attachments_tree.heading(col, text=col)
            if col == 'ID':
                self.attachments_tree.column(col, width=50)
            elif col == 'نوع الملف':
                self.attachments_tree.column(col, width=80)
            else:
                self.attachments_tree.column(col, width=120)
        
        # سكرول بار للمرفقات
        attachments_scrollbar = ttk.Scrollbar(attachments_frame, orient='vertical', command=self.attachments_tree.yview)
        self.attachments_tree.configure(yscrollcommand=attachments_scrollbar.set)
        
        self.attachments_tree.pack(side='left', fill='both', expand=True, padx=(10, 0), pady=(0, 10))
        attachments_scrollbar.pack(side='right', fill='y', pady=(0, 10))
        
        # ربط النقر المزدوج
        self.attachments_tree.bind('<Double-1>', self.open_attachment)
        self.attachments_tree.bind('<Button-3>', self.show_attachment_context_menu)
    
    def create_correspondences_tab(self):
        """إنشاء تبويب المراسلات"""
        correspondences_frame = ttk.Frame(self.notebook)
        self.notebook.add(correspondences_frame, text="المراسلات")
        
        # أزرار المراسلات
        buttons_frame = tk.Frame(correspondences_frame, bg='#ffffff')
        buttons_frame.pack(fill='x', padx=10, pady=10)
        
        add_correspondence_btn = tk.Button(buttons_frame, text="✉️ إضافة مراسلة",
                                          command=self.add_correspondence,
                                          font=self.fonts['button'], bg='#e67e22', fg='white',
                                          relief='flat', padx=15, pady=8)
        add_correspondence_btn.pack(side='right')
        
        # جدول المراسلات
        columns = ('ID', 'رقم التسلسل', 'الرقم السنوي', 'المرسل', 'المحتوى', 'التاريخ', 'الموظف')
        self.correspondences_tree = ttk.Treeview(correspondences_frame, columns=columns, show='headings', height=15)
        
        for col in columns:
            self.correspondences_tree.heading(col, text=col)
            if col == 'ID':
                self.correspondences_tree.column(col, width=50)
            elif col in ['رقم التسلسل', 'الرقم السنوي']:
                self.correspondences_tree.column(col, width=80)
            else:
                self.correspondences_tree.column(col, width=120)
        
        # سكرول بار للمراسلات
        correspondences_scrollbar = ttk.Scrollbar(correspondences_frame, orient='vertical', command=self.correspondences_tree.yview)
        self.correspondences_tree.configure(yscrollcommand=correspondences_scrollbar.set)
        
        self.correspondences_tree.pack(side='left', fill='both', expand=True, padx=(10, 0), pady=(0, 10))
        correspondences_scrollbar.pack(side='right', fill='y', pady=(0, 10))
        
        # ربط النقر المزدوج
        self.correspondences_tree.bind('<Double-1>', self.edit_correspondence)
    
    def create_audit_log_tab(self):
        """إنشاء تبويب سجل التعديلات"""
        audit_frame = ttk.Frame(self.notebook)
        self.notebook.add(audit_frame, text="سجل التعديلات")
        
        # جدول سجل التعديلات
        columns = ('التاريخ والوقت', 'الموظف', 'نوع الإجراء', 'وصف الإجراء')
        self.audit_tree = ttk.Treeview(audit_frame, columns=columns, show='headings', height=20)
        
        for col in columns:
            self.audit_tree.heading(col, text=col)
            if col == 'التاريخ والوقت':
                self.audit_tree.column(col, width=150)
            elif col == 'الموظف':
                self.audit_tree.column(col, width=120)
            else:
                self.audit_tree.column(col, width=200)
        
        # سكرول بار لسجل التعديلات
        audit_scrollbar = ttk.Scrollbar(audit_frame, orient='vertical', command=self.audit_tree.yview)
        self.audit_tree.configure(yscrollcommand=audit_scrollbar.set)
        
        self.audit_tree.pack(side='left', fill='both', expand=True, padx=10, pady=10)
        audit_scrollbar.pack(side='right', fill='y', pady=10)
    
    # سأكمل باقي الوظائف في الجزء التالي...
    
    def run(self):
        """تشغيل التطبيق"""
        self.root.mainloop()

if __name__ == "__main__":
    app = EnhancedMainWindow()
    app.run()