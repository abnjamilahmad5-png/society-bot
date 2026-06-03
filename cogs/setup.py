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
    
    @app_commands.command(name="setup", description="فتح قائمة الإعدادات التفاعلية")
    @app_commands.checks.has_permissions(administrator=True)
    async def setup_command(self, interaction: discord.Interaction):
        try:
            embed = self.embed_manager.info(
                "⚙️ إعدادات السيرفر",
                "اختر الفئة التي تريد تعديلها من الأزرار أدناه"
            )
            await interaction.response.send_message(embed=embed, view=SetupMainView(self), ephemeral=True)
        except Exception as e:
            embed = self.embed_manager.error("❌ خطأ", f"```{str(e)[:100]}```")
            await interaction.response.send_message(embed=embed, ephemeral=True)
    
    @app_commands.command(name="setup-status", description="عرض الإعدادات الحالية")
    @app_commands.checks.has_permissions(administrator=True)
    async def setup_status(self, interaction: discord.Interaction):
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
    
    @app_commands.command(name="setup-reset", description="إعادة تعيين الإعدادات")
    @app_commands.checks.has_permissions(administrator=True)
    async def setup_reset(self, interaction: discord.Interaction):
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
    
    @app_commands.command(name="set-welcome", description="تعيين قناة الترحيب")
    @app_commands.checks.has_permissions(administrator=True)
    async def set_welcome_channel(self, interaction: discord.Interaction, channel: discord.TextChannel):
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
    
    @app_commands.command(name="set-goodbye", description="تعيين قناة الوداع")
    @app_commands.checks.has_permissions(administrator=True)
    async def set_goodbye_channel(self, interaction: discord.Interaction, channel: discord.TextChannel):
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
    
    @commands.command(name="setup", aliases=["s"])
    @commands.has_permissions(administrator=True)
    async def setup_prefix(self, ctx):
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
# الواجهات التفاعلية (Select اليدوي - يعمل مع كل الإصدارات)
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


# ───────────────────────────────────────────────
# مساعد: بناء قائمة رتب
# ───────────────────────────────────────────────
def build_role_select(placeholder, custom_id):
    class RoleSelect(discord.ui.Select):
        def __init__(self, cog):
            self.cog = cog
            options = []
            # نبني الـ options لاحقاً لكل interaction
            super().__init__(
                placeholder=placeholder,
                min_values=1,
                max_values=1,
                options=[discord.SelectOption(label="جاري التحميل...", value="0")]
            )
            self.custom_id = custom_id
        
        async def callback(self, interaction: discord.Interaction):
            pass  # نعيد تعريفه في الـ View
    return RoleSelect


