import discord
from discord.ext import commands
from discord import app_commands
from main import EmbedManager, DataManager

class Setup(commands.Cog):
    """نظام إعداد البوت"""
    
    def __init__(self, bot):
        self.bot = bot
        self.embed_manager = EmbedManager()
        self.data_manager = DataManager()
    
    def get_guild_settings(self, guild_id):
        """الحصول على إعدادات السيرفر"""
        settings = self.data_manager.load_data("guild_settings.json")
        if str(guild_id) not in settings:
            settings[str(guild_id)] = {
                "prefix": "!",
                "welcome_channel": 0,
                "goodbye_channel": 0,
                "admin_role": 0,
                "mod_role": 0,
                "mute_role": 0,
                "log_channel": 0,
                "mod_log_channel": 0,
                "ticket_log_channel": 0,
                "protection_log_channel": 0,
                "ticket_category": 0,
                "ticket_panel_channel": 0,
                "support_role": 0,
                "level_channel": 0,
                "suggestions_channel": 0,
                "level_enabled": True,
                "economy_enabled": True,
                "tickets_enabled": True,
                "protection_enabled": True,
                "welcome_enabled": True,
            }
            self.data_manager.save_data("guild_settings.json", settings)
        return settings
    
    # ───────────────────────────────────────────────
    # /setup - القائمة الرئيسية التفاعلية
    # ───────────────────────────────────────────────
    @app_commands.command(name="setup", description="فتح قائمة الإعدادات التفاعلية")
    @app_commands.checks.has_permissions(administrator=True)
    async def setup_command(self, interaction: discord.Interaction):
        """أمر الإعداد الرئيسي"""
        try:
            embed = self.embed_manager.info(
                "⚙️ إعدادات السيرفر",
                "اختر الفئة التي تريد تعديلها من الأزرار أدناه"
            )
            await interaction.response.send_message(embed=embed, view=SetupMainView(self), ephemeral=True)
        except Exception as e:
            embed = self.embed_manager.error("❌ خطأ", f"```{str(e)[:100]}```")
            await interaction.response.send_message(embed=embed, ephemeral=True)
    
    # ───────────────────────────────────────────────
    # /setup-status
    # ───────────────────────────────────────────────
    @app_commands.command(name="setup-status", description="عرض الإعدادات الحالية")
    @app_commands.checks.has_permissions(administrator=True)
    async def setup_status(self, interaction: discord.Interaction):
        """عرض حالة الإعدادات"""
        try:
            settings = self.get_guild_settings(interaction.guild.id)
            guild_settings = settings[str(interaction.guild.id)]
            
            def get_mention(val):
                if val == 0 or not val:
                    return "لم تُحدد"
                ch = interaction.guild.get_channel(val)
                role = interaction.guild.get_role(val)
                return ch.mention if ch else (role.mention if role else f"`{val}`")
            
            embed = self.embed_manager.info(
                "📋 حالة الإعدادات الحالية",
                f"إعدادات السيرفر: **{interaction.guild.name}**"
            )
            
            embed.add_field(
                name="🎫 التكتات",
                value=f"**الحالة**: {'✅ مفعلة' if guild_settings.get('tickets_enabled') else '❌ معطلة'}\n"
                      f"**القناة**: {get_mention(guild_settings.get('ticket_panel_channel'))}\n"
                      f"**الفئة**: {get_mention(guild_settings.get('ticket_category'))}",
                inline=False
            )
            
            embed.add_field(
                name="🎉 الترحيب",
                value=f"**الحالة**: {'✅ مفعلة' if guild_settings.get('welcome_enabled') else '❌ معطلة'}\n"
                      f"**قناة الترحيب**: {get_mention(guild_settings.get('welcome_channel'))}\n"
                      f"**قناة الوداع**: {get_mention(guild_settings.get('goodbye_channel'))}",
                inline=False
            )
            
            embed.add_field(
                name="🛡️ الحماية",
                value=f"**الحالة**: {'✅ مفعلة' if guild_settings.get('protection_enabled') else '❌ معطلة'}",
                inline=False
            )
            
            embed.add_field(
                name="⚖️ الإشراف",
                value=f"**رتبة الأدمن**: {get_mention(guild_settings.get('admin_role'))}\n"
                      f"**رتبة المود**: {get_mention(guild_settings.get('mod_role'))}\n"
                      f"**رتبة الميوت**: {get_mention(guild_settings.get('mute_role'))}",
                inline=False
            )
            
            await interaction.response.send_message(embed=embed, ephemeral=True)
        except Exception as e:
            embed = self.embed_manager.error("❌ خطأ", f"```{str(e)[:100]}```")
            await interaction.response.send_message(embed=embed, ephemeral=True)
    
    # ───────────────────────────────────────────────
    # /setup-reset
    # ───────────────────────────────────────────────
    @app_commands.command(name="setup-reset", description="إعادة تعيين الإعدادات")
    @app_commands.checks.has_permissions(administrator=True)
    async def setup_reset(self, interaction: discord.Interaction):
        """إعادة تعيين الإعدادات للافتراضي"""
        try:
            settings = self.data_manager.load_data("guild_settings.json")
            settings[str(interaction.guild.id)] = {
                "prefix": "!",
                "welcome_channel": 0,
                "goodbye_channel": 0,
                "admin_role": 0,
                "mod_role": 0,
                "mute_role": 0,
                "log_channel": 0,
                "mod_log_channel": 0,
                "ticket_log_channel": 0,
                "protection_log_channel": 0,
                "ticket_category": 0,
                "ticket_panel_channel": 0,
                "support_role": 0,
                "level_channel": 0,
                "suggestions_channel": 0,
                "level_enabled": True,
                "economy_enabled": True,
                "tickets_enabled": True,
                "protection_enabled": True,
                "welcome_enabled": True,
            }
            self.data_manager.save_data("guild_settings.json", settings)
            
            embed = self.embed_manager.success(
                "✅ تم إعادة التعيين",
                "تم إعادة جميع الإعدادات للقيم الافتراضية بنجاح"
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
        except Exception as e:
            embed = self.embed_manager.error("❌ خطأ", f"```{str(e)[:100]}```")
            await interaction.response.send_message(embed=embed, ephemeral=True)
    
    # ───────────────────────────────────────────────
    # /set-welcome
    # ───────────────────────────────────────────────
    @app_commands.command(name="set-welcome", description="تعيين قناة الترحيب")
    @app_commands.checks.has_permissions(administrator=True)
    async def set_welcome_channel(self, interaction: discord.Interaction, channel: discord.TextChannel):
        """تعيين قناة الترحيب"""
        try:
            settings = self.get_guild_settings(interaction.guild.id)
            settings[str(interaction.guild.id)]["welcome_channel"] = channel.id
            self.data_manager.save_data("guild_settings.json", settings)
            
            embed = self.embed_manager.success(
                "✅ تم التعيين",
                f"تم تعيين قناة الترحيب: {channel.mention}"
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
        except Exception as e:
            embed = self.embed_manager.error("❌ خطأ", f"```{str(e)[:100]}```")
            await interaction.response.send_message(embed=embed, ephemeral=True)
    
    # ───────────────────────────────────────────────
    # /set-goodbye
    # ───────────────────────────────────────────────
    @app_commands.command(name="set-goodbye", description="تعيين قناة الوداع")
    @app_commands.checks.has_permissions(administrator=True)
    async def set_goodbye_channel(self, interaction: discord.Interaction, channel: discord.TextChannel):
        """تعيين قناة الوداع"""
        try:
            settings = self.get_guild_settings(interaction.guild.id)
            settings[str(interaction.guild.id)]["goodbye_channel"] = channel.id
            self.data_manager.save_data("guild_settings.json", settings)
            
            embed = self.embed_manager.success(
                "✅ تم التعيين",
                f"تم تعيين قناة الوداع: {channel.mention}"
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
        except Exception as e:
            embed = self.embed_manager.error("❌ خطأ", f"```{str(e)[:100]}```")
            await interaction.response.send_message(embed=embed, ephemeral=True)
    
    # ───────────────────────────────────────────────
    # !setup (Prefix Command)
    # ───────────────────────────────────────────────
    @commands.command(name="setup", aliases=["s"])
    @commands.has_permissions(administrator=True)
    async def setup_prefix(self, ctx):
        """نسخة الـ prefix من أمر الإعداد"""
        try:
            embed = self.embed_manager.info(
                "⚙️ الإعدادات",
                "استخدم `/setup` لفتح قائمة الإعدادات التفاعلية"
            )
            await ctx.send(embed=embed)
        except Exception as e:
            embed = self.embed_manager.error("❌ خطأ", f"```{str(e)[:100]}```")
            await ctx.send(embed=embed)


# ═══════════════════════════════════════════════════
# الـ Views (الواجهات التفاعلية)
# ═══════════════════════════════════════════════════

class SetupMainView(discord.ui.View):
    def __init__(self, cog):
        super().__init__(timeout=300)
        self.cog = cog

    @discord.ui.button(label="🎫 التكتات", style=discord.ButtonStyle.primary)
    async def tickets(self, interaction: discord.Interaction, button: discord.ui.Button):
        embed = self.cog.embed_manager.info(
            "🎫 إعدادات التكتات",
            "اختر قناة لوحة التكتات والفئة من القوائم أدناه"
        )
        await interaction.response.send_message(embed=embed, view=TicketSetupView(self.cog), ephemeral=True)

    @discord.ui.button(label="🎉 الترحيب", style=discord.ButtonStyle.primary)
    async def welcome(self, interaction: discord.Interaction, button: discord.ui.Button):
        embed = self.cog.embed_manager.info(
            "🎉 إعدادات الترحيب",
            "اختر قنوات الترحيب والوداع"
        )
        await interaction.response.send_message(embed=embed, view=WelcomeSetupView(self.cog), ephemeral=True)

    @discord.ui.button(label="🛡️ الحماية", style=discord.ButtonStyle.danger)
    async def protection(self, interaction: discord.Interaction, button: discord.ui.Button):
        embed = self.cog.embed_manager.info(
            "🛡️ إعدادات الحماية",
            "تفعيل/تعطيل أنظمة الحماية"
        )
        await interaction.response.send_message(embed=embed, view=ProtectionSetupView(self.cog), ephemeral=True)

    @discord.ui.button(label="📊 اللوق", style=discord.ButtonStyle.secondary)
    async def logging(self, interaction: discord.Interaction, button: discord.ui.Button):
        embed = self.cog.embed_manager.info(
            "📝 إعدادات اللوق",
            "اختر قنوات تسجيل الأحداث"
        )
        await interaction.response.send_message(embed=embed, view=LoggingSetupView(self.cog), ephemeral=True)

    @discord.ui.button(label="⚖️ الإشراف", style=discord.ButtonStyle.danger)
    async def moderation(self, interaction: discord.Interaction, button: discord.ui.Button):
        embed = self.cog.embed_manager.info(
            "⚖️ إعدادات الإشراف",
            "اختر رتب الإشراف من القوائم أدناه"
        )
        await interaction.response.send_message(embed=embed, view=ModSetupView(self.cog), ephemeral=True)


class ModSetupView(discord.ui.View):
    def __init__(self, cog):
        super().__init__(timeout=300)
        self.cog = cog

    @discord.ui.role_select(
        placeholder="🛡️ اختر رتبة الأدمن",
        min_values=1, max_values=1
    )
    async def select_admin(self, interaction: discord.Interaction, select: discord.ui.RoleSelect):
        settings = self.cog.get_guild_settings(interaction.guild.id)
        settings[str(interaction.guild.id)]["admin_role"] = select.values[0].id
        self.cog.data_manager.save_data("guild_settings.json", settings)
        await interaction.response.send_message(
            embed=self.cog.embed_manager.success("✅ تم", f"رتبة الأدمن: {select.values[0].mention}"),
            ephemeral=True
        )

    @discord.ui.role_select(
        placeholder="👮 اختر رتبة المود",
        min_values=1, max_values=1
    )
    async def select_mod(self, interaction: discord.Interaction, select: discord.ui.RoleSelect):
        settings = self.cog.get_guild_settings(interaction.guild.id)
        settings[str(interaction.guild.id)]["mod_role"] = select.values[0].id
        self.cog.data_manager.save_data("guild_settings.json", settings)
        await interaction.response.send_message(
            embed=self.cog.embed_manager.success("✅ تم", f"رتبة المود: {select.values[0].mention}"),
            ephemeral=True
        )

    @discord.ui.role_select(
        placeholder="🔇 اختر رتبة الميوت",
        min_values=1, max_values=1
    )
    async def select_mute(self, interaction: discord.Interaction, select: discord.ui.RoleSelect):
        settings = self.cog.get_guild_settings(interaction.guild.id)
        settings[str(interaction.guild.id)]["mute_role"] = select.values[0].id
        self.cog.data_manager.save_data("guild_settings.json", settings)
        await interaction.response.send_message(
            embed=self.cog.embed_manager.success("✅ تم", f"رتبة الميوت: {select.values[0].mention}"),
            ephemeral=True
        )

    @discord.ui.button(label="🔙 رجوع", style=discord.ButtonStyle.secondary)
    async def back(self, interaction: discord.Interaction, button: discord.ui.Button):
        embed = self.cog.embed_manager.info("⚙️ إعدادات السيرفر", "اختر الفئة التي تريد تعديلها")
        await interaction.response.send_message(embed=embed, view=SetupMainView(self.cog), ephemeral=True)


class TicketSetupView(discord.ui.View):
    def __init__(self, cog):
        super().__init__(timeout=300)
        self.cog = cog

    @discord.ui.channel_select(
        placeholder="📋 اختر قناة لوحة التكتات",
        channel_types=[discord.ChannelType.text]
    )
    async def select_panel(self, interaction: discord.Interaction, select: discord.ui.ChannelSelect):
        settings = self.cog.get_guild_settings(interaction.guild.id)
        settings[str(interaction.guild.id)]["ticket_panel_channel"] = select.values[0].id
        self.cog.data_manager.save_data("guild_settings.json", settings)
        await interaction.response.send_message(
            embed=self.cog.embed_manager.success("✅ تم", f"قناة اللوحة: {select.values[0].mention}"),
            ephemeral=True
        )

    @discord.ui.channel_select(
        placeholder="📁 اختر فئة التكتات",
        channel_types=[discord.ChannelType.category]
    )
    async def select_category(self, interaction: discord.Interaction, select: discord.ui.ChannelSelect):
        settings = self.cog.get_guild_settings(interaction.guild.id)
        settings[str(interaction.guild.id)]["ticket_category"] = select.values[0].id
        self.cog.data_manager.save_data("guild_settings.json", settings)
        await interaction.response.send_message(
            embed=self.cog.embed_manager.success("✅ تم", f"الفئة: {select.values[0].mention}"),
            ephemeral=True
        )

    @discord.ui.button(label="🔙 رجوع", style=discord.ButtonStyle.secondary)
    async def back(self, interaction: discord.Interaction, button: discord.ui.Button):
        embed = self.cog.embed_manager.info("⚙️ إعدادات السيرفر", "اختر الفئة التي تريد تعديلها")
        await interaction.response.send_message(embed=embed, view=SetupMainView(self.cog), ephemeral=True)


class WelcomeSetupView(discord.ui.View):
    def __init__(self, cog):
        super().__init__(timeout=300)
        self.cog = cog

    @discord.ui.channel_select(
        placeholder="🎉 اختر قناة الترحيب",
        channel_types=[discord.ChannelType.text]
    )
    async def select_welcome(self, interaction: discord.Interaction, select: discord.ui.ChannelSelect):
        settings = self.cog.get_guild_settings(interaction.guild.id)
        settings[str(interaction.guild.id)]["welcome_channel"] = select.values[0].id
        self.cog.data_manager.save_data("guild_settings.json", settings)
        await interaction.response.send_message(
            embed=self.cog.embed_manager.success("✅ تم", f"قناة الترحيب: {select.values[0].mention}"),
            ephemeral=True
        )

    @discord.ui.channel_select(
        placeholder="👋 اختر قناة الوداع",
        channel_types=[discord.ChannelType.text]
    )
    async def select_goodbye(self, interaction: discord.Interaction, select: discord.ui.ChannelSelect):
        settings = self.cog.get_guild_settings(interaction.guild.id)
        settings[str(interaction.guild.id)]["goodbye_channel"] = select.values[0].id
        self.cog.data_manager.save_data("guild_settings.json", settings)
        await interaction.response.send_message(
            embed=self.cog.embed_manager.success("✅ تم", f"قناة الوداع: {select.values[0].mention}"),
            ephemeral=True
        )

    @discord.ui.button(label="🔙 رجوع", style=discord.ButtonStyle.secondary)
    async def back(self, interaction: discord.Interaction, button: discord.ui.Button):
        embed = self.cog.embed_manager.info("⚙️ إعدادات السيرفر", "اختر الفئة التي تريد تعديلها")
        await interaction.response.send_message(embed=embed, view=SetupMainView(self.cog), ephemeral=True)


class ProtectionSetupView(discord.ui.View):
    def __init__(self, cog):
        super().__init__(timeout=300)
        self.cog = cog

    @discord.ui.button(label="تفعيل الحماية", style=discord.ButtonStyle.green)
    async def enable(self, interaction: discord.Interaction, button: discord.ui.Button):
        settings = self.cog.get_guild_settings(interaction.guild.id)
        settings[str(interaction.guild.id)]["protection_enabled"] = True
        self.cog.data_manager.save_data("guild_settings.json", settings)
        await interaction.response.send_message(
            embed=self.cog.embed_manager.success("✅ تم", "تم تفعيل الحماية"), ephemeral=True
        )

    @discord.ui.button(label="تعطيل الحماية", style=discord.ButtonStyle.red)
    async def disable(self, interaction: discord.Interaction, button: discord.ui.Button):
        settings = self.cog.get_guild_settings(interaction.guild.id)
        settings[str(interaction.guild.id)]["protection_enabled"] = False
        self.cog.data_manager.save_data("guild_settings.json", settings)
        await interaction.response.send_message(
            embed=self.cog.embed_manager.success("✅ تم", "تم تعطيل الحماية"), ephemeral=True
        )

    @discord.ui.button(label="🔙 رجوع", style=discord.ButtonStyle.secondary)
    async def back(self, interaction: discord.Interaction, button: discord.ui.Button):
        embed = self.cog.embed_manager.info("⚙️ إعدادات السيرفر", "اختر الفئة التي تريد تعديلها")
        await interaction.response.send_message(embed=embed, view=SetupMainView(self.cog), ephemeral=True)


class LoggingSetupView(discord.ui.View):
    def __init__(self, cog):
        super().__init__(timeout=300)
        self.cog = cog

    @discord.ui.channel_select(
        placeholder="📋 اختر قناة اللوق العام",
        channel_types=[discord.ChannelType.text]
    )
    async def select_log(self, interaction: discord.Interaction, select: discord.ui.ChannelSelect):
        settings = self.cog.get_guild_settings(interaction.guild.id)
        settings[str(interaction.guild.id)]["log_channel"] = select.values[0].id
        self.cog.data_manager.save_data("guild_settings.json", settings)
        await interaction.response.send_message(
            embed=self.cog.embed_manager.success("✅ تم", f"قناة اللوق: {select.values[0].mention}"),
            ephemeral=True
        )

    @discord.ui.button(label="🔙 رجوع", style=discord.ButtonStyle.secondary)
    async def back(self, interaction: discord.Interaction, button: discord.ui.Button):
        embed = self.cog.embed_manager.info("⚙️ إعدادات السيرفر", "اختر الفئة التي تريد تعديلها")
        await interaction.response.send_message(embed=embed, view=SetupMainView(self.cog), ephemeral=True)


async def setup(bot):
    await bot.add_cog(Setup(bot))
