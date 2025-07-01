# نص NSIS لإنشاء ملف تثبيت نظام إدارة مشاكل العملاء
# NSIS Installer Script for Customer Issues Management System

!define APP_NAME "نظام إدارة مشاكل العملاء"
!define APP_NAME_EN "Customer Issues Management System"
!define APP_VERSION "2.0.0"
!define APP_PUBLISHER "AI Assistant"
!define APP_WEBSITE "https://github.com/customer-issues-system"
!define APP_EXE "CustomerIssuesManagement.exe"
!define UNINSTALL_EXE "Uninstall.exe"

# تحديد اسم الملف الناتج
OutFile "CustomerIssuesManagement-Setup.exe"

# تحديد دليل التثبيت الافتراضي
InstallDir "$PROGRAMFILES\${APP_NAME_EN}"

# الحصول على دليل التثبيت من Registry
InstallDirRegKey HKLM "Software\${APP_NAME_EN}" "InstallDir"

# طلب صلاحيات إدارية
RequestExecutionLevel admin

# ضغط الملفات
SetCompressor /SOLID lzma

# تضمين واجهة رسومية حديثة
!include "MUI2.nsh"
!include "WinMessages.nsh"
!include "FileFunc.nsh"

# إعدادات الواجهة
!define MUI_ABORTWARNING
!define MUI_ICON "app.ico"
!define MUI_UNICON "app.ico"

# الصفحات
!insertmacro MUI_PAGE_WELCOME
!insertmacro MUI_PAGE_LICENSE "LICENSE.txt"
!insertmacro MUI_PAGE_COMPONENTS
!insertmacro MUI_PAGE_DIRECTORY
!insertmacro MUI_PAGE_INSTFILES
!define MUI_FINISHPAGE_RUN "$INSTDIR\${APP_EXE}"
!define MUI_FINISHPAGE_RUN_TEXT "تشغيل ${APP_NAME} الآن"
!insertmacro MUI_PAGE_FINISH

# صفحات إلغاء التثبيت
!insertmacro MUI_UNPAGE_CONFIRM
!insertmacro MUI_UNPAGE_INSTFILES

# اللغات
!insertmacro MUI_LANGUAGE "Arabic"
!insertmacro MUI_LANGUAGE "English"

# معلومات الإصدار
VIProductVersion "2.0.0.0"
VIAddVersionKey /LANG=${LANG_ENGLISH} "ProductName" "${APP_NAME_EN}"
VIAddVersionKey /LANG=${LANG_ENGLISH} "CompanyName" "${APP_PUBLISHER}"
VIAddVersionKey /LANG=${LANG_ENGLISH} "LegalCopyright" "© 2024 ${APP_PUBLISHER}"
VIAddVersionKey /LANG=${LANG_ENGLISH} "FileDescription" "${APP_NAME_EN} Installer"
VIAddVersionKey /LANG=${LANG_ENGLISH} "FileVersion" "${APP_VERSION}"
VIAddVersionKey /LANG=${LANG_ENGLISH} "ProductVersion" "${APP_VERSION}"

# تحقق من وجود Python
Function CheckPython
  ClearErrors
  ExecWait 'python --version' $0
  ${If} ${Errors}
    ExecWait 'python3 --version' $0
    ${If} ${Errors}
      MessageBox MB_YESNO|MB_ICONQUESTION "لم يتم العثور على Python.$\n$\nهل تريد تحميل Python من الموقع الرسمي؟" IDYES DownloadPython IDNO SkipPython
      DownloadPython:
        ExecShell "open" "https://www.python.org/downloads/"
      SkipPython:
    ${EndIf}
  ${EndIf}
FunctionEnd

