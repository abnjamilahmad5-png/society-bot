import discord
from discord.ext import commands
from discord import app_commands
from main import EmbedManager, ColorManager

class HelpView(discord.ui.View):
    """قائمة المساعدة التفاعلية"""
    
    def __init__(self, ctx):
        super().__init__(timeout=180)
        self.ctx = ctx
        self.embed_manager = EmbedManager()
    
    @discord.ui.select(
        placeholder="اختر فئة المساعدة",
        options=[
            discord.SelectOption(label="🎫 التكتات", value="tickets"),
            discord.SelectOption(label="🛡️ الحماية", value="protection"),
            discord.SelectOption(label="⚖️ الإشراف", value="moderation"),
            discord.SelectOption(label="📊 المستويات", value="levels"),
            discord.SelectOption(label="💰 الاقتصاد", value="economy"),
            discord.SelectOption(label="🎉 الهدايا", value="giveaway"),
            discord.SelectOption(label="💡 الاقتراحات", value="suggestions"),
            discord.SelectOption(label="📋 القنوات", value="channels"),
            discord.SelectOption(label="🎭 الرتب", value="roles"),
            discord.SelectOption(label="ℹ️ المعلومات", value="info"),
            discord.SelectOption(label="🎮 الترفيه", value="fun"),
            discord.SelectOption(label="📝 النصوص", value="echo"),
            discord.SelectOption(label="⚙️ الإعداد", value="setup"),
        ]
    )
    async def select_category(self, interaction: discord.Interaction, select: discord.ui.Select):
        """اختيار الفئة"""
        await interaction.response.defer()
        category = select.values[0]
        
        embeds = {
            "tickets": self._get_tickets_help(),
            "protection": self._get_protection_help(),
            "moderation": self._get_moderation_help(),
            "levels": self._get_levels_help(),
            "economy": self._get_economy_help(),
            "giveaway": self._get_giveaway_help(),
            "suggestions": self._get_suggestions_help(),
            "channels": self._get_channels_help(),
            "roles": self._get_roles_help(),
            "info": self._get_info_help(),
            "fun": self._get_fun_help(),
            "echo": self._get_echo_help(),
            "setup": self._get_setup_help(),
        }
        
        embed = embeds.get(category, self.embed_manager.error("خطأ", "فئة غير معروفة"))
        
        await interaction.followup.send(embed=embed, ephemeral=False)
    
    def _get_tickets_help(self):
        """أوامر التكتات"""
        return self.embed_manager.info(
            "🎫 نظام التكتات",
            "إدارة تكتات الدعم الفني",
            **{
                "/ticket-panel": "إرسال بانيل فتح التكتات",
                "/ticket-stats": "عرض إحصائيات التكتات",
                "/add-user @user": "إضافة مستخدم للتكت الحالي",
                "/remove-user @user": "إزالة مستخدم من التكت",
                "/ticket-close": "إغلاق التكت مع التقييم",
                "/ticket-rename [name]": "تغيير اسم التكت",
                "/ticket-claim": "استلام التكت كموظف دعم",
                "/ticket-unclaim": "إرجاع التكت",
            }
        )
    
    def _get_protection_help(self):
        """أوامر الحماية"""
        return self.embed_manager.info(
            "🛡️ نظام الحماية",
            "حماية السيرفر من الهجمات",
            **{
                "/shield-status": "عرض حالة أنظمة الحماية",
                "/shield-toggle [system]": "تفعيل/تعطيل نظام حماية",
                "/antinuke-whitelist @user": "استثناء شخص من الحماية",
                "/antinuke-whitelist-remove @user": "إزالة الاستثناء",
            }
        )
    
    def _get_moderation_help(self):
        """أوامر الإشراف"""
        return self.embed_manager.info(
            "⚖️ نظام الإشراف",
            "إدارة السيرفر والأعضاء",
            **{
                "/ban @user [reason]": "حظر مستخدم",
                "/unban [id] [reason]": "إلغاء حظر",
                "/kick @user [reason]": "طرد مستخدم",
                "/warn @user [reason]": "إنذار مستخدم",
                "/warnings @user": "عرض إنذارات المستخدم",
                "/clearwarns @user": "حذف جميع الإنذارات",
                "/timeout @user [duration] [reason]": "صمت مستخدم",
                "/untimeout @user": "إلغاء الصمت",
                "/purge [count]": "حذف رسائل",
                "/lock [reason]": "قفل القناة",
                "/unlock": "فتح القناة",
                "!ban / !kick / !warn": "نسخ الأوامر بالـ prefix",
            }
        )
    
    def _get_levels_help(self):
        """أوامر المستويات"""
        return self.embed_manager.info(
            "📊 نظام المستويات",
            "نظام الـ XP والترقية",
            **{
                "/rank [@user]": "عرض مستوى المستخدم",
                "/leaderboard": "أفضل 10 أعضاء",
                "/addxp @user [amount]": "إضافة XP",
                "/removexp @user [amount]": "إزالة XP",
                "/setxp @user [amount]": "تعيين XP",
                "/level-rewards": "عرض مكافآت المستويات",
                "/set-level-channel [#channel]": "تحديد قناة الإعلانات",
            }
        )
    
    def _get_economy_help(self):
        """أوامر الاقتصاد - نظام الكريديت"""
        return self.embed_manager.info(
            "💎 نظام الكريديت العالمي",
            "نظام الكريديت المتكامل مثل ProBot",
            **{
                "/balance [@user]": "عرض رصيد الكريديت",
                "/transfer @user [amount]": "تحويل كريديت",
                "/credits-info": "معلومات الكريديت",
            }
        )
    
    def _get_giveaway_help(self):
        """أوامر الهدايا"""
        return self.embed_manager.info(
            "🎉 نظام الهدايا",
            "تنظيم الهدايا والجوائز",
            **{
                "/giveaway-start [duration] [winners] [prize]": "بدء هدية جديدة",
                "/giveaway-end [message_id]": "إنهاء الهدية",
                "/giveaway-reroll [message_id]": "إعادة اختيار الفائزين",
                "/giveaway-list": "قائمة الهدايا الحالية",
                "/giveaway-pause [message_id]": "إيقاف الهدية مؤقتاً",
                "/giveaway-resume [message_id]": "استئناف الهدية",
            }
        )
    
    def _get_suggestions_help(self):
        """أوامر الاقتراحات"""
        return self.embed_manager.info(
            "💡 نظام الاقتراحات",
            "نظام الاقتراحات والتصويت",
            **{
                "/suggest [text]": "إرسال اقتراح جديد",
                "/suggestion-accept [id]": "قبول اقتراح",
                "/suggestion-deny [id]": "رفض اقتراح",
                "/suggestion-consider [id]": "قيد الدراسة",
                "/suggestions-list": "قائمة الاقتراحات",
            }
        )
    
    def _get_channels_help(self):
        """أوامر القنوات"""
        return self.embed_manager.info(
            "📋 نظام القنوات",
            "إنشاء قنوات تلقائية بقوالب",
            **{
                "/channels": "فتح قائمة القوالب",
                "/channels-add [category] [name] [type]": "إضافة قناة منفردة",
                "/channels-delete [template]": "حذف قالب كامل",
            }
        )
    
    def _get_roles_help(self):
        """أوامر الرتب"""
        return self.embed_manager.info(
            "🎭 نظام الرتب التفاعلية",
            "رتب اختيارية للأعضاء",
            **{
                "/roles-panel": "إرسال بانيل الرتب",
                "/add-selfrole @role [category]": "إضافة رتبة للاختيار",
                "/remove-selfrole @role": "إزالة رتبة من الاختيار",
                "/role-add @user @role": "إعطاء رتبة",
                "/role-remove @user @role": "إزالة رتبة",
                "/role-info @role": "معلومات الرتبة",
            }
        )
    
    def _get_info_help(self):
        """أوامر المعلومات"""
        return self.embed_manager.info(
            "ℹ️ نظام المعلومات",
            "معلومات عن المستخدمين والسيرفر",
            **{
                "/userinfo [@user]": "معلومات مستخدم",
                "/serverinfo": "معلومات السيرفر",
                "/botinfo": "معلومات البوت",
                "/avatar [@user]": "صورة المستخدم",
                "/ping": "اختبار الاتصال",
                "/uptime": "وقت التشغيل",
                "/invite": "رابط دعوة البوت",
            }
        )
    
    def _get_fun_help(self):
        """أوامر الترفيه - تم حذفها"""
        return self.embed_manager.info(
            "🎮 الترفيه - تم التطوير",
            "تم حذف أوامر الترفيه لتركيز أفضل على أنظمة السيرفر",
            **{
                "الهدايا والجوائز": "موجودة في نظام Giveaway",
            }
        )
    
    def _get_echo_help(self):
        """أوامر النصوص والتكرار"""
        return self.embed_manager.info(
            "📝 نظام النصوص والتكرار",
            "البوت يردد الرسائل كما هي",
            **{
                "/text [message]": "البوت يردد الرسالة بنفس الصيغة",
            }
        )
    
    def _get_setup_help(self):
        """أوامر الإعداد"""
        return self.embed_manager.info(
            "⚙️ نظام الإعداد",
            "إعدادات البوت المتقدمة",
            **{
                "/setup": "فتح قائمة الإعدادات التفاعلية",
                "/setup-status": "عرض الإعدادات الحالية",
                "/setup-reset": "إعادة تعيين الإعدادات",
                "/log-set [#channel] [type]": "تعيين قناة لوق",
                "/set-welcome [#channel]": "تعيين قناة الترحيب",
                "/set-goodbye [#channel]": "تعيين قناة الوداع",
                "/balance [@user]": "عرض الكريديت",
            }
        )


