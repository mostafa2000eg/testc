@echo off
chcp 65001 > nul
cd /d "%~dp0"
echo 🧪 اختبار النظام...
python3 test_enhanced_system.py
pause
