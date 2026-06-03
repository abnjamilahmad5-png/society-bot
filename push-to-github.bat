@echo off
REM ====================================================
REM بوت Society - سكريبت الرفع التلقائي على GitHub
REM ====================================================

echo.
echo ==================================================
echo   🚀 سكريبت رفع بوت Society على GitHub
echo ==================================================
echo.

REM الذهاب للمجلد الصحيح
cd /d "C:\Users\abnja\شاي"

echo ✓ المجلد الحالي:
cd

echo.
echo ====================================================
echo   الخطوة 1: تجهيز Git
echo ====================================================
echo.

REM التحقق من وجود Git
git --version
if errorlevel 1 (
    echo ❌ Git غير مثبت! ثبت Git من https://git-scm.com/
    pause
    exit /b 1
)

echo ✓ Git مثبت بنجاح

echo.
echo ====================================================
echo   الخطوة 2: إضافة الملفات
echo ====================================================
echo.

git add .
echo ✓ تم إضافة جميع الملفات

echo.
echo ====================================================
echo   الخطوة 3: الكود الحالي
echo ====================================================
echo.

git status

echo.
echo ====================================================
echo   الخطوة 4: الرفع على GitHub
echo ====================================================
echo.

echo ⏳ جاري الرفع...
echo.

REM محاولة الرفع
git push -u origin main

if errorlevel 1 (
    echo.
    echo ❌ حدث خطأ في الرفع!
    echo.
    echo الحلول المحتملة:
    echo 1. تأكد من أن المستودع نشأ على GitHub
    echo    https://github.com/new
    echo.
    echo 2. استخدم Personal Access Token:
    echo    https://github.com/settings/tokens
    echo.
    echo 3. جرب SSH بدل HTTPS:
    echo    git remote remove origin
    echo    git remote add origin git@github.com:abnjamilahmad5-png/society-bot.git
    echo.
    pause
    exit /b 1
) else (
    echo.
    echo ==================================================
    echo   ✅ تم الرفع بنجاح على GitHub!
    echo ==================================================
    echo.
    echo الخطوة التالية: Railway.com
    echo.
    echo 1. اذهب إلى: https://railway.app
    echo 2. اختر: New Project
    echo 3. اختر: Deploy from GitHub repo
    echo 4. اختر: society-bot
    echo 5. أضف Variables:
    echo    - TOKEN = (توكن البوت)
    echo    - GUILD_ID = (ID السيرفر)
    echo    - PREFIX = !
    echo 6. اضغط: Deploy
    echo.
    echo 🎉 البوت سيعمل 24/7 بعد دقيقتين!
    echo.
    pause
)