class ModSetupView(discord.ui.View):
    def __init__(self, cog):
        super().__init__(timeout=300)
        self.cog = cog
        
        # رتبة الأدمن
        self.admin_select = discord.ui.Select(
            placeholder="🛡️ اختر رتبة الأدمن",
            min_values=1, max_values=1,
            options=[discord.SelectOption(label="اضغط هنا لعرض الرتب", value="0")]
        )
        self.admin_select.callback = self.admin_callback
        self.add_item(self.admin_select)
        
        # رتبة المود
        self.mod_select = discord.ui.Select(
            placeholder="👮 اختر رتبة المود",
            min_values=1, max_values=1,
            options=[discord.SelectOption(label="اضغط هنا لعرض الرتب", value="0")]
        )
        self.mod_select.callback = self.mod_callback
        self.add_item(self.mod_select)
        
        # رتبة الميوت
        self.mute_select = discord.ui.Select(
            placeholder="🔇 اختر رتبة الميوت",
            min_values=1, max_values=1,
            options=[discord.SelectOption(label="اضغط هنا لعرض الرتب", value="0")]
        )
        self.mute_select.callback = self.mute_callback
        self.add_item(self.mute_select)
    
    async def refresh_options(self, interaction: discord.Interaction):
        """تحديث الـ options بقائمة الرتب الفعلية"""
        roles = [r for r in interaction.guild.roles if not r.is_default() and not r.managed]
        roles = sorted(roles, key=lambda r: r.position, reverse=True)[:24]
        
        options = [discord.SelectOption(label=r.name, value=str(r.id), description=f"اللون: {str(r.color)}") for r in roles]
        if not options:
            options = [discord.SelectOption(label="لا يوجد رتب", value="0")]
        
        self.admin_select.options = options.copy()
        self.mod_select.options = options.copy()
        self.mute_select.options = options.copy()
    
    async def admin_callback(self, interaction: discord.Interaction):
        if self.admin_select.values[0] == "0":
            await self.refresh_options(interaction)
            await interaction.response.edit_message(view=self)
            return
        role_id = int(self.admin_select.values[0])
        role = interaction.guild.get_role(role_id)
        settings = self.cog.get_guild_settings(interaction.guild.id)
        settings[str(interaction.guild.id)]["admin_role"] = role_id
        self.cog.data_manager.save_data("guild_settings.json", settings)
        await interaction.response.send_message(
            embed=self.cog.embed_manager.success("✅ تم", f"رتبة الأدمن: {role.mention}"),
            ephemeral=True
        )
    
    async def mod_callback(self, interaction: discord.Interaction):
        if self.mod_select.values[0] == "0":
            await self.refresh_options(interaction)
            await interaction.response.edit_message(view=self)
            return
        role_id = int(self.mod_select.values[0])
        role = interaction.guild.get_role(role_id)
        settings = self.cog.get_guild_settings(interaction.guild.id)
        settings[str(interaction.guild.id)]["mod_role"] = role_id
        self.cog.data_manager.save_data("guild_settings.json", settings)
        await interaction.response.send_message(
            embed=self.cog.embed_manager.success("✅ تم", f"رتبة المود: {role.mention}"),
            ephemeral=True
        )
    
    async def mute_callback(self, interaction: discord.Interaction):
        if self.mute_select.values[0] == "0":
            await self.refresh_options(interaction)
            await interaction.response.edit_message(view=self)
            return
        role_id = int(self.mute_select.values[0])
        role = interaction.guild.get_role(role_id)
        settings = self.cog.get_guild_settings(interaction.guild.id)
        settings[str(interaction.guild.id)]["mute_role"] = role_id
        self.cog.data_manager.save_data("guild_settings.json", settings)
        await interaction.response.send_message(
            embed=self.cog.embed_manager.success("✅ تم", f"رتبة الميوت: {role.mention}"),
            ephemeral=True
        )

    @discord.ui.button(label="🔙 رجوع", style=discord.ButtonStyle.secondary)
    async def back(self, interaction: discord.Interaction, button: discord.ui.Button):
        embed = self.cog.embed_manager.info("⚙️ إعدادات السيرفر", "اختر الفئة التي تريد تعديلها")
        await interaction.response.send_message(embed=embed, view=SetupMainView(self.cog), ephemeral=True)


