# 📱 خطوات نشر بوت 𝑆𝑜𝑐𝑖𝑒𝑡𝑦 على Railway.com (في 15 دقيقة)

---

## ✅ قبل البدء، تأكد من وجود:

- [ ] توكن البوت من Discord
- [ ] حساب GitHub (مجاني)
- [ ] حساب Railway.com (مجاني)

---

## 🎯 الخطوات:

### **الخطوة 1: إنشاء مستودع GitHub**

```bash
# 1. فتح موقع GitHub والتسجيل
https://github.com

# 2. إنشاء مستودع جديد:
# - اسم: society-bot
# - اختر: Public
# - أضف: Add a README file
```

### **الخطوة 2: رفع الكود على GitHub**

```bash
# في Terminal (Windows: PowerShell)
cd C:\Users\abnja\شاي

# تهيئة Git
git init
git add .
git commit -m "🎉 بوت Society الأول"
git remote add origin https://github.com/YOUR_USERNAME/society-bot.git
git branch -M main
git push -u origin main
```

**ملاحظة:** استبدل `YOUR_USERNAME` باسم حسابك على GitHub

### **الخطوة 3: إنشاء حساب Railway**

1. اذهب إلى: **https://railway.app/**
2. اضغط **Sign Up**
3. اختر **Continue with GitHub**
4. وافق على الأذونات

### **الخطوة 4: ربط المشروع بـ Railway**

1. بعد تسجيل الدخول، اضغط **Create New Project**
2. اختر **Deploy from GitHub repo**
3. ابحث عن **society-bot**
4. اختره واضغط **Deploy**

**استرجع 2-3 دقائق لحين الإعداد...**

### **الخطوة 5: إضافة متغيرات البيئة**

بعد نجاح النشر:

1. في صفحة Railway، اختر **Variables**
2. أضف المتغيرات التالية:

```
TOKEN = (انسخ توكن البوت هنا)
PREFIX = !
GUILD_ID = (ID السيرفر الخاص بك)
ADMIN_ROLE = (ID رتبة الأدمن)
MOD_ROLE = (ID رتبة المود)
```

3. اضغط **Save** و **Redeploy**

---

## 🔑 كيف تحصل على التوكن؟

```
1. اذهب إلى: https://discord.com/developers/applications
2. اختر تطبيقك (Society Bot)
3. اختر: Bot
4. انسخ TOKEN من قسم "TOKEN"
5. ألصقه في متغير TOKEN في Railway
```

---

## 🔢 كيف تحصل على IDs؟

### GUILD_ID (ID السيرفر):
```
1. في Discord، أتفعّل "Developer Mode"
   - Settings → Advanced → Developer Mode → تفعيل
2. انقر بزر اليمين على اسم السيرفر
3. اختر "Copy Server ID"
```

### ADMIN_ROLE و MOD_ROLE:
```
1. انقر بزر اليمين على الرتبة
2. اختر "Copy Role ID"
```

### CHANNEL IDs:
```
1. انقر بزر اليمين على القناة
2. اختر "Copy Channel ID"
```

---

## 📊 مراقبة البوت:

في Railway:

1. اختر **Logs** لرؤية السجلات
2. ستشاهد رسائل مثل:
   ```
   ✓ تم تسجيل دخول البوت: 𝑆𝑜𝑐𝑖𝑒𝑡𝑦
   ✓ تم مزامنة 60 أمر Slash
   ```

---

## 🔄 تحديث الكود:

كل مرة تريد تحديث الكود:

```bash
# عدّل الملفات محلياً
# ثم:

git add .
git commit -m "🔧 تحديث: وصف التحديث"
git push origin main

# Railway سيعيد النشر تلقائياً! 🚀
```

---

## 🆘 حل المشاكل:

### ❌ البوت لا يظهر أنه اتصل

```
✓ تحقق من الـ Logs في Railway
✓ تأكد من TOKEN صحيح
✓ اضغط Redeploy
```

### ❌ الأوامر لا تعمل

```
✓ تأكد من GUILD_ID صحيح
✓ انتظر 5 دقائق بعد النشر
✓ أعد شحن Discord (Ctrl+Shift+R)
```

### ❌ الأخطاء في الـ Logs

```
✓ اقرأ رسالة الخطأ بعناية
✓ ابحث عن السطر الأخير
✓ جرب الحل المناسب
```

---

## 💾 الحفاظ على البيانات:

البيانات تُحفظ في مجلد `data/` تلقائياً.

لكن عند إعادة تشغيل Railway، قد تُفقد البيانات.

### الحل: استخدام Volume

```
في Railway → Variables:
- Mount path: /app/data
- Size: 100 MB (مثالي للبوت الصغير)
```

---

## 💰 التكلفة:

| الخدمة | السعر |
|-------|-------|
| GitHub | مجاني 🎉 |
| Railway | $5/شهر (مجاني في البداية) |
| Discord | مجاني 🎉 |
| **الإجمالي** | **مجاني تماماً** |

---

## 🎊 هذا كل شيء!

الآن:
- البوت يعمل 24/7 على Railway
- لا تحتاج لتشغيل جهازك
- كل تحديث GitHub ينشر تلقائياً

---

## 📚 روابط مفيدة:

- Railway Docs: https://docs.railway.app/
- Discord.py: https://discordpy.readthedocs.io/
- Discord Developers: https://discord.com/developers/

---

**🚀 عاش! البوت الآن متصل مع السحابة!**

