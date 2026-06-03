import discord
from discord.ext import commands
import json
import os
from datetime import datetime
import asyncio
from dotenv import load_dotenv

load_dotenv()

class DataManager:
    """إدارة ملفات البيانات JSON"""
    
    @staticmethod
    def load_data(filename):
        """تحميل بيانات من ملف JSON"""
        if os.path.exists(f"data/{filename}"):
            with open(f"data/{filename}", "r", encoding="utf-8") as f:
                return json.load(f)
        return {}
    
    @staticmethod
    def save_data(filename, data):
        """حفظ البيانات في ملف JSON"""
        os.makedirs("data", exist_ok=True)
        with open(f"data/{filename}", "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

class ColorManager:
    """إدارة الألوان في الإمبيدات"""
    PRIMARY = 0x36017F  # بنفسجي داكن
    SUCCESS = 0x00AA00  # أخضر
    ERROR = 0xFF0000    # أحمر
    WARNING = 0xFFAA00  # برتقالي
    INFO = 0x0099FF    # أزرق

class EmbedManager:
    """مدير الإمبيدات الموحد"""
    
    @staticmethod
    def get_timestamp():
        """الحصول على التاريخ والوقت الحالي"""
        return datetime.now().strftime("%d/%m/%Y • %H:%M:%S")
    
    @staticmethod
    def create_embed(title="", description="", color=ColorManager.PRIMARY, **kwargs):
        """إنشاء إمبيد موحد"""
        embed = discord.Embed(
            title=title,
            description=description,
            color=color,
            timestamp=datetime.now()
        )
        embed.set_footer(text=f"𝑆𝑜𝑐𝑖𝑒𝑡𝑦 ✦ {EmbedManager.get_timestamp()}")
        
        for field_title, field_value in kwargs.items():
            embed.add_field(name=field_title, value=field_value, inline=False)
        
        return embed
    
    @staticmethod
    def success(title, description, **kwargs):
        """إمبيد نجاح"""
        return EmbedManager.create_embed(title, description, ColorManager.SUCCESS, **kwargs)
    
    @staticmethod
    def error(title, description, **kwargs):
        """إمبيد خطأ"""
        return EmbedManager.create_embed(title, description, ColorManager.ERROR, **kwargs)
    
    @staticmethod
    def warning(title, description, **kwargs):
        """إمبيد تحذير"""
        return EmbedManager.create_embed(title, description, ColorManager.WARNING, **kwargs)
    
    @staticmethod
    def info(title, description, **kwargs):
        """إمبيد معلومات"""
        return EmbedManager.create_embed(title, description, ColorManager.INFO, **kwargs)

class Society(commands.Bot):
    """بوت 𝑆𝑜𝑐𝑖𝑒𝑡𝑦 الرئيسي"""
    
    def __init__(self):
        intents = discord.Intents.all()
        super().__init__(
            command_prefix="!",
            intents=intents,
            help_command=None,
            activity=discord.Activity(
                type=discord.ActivityType.watching,
                name="👁️ يراقب 𝑆𝑜𝑐𝑖𝑒𝑡𝑦 • /help"
            )
        )
        self.config = self.load_config()
        self.data_manager = DataManager()
        self.embed_manager = EmbedManager()
        self.color_manager = ColorManager()
        self.start_time = None
    
    def load_config(self):
        """تحميل الإعدادات من متغيرات البيئة أو config.json"""
        config = {}
        
        # حاول تحميل من متغيرات البيئة أولاً
        if os.getenv('TOKEN'):
            config['TOKEN'] = os.getenv('TOKEN')
        
        # ثم حاول تحميل من config.json
        try:
            if os.path.exists("config.json"):
                with open("config.json", "r", encoding="utf-8") as f:
                    config.update(json.load(f))
        except Exception as e:
            print(f"⚠️ تحذير: لم يتمكن من تحميل config.json: {e}")
        
        # استخدم متغيرات البيئة إن وجدت
        config['TOKEN'] = os.getenv('TOKEN', config.get('TOKEN'))
        config['PREFIX'] = os.getenv('PREFIX', config.get('PREFIX', '!'))
        config['GUILD_ID'] = int(os.getenv('GUILD_ID', config.get('GUILD_ID', 0)))
        
        return config
    
    def save_config(self):
        """حفظ الإعدادات في config.json"""
        with open("config.json", "w", encoding="utf-8") as f:
            json.dump(self.config, f, ensure_ascii=False, indent=2)
    
    async def load_cogs(self):
        """تحميل جميع الـ Cogs"""
        cogs_folder = "cogs"
        if not os.path.exists(cogs_folder):
            os.makedirs(cogs_folder)
            print(f"✓ تم إنشاء مجلد {cogs_folder}")
        
        for filename in os.listdir(cogs_folder):
            if filename.endswith(".py") and filename != "__init__.py":
                try:
                    await self.load_extension(f"cogs.{filename[:-3]}")
                    print(f"✓ تم تحميل Cog: {filename}")
                except Exception as e:
                    print(f"✗ خطأ في تحميل {filename}: {e}")
    
    async def setup_hook(self):
        """تنفيذ الإعداد الأولي"""
        await self.load_cogs()
    
    async def on_ready(self):
        """تم الاتصال بـ Discord"""
        self.start_time = datetime.now()
        print(f"\n{'='*50}")
        print(f"✓ تم تسجيل دخول البوت: {self.user.name}")
        print(f"✓ ID البوت: {self.user.id}")
        print(f"✓ عدد السيرفرات: {len(self.guilds)}")
        print(f"✓ عدد المستخدمين: {sum(g.member_count for g in self.guilds)}")
        print(f"{'='*50}\n")
        
        try:
            synced = await self.tree.sync()
            print(f"✓ تم مزامنة {len(synced)} أمر Slash")
        except Exception as e:
            print(f"✗ خطأ في مزامنة الأوامر: {e}")
    
    async def on_command_error(self, ctx, error):
        """معالجة أخطاء الأوامر العادية"""
        if isinstance(error, commands.MissingPermissions):
            embed = self.embed_manager.error(
                "❌ صلاحيات غير كافية",
                "ليس لديك صلاحيات كافية لتنفيذ هذا الأمر"
            )
        elif isinstance(error, commands.CommandOnCooldown):
            embed = self.embed_manager.warning(
                "⏱️ الأمر قيد الانتظار",
                f"يرجى الانتظار {error.retry_after:.1f} ثانية قبل إعادة المحاولة"
            )
        elif isinstance(error, commands.MissingRequiredArgument):
            embed = self.embed_manager.error(
                "❌ معاملات ناقصة",
                "يرجى التحقق من صيغة الأمر"
            )
        else:
            embed = self.embed_manager.error(
                "❌ حدث خطأ",
                f"```{str(error)[:100]}```"
            )
        
        try:
            await ctx.reply(embed=embed, ephemeral=True)
        except:
            pass

async def main():
    """نقطة البداية الرئيسية"""
    bot = Society()
    async with bot:
        token = bot.config.get("TOKEN")
        if not token or token == "أضف توكن البوت هنا":
            print("❌ خطأ: التوكن غير موجود!")
            print("📍 في Railway: أضف TOKEN في Variables")
            print("📍 محلياً: أضف TOKEN في config.json")
            return
        
        try:
            await bot.start(token)
        except Exception as e:
            print(f"❌ خطأ في بدء البوت: {e}")

if __name__ == "__main__":
    asyncio.run(main())
