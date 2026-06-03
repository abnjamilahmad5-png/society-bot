# 🚀 تشغيل بوت 𝑆𝑜𝑐𝑖𝑒𝑡𝑦 على Railway.com

---

## 📋 المتطلبات:

✅ حساب GitHub (مجاني)  
✅ حساب Railway.com (مجاني)  
✅ توكن البوت من Discord  
✅ فهم أساسي لـ Git  

---

## 🎯 الخطوات (10 دقائق فقط):

### **الخطوة 1️⃣ : تحضير المشروع على GitHub**

```bash
# 1. فتح Terminal في مجلد المشروع
cd c:\Users\abnja\شاي

# 2. إنشاء مستودع Git محلي
git init

# 3. إضافة كل الملفات
git add .

# 4. كتابة أول commit
git commit -m "🎉 بوت Society الأول"

# 5. إضافة المستودع البعيد (GitHub)
# (بعد إنشاء مستودع على GitHub)
git remote add origin https://github.com/YOUR_USERNAME/society-bot.git
git branch -M main
git push -u origin main
```

### **الخطوة 2️⃣ : إنشاء حساب Railway**

1. اذهب إلى **https://railway.app**
2. اضغط **Sign Up** (يمكنك استخدام GitHub)
3. سجل الدخول باستخدام حسابك على GitHub
4. اختر **Create New Project**

### **الخطوة 3️⃣ : ربط GitHub مع Railway**

1. اختر **Deploy from GitHub**
2. اختر المستودع **society-bot**
3. اضغط **Deploy**


### **الخطوة 5️⃣ : تعديل main.py لقراءة متغيرات البيئة**

استبدل الأسطر الأولى في `main.py`:

```python
import discord
from discord.ext import commands
import json
import os
from datetime import datetime
import asyncio
from dotenv import load_dotenv  # ← أضف هذا

load_dotenv()  # ← أضف هذا

# قراءة من متغيرات البيئة
TOKEN = os.getenv('TOKEN')
if not TOKEN:
    # استخدم config.json كـ fallback
    try:
        with open('config.json', 'r', encoding='utf-8') as f:
            config = json.load(f)
            TOKEN = config.get('TOKEN')
    except:
        TOKEN = None

if not TOKEN:
    raise ValueError("❌ التوكن غير موجود! أضفه في متغيرات البيئة")
```

### **الخطوة 6️⃣ : تحديث requirements.txt**

أضف `python-dotenv`:

```
discord.py==2.3.2
python-dotenv==1.0.0
aiohttp==3.9.1
```

### **الخطوة 7️⃣ : رفع التحديثات إلى GitHub**

```bash
git add .
git commit -m "🔧 تحضير Railway deployment"
git push origin main
```

---

## ✨ Railway سيقوم بـ:

✅ سحب الكود من GitHub تلقائياً  
✅ تثبيت المكتبات من `requirements.txt`  
✅ تشغيل `python main.py` تلقائياً  
✅ إعادة التشغيل عند الأعطال  
✅ الاحتفاظ بالبيانات JSON في مجلد `data/`  

---

## 📊 مشاهدة السجلات:

في Railway:
- اذهب إلى **Logs**
- شاهد رسائل البوت في الوقت الفعلي
- تحقق من الأخطاء

```
✓ تم تسجيل دخول البوت: 𝑆𝑜𝑐𝑖𝑒𝑡𝑦
✓ تم مزامنة 60 أمر
✓ البوت جاهز!
```

---

## 🔧 حل المشاكل الشائعة:

### ❌ الخطأ: "ModuleNotFoundError: No module named 'discord'"

**الحل:**
```
✓ تأكد من requirements.txt يحتوي على discord.py==2.3.2
✓ اضغط Redeploy في Railway
```

### ❌ الخطأ: "TOKEN is invalid"

**الحل:**
```
✓ تحقق من TOKEN في Variables
✓ انسخ التوكن الكامل بدون مسافات
✓ اضغط Redeploy
```

### ❌ البيانات لا تُحفظ

**الحل:**
```
✓ Railway يحفظ البيانات في /data/ افتراضياً
✓ لكن قد تُفقد عند إعادة تشغيل
✓ استخدم قاعدة بيانات خارجية (MongoDB, PostgreSQL)
```

### ❌ البوت يتوقف بعد دقائق

**الحل:**
```
✓ تأكد من أن main.py ينفذ bot.run() في النهاية
✓ استخدم try/except للأخطاء
✓ اضغط Redeploy
```

---

## 📚 متغيرات البيئة الموصى بها:

```
TOKEN = توكن البوت
GUILD_ID = ID السيرفر الرئيسي
ADMIN_ROLE = ID رتبة الأدمن
MOD_ROLE = ID رتبة المود
PREFIX = !
```

---

## 🎊 بعد النجاح:

1. البوت سيعمل **24/7** على خوادم Railway
2. لن تحتاج لتشغيل البوت على جهازك
3. يمكنك إيقاف جهازك والبوت مستمر يعمل
4. كل تحديث على GitHub سيُطبق تلقائياً

---

## 💡 نصائح إضافية:

### استخدام PostgreSQL لـ Volumes:

أضف volume في Railway:
```
Mount Path: /app/data
```

هذا سيحفظ البيانات حتى عند إعادة التشغيل.

### الحد المجاني:

- Railway توفر **$5 شهرياً** مجاني
- يكفي لبوت صغير/متوسط
- لا حاجة لبطاقة ائتمان في البداية

---

## 🚀 جرب الآن!

1. إنشاء مستودع GitHub
2. اذهب إلى railway.app
3. اختر "Deploy from GitHub"
4. اختر المشروع
5. أضف متغيرات البيئة
6. اضغط Deploy

**وخلاص! البوت يعمل! 🎉**

---

## 📞 الدعم:

- **Railway Docs**: https://docs.railway.app/
- **Discord.py**: https://discordpy.readthedocs.io/
- **GitHub**: https://github.com/

