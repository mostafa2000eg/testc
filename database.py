import sqlite3
import os
from datetime import datetime

class Database:
    def __init__(self, db_name="customer_issues.db"):
        self.db_name = db_name
        self.init_database()
    
    def init_database(self):
        """إنشاء قاعدة البيانات والجداول"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        # جدول العملاء
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS customers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                subscriber_number TEXT UNIQUE NOT NULL,
                name TEXT NOT NULL,
                address TEXT NOT NULL,
                phone TEXT,
                last_reading REAL,
                last_reading_date TEXT,
                debt_amount REAL DEFAULT 0,
                created_date TEXT,
                modified_date TEXT,
                created_by TEXT,
                modified_by TEXT
            )
        ''')
        
        # جدول تصنيفات المشاكل
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS issue_categories (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                category_name TEXT UNIQUE NOT NULL,
                description TEXT
            )
        ''')
        
        # جدول المشاكل
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS issues (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                customer_id INTEGER,
                category_id INTEGER,
                title TEXT NOT NULL,
                description TEXT,
                status TEXT DEFAULT 'مفتوحة',
                priority TEXT DEFAULT 'متوسطة',
                responsible_employee TEXT,
                created_date TEXT,
                modified_date TEXT,
                created_by TEXT,
                modified_by TEXT,
                FOREIGN KEY (customer_id) REFERENCES customers (id),
                FOREIGN KEY (category_id) REFERENCES issue_categories (id)
            )
        ''')
        
        # جدول المراسلات
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS correspondences (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                issue_id INTEGER,
                correspondence_number TEXT,
                sender TEXT,
                receiver TEXT,
                subject TEXT,
                content TEXT,
                date_sent TEXT,
                date_received TEXT,
                response_content TEXT,
                response_date TEXT,
                created_date TEXT,
                created_by TEXT,
                FOREIGN KEY (issue_id) REFERENCES issues (id)
            )
        ''')
        
        # جدول المرفقات
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS attachments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                issue_id INTEGER,
                file_name TEXT NOT NULL,
                file_path TEXT NOT NULL,
                file_type TEXT,
                description TEXT,
                upload_date TEXT,
                uploaded_by TEXT,
                FOREIGN KEY (issue_id) REFERENCES issues (id)
            )
        ''')
        
        # جدول سجل التعديلات
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS audit_log (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                table_name TEXT,
                record_id INTEGER,
                action TEXT,
                old_values TEXT,
                new_values TEXT,
                user_name TEXT,
                timestamp TEXT
            )
        ''')
        
        # إدخال تصنيفات المشاكل الافتراضية
        default_categories = [
            ('حالة عبث بالعداد', 'التلاعب في قراءات العداد أو كسره'),
            ('حالة توصيلات غير شرعية', 'توصيلات غاز غير مرخصة'),
            ('حالة خطأ قراءة', 'خطأ في قراءة العداد'),
            ('شكوى عامة', 'شكاوى عامة من العملاء'),
            ('طلب صيانة', 'طلبات صيانة العدادات'),
            ('مشكلة فنية', 'مشاكل فنية في التوصيلات')
        ]
        
        cursor.executemany('''
            INSERT OR IGNORE INTO issue_categories (category_name, description)
            VALUES (?, ?)
        ''', default_categories)
        
        conn.commit()
        conn.close()
    
    def get_connection(self):
        """الحصول على اتصال بقاعدة البيانات"""
        return sqlite3.connect(self.db_name)
    
    def execute_query(self, query, params=None):
        """تنفيذ استعلام قاعدة بيانات"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        
        result = cursor.fetchall()
        conn.commit()
        conn.close()
        
        return result
    
    def log_audit(self, table_name, record_id, action, old_values, new_values, user_name):
        """تسجيل عملية في سجل التدقيق"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO audit_log (table_name, record_id, action, old_values, new_values, user_name, timestamp)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (table_name, record_id, action, str(old_values), str(new_values), user_name, timestamp))
        
        conn.commit()
        conn.close()

# إنشاء مثيل قاعدة البيانات
db = Database()