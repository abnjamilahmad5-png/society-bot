import discord
from discord.ext import commands
from discord import app_commands
from main import EmbedManager
from typing import Optional, Literal

class Echo(commands.Cog):
    """نظام تكرار الرسائل - البوت يردد كلامك"""
    
    def __init__(self, bot):
        self.bot = bot
        self.embed_manager = EmbedManager()
    
    @app_commands.command(name="text", description="البوت يردد كلامك")
    @app_commands.describe(
        message="الرسالة اللي تبي تردد",
        user="منشن شخص (اختياري)",
        style="أسلوب الرسالة (اختياري)"
    )
    async def text(
        self,
        interaction: discord.Interaction,
        message: str,
        user: Optional[discord.Member] = None,
        style: Optional[Literal["عادي 📝", "أحرف كبيرة 🔤", "أحرف صغيرة 🔡", "عكسي 🔄", "فراغات 🔲"]] = None
    ):
        """البوت يردد الرسالة بالأسلوب المطلوب"""
        try:
            # معالجة الرسالة حسب الأسلوب
            if style == "أحرف كبيرة 🔤":
                formatted_message = message.upper()
            elif style == "أحرف صغيرة 🔡":
                formatted_message = message.lower()
            elif style == "عكسي 🔄":
                formatted_message = message[::-1]
            elif style == "فراغات 🔲":
                formatted_message = " ".join(message)
            else:
                formatted_message = message
            
            # بناء الرسالة النهائية
            final_message = formatted_message
            
            if user:
                final_message = f"{user.mention}\n{final_message}"
            
            # إرسال الرسالة
            await interaction.response.send_message(final_message)
        except Exception as e:
            embed = self.embed_manager.error("❌ خطأ", f"```{str(e)[:100]}```")
            await interaction.response.send_message(embed=embed, ephemeral=True)


async def setup(bot):
    await bot.add_cog(Echo(bot))
