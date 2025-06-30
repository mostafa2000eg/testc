# Pull Request | طلب السحب

## 📋 Description | الوصف
**Please include a summary of the changes and the related issue.**  
**يرجى تضمين ملخص للتغييرات والمشكلة ذات الصلة.**

Fixes # (issue number)  
يحل # (رقم المشكلة)

## 🔄 Type of Change | نوع التغيير
**What type of change does your code introduce?**  
**ما نوع التغيير الذي يقدمه كودك؟**

- [ ] **Bug fix | إصلاح خطأ** (non-breaking change which fixes an issue)
- [ ] **New feature | ميزة جديدة** (non-breaking change which adds functionality)
- [ ] **Breaking change | تغيير جذري** (fix or feature that would cause existing functionality to not work as expected)
- [ ] **Documentation update | تحديث الوثائق** (changes to documentation only)
- [ ] **Code refactoring | إعادة هيكلة الكود** (code changes that neither fix a bug nor add a feature)
- [ ] **Performance improvement | تحسين الأداء** (changes that improve performance)
- [ ] **Test addition | إضافة اختبارات** (adding missing tests or correcting existing tests)

## 🧪 Testing | الاختبار
**Describe the tests that you ran to verify your changes.**  
**صف الاختبارات التي قمت بتشغيلها للتحقق من تغييراتك.**

- [ ] **Unit tests | اختبارات الوحدة** - All tests pass
- [ ] **Integration tests | اختبارات التكامل** - System works end-to-end
- [ ] **Manual testing | اختبار يدوي** - Tested user scenarios
- [ ] **Performance testing | اختبار الأداء** - No performance degradation
- [ ] **Cross-platform testing | اختبار متعدد المنصات** - Tested on multiple OS

### Test Configuration | إعداد الاختبار:
- **OS | نظام التشغيل**: [e.g. Windows 10, Ubuntu 20.04]
- **Python Version | إصدار Python**: [e.g. 3.9.7]
- **Database Size | حجم قاعدة البيانات**: [e.g. 100 records]

## 📸 Screenshots | لقطات الشاشة
**If applicable, add screenshots to help explain your changes.**  
**إذا كان ذلك مناسباً، أضف لقطات شاشة لمساعدة في شرح تغييراتك.**

### Before | قبل:
<!-- Add screenshots of the system before your changes -->

### After | بعد:
<!-- Add screenshots of the system after your changes -->

## 🔧 Implementation Details | تفاصيل التنفيذ
**Provide details about your implementation:**  
**قدم تفاصيل حول تنفيذك:**

### Changes Made | التغييرات المُجراة:
- **Files Modified | الملفات المُعدلة:**
  - `file1.py`: Description of changes
  - `file2.py`: Description of changes

- **New Files Added | الملفات الجديدة المضافة:**
  - `new_file.py`: Purpose and functionality

- **Files Deleted | الملفات المحذوفة:**
  - `old_file.py`: Reason for deletion

### Database Changes | تغييرات قاعدة البيانات:
- [ ] **Schema changes | تغييرات المخطط** - New tables/columns added
- [ ] **Data migration | نقل البيانات** - Migration script provided
- [ ] **No database changes | لا توجد تغييرات** - Database unchanged

### API Changes | تغييرات API:
- [ ] **New API endpoints | نقاط API جديدة** - Added new functionality
- [ ] **Modified existing APIs | تعديل APIs موجودة** - Changed behavior
- [ ] **Deprecated APIs | APIs مهجورة** - Marked for future removal
- [ ] **No API changes | لا توجد تغييرات** - API unchanged

## 🔄 Backward Compatibility | التوافق مع الإصدارات السابقة
**Will this change break existing functionality?**  
**هل سيكسر هذا التغيير الوظائف الموجودة؟**

- [ ] **Fully backward compatible | متوافق تماماً مع السابق** - No breaking changes
- [ ] **Minor compatibility issues | مشاكل توافق طفيفة** - Easily addressable
- [ ] **Major breaking changes | تغييرات جذرية** - Requires user action
- [ ] **Migration required | يتطلب نقل** - Users must migrate data/settings

