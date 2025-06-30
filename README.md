# 🏢 نظام إدارة مشاكل العملاء
## Customer Issues Management System

[![Release](https://img.shields.io/github/v/release/customer-issues-system/releases?style=for-the-badge)](https://github.com/customer-issues-system/releases/latest)
[![Downloads](https://img.shields.io/github/downloads/customer-issues-system/total?style=for-the-badge)](https://github.com/customer-issues-system/releases)
[![License](https://img.shields.io/badge/license-Free%20Use-green?style=for-the-badge)](LICENSE.txt)
[![Language](https://img.shields.io/badge/language-عربي-blue?style=for-the-badge)](README.md)

**نظام إلكتروني متكامل لإدارة مشاكل عملاء شركات الغاز - بديل عصري للملفات الورقية**

---

## 🎯 نظرة عامة

تم تطوير هذا النظام خصيصاً لشركات الغاز لإدارة مشاكل العملاء بشكل إلكتروني متطور، ليحل محل الملفات الورقية التقليدية بحل تقني شامل وسهل الاستخدام.

### ✨ المميزات الرئيسية:
- 🔧 **واجهة رسومية عربية** كاملة مع تخطيط مقسم احترافي
- 📊 **11 تصنيف للمشاكل** (عبث بالعداد، توصيلات غير شرعية، إلخ...)
- 🔍 **بحث متقدم بـ 7 أنواع** مختلفة
- � **إدارة المراسلات** مع ترقيم مزدوج (حالة + سنوي)
- 📎 **رفع المرفقات** في مجلدات منظمة
- 👥 **إدارة الموظفين** المدمجة
- � **نسخ احتياطية تلقائية** مع تنظيف ذكي
- 📋 **تقارير PDF** بالعربية
- � **واجهة سهلة الاستخدام** للموظفين غير التقنيين

---

## � التحميل والتثبيت

### 🚀 التحميل السريع:

#### للويندوز (مستحسن):
[![Download for Windows](https://img.shields.io/badge/تحميل%20للويندوز-CustomerIssuesManagement--Setup.exe-blue?style=for-the-badge&logo=windows)](https://github.com/customer-issues-system/releases/latest/download/CustomerIssuesManagement-Setup.exe)

#### النسخة المحمولة:
[![Download Portable](https://img.shields.io/badge/النسخة%20المحمولة-portable--package.zip-green?style=for-the-badge&logo=zip)](https://github.com/customer-issues-system/releases/latest/download/portable_package.zip)

#### للينكس:
[![Download for Linux](https://img.shields.io/badge/تحميل%20للينكس-customer--issues--linux.tar.gz-orange?style=for-the-badge&logo=linux)](https://github.com/customer-issues-system/releases/latest/download/customer-issues-management-linux.tar.gz)

---

## 🛠️ متطلبات التشغيل

### ✅ الحد الأدنى:
- **نظام التشغيل**: ويندوز 7 أو أحدث / لينكس
- **الذاكرة**: 2 جيجابايت RAM
- **التخزين**: 100 ميجابايت مساحة فارغة
- **Python**: 3.7+ (للنسخة المصدرية فقط)

### 🎯 مستحسن:
- **نظام التشغيل**: ويندوز 10/11
- **الذاكرة**: 4 جيجابايت RAM
- **التخزين**: 1 جيجابايت للبيانات
- **الشاشة**: 1366x768 أو أعلى

---

## 🚀 بداية سريعة

### 1️⃣ التثبيت (ويندوز):
```
1. حمّل CustomerIssuesManagement-Setup.exe
2. شغل الملف كمدير (Run as Administrator)
3. اتبع معالج التثبيت
4. شغل البرنامج من قائمة ابدأ
```

### 2️⃣ النسخة المحمولة:
```
1. حمّل portable_package.zip
2. استخرج الملفات لمجلد جديد
3. شغل run.bat أو CustomerIssuesManagement.exe
```

### 3️⃣ أول استخدام:
```
1. أنشئ حالة عميل جديدة
2. أدخل بيانات العميل
3. حدد نوع المشكلة
4. احفظ ملفات المراسلات
5. ارفع المرفقات حسب الحاجة
```

---

## 📸 لقطات الشاشة

### الواجهة الرئيسية:
![الواجهة الرئيسية](docs/screenshots/main-interface.png)

### البحث المتقدم:
![البحث المتقدم](docs/screenshots/advanced-search.png)

### إدارة المراسلات:
![إدارة المراسلات](docs/screenshots/correspondence.png)

---

## 📚 الوثائق

### 📖 للمستخدمين:
- [دليل الاستخدام الكامل](دليل_النظام_المحسن.md)
- [دليل البداية السريعة](README_Enhanced.md)
- [الأسئلة الشائعة](docs/FAQ.md)

### 🔧 للمطورين:
- [الملخص التقني](ملخص_النظام_المحسن.md)
- [دليل التطوير](docs/DEVELOPMENT.md)
- [دليل إنشاء الحزم](دليل_إنشاء_الحزمة.md)

---

## 🏗️ البناء من المصدر

### المتطلبات:
```bash
pip install -r enhanced_requirements.txt
```

### التشغيل:
```bash
python enhanced_main.py
```

### بناء الحزمة:
```bash
# ويندوز
./إنشاء_الحزمة_المحمولة.bat

# لينكس/ماك
./create_portable_package.sh
```

---

## 🤝 المساهمة

نرحب بالمساهمات! يرجى:

1. **Fork** المستودع
2. إنشاء **branch** جديد للميزة
3. **Commit** التغييرات
4. **Push** للـ branch
5. إنشاء **Pull Request**

### قواعد المساهمة:
- ✅ اتباع معايير الكود الموجودة
- ✅ إضافة اختبارات للميزات الجديدة
- ✅ تحديث الوثائق حسب الحاجة
- ✅ استخدام أسماء واضحة للـ commits

---

## 🐛 الإبلاغ عن المشاكل

وجدت مشكلة؟ ساعدنا في إصلاحها:

[![Report Issue](https://img.shields.io/badge/أبلغ%20عن%20مشكلة-GitHub%20Issues-red?style=for-the-badge&logo=github)](https://github.com/customer-issues-system/issues/new)

### عند الإبلاغ يرجى تضمين:
- 🖥️ نظام التشغيل والإصدار
- 🐍 إصدار Python (إن أمكن)
- 📝 وصف مفصل للمشكلة
- 🔄 خطوات إعادة إنتاج المشكلة
- 📸 لقطات شاشة (إن أمكن)

---

## 📈 إحصائيات المشروع

- **📦 إجمالي الملفات**: 24+ ملف
- **💻 أسطر الكود**: 2400+ سطر Python
- **📚 أسطر التوثيق**: 980+ سطر
- **🔧 المكونات**: 6 وحدات أساسية
- **🧪 التغطية**: اختبارات شاملة
- **🌍 اللغات**: العربية (أساسي) + الإنجليزية

---

## 🏆 الإصدارات

### النسخة الحالية: v2.0.0
- ✅ واجهة محسنة مع تخطيط مقسم
- ✅ بحث متقدم بـ 7 أنواع
- ✅ إدارة موظفين مدمجة
- ✅ نظام ترقيم مزدوج للمراسلات
- ✅ نسخ احتياطية تلقائية

### الإصدارات السابقة:
- **v1.0.0**: النسخة الأساسية الأولى
- **v1.5.0**: إضافة البحث والتقارير

---

## 📞 الدعم والتواصل

### 💬 للدعم التقني:
- 📧 **البريد الإلكتروني**: support@customer-issues-system.com
- 💬 **المحادثات**: [GitHub Discussions](https://github.com/customer-issues-system/discussions)
- 📖 **الوثائق**: متوفرة في مجلد البرنامج

### 🌟 تقييم المشروع:
إذا أعجبك المشروع، لا تنسى إعطاءه ⭐ على GitHub!

[![GitHub stars](https://img.shields.io/github/stars/customer-issues-system/customer-issues-management-system?style=social)](https://github.com/customer-issues-system/customer-issues-management-system/stargazers)

---

## 📄 الترخيص

هذا المشروع مُرخص تحت رخصة الاستخدام الحر - راجع ملف [LICENSE.txt](LICENSE.txt) للتفاصيل.

### الاستخدام المسموح:
- ✅ **الاستخدام التجاري** في الشركات
- ✅ **التعديل** للاحتياجات الخاصة  
- ✅ **التوزيع** مع الحفاظ على الترخيص
- ✅ **الاستخدام الشخصي** بدون قيود

---

## 🙏 شكر وتقدير

### المطور الأصلي:
**مساعد الذكي الاصطناعي** - تطوير وتصميم النظام الكامل

### شكر خاص لـ:
- **مجتمع Python** على الأدوات الرائعة
- **مجتمع GitHub** على المنصة الممتازة
- **مستخدمي النظام** على التغذية الراجعة القيمة

---

## 🚀 ما القادم؟

### الميزات المخططة:
- 📱 **تطبيق الهاتف المحمول** للوصول السريع
- ☁️ **النسخة السحابية** للعمل عن بُعد
- 🔗 **تكامل API** مع أنظمة أخرى
- 📊 **لوحة تحكم تحليلية** متقدمة
- 🌐 **واجهة ويب** للوصول من المتصفح

### المساهمة في التطوير:
نرحب بمساهماتكم في تطوير هذه الميزات!

---

<div align="center">

**⭐ إذا كان هذا المشروع مفيداً لك، لا تنسى إعطاءه نجمة! ⭐**

**صُنع بـ ❤️ للمجتمع العربي وشركات الغاز**

---

*آخر تحديث: ديسمبر 2024*

</div>