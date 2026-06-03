import discord
from discord.ext import commands
from discord import app_commands
from main import EmbedManager, DataManager
from datetime import datetime

class Suggestions(commands.Cog):
    """نظام الاقتراحات"""
    
    def __init__(self, bot):
        self.bot = bot
        self.embed_manager = EmbedManager()
        self.data_manager = DataManager()
        self.suggestion_counter = 1
    
    def get_suggestions(self):
        """الحصول على الاقتراحات"""
        return self.data_manager.load_data("suggestions.json")
    
    def save_suggestions(self, data):
        """حفظ الاقتراحات"""
        self.data_manager.save_data("suggestions.json", data)
    
    @app_commands.command(name="suggest", description="إرسال اقتراح")
    async def suggest(self, interaction: discord.Interaction, suggestion: str):
        """إرسال اقتراح"""
        try:
            suggestions = self.get_suggestions()
            
            suggestion_id = self.suggestion_counter
            self.suggestion_counter += 1
            
            suggestions[str(suggestion_id)] = {
                "author_id": interaction.user.id,
                "author_name": interaction.user.name,
                "content": suggestion,
                "status": "معلق",
                "upvotes": 0,
                "downvotes": 0,
                "created_at": datetime.now().isoformat()
            }
            
            self.save_suggestions(suggestions)
            
            embed = self.embed_manager.success(
                "✅ تم الإرسال",
                f"تم إرسال اقتراحك برقم **#{suggestion_id}**\n"
                f"**الاقتراح**: {suggestion}"
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
            
            for channel in interaction.guild.text_channels:
                if "suggestion" in channel.name.lower():
                    suggest_embed = self.embed_manager.info(
                        f"💡 اقتراح جديد #{suggestion_id}",
                        f"**من**: {interaction.user.mention}\n"
                        f"**الاقتراح**: {suggestion}\n"
                        f"**الحالة**: معلق"
                    )
                    
                    class SuggestionView(discord.ui.View):
                        def __init__(view_self):
                            super().__init__(timeout=None)
                        
                        @discord.ui.button(label="✅", style=discord.ButtonStyle.success)
                        async def upvote(view_self, inter: discord.Interaction, btn):
                            await inter.response.defer()
                            suggestions[str(suggestion_id)]["upvotes"] += 1
                            self.save_suggestions(suggestions)
                        
                        @discord.ui.button(label="❌", style=discord.ButtonStyle.danger)
                        async def downvote(view_self, inter: discord.Interaction, btn):
                            await inter.response.defer()
                            suggestions[str(suggestion_id)]["downvotes"] += 1
                            self.save_suggestions(suggestions)
                    
                    try:
                        await channel.send(embed=suggest_embed, view=SuggestionView())
                        break
                    except:
                        pass
        except Exception as e:
            embed = self.embed_manager.error("❌ خطأ", f"```{str(e)[:100]}```")
            await interaction.response.send_message(embed=embed, ephemeral=True)
    
    @app_commands.command(name="suggestion-accept", description="قبول اقتراح")
    @app_commands.checks.has_permissions(administrator=True)
    async def accept_suggestion(self, interaction: discord.Interaction, suggestion_id: int):
        """قبول اقتراح"""
        try:
            suggestions = self.get_suggestions()
            
            if str(suggestion_id) not in suggestions:
                embed = self.embed_manager.error("❌ خطأ", "الاقتراح غير موجود")
                await interaction.response.send_message(embed=embed, ephemeral=True)
                return
            
            suggestions[str(suggestion_id)]["status"] = "مقبول"
            self.save_suggestions(suggestions)
            
            embed = self.embed_manager.success(
                "✅ تم القبول",
                f"تم قبول الاقتراح #{suggestion_id}"
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
        except Exception as e:
            embed = self.embed_manager.error("❌ خطأ", f"```{str(e)[:100]}```")
            await interaction.response.send_message(embed=embed, ephemeral=True)
    
    @app_commands.command(name="suggestion-deny", description="رفض اقتراح")
    @app_commands.checks.has_permissions(administrator=True)
    async def deny_suggestion(self, interaction: discord.Interaction, suggestion_id: int):
        """رفض اقتراح"""
        try:
            suggestions = self.get_suggestions()
            
            if str(suggestion_id) not in suggestions:
                embed = self.embed_manager.error("❌ خطأ", "الاقتراح غير موجود")
                await interaction.response.send_message(embed=embed, ephemeral=True)
                return
            
            suggestions[str(suggestion_id)]["status"] = "مرفوض"
            self.save_suggestions(suggestions)
            
            embed = self.embed_manager.warning(
                "❌ تم الرفض",
                f"تم رفض الاقتراح #{suggestion_id}"
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
        except Exception as e:
            embed = self.embed_manager.error("❌ خطأ", f"```{str(e)[:100]}```")
            await interaction.response.send_message(embed=embed, ephemeral=True)
    
    @app_commands.command(name="suggestions-list", description="قائمة الاقتراحات")
    async def suggestions_list(self, interaction: discord.Interaction):
        """عرض الاقتراحات"""
        try:
            suggestions = self.get_suggestions()
            
            if not suggestions:
                embed = self.embed_manager.info("💡 الاقتراحات", "لا توجد اقتراحات حالية")
                await interaction.response.send_message(embed=embed, ephemeral=False)
                return
            
            embed = self.embed_manager.info(
                "💡 قائمة الاقتراحات",
                f"إجمالي الاقتراحات: {len(suggestions)}"
            )
            
            for sid, sdata in list(suggestions.items())[:5]:
                status_emoji = "✅" if sdata["status"] == "مقبول" else ("❌" if sdata["status"] == "مرفوض" else "⏳")
                embed.add_field(
                    name=f"{status_emoji} #{sid}",
                    value=f"{sdata['content'][:100]}...",
                    inline=False
                )
            
            await interaction.response.send_message(embed=embed, ephemeral=False)
        except Exception as e:
            embed = self.embed_manager.error("❌ خطأ", f"```{str(e)[:100]}```")
            await interaction.response.send_message(embed=embed, ephemeral=True)


async def setup(bot):
    await bot.add_cog(Suggestions(bot))
