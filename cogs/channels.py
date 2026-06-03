import discord
from discord.ext import commands
from discord import app_commands
from main import EmbedManager

class Channels(commands.Cog):
    """نظام إنشاء القنوات التلقائي"""
    
    def __init__(self, bot):
        self.bot = bot
        self.embed_manager = EmbedManager()
    
    @app_commands.command(name="channels", description="فتح قائمة القوالب")
    @app_commands.checks.has_permissions(administrator=True)
    async def channels_command(self, interaction: discord.Interaction):
        """فتح قائمة القوالب"""
        try:
            embed = self.embed_manager.info(
                "📋 قوالب السيرفر",
                "اختر قالب لإنشاء قنوات تلقائية"
            )
            
            class TemplatesView(discord.ui.View):
                def __init__(view_self):
                    super().__init__(timeout=180)
                
                @discord.ui.button(label="عام", style=discord.ButtonStyle.primary)
                async def general_template(view_self, inter: discord.Interaction, btn):
                    await inter.response.defer()
                    await self._create_general_template(inter)
                
                @discord.ui.button(label="ألعاب", style=discord.ButtonStyle.primary)
                async def games_template(view_self, inter: discord.Interaction, btn):
                    await inter.response.defer()
                    await self._create_games_template(inter)
                
                @discord.ui.button(label="مجتمع", style=discord.ButtonStyle.secondary)
                async def community_template(view_self, inter: discord.Interaction, btn):
                    await inter.response.defer()
                    await self._create_community_template(inter)
            
            await interaction.response.send_message(embed=embed, view=TemplatesView(), ephemeral=True)
        except Exception as e:
            embed = self.embed_manager.error("❌ خطأ", f"```{str(e)[:100]}```")
            await interaction.response.send_message(embed=embed, ephemeral=True)
    
    async def _create_general_template(self, interaction):
        """إنشاء قالب عام"""
        try:
            categories_channels = {
                "📋 المعلومات": ["📜 القوانين", "📢 الإعلانات", "🤝 الشراكات"],
                "💬 العام": ["🌌 عام", "😂 ميمز", "🖼️ صور"],
                "🎫 الدعم": ["📩 افتح-تكت", "📋 لوق-التكتات"],
                "🔧 الإدارة": ["📝 لوق-الأحداث", "🛡️ لوق-الحماية"],
            }
            
            created_count = 0
            for cat_name, channels in categories_channels.items():
                category = await interaction.guild.create_category(cat_name)
                for ch_name in channels:
                    await category.create_text_channel(ch_name)
                    created_count += 1
            
            embed = self.embed_manager.success(
                "✅ تم الإنشاء",
                f"تم إنشاء {created_count} قناة في {len(categories_channels)} فئات"
            )
            await interaction.followup.send(embed=embed, ephemeral=True)
        except Exception as e:
            embed = self.embed_manager.error("❌ خطأ", f"```{str(e)[:100]}```")
            await interaction.followup.send(embed=embed, ephemeral=True)
    
    async def _create_games_template(self, interaction):
        """إنشاء قالب ألعاب"""
        try:
            categories_channels = {
                "🎮 الألعاب": ["🎯 ماين كرافت", "🏀 فورتنايت", "⚔️ كاونتر سترايك"],
                "💬 التواصل": ["🌌 عام", "🎙️ الصوت"],
            }
            
            created_count = 0
            for cat_name, channels in categories_channels.items():
                category = await interaction.guild.create_category(cat_name)
                for ch_name in channels:
                    await category.create_text_channel(ch_name)
                    created_count += 1
            
            embed = self.embed_manager.success(
                "✅ تم الإنشاء",
                f"تم إنشاء {created_count} قناة ألعاب"
            )
            await interaction.followup.send(embed=embed, ephemeral=True)
        except Exception as e:
            embed = self.embed_manager.error("❌ خطأ", f"```{str(e)[:100]}```")
            await interaction.followup.send(embed=embed, ephemeral=True)
    
    async def _create_community_template(self, interaction):
        """إنشاء قالب مجتمع"""
        try:
            categories_channels = {
                "📋 المعلومات": ["📜 القوانين", "📢 الإعلانات"],
                "💬 النقاش": ["🌌 عام", "💡 أفكار"],
                "🎉 الفعاليات": ["🎊 الهدايا", "📊 الاستطلاعات"],
            }
            
            created_count = 0
            for cat_name, channels in categories_channels.items():
                category = await interaction.guild.create_category(cat_name)
                for ch_name in channels:
                    await category.create_text_channel(ch_name)
                    created_count += 1
            
            embed = self.embed_manager.success(
                "✅ تم الإنشاء",
                f"تم إنشاء {created_count} قناة مجتمع"
            )
            await interaction.followup.send(embed=embed, ephemeral=True)
        except Exception as e:
            embed = self.embed_manager.error("❌ خطأ", f"```{str(e)[:100]}```")
            await interaction.followup.send(embed=embed, ephemeral=True)


async def setup(bot):
    await bot.add_cog(Channels(bot))
