import discord
from discord.ext import commands
import json
import os
import sys
from datetime import datetime
import asyncio

# ══════════════════════════════════════════
#   𝑆𝑜𝑐𝑖𝑒𝑡𝑦 — البوت الأسطوري الشامل
# ══════════════════════════════════════════

class DataManager:
    """إدارة ملفات البيانات JSON"""
    
    @staticmethod
    def load_data(filename):
        if os.path.exists(f"data/{filename}"):
            with open(f"data/{filename}", "r", encoding="utf-8") as f:
                return json.load(f)
        return {}
    
    @staticmethod
    def save_data(filename, data):
        os.makedirs("data", exist_ok=True)
        with open(f"data/{filename}", "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

class ColorManager:
    PRIMARY = 0x36017F
    SUCCESS = 0x00AA00
    ERROR = 0xFF0000
    WARNING = 0xFFAA00
    INFO = 0x0099FF

class EmbedManager:
    @staticmethod
    def get_timestamp():
        return datetime.now().strftime("%d/%m/%Y • %H:%M:%S")
    
    @staticmethod
    def create_embed(title="", description="", color=ColorManager.PRIMARY, **kwargs):
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

class Society(commands.Bot):
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
        """الأولوية: متغيرات البيئة → ثم config.json"""
        config = {}
        
        # 1. اقرأ من config.json (الإعدادات العامة فقط)
        try:
            if os.path.exists("config.json"):
                with open("config.json", "r", encoding="utf-8") as f:
                    config.update(json.load(f))
        except Exception as e:
            print(f"⚠️ تحذير: {e}")
        
        # 2. متغيرات البيئة تتجاوز كل شيء (الأولوية القصوى)
        env_token = os.environ.get("TOKEN") or os.environ.get("BOT_TOKEN")
        if env_token:
            config['TOKEN'] = env_token
            print("✅ تم تحميل التوكن من متغيرات البيئة")
        else:
            print("⚠️ لم يتم العثور على TOKEN في البيئة")
        
        # باقي المتغيرات
        config['PREFIX'] = os.environ.get('PREFIX', config.get('PREFIX', '!'))
        
        return config
    
    async def load_cogs(self):
        cogs_folder = "cogs"
        if not os.path.exists(cogs_folder):
            os.makedirs(cogs_folder)
        
        for filename in os.listdir(cogs_folder):
            if filename.endswith(".py") and filename != "__init__.py":
                try:
                    await self.load_extension(f"cogs.{filename[:-3]}")
                    print(f"✅ تم تحميل: {filename}")
                except Exception as e:
                    print(f"❌ خطأ في {filename}: {e}")
    
    async def setup_hook(self):
        await self.load_cogs()
    
    async def on_ready(self):
        self.start_time = datetime.now()
        print(f"\n{'='*50}")
        print(f"✅ 𝑆𝑜𝑐𝑖𝑒𝑡𝑦 Bot Online!")
        print(f"✅ الاسم: {self.user.name}")
        print(f"✅ ID: {self.user.id}")
        print(f"✅ السيرفرات: {len(self.guilds)}")
        print(f"{'='*50}\n")
        
        try:
            synced = await self.tree.sync()
            print(f"✅ تم مزامنة {len(synced)} أمر Slash")
        except Exception as e:
            print(f"⚠️ مزامنة الأوامر: {e}")

async def main():
    bot = Society()
    
    token = bot.config.get("TOKEN")
    
    # التحقق من التوكن
    if not token or token in ["أضف توكن البوت هنا", "YOUR_BOT_TOKEN", ""]:
        print("❌ خطأ: التوكن غير موجود أو غير صحيح!")
        print(f"📋 التوكن الحالي: {token[:20] if token else 'None'}...")
        print("🔧 الحلول:")
        print("   1. في Railway: Variables → New Variable → KEY: TOKEN → VALUE: توكنك")
        print("   2. محلياً: export TOKEN='توكنك'")
        sys.exit(1)
    
    # التحقق من صحة التوكن (الطول والصيغة)
    if len(token) < 50:
        print(f"❌ التوكن قصير جداً ({len(token)} حرف)! يجب ~70 حرف")
        sys.exit(1)
    
    print(f"🔑 التوكن: {token[:20]}... ({len(token)} حرف)")
    
    try:
        await bot.start(token)
    except discord.LoginFailure as e:
        print(f"❌ فشل تسجيل الدخول: {e}")
        print("🔧 التوكن غلط! جيب توكن جديد من Discord Developer Portal")
        sys.exit(1)
    except Exception as e:
        print(f"❌ خطأ: {e}")
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(main())