class Help(commands.Cog):
    """نظام المساعدة"""
    
    def __init__(self, bot):
        self.bot = bot
        self.embed_manager = EmbedManager()
    
    @app_commands.command(name="help", description="عرض المساعدة الكاملة للبوت")
    async def help_command(self, interaction: discord.Interaction):
        """أمر المساعدة الرئيسي"""
        try:
            embed = self.embed_manager.info(
                "مرحباً بك في 𝑆𝑜𝑐𝑖𝑒𝑡𝑦",
                "اختر فئة من القائمة أدناه لعرض الأوامر المتاحة"
            )
            embed.add_field(
                name="📌 المميزات",
                value="""
                🎫 **13 نظام مستقل** — التكتات، الحماية، الإشراف، وغيرها
                ⚡ **60+ أمر متكامل** — جميع الأوامر جاهزة للاستخدام
                🌍 **واجهة عربية 100%** — كل شيء بالعربية
                🔧 **إعدادات متقدمة** — خصص البوت حسب احتياجك
                """,
                inline=False
            )
            
            view = HelpView(interaction)
            await interaction.response.send_message(embed=embed, view=view, ephemeral=False)
        except Exception as e:
            embed = self.embed_manager.error("❌ خطأ", f"```{str(e)[:100]}```")
            await interaction.response.send_message(embed=embed, ephemeral=True)
    
    @commands.command(name="help", aliases=["h"], description="عرض المساعدة")
    async def help_prefix_command(self, ctx):
        """نسخة الـ prefix من أمر المساعدة"""
        try:
            embed = self.embed_manager.info(
                "مرحباً بك في 𝑆𝑜𝑐𝑖𝑒𝑡𝑦",
                "استخدم `/help` لعرض قائمة المساعدة التفاعلية"
            )
            await ctx.send(embed=embed)
        except Exception as e:
            embed = self.embed_manager.error("❌ خطأ", f"```{str(e)[:100]}```")
            await ctx.send(embed=embed)


async def setup(bot):
    await bot.add_cog(Help(bot))
