from reportlab.lib.pagesizes import A4, letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib import colors
from reportlab.lib.enums import TA_RIGHT, TA_CENTER
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from datetime import datetime
import os

class ReportGenerator:
    def __init__(self):
        self.setup_fonts()
        self.styles = self.create_styles()
    
    def setup_fonts(self):
        """إعداد الخطوط العربية"""
        try:
            # محاولة تحميل خط عربي (يمكن تغييره حسب النظام)
            pdfmetrics.registerFont(TTFont('Arabic', 'arial.ttf'))
        except:
            # في حالة عدم وجود الخط، استخدام الخط الافتراضي
            pass
    
    def create_styles(self):
        """إنشاء أنماط النص"""
        styles = getSampleStyleSheet()
        
        # نمط النص العربي
        arabic_style = ParagraphStyle(
            'Arabic',
            parent=styles['Normal'],
            alignment=TA_RIGHT,
            fontSize=12,
            fontName='Arial'
        )
        
        # نمط العنوان العربي
        arabic_title = ParagraphStyle(
            'ArabicTitle',
            parent=styles['Title'],
            alignment=TA_CENTER,
            fontSize=18,
            fontName='Arial',
            spaceAfter=20
        )
        
        # نمط العنوان الفرعي
        arabic_heading = ParagraphStyle(
            'ArabicHeading',
            parent=styles['Heading1'],
            alignment=TA_RIGHT,
            fontSize=14,
            fontName='Arial',
            spaceBefore=12,
            spaceAfter=6
        )
        
        return {
            'arabic': arabic_style,
            'title': arabic_title,
            'heading': arabic_heading
        }
    
    def generate_customer_report(self, customer_data, issues_data, output_path):
        """إنتاج تقرير عميل"""
        doc = SimpleDocTemplate(output_path, pagesize=A4)
        story = []
        
        # العنوان الرئيسي
        title = Paragraph("تقرير العميل", self.styles['title'])
        story.append(title)
        story.append(Spacer(1, 20))
        
        # بيانات العميل
        story.append(Paragraph("بيانات العميل", self.styles['heading']))
        
        customer_info = [
            ["رقم المشترك:", customer_data.get('subscriber_number', '')],
            ["اسم العميل:", customer_data.get('name', '')],
            ["العنوان:", customer_data.get('address', '')],
            ["رقم الهاتف:", customer_data.get('phone', '')],
            ["آخر قراءة:", str(customer_data.get('last_reading', ''))],
            ["تاريخ آخر قراءة:", customer_data.get('last_reading_date', '')],
            ["المديونية:", f"{customer_data.get('debt_amount', 0)} جنيه"]
        ]
        
        customer_table = Table(customer_info, colWidths=[2*inch, 3*inch])
        customer_table.setStyle(TableStyle([
            ('ALIGN', (0, 0), (-1, -1), 'RIGHT'),
            ('FONTNAME', (0, 0), (-1, -1), 'Arial'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('BACKGROUND', (0, 0), (0, -1), colors.lightgrey)
        ]))
        
        story.append(customer_table)
        story.append(Spacer(1, 20))
        
        # المشاكل
        if issues_data:
            story.append(Paragraph("المشاكل والحالات", self.styles['heading']))
            
            for issue in issues_data:
                issue_info = [
                    ["رقم الحالة:", str(issue.get('id', ''))],
                    ["تصنيف المشكلة:", issue.get('category', '')],
                    ["العنوان:", issue.get('title', '')],
                    ["الوصف:", issue.get('description', '')],
                    ["الحالة:", issue.get('status', '')],
                    ["الأولوية:", issue.get('priority', '')],
                    ["الموظف المسؤول:", issue.get('responsible_employee', '')],
                    ["تاريخ الإنشاء:", issue.get('created_date', '')]
                ]
                
                issue_table = Table(issue_info, colWidths=[2*inch, 3*inch])
                issue_table.setStyle(TableStyle([
                    ('ALIGN', (0, 0), (-1, -1), 'RIGHT'),
                    ('FONTNAME', (0, 0), (-1, -1), 'Arial'),
                    ('FONTSIZE', (0, 0), (-1, -1), 9),
                    ('GRID', (0, 0), (-1, -1), 1, colors.black),
                    ('BACKGROUND', (0, 0), (0, -1), colors.lightblue)
                ]))
                
                story.append(issue_table)
                story.append(Spacer(1, 10))
        
        # تاريخ إنتاج التقرير
        story.append(Spacer(1, 20))
        story.append(Paragraph(f"تاريخ إنتاج التقرير: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", 
                              self.styles['arabic']))
        
        doc.build(story)
        return output_path
    
    def generate_issues_summary_report(self, issues_data, output_path):
        """إنتاج تقرير ملخص المشاكل"""
        doc = SimpleDocTemplate(output_path, pagesize=A4)
        story = []
        
        # العنوان الرئيسي
        title = Paragraph("تقرير ملخص المشاكل", self.styles['title'])
        story.append(title)
        story.append(Spacer(1, 20))
        
        if issues_data:
            # إحصائيات
            total_issues = len(issues_data)
            open_issues = len([i for i in issues_data if i.get('status') == 'مفتوحة'])
            closed_issues = total_issues - open_issues
            
            stats_info = [
                ["إجمالي المشاكل:", str(total_issues)],
                ["المشاكل المفتوحة:", str(open_issues)],
                ["المشاكل المغلقة:", str(closed_issues)]
            ]
            
            stats_table = Table(stats_info, colWidths=[2*inch, 1*inch])
            stats_table.setStyle(TableStyle([
                ('ALIGN', (0, 0), (-1, -1), 'RIGHT'),
                ('FONTNAME', (0, 0), (-1, -1), 'Arial'),
                ('FONTSIZE', (0, 0), (-1, -1), 12),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
                ('BACKGROUND', (0, 0), (0, -1), colors.yellow)
            ]))
            
            story.append(stats_table)
            story.append(Spacer(1, 20))
            
            # جدول المشاكل
            story.append(Paragraph("تفاصيل المشاكل", self.styles['heading']))
            
            issues_table_data = [["رقم الحالة", "العميل", "التصنيف", "العنوان", "الحالة", "التاريخ"]]
            
            for issue in issues_data:
                issues_table_data.append([
                    str(issue.get('id', '')),
                    issue.get('customer_name', ''),
                    issue.get('category', ''),
                    issue.get('title', ''),
                    issue.get('status', ''),
                    issue.get('created_date', '').split(' ')[0] if issue.get('created_date') else ''
                ])
            
            issues_table = Table(issues_table_data, colWidths=[0.8*inch, 1.5*inch, 1.2*inch, 2*inch, 1*inch, 1*inch])
            issues_table.setStyle(TableStyle([
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, -1), 'Arial'),
                ('FONTSIZE', (0, 0), (-1, -1), 8),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke)
            ]))
            
            story.append(issues_table)
        
        # تاريخ إنتاج التقرير
        story.append(Spacer(1, 20))
        story.append(Paragraph(f"تاريخ إنتاج التقرير: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", 
                              self.styles['arabic']))
        
        doc.build(story)
        return output_path
    
    def generate_correspondence_report(self, correspondence_data, output_path):
        """إنتاج تقرير المراسلات"""
        doc = SimpleDocTemplate(output_path, pagesize=A4)
        story = []
        
        # العنوان الرئيسي
        title = Paragraph("تقرير المراسلات", self.styles['title'])
        story.append(title)
        story.append(Spacer(1, 20))
        
        if correspondence_data:
            for corr in correspondence_data:
                story.append(Paragraph(f"رقم المراسلة: {corr.get('correspondence_number', '')}", 
                                     self.styles['heading']))
                
                corr_info = [
                    ["المرسل:", corr.get('sender', '')],
                    ["المستقبل:", corr.get('receiver', '')],
                    ["الموضوع:", corr.get('subject', '')],
                    ["تاريخ الإرسال:", corr.get('date_sent', '')],
                    ["تاريخ الاستلام:", corr.get('date_received', '')],
                ]
                
                corr_table = Table(corr_info, colWidths=[2*inch, 3*inch])
                corr_table.setStyle(TableStyle([
                    ('ALIGN', (0, 0), (-1, -1), 'RIGHT'),
                    ('FONTNAME', (0, 0), (-1, -1), 'Arial'),
                    ('FONTSIZE', (0, 0), (-1, -1), 10),
                    ('GRID', (0, 0), (-1, -1), 1, colors.black),
                    ('BACKGROUND', (0, 0), (0, -1), colors.lightgreen)
                ]))
                
                story.append(corr_table)
                
                # محتوى المراسلة
                if corr.get('content'):
                    story.append(Spacer(1, 10))
                    story.append(Paragraph("المحتوى:", self.styles['heading']))
                    story.append(Paragraph(corr.get('content', ''), self.styles['arabic']))
                
                # الرد
                if corr.get('response_content'):
                    story.append(Spacer(1, 10))
                    story.append(Paragraph("الرد:", self.styles['heading']))
                    story.append(Paragraph(corr.get('response_content', ''), self.styles['arabic']))
                    story.append(Paragraph(f"تاريخ الرد: {corr.get('response_date', '')}", 
                                         self.styles['arabic']))
                
                story.append(Spacer(1, 20))
        
        # تاريخ إنتاج التقرير
        story.append(Paragraph(f"تاريخ إنتاج التقرير: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", 
                              self.styles['arabic']))
        
        doc.build(story)
        return output_path