import os
import shutil
from datetime import datetime

try:
    import tkinter.filedialog as filedialog
    import tkinter.messagebox as messagebox
    TKINTER_AVAILABLE = True
except ImportError:
    TKINTER_AVAILABLE = False
    filedialog = None
    messagebox = None

class FileManager:
    def __init__(self, base_path="d:/test"):
        self.base_path = base_path
        self.ensure_base_directory()
    
    def ensure_base_directory(self):
        """التأكد من وجود المجلد الأساسي"""
        if not os.path.exists(self.base_path):
            os.makedirs(self.base_path)
    
    def create_customer_folder(self, subscriber_number):
        """إنشاء مجلد للعميل"""
        customer_folder = os.path.join(self.base_path, subscriber_number)
        if not os.path.exists(customer_folder):
            os.makedirs(customer_folder)
        return customer_folder
    
    def add_attachment(self, subscriber_number, description=""):
        """إضافة مرفق جديد"""
        if not TKINTER_AVAILABLE:
            print("تحذير: tkinter غير متوفر. استخدم copy_file_to_customer_folder مباشرة")
            return None
            
        # اختيار الملف
        file_path = filedialog.askopenfilename(
            title="اختر الملف",
            filetypes=[
                ("ملفات الصور", "*.jpg *.jpeg *.png *.gif *.bmp"),
                ("ملفات PDF", "*.pdf"),
                ("جميع الملفات", "*.*")
            ]
        )
        
        if not file_path:
            return None
        
        return self.copy_file_to_customer_folder(file_path, subscriber_number, description)
    
    def copy_file_to_customer_folder(self, file_path, subscriber_number, description=""):
        """نسخ ملف إلى مجلد العميل"""
        if not file_path or not os.path.exists(file_path):
            return None
        
        # إنشاء مجلد العميل
        customer_folder = self.create_customer_folder(subscriber_number)
        
        # الحصول على اسم الملف
        file_name = os.path.basename(file_path)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        new_file_name = f"{timestamp}_{file_name}"
        new_file_path = os.path.join(customer_folder, new_file_name)
        
        try:
            # نسخ الملف
            shutil.copy2(file_path, new_file_path)
            
            return {
                'original_name': file_name,
                'new_name': new_file_name,
                'path': new_file_path,
                'type': self.get_file_type(file_name),
                'description': description
            }
        except Exception as e:
            error_msg = f"فشل في نسخ الملف: {str(e)}"
            if TKINTER_AVAILABLE and messagebox:
                messagebox.showerror("خطأ", error_msg)
            else:
                print(f"خطأ: {error_msg}")
            return None
    
    def get_file_type(self, file_name):
        """تحديد نوع الملف"""
        extension = os.path.splitext(file_name)[1].lower()
        
        if extension in ['.jpg', '.jpeg', '.png', '.gif', '.bmp']:
            return 'صورة'
        elif extension == '.pdf':
            return 'PDF'
        else:
            return 'آخر'
    
    def open_customer_folder(self, subscriber_number):
        """فتح مجلد العميل"""
        customer_folder = os.path.join(self.base_path, subscriber_number)
        
        if os.path.exists(customer_folder):
            try:
                os.startfile(customer_folder)  # لنظام Windows
            except:
                try:
                    os.system(f'xdg-open "{customer_folder}"')  # لنظام Linux
                except:
                    info_msg = f"مسار المجلد: {customer_folder}"
                    if TKINTER_AVAILABLE and messagebox:
                        messagebox.showinfo("معلومات", info_msg)
                    else:
                        print(f"معلومات: {info_msg}")
        else:
            warning_msg = "مجلد العميل غير موجود"
            if TKINTER_AVAILABLE and messagebox:
                messagebox.showwarning("تحذير", warning_msg)
            else:
                print(f"تحذير: {warning_msg}")
    
    def open_file(self, file_path):
        """فتح ملف"""
        if os.path.exists(file_path):
            try:
                os.startfile(file_path)  # لنظام Windows
            except:
                try:
                    os.system(f'xdg-open "{file_path}"')  # لنظام Linux
                except:
                    info_msg = f"مسار الملف: {file_path}"
                    if TKINTER_AVAILABLE and messagebox:
                        messagebox.showinfo("معلومات", info_msg)
                    else:
                        print(f"معلومات: {info_msg}")
        else:
            error_msg = "الملف غير موجود"
            if TKINTER_AVAILABLE and messagebox:
                messagebox.showerror("خطأ", error_msg)
            else:
                print(f"خطأ: {error_msg}")
    
    def delete_file(self, file_path):
        """حذف ملف"""
        if os.path.exists(file_path):
            try:
                os.remove(file_path)
                return True
            except Exception as e:
                error_msg = f"فشل في حذف الملف: {str(e)}"
                if TKINTER_AVAILABLE and messagebox:
                    messagebox.showerror("خطأ", error_msg)
                else:
                    print(f"خطأ: {error_msg}")
                return False
        return False
    
    def get_file_size(self, file_path):
        """الحصول على حجم الملف"""
        if os.path.exists(file_path):
            size_bytes = os.path.getsize(file_path)
            
            if size_bytes < 1024:
                return f"{size_bytes} بايت"
            elif size_bytes < 1024 * 1024:
                return f"{size_bytes / 1024:.1f} كيلوبايت"
            else:
                return f"{size_bytes / (1024 * 1024):.1f} ميجابايت"
        return "غير معروف"