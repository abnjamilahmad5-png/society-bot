import discord
from discord.ext import commands
from discord import app_commands
from main import EmbedManager, DataManager
import json

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
        return settings
    
    @app_commands.command(name="setup", description="فتح قائمة الإعدادات التفاعلية")
    @app_commands.checks.has_permissions(administrator=True)
    async def setup_command(self, interaction: discord.Interaction):
        """أمر الإعداد الرئيسي"""
        try:
            embed = self.embed_manager.info(
                "⚙️ إعدادات السيرفر",
                "اختر الفئة التي تريد تعديلها"
            )
            
            class SetupView(discord.ui.View):
                def __init__(view_self):
                    super().__init__(timeout=300)
                
                @discord.ui.button(label="🎫 التكتات", style=discord.ButtonStyle.primary)
                async def tickets(view_self, inter: discord.Interaction, button):
                    await inter.response.defer()
                    embed = self.embed_manager.info(
                        "🎫 إعدادات التكتات",
                        "قم بتحديد قنوات وفئات التكتات"
                    )
                    await inter.followup.send(embed=embed, ephemeral=True)
                
                @discord.ui.button(label="🎉 الترحيب", style=discord.ButtonStyle.primary)
                async def welcome(view_self, inter: discord.Interaction, button):
                    await inter.response.defer()
                    embed = self.embed_manager.info(
                        "🎉 إعدادات الترحيب",
                        "تحديد قنوات الترحيب والوداع"
                    )
                    await inter.followup.send(embed=embed, ephemeral=True)
                
                @discord.ui.button(label="🛡️ الحماية", style=discord.ButtonStyle.danger)
                async def protection(view_self, inter: discord.Interaction, button):
                    await inter.response.defer()
                    embed = self.embed_manager.info(
                        "🛡️ إعدادات الحماية",
                        "تفعيل أنظمة الحماية المتقدمة"
                    )
                    await inter.followup.send(embed=embed, ephemeral=True)
                
                @discord.ui.button(label="📊 اللوق", style=discord.ButtonStyle.secondary)
                async def logging(view_self, inter: discord.Interaction, button):
                    await inter.response.defer()
                    embed = self.embed_manager.info(
                        "📝 إعدادات اللوق",
                        "تعيين قنوات تسجيل الأحداث"
                    )
                    await inter.followup.send(embed=embed, ephemeral=True)
                
                @discord.ui.button(label="⚖️ الإشراف", style=discord.ButtonStyle.danger)
                async def moderation(view_self, inter: discord.Interaction, button):
                    await inter.response.defer()
                    embed = self.embed_manager.info(
                        "⚖️ إعدادات الإشراف",
                        "تحديد رتب الإشراف والصلاحيات"
                    )
                    await inter.followup.send(embed=embed, ephemeral=True)
            
            await interaction.response.send_message(embed=embed, view=SetupView(), ephemeral=True)
        except Exception as e:
            embed = self.embed_manager.error("❌ خطأ", f"```{str(e)[:100]}```")
            await interaction.response.send_message(embed=embed, ephemeral=True)
    
    @app_commands.command(name="setup-status", description="عرض الإعدادات الحالية")
    @app_commands.checks.has_permissions(administrator=True)
    async def setup_status(self, interaction: discord.Interaction):
        """عرض حالة الإعدادات"""
        try:
            settings = self.get_guild_settings(interaction.guild.id)
            guild_settings = settings[str(interaction.guild.id)]
            
            embed = self.embed_manager.info(
                "📋 حالة الإعدادات الحالية",
                f"إعدادات السيرفر: **{interaction.guild.name}**"
            )
            
            embed.add_field(
                name="🎫 التكتات",
                value=f"**الحالة**: {'✅ مفعلة' if guild_settings.get('tickets_enabled') else '❌ معطلة'}\n"
                      f"**القناة**: {guild_settings.get('ticket_panel_channel', 'لم تُحدد')}\n"
                      f"**الفئة**: {guild_settings.get('ticket_category', 'لم تُحدد')}",
                inline=False
            )
            
            embed.add_field(
                name="🎉 الترحيب",
                value=f"**الحالة**: {'✅ مفعلة' if guild_settings.get('welcome_enabled') else '❌ معطلة'}\n"
                      f"**قناة الترحيب**: {guild_settings.get('welcome_channel', 'لم تُحدد')}\n"
                      f"**قناة الوداع**: {guild_settings.get('goodbye_channel', 'لم تُحدد')}",
                inline=False
            )
            
            embed.add_field(
                name="🛡️ الحماية",
                value=f"**الحالة**: {'✅ مفعلة' if guild_settings.get('protection_enabled') else '❌ معطلة'}",
                inline=False
            )
            
            embed.add_field(
                name="⚖️ الإشراف",
                value=f"**رتبة الأدمن**: {guild_settings.get('admin_role', 'لم تُحدد')}\n"
                      f"**رتبة المود**: {guild_settings.get('mod_role', 'لم تُحدد')}\n"
                      f"**رتبة الميوت**: {guild_settings.get('mute_role', 'لم تُحدد')}",
                inline=False
            )
            
            await interaction.response.send_message(embed=embed, ephemeral=True)
        except Exception as e:
            embed = self.embed_manager.error("❌ خطأ", f"```{str(e)[:100]}```")
            await interaction.response.send_message(embed=embed, ephemeral=True)
    
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


async def setup(bot):
    await bot.add_cog(Setup(bot))
