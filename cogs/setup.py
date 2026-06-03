import discord
from discord.ext import commands
from discord import app_commands
from main import EmbedManager, DataManager

class Setup(commands.Cog):
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

# ───────────────────────────────────────────────
# الواجهة الرئيسية (الأزرار الأولى)
# ───────────────────────────────────────────────
class SetupMainView(discord.ui.View):
    def __init__(self, cog):
        super().__init__(timeout=300)
        self.cog = cog

    @discord.ui.button(label="🎫 التكتات", style=discord.ButtonStyle.primary)
    async def tickets(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message(
            embed=self.cog.embed_manager.info("🎫 إعدادات التكتات", "اختر قناة لوحة التكتات والفئة من القوائم أدناه"),
            view=TicketSetupView(self.cog),
            ephemeral=True
        )

    @discord.ui.button(label="🎉 الترحيب", style=discord.ButtonStyle.primary)
    async def welcome(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message(
            embed=self.cog.embed_manager.info("🎉 إعدادات الترحيب", "اختر قنوات الترحيب والوداع"),
            view=WelcomeSetupView(self.cog),
            ephemeral=True
        )

    @discord.ui.button(label="🛡️ الحماية", style=discord.ButtonStyle.danger)
    async def protection(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message(
            embed=self.cog.embed_manager.info("🛡️ إعدادات الحماية", "تفعيل/تعطيل أنظمة الحماية"),
            view=ProtectionSetupView(self.cog),
            ephemeral=True
        )

    @discord.ui.button(label="📊 اللوق", style=discord.ButtonStyle.secondary)
    async def logging(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message(
            embed=self.cog.embed_manager.info("📝 إعدادات اللوق", "اختر قنوات تسجيل الأحداث"),
            view=LoggingSetupView(self.cog),
            ephemeral=True
        )

    @discord.ui.button(label="⚖️ الإشراف", style=discord.ButtonStyle.danger)
    async def moderation(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message(
            embed=self.cog.embed_manager.info("⚖️ إعدادات الإشراف", "اختر رتب الإشراف من القائمة أدناه"),
            view=ModSetupView(self.cog),
            ephemeral=True
        )

# ───────────────────────────────────────────────
# واجهة إعداد الإشراف (محدد الرتب)
# ───────────────────────────────────────────────
class ModSetupView(discord.ui.View):
    def __init__(self, cog):
        super().__init__(timeout=300)
        self.cog = cog

    @discord.ui.role_select(
        placeholder="🛡️ اختر رتبة الأدمن",
        min_values=1,
        max_values=1,
        custom_id="select_admin_role"
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
        min_values=1,
        max_values=1,
        custom_id="select_mod_role"
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
        min_values=1,
        max_values=1,
        custom_id="select_mute_role"
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

# ───────────────────────────────────────────────
# واجهات بسيطة للباقي (مثال)
# ───────────────────────────────────────────────
class TicketSetupView(discord.ui.View):
    def __init__(self, cog):
        super().__init__(timeout=300)
        self.cog = cog

    @discord.ui.channel_select(
        placeholder="📋 اختر قناة لوحة التكتات",
        channel_types=[discord.ChannelType.text],
        custom_id="select_ticket_panel"
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
        channel_types=[discord.ChannelType.category],
        custom_id="select_ticket_category"
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
        channel_types=[discord.ChannelType.text],
        custom_id="select_welcome"
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
        channel_types=[discord.ChannelType.text],
        custom_id="select_goodbye"
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
        channel_types=[discord.ChannelType.text],
        custom_id="select_log"
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
