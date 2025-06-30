import sqlite3
import os
from datetime import datetime

class EnhancedDatabase:
    def __init__(self, db_name="customer_issues_enhanced.db"):
        self.db_name = db_name
        self.init_database()
    
    def init_database(self):
        """إنشاء قاعدة البيانات والجداول المحسنة"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        # جدول الموظفين
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS employees (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE NOT NULL,
                position TEXT,
                created_date TEXT,
                is_active INTEGER DEFAULT 1
            )
        ''')
        
        # جدول تصنيفات المشاكل المحسن
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS issue_categories (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                category_name TEXT UNIQUE NOT NULL,
                description TEXT,
                color_code TEXT DEFAULT '#3498db'
            )
        ''')
        
        # جدول الحالات المحسن
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS cases (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                customer_name TEXT NOT NULL,
                subscriber_number TEXT NOT NULL,
                phone TEXT,
                address TEXT,
                category_id INTEGER,
                status TEXT DEFAULT 'جديدة',
                problem_description TEXT,
                actions_taken TEXT,
                last_meter_reading REAL,
                last_reading_date TEXT,
                debt_amount REAL DEFAULT 0,
                created_date TEXT,
                created_by INTEGER,
                modified_date TEXT,
                modified_by INTEGER,
                solved_by INTEGER,
                solved_date TEXT,
                FOREIGN KEY (category_id) REFERENCES issue_categories (id),
                FOREIGN KEY (created_by) REFERENCES employees (id),
                FOREIGN KEY (modified_by) REFERENCES employees (id),
                FOREIGN KEY (solved_by) REFERENCES employees (id)
            )
        ''')
        
        # جدول المراسلات المحسن
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS correspondences (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                case_id INTEGER,
                case_sequence_number INTEGER,
                yearly_sequence_number TEXT,
                sender TEXT,
                message_content TEXT,
                sent_date TEXT,
                created_by INTEGER,
                created_date TEXT,
                FOREIGN KEY (case_id) REFERENCES cases (id),
                FOREIGN KEY (created_by) REFERENCES employees (id)
            )
        ''')
        
        # جدول المرفقات المحسن
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS attachments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                case_id INTEGER,
                file_name TEXT NOT NULL,
                file_path TEXT NOT NULL,
                file_type TEXT,
                description TEXT,
                upload_date TEXT,
                uploaded_by INTEGER,
                FOREIGN KEY (case_id) REFERENCES cases (id),
                FOREIGN KEY (uploaded_by) REFERENCES employees (id)
            )
        ''')
        
        # جدول سجل التعديلات المحسن
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS audit_log (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                case_id INTEGER,
                action_type TEXT,
                action_description TEXT,
                performed_by INTEGER,
                timestamp TEXT,
                old_values TEXT,
                new_values TEXT,
                FOREIGN KEY (case_id) REFERENCES cases (id),
                FOREIGN KEY (performed_by) REFERENCES employees (id)
            )
        ''')
        
        # إدخال الموظفين الافتراضيين
        default_employees = [
            ('مدير النظام', 'مدير'),
            ('أحمد محمد', 'موظف خدمة عملاء'),
            ('فاطمة علي', 'مهندس صيانة'),
            ('محمد حسن', 'فني أول')
        ]
        
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        for emp_name, position in default_employees:
            cursor.execute('''
                INSERT OR IGNORE INTO employees (name, position, created_date)
                VALUES (?, ?, ?)
            ''', (emp_name, position, current_time))
        
        # إدخال تصنيفات المشاكل المحسنة
        enhanced_categories = [
            ('عبث بالعداد', 'التلاعب في قراءات العداد أو كسره', '#e74c3c'),
            ('توصيلات غير شرعية', 'توصيلات غاز غير مرخصة', '#e67e22'),
            ('خطأ قراءة', 'خطأ في قراءة العداد', '#f39c12'),
            ('مشكلة فواتير', 'مشاكل في الفواتير والمدفوعات', '#9b59b6'),
            ('تغيير نشاط', 'طلب تغيير نوع النشاط', '#3498db'),
            ('تصحيح رقم عداد', 'تصحيح أرقام العدادات', '#1abc9c'),
            ('نقل رقم مشترك', 'نقل الاشتراك لموقع آخر', '#2ecc71'),
            ('كسر بالشاشة', 'كسر أو تلف شاشة العداد', '#e74c3c'),
            ('عطل عداد', 'أعطال فنية في العداد', '#c0392b'),
            ('هدم وازالة', 'طلبات هدم أو إزالة التوصيلات', '#7f8c8d'),
            ('أخرى', 'مشاكل أخرى غير مصنفة', '#95a5a6')
        ]
        
        for cat_name, description, color in enhanced_categories:
            cursor.execute('''
                INSERT OR IGNORE INTO issue_categories (category_name, description, color_code)
                VALUES (?, ?, ?)
            ''', (cat_name, description, color))
        
        conn.commit()
        conn.close()
    
    def get_connection(self):
        """الحصول على اتصال بقاعدة البيانات"""
        return sqlite3.connect(self.db_name)
    
    def execute_query(self, query, params=None):
        """تنفيذ استعلام قاعدة بيانات"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            
            result = cursor.fetchall()
            conn.commit()
            return result
        except Exception as e:
            print(f"خطأ في قاعدة البيانات: {e}")
            return []
        finally:
            conn.close()
    
    def get_employees(self, active_only=True):
        """الحصول على قائمة الموظفين"""
        query = "SELECT id, name, position FROM employees"
        if active_only:
            query += " WHERE is_active = 1"
        query += " ORDER BY name"
        return self.execute_query(query)
    
    def add_employee(self, name, position="موظف"):
        """إضافة موظف جديد"""
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        query = "INSERT INTO employees (name, position, created_date) VALUES (?, ?, ?)"
        try:
            self.execute_query(query, (name, position, current_time))
            return True
        except:
            return False
    
    def delete_employee(self, employee_id):
        """حذف موظف (تعطيل)"""
        query = "UPDATE employees SET is_active = 0 WHERE id = ?"
        try:
            self.execute_query(query, (employee_id,))
            return True
        except:
            return False
    
    def get_cases_by_year(self, year=None):
        """الحصول على الحالات حسب السنة"""
        if year:
            query = """
                SELECT c.id, c.customer_name, c.subscriber_number, c.status, 
                       ic.category_name, ic.color_code, e.name as modified_by_name,
                       c.created_date, c.modified_date
                FROM cases c
                LEFT JOIN issue_categories ic ON c.category_id = ic.id
                LEFT JOIN employees e ON c.modified_by = e.id
                WHERE strftime('%Y', c.created_date) = ?
                ORDER BY c.modified_date DESC, c.created_date DESC
            """
            return self.execute_query(query, (str(year),))
        else:
            query = """
                SELECT c.id, c.customer_name, c.subscriber_number, c.status, 
                       ic.category_name, ic.color_code, e.name as modified_by_name,
                       c.created_date, c.modified_date
                FROM cases c
                LEFT JOIN issue_categories ic ON c.category_id = ic.id
                LEFT JOIN employees e ON c.modified_by = e.id
                ORDER BY c.modified_date DESC, c.created_date DESC
            """
            return self.execute_query(query)
    
    def search_cases(self, search_field, search_value):
        """البحث في الحالات"""
        if search_field == "شامل":
            query = """
                SELECT DISTINCT c.id, c.customer_name, c.subscriber_number, c.status, 
                       ic.category_name, ic.color_code, e.name as modified_by_name,
                       c.created_date, c.modified_date
                FROM cases c
                LEFT JOIN issue_categories ic ON c.category_id = ic.id
                LEFT JOIN employees e ON c.modified_by = e.id
                LEFT JOIN correspondences co ON c.id = co.case_id
                LEFT JOIN attachments a ON c.id = a.case_id
                WHERE c.customer_name LIKE ? OR c.subscriber_number LIKE ? 
                   OR c.address LIKE ? OR c.problem_description LIKE ?
                   OR c.actions_taken LIKE ? OR co.message_content LIKE ?
                   OR a.description LIKE ?
                ORDER BY c.modified_date DESC, c.created_date DESC
            """
            search_pattern = f"%{search_value}%"
            return self.execute_query(query, (search_pattern,) * 7)
        
        elif search_field == "اسم العميل":
            query = """
                SELECT c.id, c.customer_name, c.subscriber_number, c.status, 
                       ic.category_name, ic.color_code, e.name as modified_by_name,
                       c.created_date, c.modified_date
                FROM cases c
                LEFT JOIN issue_categories ic ON c.category_id = ic.id
                LEFT JOIN employees e ON c.modified_by = e.id
                WHERE c.customer_name LIKE ?
                ORDER BY c.modified_date DESC, c.created_date DESC
            """
            return self.execute_query(query, (f"%{search_value}%",))
        
        elif search_field == "رقم المشترك":
            query = """
                SELECT c.id, c.customer_name, c.subscriber_number, c.status, 
                       ic.category_name, ic.color_code, e.name as modified_by_name,
                       c.created_date, c.modified_date
                FROM cases c
                LEFT JOIN issue_categories ic ON c.category_id = ic.id
                LEFT JOIN employees e ON c.modified_by = e.id
                WHERE c.subscriber_number LIKE ?
                ORDER BY c.modified_date DESC, c.created_date DESC
            """
            return self.execute_query(query, (f"%{search_value}%",))
        
        elif search_field == "العنوان":
            query = """
                SELECT c.id, c.customer_name, c.subscriber_number, c.status, 
                       ic.category_name, ic.color_code, e.name as modified_by_name,
                       c.created_date, c.modified_date
                FROM cases c
                LEFT JOIN issue_categories ic ON c.category_id = ic.id
                LEFT JOIN employees e ON c.modified_by = e.id
                WHERE c.address LIKE ?
                ORDER BY c.modified_date DESC, c.created_date DESC
            """
            return self.execute_query(query, (f"%{search_value}%",))
        
        elif search_field == "تصنيف المشكلة":
            query = """
                SELECT c.id, c.customer_name, c.subscriber_number, c.status, 
                       ic.category_name, ic.color_code, e.name as modified_by_name,
                       c.created_date, c.modified_date
                FROM cases c
                LEFT JOIN issue_categories ic ON c.category_id = ic.id
                LEFT JOIN employees e ON c.modified_by = e.id
                WHERE ic.category_name = ?
                ORDER BY c.modified_date DESC, c.created_date DESC
            """
            return self.execute_query(query, (search_value,))
        
        elif search_field == "حالة المشكلة":
            query = """
                SELECT c.id, c.customer_name, c.subscriber_number, c.status, 
                       ic.category_name, ic.color_code, e.name as modified_by_name,
                       c.created_date, c.modified_date
                FROM cases c
                LEFT JOIN issue_categories ic ON c.category_id = ic.id
                LEFT JOIN employees e ON c.modified_by = e.id
                WHERE c.status = ?
                ORDER BY c.modified_date DESC, c.created_date DESC
            """
            return self.execute_query(query, (search_value,))
        
        elif search_field == "اسم الموظف":
            query = """
                SELECT c.id, c.customer_name, c.subscriber_number, c.status, 
                       ic.category_name, ic.color_code, e.name as modified_by_name,
                       c.created_date, c.modified_date
                FROM cases c
                LEFT JOIN issue_categories ic ON c.category_id = ic.id
                LEFT JOIN employees e ON c.modified_by = e.id
                WHERE e.name = ?
                ORDER BY c.modified_date DESC, c.created_date DESC
            """
            return self.execute_query(query, (search_value,))
        
        return []
    
    def get_case_details(self, case_id):
        """الحصول على تفاصيل حالة محددة"""
        query = """
            SELECT c.*, ic.category_name, ic.color_code,
                   creator.name as created_by_name,
                   modifier.name as modified_by_name,
                   solver.name as solved_by_name
            FROM cases c
            LEFT JOIN issue_categories ic ON c.category_id = ic.id
            LEFT JOIN employees creator ON c.created_by = creator.id
            LEFT JOIN employees modifier ON c.modified_by = modifier.id
            LEFT JOIN employees solver ON c.solved_by = solver.id
            WHERE c.id = ?
        """
        result = self.execute_query(query, (case_id,))
        return result[0] if result else None
    
    def get_case_correspondences(self, case_id):
        """الحصول على مراسلات الحالة"""
        query = """
            SELECT co.*, e.name as created_by_name
            FROM correspondences co
            LEFT JOIN employees e ON co.created_by = e.id
            WHERE co.case_id = ?
            ORDER BY co.sent_date DESC
        """
        return self.execute_query(query, (case_id,))
    
    def get_case_attachments(self, case_id):
        """الحصول على مرفقات الحالة"""
        query = """
            SELECT a.*, e.name as uploaded_by_name
            FROM attachments a
            LEFT JOIN employees e ON a.uploaded_by = e.id
            WHERE a.case_id = ?
            ORDER BY a.upload_date DESC
        """
        return self.execute_query(query, (case_id,))
    
    def get_case_audit_log(self, case_id):
        """الحصول على سجل تعديلات الحالة"""
        query = """
            SELECT al.*, e.name as performed_by_name
            FROM audit_log al
            LEFT JOIN employees e ON al.performed_by = e.id
            WHERE al.case_id = ?
            ORDER BY al.timestamp DESC
        """
        return self.execute_query(query, (case_id,))
    
    def get_categories(self):
        """الحصول على تصنيفات المشاكل"""
        query = "SELECT id, category_name, color_code FROM issue_categories ORDER BY category_name"
        return self.execute_query(query)
    
    def get_status_options(self):
        """الحصول على خيارات الحالة"""
        return [
            ('جديدة', '#3498db'),
            ('قيد التنفيذ', '#f39c12'), 
            ('تم حلها', '#27ae60'),
            ('مغلقة', '#95a5a6')
        ]
    
    def get_next_correspondence_numbers(self, case_id):
        """الحصول على أرقام المراسلة التالية"""
        # رقم تسلسلي خاص بالحالة
        case_seq_query = "SELECT COALESCE(MAX(case_sequence_number), 0) + 1 FROM correspondences WHERE case_id = ?"
        case_seq_result = self.execute_query(case_seq_query, (case_id,))
        case_sequence = case_seq_result[0][0] if case_seq_result else 1
        
        # رقم تسلسلي عام على مستوى السنة
        current_year = datetime.now().year
        yearly_seq_query = """
            SELECT COALESCE(MAX(CAST(SUBSTR(yearly_sequence_number, 1, INSTR(yearly_sequence_number, '-') - 1) AS INTEGER)), 0) + 1
            FROM correspondences 
            WHERE yearly_sequence_number LIKE ?
        """
        yearly_seq_result = self.execute_query(yearly_seq_query, (f"%-{current_year}",))
        yearly_sequence = yearly_seq_result[0][0] if yearly_seq_result and yearly_seq_result[0][0] else 1
        yearly_sequence_number = f"{yearly_sequence}-{current_year}"
        
        return case_sequence, yearly_sequence_number
    
    def log_action(self, case_id, action_type, action_description, performed_by, old_values=None, new_values=None):
        """تسجيل إجراء في سجل التعديلات"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        query = """
            INSERT INTO audit_log (case_id, action_type, action_description, performed_by, timestamp, old_values, new_values)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """
        self.execute_query(query, (case_id, action_type, action_description, performed_by, timestamp, str(old_values) if old_values else None, str(new_values) if new_values else None))

# إنشاء مثيل قاعدة البيانات المحسنة
enhanced_db = EnhancedDatabase()