# المكونات
Section "الملفات الأساسية" SecMain
  SectionIn RO  # مطلوب
  
  SetOutPath "$INSTDIR"
  
  # نسخ الملف الرئيسي
  File "dist\${APP_EXE}"
  
  # نسخ ملفات Python الاحتياطية
  File "enhanced_main.py"
  File "enhanced_database.py"
  File "enhanced_main_window.py"
  File "enhanced_functions.py"
  File "enhanced_file_manager.py"
  File "test_enhanced_system.py"
  
  # نسخ الوثائق
  File "دليل_النظام_المحسن.md"
  File "ملخص_النظام_المحسن.md"
  File "README_Enhanced.md"
  File "enhanced_requirements.txt"
  
  # إنشاء ملفات تشغيل
  FileOpen $0 "$INSTDIR\تشغيل_النظام.bat" w
  FileWrite $0 "@echo off$\r$\n"
  FileWrite $0 "chcp 65001 > nul$\r$\n"
  FileWrite $0 "cd /d `"%~dp0`"$\r$\n"
  FileWrite $0 "start `"`" `"${APP_EXE}`"$\r$\n"
  FileClose $0
  
  FileOpen $0 "$INSTDIR\تشغيل_بايثون.bat" w
  FileWrite $0 "@echo off$\r$\n"
  FileWrite $0 "chcp 65001 > nul$\r$\n"
  FileWrite $0 "cd /d `"%~dp0`"$\r$\n"
  FileWrite $0 "python enhanced_main.py$\r$\n"
  FileWrite $0 "if %errorlevel% neq 0 ($\r$\n"
  FileWrite $0 "    echo خطأ: تأكد من تثبيت Python$\r$\n"
  FileWrite $0 "    pause$\r$\n"
  FileWrite $0 ")$\r$\n"
  FileClose $0
  
  # إنشاء ملف اختبار
  FileOpen $0 "$INSTDIR\اختبار_النظام.bat" w
  FileWrite $0 "@echo off$\r$\n"
  FileWrite $0 "chcp 65001 > nul$\r$\n"
  FileWrite $0 "cd /d `"%~dp0`"$\r$\n"
  FileWrite $0 "python test_enhanced_system.py$\r$\n"
  FileWrite $0 "pause$\r$\n"
  FileClose $0
  
  # إنشاء مجلد البيانات
  CreateDirectory "$INSTDIR\files"
  CreateDirectory "$INSTDIR\backups"
  
  # كتابة معلومات إلغاء التثبيت
  WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APP_NAME_EN}" "DisplayName" "${APP_NAME}"
  WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APP_NAME_EN}" "UninstallString" "$INSTDIR\${UNINSTALL_EXE}"
  WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APP_NAME_EN}" "DisplayIcon" "$INSTDIR\${APP_EXE}"
  WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APP_NAME_EN}" "Publisher" "${APP_PUBLISHER}"
  WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APP_NAME_EN}" "URLInfoAbout" "${APP_WEBSITE}"
  WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APP_NAME_EN}" "DisplayVersion" "${APP_VERSION}"
  WriteRegDWORD HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APP_NAME_EN}" "NoModify" 1
  WriteRegDWORD HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APP_NAME_EN}" "NoRepair" 1
  
  # حساب حجم التثبيت
  ${GetSize} "$INSTDIR" "/S=0K" $0 $1 $2
  IntFmt $0 "0x%08X" $0
  WriteRegDWORD HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APP_NAME_EN}" "EstimatedSize" "$0"
  
  # حفظ دليل التثبيت
  WriteRegStr HKLM "Software\${APP_NAME_EN}" "InstallDir" "$INSTDIR"
  
  # إنشاء ملف إلغاء التثبيت
  WriteUninstaller "$INSTDIR\${UNINSTALL_EXE}"
SectionEnd

Section "اختصارات سطح المكتب" SecDesktop
  CreateShortcut "$DESKTOP\${APP_NAME}.lnk" "$INSTDIR\${APP_EXE}" "" "$INSTDIR\${APP_EXE}" 0
  CreateShortcut "$DESKTOP\تشغيل ${APP_NAME} (Python).lnk" "$INSTDIR\تشغيل_بايثون.bat" "" "$INSTDIR\${APP_EXE}" 0
SectionEnd