# ───────────────────────────────────────────────
# واجهة التكتات
# ───────────────────────────────────────────────
class TicketSetupView(discord.ui.View):
    def __init__(self, cog):
        super().__init__(timeout=300)
        self.cog = cog
        
        self.panel_select = discord.ui.Select(
            placeholder="📋 اختر قناة لوحة التكتات",
            min_values=1, max_values=1,
            options=[discord.SelectOption(label="اضغط هنا لعرض القنوات", value="0")]
        )
        self.panel_select.callback = self.panel_callback
        self.add_item(self.panel_select)
        
        self.cat_select = discord.ui.Select(
            placeholder="📁 اختر فئة التكتات",
            min_values=1, max_values=1,
            options=[discord.SelectOption(label="اضغط هنا لعرض الفئات", value="0")]
        )
        self.cat_select.callback = self.cat_callback
        self.add_item(self.cat_select)
    
    async def refresh_options(self, interaction: discord.Interaction):
        text_chs = [c for c in interaction.guild.text_channels][:24]
        cats = [c for c in interaction.guild.categories][:24]
        
        panel_opts = [discord.SelectOption(label=f"#{c.name}", value=str(c.id)) for c in text_chs]
        cat_opts = [discord.SelectOption(label=f"📁 {c.name}", value=str(c.id)) for c in cats]
        
        if not panel_opts: panel_opts = [discord.SelectOption(label="لا يوجد قنوات", value="0")]
        if not cat_opts: cat_opts = [discord.SelectOption(label="لا يوجد فئات", value="0")]
        
        self.panel_select.options = panel_opts
        self.cat_select.options = cat_opts
    
    async def panel_callback(self, interaction: discord.Interaction):
        if self.panel_select.values[0] == "0":
            await self.refresh_options(interaction)
            await interaction.response.edit_message(view=self)
            return
        ch_id = int(self.panel_select.values[0])
        ch = interaction.guild.get_channel(ch_id)
        settings = self.cog.get_guild_settings(interaction.guild.id)
        settings[str(interaction.guild.id)]["ticket_panel_channel"] = ch_id
        self.cog.data_manager.save_data("guild_settings.json", settings)
        await interaction.response.send_message(
            embed=self.cog.embed_manager.success("✅ تم", f"قناة اللوحة: {ch.mention}"),
            ephemeral=True
        )
    
    async def cat_callback(self, interaction: discord.Interaction):
        if self.cat_select.values[0] == "0":
            await self.refresh_options(interaction)
            await interaction.response.edit_message(view=self)
            return
        ch_id = int(self.cat_select.values[0])
        ch = interaction.guild.get_channel(ch_id)
        settings = self.cog.get_guild_settings(interaction.guild.id)
        settings[str(interaction.guild.id)]["ticket_category"] = ch_id
        self.cog.data_manager.save_data("guild_settings.json", settings)
        await interaction.response.send_message(
            embed=self.cog.embed_manager.success("✅ تم", f"الفئة: {ch.mention}"),
            ephemeral=True
        )

    @discord.ui.button(label="🔙 رجوع", style=discord.ButtonStyle.secondary)
    async def back(self, interaction: discord.Interaction, button: discord.ui.Button):
        embed = self.cog.embed_manager.info("⚙️ إعدادات السيرفر", "اختر الفئة التي تريد تعديلها")
        await interaction.response.send_message(embed=embed, view=SetupMainView(self.cog), ephemeral=True)


