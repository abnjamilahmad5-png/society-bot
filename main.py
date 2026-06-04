import discord
from discord.ext import commands
import json
import os
import sys
from datetime import datetime
import asyncio
from dotenv import load_dotenv
from config.logger import logger

# تحميل متغيرات البيئة من .env
load_dotenv()

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
    """مدير الـ Embeds - يحتوي على جميع أنواع الإمبيدات المستخدمة في الكوجز"""

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

    # ─── الأنواع المختصرة التي تستخدمها الكوجز ───────────────────────────

    @staticmethod
    def info(title="", description="", **kwargs):
        """Embed معلومات - لون أزرق"""
        embed = discord.Embed(
            title=title,
            description=description,
            color=ColorManager.INFO,
            timestamp=datetime.now()
        )
        embed.set_footer(text=f"𝑆𝑜𝑐𝑖𝑒𝑡𝑦 ✦ {EmbedManager.get_timestamp()}")
        for k, v in kwargs.items():
            embed.add_field(name=k, value=v, inline=False)
        return embed

    @staticmethod
    def success(title="", description="", **kwargs):
        """Embed نجاح - لون أخضر"""
        embed = discord.Embed(
            title=title,
            description=description,
            color=ColorManager.SUCCESS,
            timestamp=datetime.now()
        )
        embed.set_footer(text=f"𝑆𝑜𝑐𝑖𝑒𝑡𝑦 ✦ {EmbedManager.get_timestamp()}")
        for k, v in kwargs.items():
            embed.add_field(name=k, value=v, inline=False)
        return embed

    @staticmethod
    def error(title="", description="", **kwargs):
        """Embed خطأ - لون أحمر"""
        embed = discord.Embed(
            title=title,
            description=description,
            color=ColorManager.ERROR,
            timestamp=datetime.now()
        )
        embed.set_footer(text=f"𝑆𝑜𝑐𝑖𝑒𝑡𝑦 ✦ {EmbedManager.get_timestamp()}")
        for k, v in kwargs.items():
            embed.add_field(name=k, value=v, inline=False)
        return embed

    @staticmethod
    def warning(title="", description="", **kwargs):
        """Embed تحذير - لون برتقالي"""
        embed = discord.Embed(
            title=title,
            description=description,
            color=ColorManager.WARNING,
            timestamp=datetime.now()
        )
        embed.set_footer(text=f"𝑆𝑜𝑐𝑖𝑒𝑡𝑦 ✦ {EmbedManager.get_timestamp()}")
        for k, v in kwargs.items():
            embed.add_field(name=k, value=v, inline=False)
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
        self.logger = logger
        self.start_time = None

    def load_config(self):
        """الأولوية: متغيرات البيئة (.env) → ثم config.json"""
        config = {}

        # 1. اقرأ من config.json
        try:
            if os.path.exists("config.json"):
                with open("config.json", "r", encoding="utf-8") as f:
                    config.update(json.load(f))
                logger.info("✅ تم تحميل config.json")
        except Exception as e:
            logger.warning(f"⚠️ تحذير قراءة config.json: {e}")

        # 2. متغيرات البيئة تتجاوز كل شيء (.env و Railway)
        env_token = os.getenv("TOKEN") or os.getenv("BOT_TOKEN")
        if env_token and env_token != "YOUR_BOT_TOKEN_HERE":
            config['TOKEN'] = env_token
            logger.info("✅ تم تحميل التوكن من ملف .env أو متغيرات البيئة")
        else:
            logger.warning("⚠️ التوكن لم يتم تحميله من .env - يُرجى تحديثه في .env")

        config['PREFIX'] = os.getenv('PREFIX', config.get('PREFIX', '!'))

        return config

    async def load_cogs(self):
        cogs_folder = "cogs"
        if not os.path.exists(cogs_folder):
            os.makedirs(cogs_folder)

        loaded = 0
        failed = 0
        for filename in sorted(os.listdir(cogs_folder)):
            if filename.endswith(".py") and filename != "__init__.py":
                try:
                    await self.load_extension(f"cogs.{filename[:-3]}")
                    logger.info(f"  ✅ {filename}")
                    loaded += 1
                except Exception as e:
                    logger.error(f"  ❌ {filename}: {e}")
                    failed += 1
        logger.info(f"\n📦 الكوجز: {loaded} محملة، {failed} فشلت\n")

    async def setup_hook(self):
        await self.load_cogs()

    async def on_ready(self):
        self.start_time = datetime.now()
        logger.info(f"\n{'='*50}")
        logger.info(f"✅ 𝑆𝑜𝑐𝑖𝑒𝑡𝑦 Bot Online!")
        logger.info(f"✅ الاسم: {self.user.name}")
        logger.info(f"✅ ID: {self.user.id}")
        logger.info(f"✅ السيرفرات: {len(self.guilds)}")
        logger.info(f"{'='*50}\n")

        try:
            # إزالة أي أوامر مكررة قديمة
            self.tree.clear_commands(guild=None)
            synced = await self.tree.sync()
            logger.info(f"✅ تم مزامنة {len(synced)} أمر Slash (Global)")
        except Exception as e:
            logger.warning(f"⚠️ مزامنة الأوامر: {e}")


async def main():
    bot = Society()

    token = bot.config.get("TOKEN")

    # التحقق من التوكن
    if not token or token in ["أضف توكن البوت هنا", "YOUR_BOT_TOKEN", "YOUR_BOT_TOKEN_HERE", ""]:
        logger.critical("❌ خطأ: التوكن غير موجود أو غير صحيح!")
        logger.critical("🔧 الحلول:")
        logger.critical("   • حدّث ملف .env مع التوكن الصحيح")
        logger.critical("   • في Railway: Variables → New Variable → KEY: TOKEN → VALUE: توكنك")
        sys.exit(1)

    if len(token) < 50:
        logger.critical(f"❌ التوكن قصير جداً ({len(token)} حرف)! يجب ~70 حرف")
        sys.exit(1)

    # إخفاء التوكن - طباعة آمنة فقط
    masked_token = f"{token[:10]}...{token[-5:]}" if len(token) > 15 else "***"
    logger.info(f"🔑 التوكن محمّل بنجاح (الطول: {len(token)} حرف)")

    try:
        await bot.start(token)
    except discord.LoginFailure as e:
        logger.critical(f"❌ فشل تسجيل الدخول: {e}")
        logger.critical("🔧 التوكن غلط! جيب توكن جديد من Discord Developer Portal")
        sys.exit(1)
    except Exception as e:
        logger.critical(f"❌ خطأ غير متوقع: {e}")
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