### Migration Guide | دليل النقل:
<!-- If breaking changes exist, provide migration steps -->

## 📋 Checklist | قائمة التحقق
**Please check all that apply:**  
**يرجى تحديد كل ما ينطبق:**

### Code Quality | جودة الكود:
- [ ] My code follows the project's style guidelines | كودي يتبع إرشادات النمط للمشروع
- [ ] I have performed a self-review of my code | قمت بمراجعة ذاتية لكودي
- [ ] I have commented my code, particularly hard-to-understand areas | علقت على كودي، خاصة المناطق صعبة الفهم
- [ ] My changes generate no new warnings | تغييراتي لا تولد تحذيرات جديدة

### Testing | الاختبار:
- [ ] I have added tests that prove my fix is effective or that my feature works | أضفت اختبارات تثبت فعالية إصلاحي أو عمل ميزتي
- [ ] New and existing unit tests pass locally with my changes | الاختبارات الجديدة والموجودة تمر محلياً مع تغييراتي
- [ ] I have tested the changes on multiple platforms | اختبرت التغييرات على منصات متعددة

### Documentation | التوثيق:
- [ ] I have updated the documentation accordingly | حدثت الوثائق وفقاً لذلك
- [ ] I have updated the CHANGELOG.md | حدثت ملف CHANGELOG.md
- [ ] Any new functions/classes have appropriate docstrings | أي وظائف/كلاسات جديدة لها docstrings مناسبة

### Dependencies | المتطلبات:
- [ ] I have checked that no new dependencies are introduced unnecessarily | تحققت من عدم إدخال متطلبات جديدة غير ضرورية
- [ ] If new dependencies are added, I have updated requirements.txt | إذا أُضيفت متطلبات جديدة، حدثت requirements.txt
- [ ] All dependencies are compatible with the project's Python version requirements | جميع المتطلبات متوافقة مع متطلبات إصدار Python للمشروع

## 🚀 Performance Impact | تأثير الأداء
**Describe any performance implications:**  
**صف أي آثار على الأداء:**

- [ ] **Performance improvement | تحسين الأداء** - Changes improve performance
- [ ] **No performance impact | لا تأثير على الأداء** - Performance unchanged
- [ ] **Minor performance impact | تأثير طفيف على الأداء** - Acceptable trade-off
- [ ] **Significant performance impact | تأثير كبير على الأداء** - Requires discussion

### Benchmarks | القياسات:
<!-- If performance testing was done, include results -->

## 🔒 Security Considerations | اعتبارات الأمان
**Any security implications of your changes:**  
**أي آثار أمنية لتغييراتك:**

- [ ] **No security impact | لا تأثير أمني** - Changes don't affect security
- [ ] **Security improvement | تحسين أمني** - Changes enhance security
- [ ] **Potential security risk | خطر أمني محتمل** - Requires security review

## 📝 Additional Notes | ملاحظات إضافية
**Any additional information that reviewers should know:**  
**أي معلومات إضافية يجب أن يعرفها المراجعون:**

## 🔗 Related Issues/PRs | المشاكل/PRs ذات الصلة
**Link related issues and pull requests:**  
**اربط المشاكل وطلبات السحب ذات الصلة:**

- Closes #
- Related to #
- Depends on #
- Blocks #

---

## 👀 Reviewer Guidelines | إرشادات المراجع
**For reviewers, please check:**  
**للمراجعين، يرجى التحقق من:**

- [ ] Code quality and style consistency | جودة الكود وثبات النمط
- [ ] Test coverage adequacy | كفاية تغطية الاختبارات
- [ ] Documentation completeness | اكتمال التوثيق
- [ ] Performance implications | آثار الأداء
- [ ] Security considerations | الاعتبارات الأمنية
- [ ] Backward compatibility | التوافق مع السابق

**Thank you for contributing to the Customer Issues Management System!**  
**شكراً لمساهمتك في نظام إدارة مشاكل العملاء!**