Section "قائمة ابدأ" SecStartMenu
  CreateDirectory "$SMPROGRAMS\${APP_NAME}"
  CreateShortcut "$SMPROGRAMS\${APP_NAME}\${APP_NAME}.lnk" "$INSTDIR\${APP_EXE}" "" "$INSTDIR\${APP_EXE}" 0
  CreateShortcut "$SMPROGRAMS\${APP_NAME}\تشغيل بـ Python.lnk" "$INSTDIR\تشغيل_بايثون.bat" "" "$INSTDIR\${APP_EXE}" 0
  CreateShortcut "$SMPROGRAMS\${APP_NAME}\اختبار النظام.lnk" "$INSTDIR\اختبار_النظام.bat" "" "$INSTDIR\${APP_EXE}" 0
  CreateShortcut "$SMPROGRAMS\${APP_NAME}\دليل الاستخدام.lnk" "$INSTDIR\دليل_النظام_المحسن.md" "" "" 0
  CreateShortcut "$SMPROGRAMS\${APP_NAME}\إلغاء التثبيت.lnk" "$INSTDIR\${UNINSTALL_EXE}" "" "$INSTDIR\${UNINSTALL_EXE}" 0
SectionEnd

Section "فحص Python" SecPython
  Call CheckPython
SectionEnd

# أوصاف المكونات
LangString DESC_SecMain ${LANG_ARABIC} "الملفات الأساسية للنظام (مطلوب)"
LangString DESC_SecDesktop ${LANG_ARABIC} "إنشاء اختصارات على سطح المكتب"
LangString DESC_SecStartMenu ${LANG_ARABIC} "إضافة البرنامج لقائمة ابدأ"
LangString DESC_SecPython ${LANG_ARABIC} "فحص وجود Python وتنزيله إذا لزم الأمر"

LangString DESC_SecMain ${LANG_ENGLISH} "Core system files (required)"
LangString DESC_SecDesktop ${LANG_ENGLISH} "Create desktop shortcuts"
LangString DESC_SecStartMenu ${LANG_ENGLISH} "Add program to Start Menu"
LangString DESC_SecPython ${LANG_ENGLISH} "Check for Python installation"

!insertmacro MUI_FUNCTION_DESCRIPTION_BEGIN
  !insertmacro MUI_DESCRIPTION_TEXT ${SecMain} $(DESC_SecMain)
  !insertmacro MUI_DESCRIPTION_TEXT ${SecDesktop} $(DESC_SecDesktop)
  !insertmacro MUI_DESCRIPTION_TEXT ${SecStartMenu} $(DESC_SecStartMenu)
  !insertmacro MUI_DESCRIPTION_TEXT ${SecPython} $(DESC_SecPython)
!insertmacro MUI_FUNCTION_DESCRIPTION_END

# وظائف إلغاء التثبيت
Section "Uninstall"
  # حذف الملفات
  Delete "$INSTDIR\${APP_EXE}"
  Delete "$INSTDIR\*.py"
  Delete "$INSTDIR\*.md"
  Delete "$INSTDIR\*.txt"
  Delete "$INSTDIR\*.bat"
  Delete "$INSTDIR\${UNINSTALL_EXE}"
  
  # حذف المجلدات (إذا كانت فارغة)
  RMDir "$INSTDIR\files"
  RMDir "$INSTDIR\backups"
  RMDir "$INSTDIR"
  
  # حذف الاختصارات
  Delete "$DESKTOP\${APP_NAME}.lnk"
  Delete "$DESKTOP\تشغيل ${APP_NAME} (Python).lnk"
  
  # حذف مجلد قائمة ابدأ
  RMDir /r "$SMPROGRAMS\${APP_NAME}"
  
  # حذف مدخلات التسجيل
  DeleteRegKey HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APP_NAME_EN}"
  DeleteRegKey HKLM "Software\${APP_NAME_EN}"
SectionEnd

# وظيفة التهيئة
Function .onInit
  # فحص إذا كان البرنامج مثبت مسبقاً
  ReadRegStr $R0 HKLM "Software\${APP_NAME_EN}" "InstallDir"
  StrCmp $R0 "" done
  
  MessageBox MB_OKCANCEL|MB_ICONEXCLAMATION "${APP_NAME} مثبت مسبقاً في $R0$\n$\nانقر موافق لإزالة النسخة السابقة أو إلغاء للخروج." IDOK uninst
  Abort
  
  uninst:
    ClearErrors
    ExecWait '$R0\${UNINSTALL_EXE} _?=$R0'
    
    IfErrors no_remove_uninstaller done
      no_remove_uninstaller:
  
  done:
FunctionEnd