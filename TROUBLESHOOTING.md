# 🆘 دليل استكشاف الأخطاء — بوت 𝑆𝑜𝑐𝑖𝑒𝑡𝑦

---

## ❓ الأسئلة الشائعة

### ❌ البوت لا يعمل/لا يستجيب

**الحل:**
```bash
# 1. تأكد من التوكن
✓ افتح config.json
✓ تأكد أن TOKEN ليس "أضف توكن البوت هنا"

# 2. تأكد من المكتبات
pip install -r requirements.txt

# 3. شغل البوت
python main.py
```

### ❌ "ModuleNotFoundError: No module named 'discord'"

**الحل:**
```bash
pip install discord.py==2.3.2
```

### ❌ البوت يشتغل لكن الأوامر لا تظهر

**الحل:**
```
✓ انتظر 5 ثواني بعد التشغيل
✓ جرب /help أو !help
✓ تأكد من صلاحيات البوت في السيرفر
✓ أعد شحن الديسكورد (Ctrl+Shift+R)
```

### ❌ "Invalid Token" أو "Unauthorized"

**الحل:**
```
✓ تأكد من نسخ التوكن بشكل صحيح
✓ لا تضع مسافات قبل أو بعد التوكن
✓ تأكد أن البوت مفعل في Discord Developer Portal
```

### ❌ "MissingPermissions" عند تنفيذ الأوامر

**الحل:**
```
✓ تأكد من أن البوت لديه الصلاحيات:
  - Send Messages
  - Embed Links
  - Manage Roles
  - Manage Channels
  - Ban Members
```

### ❌ قاعدة البيانات لا تحفظ البيانات

**الحل:**
```bash
# حذف مجلد data وأعد التشغيل
rm -r data/
python main.py

# ستُعاد البيانات تلقائياً
```

---

## 🔍 خطوات التشخيص

### 1. تحقق من المكتبات
```bash
pip list | grep discord
```

### 2. تحقق من المسار
```bash
pwd  # Linux/Mac
cd   # Windows
```

### 3. تحقق من الملفات
```bash
ls -la config.json main.py requirements.txt
```

### 4. جرب البوت يدويّاً
```bash
python main.py
```

### 5. انظر إلى رسائل الخطأ
```
✓ انسخ رسالة الخطأ الكاملة
✓ ابحث عن السطر الأخير في الخطأ
✓ جرب الحل المناسب
```

---

## 📋 قائمة التحقق قبل البدء

- [ ] تثبيت Python 3.10+
- [ ] تثبيت pip
- [ ] تثبيت المكتبات: `pip install -r requirements.txt`
- [ ] نسخ التوكن من Discord Developer Portal
- [ ] وضع التوكن في config.json
- [ ] تحديد GUILD_ID (ID السيرفر)
- [ ] التحقق من صلاحيات البوت
- [ ] تشغيل: `python main.py`

---

## 🎯 خطوات تصحيح الأخطاء الشائعة

### الخطأ: "intents flag value must be int"

**الحل:**
تأكد من أن IntentsManagerintents بشكل صحيح في main.py:
```python
intents = discord.Intents.all()
```

### الخطأ: "Cog 'help' not found"

**الحل:**
```bash
# تأكد من وجود help.py في مجلد cogs
ls cogs/help.py

# تأكد من أن الملف ليس فارغاً
cat cogs/help.py | head -5
```

### الخطأ: "JSONDecodeError"

**الحل:**
قد يكون ملف JSON تالفاً:
```bash
# احذف ملف البيانات وأعد التشغيل
rm data/economy.json  # مثال
python main.py
```

### الخطأ: "AttributeError: 'NoneType' object"

**الحل:**
قد تكون قيمة معينة غير معرّفة في config.json:
```json
{
  "GUILD_ID": 123456789,
  "ADMIN_ROLE": 987654321
}
```

---

## 🆘 اطلب المساعدة

إذا لم تجد الحل:

1. **اقرأ الخطأ بعناية**
   - انظر إلى رقم السطر
   - اقرأ الرسالة الكاملة

2. **ابحث عن الخطأ على Google**
   - نسخ الخطأ الدقيق
   - أضف "discord.py" للبحث

3. **تحقق من Discord.py Documentation**
   - https://discordpy.readthedocs.io/

4. **جرب المثال البسيط**
```python
import discord
from discord.ext import commands

bot = commands.Bot(command_prefix="!")

@bot.event
async def on_ready():
    print(f"تم تسجيل دخول البوت: {bot.user}")

bot.run("YOUR_TOKEN")
```

---

## ✅ علامات النجاح

عند النجاح ستشاهد:

```
==================================================
✓ تم تسجيل دخول البوت: 𝑆𝑜𝑐𝑖𝑒𝑡𝑦
✓ ID البوت: 1234567890
✓ عدد السيرفرات: 1
✓ عدد المستخدمين: 50
✓ تم مزامنة 60 أمر Slash
==================================================
```

---

## 🎓 المزيد من الموارد

- **Discord.py Documentation**: https://discordpy.readthedocs.io/
- **Discord Developer Portal**: https://discord.com/developers/applications
- **Python Documentation**: https://docs.python.org/3/

---

**نتمنى لك التوفيق! 🚀**

