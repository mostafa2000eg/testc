# Contributing to Customer Issues Management System
## المساهمة في نظام إدارة مشاكل العملاء

🎉 **Thank you for your interest in contributing!**  
**شكراً لاهتمامك بالمساهمة!**

This document provides guidelines for contributing to the Customer Issues Management System. Please read it carefully before submitting any contributions.

تقدم هذه الوثيقة إرشادات للمساهمة في نظام إدارة مشاكل العملاء. يرجى قراءتها بعناية قبل تقديم أي مساهمات.

## 📋 Table of Contents | جدول المحتويات

1. [Code of Conduct | مدونة السلوك](#code-of-conduct--مدونة-السلوك)
2. [Getting Started | البداية](#getting-started--البداية)
3. [Development Setup | إعداد التطوير](#development-setup--إعداد-التطوير)
4. [Contribution Types | أنواع المساهمة](#contribution-types--أنواع-المساهمة)
5. [Pull Request Process | عملية Pull Request](#pull-request-process--عملية-pull-request)
6. [Coding Guidelines | إرشادات البرمجة](#coding-guidelines--إرشادات-البرمجة)
7. [Testing Requirements | متطلبات الاختبار](#testing-requirements--متطلبات-الاختبار)
8. [Documentation Standards | معايير التوثيق](#documentation-standards--معايير-التوثيق)

---

## 🤝 Code of Conduct | مدونة السلوك

This project and everyone participating in it is governed by our Code of Conduct. By participating, you are expected to uphold this code.

يحكم هذا المشروع وكل من يشارك فيه مدونة السلوك الخاصة بنا. من خلال المشاركة، من المتوقع أن تلتزم بهذه المدونة.

### Our Standards | معاييرنا

**Examples of behavior that contributes to a positive environment:**
- Using welcoming and inclusive language
- Being respectful of differing viewpoints and experiences
- Gracefully accepting constructive criticism
- Focusing on what is best for the community
- Showing empathy towards other community members

**أمثلة على السلوك الذي يساهم في بيئة إيجابية:**
- استخدام لغة ترحيبية وشاملة
- احترام وجهات النظر والتجارب المختلفة
- قبول النقد البناء بأناقة
- التركيز على ما هو أفضل للمجتمع
- إظهار التعاطف مع أعضاء المجتمع الآخرين

---

## 🚀 Getting Started | البداية

### Prerequisites | المتطلبات الأساسية

Before you begin, ensure you have:
- **Python 3.7+** installed
- **Git** installed and configured
- A **GitHub account**
- Basic knowledge of **Python** and **tkinter**
- Understanding of **SQLite** databases

قبل البدء، تأكد من أن لديك:
- **Python 3.7+** مثبت
- **Git** مثبت ومُعد
- حساب **GitHub**
- معرفة أساسية بـ **Python** و **tkinter**
- فهم لقواعد بيانات **SQLite**

### Fork and Clone | Fork والاستنساخ

1. **Fork the repository** on GitHub
2. **Clone your fork** locally:
   ```bash
   git clone https://github.com/yourusername/customer-issues-management.git
   cd customer-issues-management
   ```
3. **Add the upstream remote**:
   ```bash
   git remote add upstream https://github.com/originalowner/customer-issues-management.git
   ```

---

## 🛠️ Development Setup | إعداد التطوير

### 1. Create Virtual Environment | إنشاء بيئة افتراضية

```bash
# Create virtual environment
python -m venv venv

# Activate it
# On Windows:
venv\Scripts\activate
# On Linux/Mac:
source venv/bin/activate
```

### 2. Install Dependencies | تثبيت المتطلبات

```bash
# Install development dependencies
pip install -r requirements.txt

# Install additional dev tools (optional)
pip install pytest black flake8
```

### 3. Run Tests | تشغيل الاختبارات

```bash
# Run the test suite
python test_customer_issues.py

# Or use pytest if installed
pytest
```

### 4. Run the Application | تشغيل التطبيق

```bash
# Run the main application
python customer_issues_main.py

# Or use the shell scripts
./run_system.sh    # Linux/Mac
run_system.bat     # Windows
```

---

## 🎯 Contribution Types | أنواع المساهمة

We welcome various types of contributions:

### 🐛 Bug Reports | تقارير الأخطاء
- Use the [Bug Report Template](.github/ISSUE_TEMPLATE/bug_report.md)
- Include detailed steps to reproduce
- Provide system information and logs
- Test on the latest version first

### ✨ Feature Requests | طلبات الميزات
- Use the [Feature Request Template](.github/ISSUE_TEMPLATE/feature_request.md)
- Describe the problem you're trying to solve
- Propose a detailed solution
- Consider implementation complexity

### 💻 Code Contributions | المساهمات البرمجية
- Bug fixes
- New features
- Performance improvements
- Code refactoring
- Test additions

### 📚 Documentation | التوثيق
- README improvements
- Code comments
- User guides
- API documentation
- Translation improvements

### 🌐 Translations | الترجمات
- Arabic text improvements
- English text improvements
- Interface localization
- Error message translations

---

## 🔄 Pull Request Process | عملية Pull Request

### 1. Create a Branch | إنشاء فرع

```bash
# Update your fork
git fetch upstream
git checkout main
git merge upstream/main

# Create a new branch
git checkout -b feature/your-feature-name
# or
git checkout -b fix/your-bug-fix
```

### 2. Make Changes | إجراء التغييرات

- Follow the [Coding Guidelines](#coding-guidelines--إرشادات-البرمجة)
- Write tests for new functionality
- Update documentation as needed
- Ensure all tests pass

### 3. Commit Changes | تثبيت التغييرات

```bash
# Add files
git add .

# Commit with descriptive message
git commit -m "feat: add advanced search functionality

- Implement 7 search types
- Add dynamic field configuration
- Update database schema
- Add comprehensive tests

Closes #123"
```

#### Commit Message Format | تنسيق رسالة التثبيت

```
<type>(<scope>): <description>

[optional body]

[optional footer]
```

**Types:**
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation
- `style`: Code style changes
- `refactor`: Code refactoring
- `test`: Test additions
- `chore`: Maintenance tasks

### 4. Push and Create PR | الدفع وإنشاء PR

```bash
# Push to your fork
git push origin feature/your-feature-name

# Create Pull Request on GitHub
# Use the PR template and fill all sections
```

### 5. Review Process | عملية المراجعة

- **Automated checks** will run (CI/CD)
- **Code review** by maintainers
- **Address feedback** promptly
- **Update documentation** if requested
- **Rebase/squash** commits if needed

---

## 📝 Coding Guidelines | إرشادات البرمجة

### Python Style | نمط Python

Follow **PEP 8** with these specifics:

```python
# Line length: 88 characters (Black default)
# Indentation: 4 spaces
# Quotes: Use double quotes for strings
# Imports: Group and sort properly

# Good example:
def search_customers(query: str, search_type: str) -> List[Dict]:
    """
    Search customers based on query and type.
    
    Args:
        query: Search query string
        search_type: Type of search to perform
        
    Returns:
        List of matching customer records
    """
    if not query or not search_type:
        return []
    
    # Implementation here
    pass
```

### File Organization | تنظيم الملفات

```
customer-issues-management/
├── customer_issues_main.py          # Main application entry
├── customer_issues_database.py      # Database operations
├── customer_issues_window.py        # Main GUI window
├── customer_issues_functions.py     # Core business logic
├── customer_issues_file_manager.py  # File operations
├── test_customer_issues.py          # Test suite
└── docs/                            # Documentation
```

### Variable Naming | تسمية المتغيرات

```python
# Use descriptive names
customer_id = 123           # Good
c_id = 123                 # Bad

# Constants in UPPER_CASE
DATABASE_PATH = "data.db"

# Functions and variables in snake_case
def get_customer_info():
    pass

# Classes in PascalCase
class CustomerManager:
    pass
```

### Error Handling | معالجة الأخطاء

```python
import logging

def save_customer(customer_data):
    """Save customer data with proper error handling."""
    try:
        # Validate input
        if not customer_data:
            raise ValueError("Customer data cannot be empty")
        
        # Save to database
        result = database.save(customer_data)
        logging.info(f"Customer saved successfully: {result}")
        return result
        
    except ValueError as e:
        logging.error(f"Validation error: {e}")
        raise
    except DatabaseError as e:
        logging.error(f"Database error: {e}")
        raise
    except Exception as e:
        logging.error(f"Unexpected error: {e}")
        raise
```

---

## 🧪 Testing Requirements | متطلبات الاختبار

### Test Coverage | تغطية الاختبارات

- **New features** must include tests
- **Bug fixes** must include regression tests
- **Maintain 80%+** test coverage
- **Test all platforms** (Windows, Linux, Mac)

### Test Types | أنواع الاختبارات

```python
# Unit tests - test individual functions
def test_customer_validation():
    assert validate_customer_data(valid_data) == True
    assert validate_customer_data(invalid_data) == False

# Integration tests - test component interaction
def test_database_customer_operations():
    db = DatabaseManager()
    customer_id = db.add_customer(test_data)
    retrieved = db.get_customer(customer_id)
    assert retrieved['name'] == test_data['name']

# UI tests - test user interface
def test_main_window_creation():
    root = tk.Tk()
    window = CustomerIssuesWindow(root)
    assert window.title() == "نظام إدارة مشاكل العملاء v2.0.0"
```

### Running Tests | تشغيل الاختبارات

```bash
# Run all tests
python test_customer_issues.py

# Run with coverage (if pytest installed)
pytest --cov=. --cov-report=html

# Run specific test
python -m pytest test_customer_issues.py::test_database_connection
```

---

## 📖 Documentation Standards | معايير التوثيق

### Code Documentation | توثيق الكود

```python
def search_issues(query: str, search_type: str, date_range: tuple = None) -> List[Dict]:
    """
    Search issues based on criteria.
    
    This function searches through customer issues using various search types
    and optional date filtering.
    
    Args:
        query (str): The search query string
        search_type (str): Type of search ('customer_name', 'issue_type', etc.)
        date_range (tuple, optional): Start and end dates for filtering
        
    Returns:
        List[Dict]: List of matching issue records with the following keys:
            - id (int): Issue ID
            - customer_name (str): Customer name
            - issue_type (str): Type of issue
            - created_date (str): Creation date
            - status (str): Current status
            
    Raises:
        ValueError: If search_type is not supported
        DatabaseError: If database query fails
        
    Example:
        >>> results = search_issues("أحمد", "customer_name")
        >>> len(results)
        5
        >>> results[0]['customer_name']
        'أحمد محمد'
    """
    pass
```

### README Updates | تحديثات README

When adding features, update:
- **Feature list** in README.md
- **Usage examples**
- **Installation instructions** if needed
- **Screenshots** if UI changes

### Changelog | سجل التغييرات

Always update CHANGELOG.md:
```markdown
## [Unreleased]

### Added
- Advanced search functionality with 7 search types
- Dynamic field configuration for search forms

### Fixed
- Database connection timeout issues
- Arabic text rendering in search results
```

---

## 🌍 Internationalization | التدويل

### Arabic Support | دعم العربية

- **Right-to-left** text support
- **Arabic fonts** compatibility
- **Cultural considerations** (date formats, etc.)
- **Proper encoding** (UTF-8)

```python
# Arabic text handling example
def format_arabic_text(text):
    """Ensure proper Arabic text formatting."""
    if not text:
        return ""
    
    # Handle RTL text direction
    return f"\u202B{text}\u202C"  # RTL override
```

### Translation Guidelines | إرشادات الترجمة

- **Consistent terminology** across the application
- **Context-appropriate** translations
- **Professional language** for business environment
- **Bilingual documentation** (Arabic/English)

---

## 🚀 Release Process | عملية الإصدار

### Version Numbering | ترقيم الإصدارات

We follow [Semantic Versioning](https://semver.org/):
- **MAJOR.MINOR.PATCH** (e.g., 2.1.0)
- **Major**: Breaking changes
- **Minor**: New features (backward compatible)
- **Patch**: Bug fixes (backward compatible)

### Release Checklist | قائمة الإصدار

- [ ] All tests pass
- [ ] Documentation updated
- [ ] CHANGELOG.md updated
- [ ] Version number updated
- [ ] GitHub release created
- [ ] Release notes published

---

## 🆘 Getting Help | الحصول على المساعدة

### Communication Channels | قنوات التواصل

- **GitHub Issues**: Bug reports and feature requests
- **GitHub Discussions**: General questions and ideas
- **Email**: For sensitive security issues

### Before Asking | قبل السؤال

1. **Search existing issues** and discussions
2. **Check documentation** thoroughly
3. **Try the latest version**
4. **Provide detailed information**

### Question Template | قالب السؤال

```
**What are you trying to achieve?**
What I want to do...

**What have you tried?**
I have tried...

**What happened instead?**
Instead of expected behavior...

**System information:**
- OS: Windows 10
- Python: 3.9.7
- App version: 2.0.0
```

---

## 🏆 Recognition | التقدير

### Contributors | المساهمون

All contributors will be:
- **Listed** in the project README
- **Credited** in release notes
- **Mentioned** in relevant documentation

### Types of Recognition | أنواع التقدير

- **Code contributors**: Direct code contributions
- **Issue reporters**: High-quality bug reports
- **Feature requesters**: Valuable feature suggestions
- **Documentation helpers**: Documentation improvements
- **Testers**: Thorough testing and feedback

---

## 📞 Contact | التواصل

For questions about contributing:

- **GitHub Issues**: [Create an issue](https://github.com/yourusername/customer-issues-management/issues)
- **Email**: contribute@customer-issues-system.com
- **Discussions**: [GitHub Discussions](https://github.com/yourusername/customer-issues-management/discussions)

---

**Thank you for contributing to the Customer Issues Management System!**  
**شكراً لمساهمتك في نظام إدارة مشاكل العملاء!**

Your contributions help make this system better for gas companies worldwide.  
مساهماتك تساعد في جعل هذا النظام أفضل لشركات الغاز حول العالم.