# ───────────────────────────────────────────────
# واجهة الترحيب
# ───────────────────────────────────────────────
class WelcomeSetupView(discord.ui.View):
    def __init__(self, cog):
        super().__init__(timeout=300)
        self.cog = cog
        
        self.welcome_select = discord.ui.Select(
            placeholder="🎉 اختر قناة الترحيب",
            min_values=1, max_values=1,
            options=[discord.SelectOption(label="اضغط هنا لعرض القنوات", value="0")]
        )
        self.welcome_select.callback = self.welcome_callback
        self.add_item(self.welcome_select)
        
        self.goodbye_select = discord.ui.Select(
            placeholder="👋 اختر قناة الوداع",
            min_values=1, max_values=1,
            options=[discord.SelectOption(label="اضغط هنا لعرض القنوات", value="0")]
        )
        self.goodbye_select.callback = self.goodbye_callback
        self.add_item(self.goodbye_select)
    
    async def refresh_options(self, interaction: discord.Interaction):
        text_chs = [c for c in interaction.guild.text_channels][:24]
        opts = [discord.SelectOption(label=f"#{c.name}", value=str(c.id)) for c in text_chs]
        if not opts: opts = [discord.SelectOption(label="لا يوجد قنوات", value="0")]
        self.welcome_select.options = opts
        self.goodbye_select.options = opts.copy()
    
    async def welcome_callback(self, interaction: discord.Interaction):
        if self.welcome_select.values[0] == "0":
            await self.refresh_options(interaction)
            await interaction.response.edit_message(view=self)
            return
        ch_id = int(self.welcome_select.values[0])
        ch = interaction.guild.get_channel(ch_id)
        settings = self.cog.get_guild_settings(interaction.guild.id)
        settings[str(interaction.guild.id)]["welcome_channel"] = ch_id
        self.cog.data_manager.save_data("guild_settings.json", settings)
        await interaction.response.send_message(
            embed=self.cog.embed_manager.success("✅ تم", f"قناة الترحيب: {ch.mention}"),
            ephemeral=True
        )
    
    async def goodbye_callback(self, interaction: discord.Interaction):
        if self.goodbye_select.values[0] == "0":
            await self.refresh_options(interaction)
            await interaction.response.edit_message(view=self)
            return
        ch_id = int(self.goodbye_select.values[0])
        ch = interaction.guild.get_channel(ch_id)
        settings = self.cog.get_guild_settings(interaction.guild.id)
        settings[str(interaction.guild.id)]["goodbye_channel"] = ch_id
        self.cog.data_manager.save_data("guild_settings.json", settings)
        await interaction.response.send_message(
            embed=self.cog.embed_manager.success("✅ تم", f"قناة الوداع: {ch.mention}"),
            ephemeral=True
        )

    @discord.ui.button(label="🔙 رجوع", style=discord.ButtonStyle.secondary)
    async def back(self, interaction: discord.Interaction, button: discord.ui.Button):
        embed = self.cog.embed_manager.info("⚙️ إعدادات السيرفر", "اختر الفئة التي تريد تعديلها")
        await interaction.response.send_message(embed=embed, view=SetupMainView(self.cog), ephemeral=True)


# ───────────────────────────────────────────────
# واجهة الحماية
# ───────────────────────────────────────────────
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


# ───────────────────────────────────────────────
# واجهة اللوق
# ───────────────────────────────────────────────
class LoggingSetupView(discord.ui.View):
    def __init__(self, cog):
        super().__init__(timeout=300)
        self.cog = cog
        
        self.log_select = discord.ui.Select(
            placeholder="📋 اختر قناة اللوق العام",
            min_values=1, max_values=1,
            options=[discord.SelectOption(label="اضغط هنا لعرض القنوات", value="0")]
        )
        self.log_select.callback = self.log_callback
        self.add_item(self.log_select)
    
    async def refresh_options(self, interaction: discord.Interaction):
        text_chs = [c for c in interaction.guild.text_channels][:24]
        opts = [discord.SelectOption(label=f"#{c.name}", value=str(c.id)) for c in text_chs]
        if not opts: opts = [discord.SelectOption(label="لا يوجد قنوات", value="0")]
        self.log_select.options = opts
    
    async def log_callback(self, interaction: discord.Interaction):
        if self.log_select.values[0] == "0":
            await self.refresh_options(interaction)
            await interaction.response.edit_message(view=self)
            return
        ch_id = int(self.log_select.values[0])
        ch = interaction.guild.get_channel(ch_id)
        settings = self.cog.get_guild_settings(interaction.guild.id)
        settings[str(interaction.guild.id)]["log_channel"] = ch_id
        self.cog.data_manager.save_data("guild_settings.json", settings)
        await interaction.response.send_message(
            embed=self.cog.embed_manager.success("✅ تم", f"قناة اللوق: {ch.mention}"),
            ephemeral=True
        )

    @discord.ui.button(label="🔙 رجوع", style=discord.ButtonStyle.secondary)
    async def back(self, interaction: discord.Interaction, button: discord.ui.Button):
        embed = self.cog.embed_manager.info("⚙️ إعدادات السيرفر", "اختر الفئة التي تريد تعديلها")
        await interaction.response.send_message(embed=embed, view=SetupMainView(self.cog), ephemeral=True)


async def setup(bot):
    await bot.add_cog(Setup(bot))
