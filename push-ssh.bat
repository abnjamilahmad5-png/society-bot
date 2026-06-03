@echo off
REM ====================================================
REM حل مشكلة GitHub Permission - استخدام SSH
REM ====================================================

echo.
echo ==================================================
echo   🔧 حل مشكلة GitHub Authentication
echo ==================================================
echo.

cd /d "C:\Users\abnja\شاي"

echo ✓ المجلد الحالي:
echo   %cd%
echo.

echo ==================================================
echo   الخطوة 1: حذف الـ remote القديم
echo ==================================================
echo.

git remote remove origin
echo ✓ تم حذف الـ remote

echo.
echo ==================================================
echo   الخطوة 2: إضافة remote SSH جديد
echo ==================================================
echo.

git remote add origin git@github.com:abnjamilahmad5-png/society-bot.git
echo ✓ تم إضافة SSH remote

echo.
echo ==================================================
echo   الخطوة 3: الرفع على GitHub
echo ==================================================
echo.

echo ⏳ جاري الرفع (قد يطلب SSH passphrase)...
echo.

git push -u origin main

if errorlevel 1 (
    echo.
    echo ==================================================
    echo   🚨 حدث خطأ في SSH
    echo ==================================================
    echo.
    echo الحل: إنشاء SSH Key جديد
    echo.
    echo الخطوات:
    echo 1. تشغيل: ssh-keygen -t ed25519 -C "abnjamilahmad5-png@github.com"
    echo 2. اضغط Enter عند كل سؤال
    echo 3. نسخ المفتاح: Get-Content $HOME\.ssh\id_ed25519.pub ^| Set-Clipboard
    echo 4. اذهب إلى: https://github.com/settings/ssh/new
    echo 5. الصق المفتاح
    echo 6. جرب الرفع مرة أخرى
    echo.
    pause
    exit /b 1
) else (
    echo.
    echo ==================================================
    echo   ✅ تم الرفع على GitHub بنجاح!
    echo ==================================================
    echo.
    echo 🎉 الخطوة التالية: Railway
    echo.
    echo 1. اذهب إلى: https://railway.app
    echo 2. اختر: New Project
    echo 3. اختر: Deploy from GitHub
    echo 4. اختر: society-bot
    echo 5. أضف Variables:
    echo    - TOKEN
    echo    - GUILD_ID
    echo    - PREFIX
    echo 6. اضغط: Deploy
    echo.
    echo 🚀 البوت سيعمل خلال دقيقتين!
    echo.
    pause
)
