import discord
from discord.ext import commands
from discord import app_commands
from main import EmbedManager

class Echo(commands.Cog):
    """نظام تكرار الرسائل - البوت يردد كلامك"""
    
    def __init__(self, bot):
        self.bot = bot
        self.embed_manager = EmbedManager()
    
    @app_commands.command(name="text", description="البوت يردد الرسالة")
    @app_commands.describe(message="الرسالة اللي تبي تردد")
    async def text(self, interaction: discord.Interaction, message: str):
        """البوت يردد الرسالة بنفس الصيغة مع الخط الأصفر"""
        try:
            class EchoView(discord.ui.View):
                def __init__(view_self):
                    super().__init__()
                
                @discord.ui.button(label="تم الرد", style=discord.ButtonStyle.success, emoji="✅")
                async def confirmed(view_self, inter: discord.Interaction, btn):
                    await inter.response.defer()
            
            # إرسال الرسالة مع السماح بالمنشن (الخط الأصفر)
            await interaction.response.send_message(
                message, 
                view=EchoView(),
                allowed_mentions=discord.AllowedMentions(
                    everyone=True,
                    roles=True,
                    users=True
                )
            )
        except Exception as e:
            embed = self.embed_manager.error("❌ خطأ", f"```{str(e)[:100]}```")
            await interaction.response.send_message(embed=embed, ephemeral=True)


async def setup(bot):
    await bot.add_cog(Echo(bot))
