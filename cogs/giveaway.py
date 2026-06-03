import discord
from discord.ext import commands
from discord import app_commands
from main import EmbedManager, DataManager
from datetime import datetime, timedelta
import random
import asyncio

class Giveaway(commands.Cog):
    """نظام الهدايا"""
    
    def __init__(self, bot):
        self.bot = bot
        self.embed_manager = EmbedManager()
        self.data_manager = DataManager()
    
    def get_giveaways(self):
        """الحصول على بيانات الهدايا"""
        return self.data_manager.load_data("giveaways.json")
    
    def save_giveaways(self, data):
        """حفظ بيانات الهدايا"""
        self.data_manager.save_data("giveaways.json", data)
    
    @app_commands.command(name="giveaway-start", description="بدء هدية جديدة")
    @app_commands.checks.has_permissions(administrator=True)
    async def start_giveaway(
        self,
        interaction: discord.Interaction,
        duration: int,
        winners: int,
        prize: str,
        channel: discord.TextChannel = None
    ):
        """بدء هدية"""
        try:
            if channel is None:
                channel = interaction.channel
            
            duration_seconds = duration * 60
            end_time = datetime.now() + timedelta(seconds=duration_seconds)
            
            embed = self.embed_manager.success(
                "🎉 هدية جديدة!",
                f"**الجائزة**: {prize}\n"
                f"**الفائزون**: {winners}\n"
                f"**المدة**: {duration} دقيقة\n"
                f"**ينتهي في**: <t:{int(end_time.timestamp())}:R>"
            )
            embed.set_footer(text="اضغط الزر أدناه للمشاركة!")
            
            class GiveawayView(discord.ui.View):
                def __init__(view_self):
                    super().__init__(timeout=duration_seconds)
                    view_self.participants = set()
                
                @discord.ui.button(label="اضغط للمشاركة", style=discord.ButtonStyle.primary, emoji="🎁")
                async def participate(view_self, inter: discord.Interaction, btn):
                    await inter.response.defer()
                    view_self.participants.add(inter.user.id)
                    embed = self.embed_manager.success(
                        "✅ تمت المشاركة",
                        f"لقد شاركت في الهدية!"
                    )
                    await inter.followup.send(embed=embed, ephemeral=True)
                
                async def on_timeout(view_self):
                    if view_self.participants:
                        selected = random.sample(list(view_self.participants), min(winners, len(view_self.participants)))
                        winners_text = ", ".join([f"<@{uid}>" for uid in selected])
                        
                        result_embed = self.embed_manager.success(
                            "🏆 انتهت الهدية!",
                            f"**الفائزون**: {winners_text}\n"
                            f"**الجائزة**: {prize}"
                        )
                        
                        try:
                            await channel.send(embed=result_embed)
                        except:
                            pass
                    else:
                        no_winner_embed = self.embed_manager.warning(
                            "❌ لا فائزين",
                            "لم يشارك أحد في الهدية"
                        )
                        try:
                            await channel.send(embed=no_winner_embed)
                        except:
                            pass
            
            msg = await channel.send(embed=embed, view=GiveawayView())
            
            giveaways = self.get_giveaways()
            giveaways[str(msg.id)] = {
                "channel_id": channel.id,
                "prize": prize,
                "winners": winners,
                "end_time": end_time.isoformat()
            }
            self.save_giveaways(giveaways)
            
            response_embed = self.embed_manager.success(
                "✅ تمت البداية",
                f"تم بدء الهدية في {channel.mention}"
            )
            await interaction.response.send_message(embed=response_embed, ephemeral=True)
        except Exception as e:
            embed = self.embed_manager.error("❌ خطأ", f"```{str(e)[:100]}```")
            await interaction.response.send_message(embed=embed, ephemeral=True)
    
    @app_commands.command(name="giveaway-list", description="قائمة الهدايا")
    async def giveaway_list(self, interaction: discord.Interaction):
        """عرض قائمة الهدايا"""
        try:
            giveaways = self.get_giveaways()
            
            if not giveaways:
                embed = self.embed_manager.info("🎉 الهدايا", "لا توجد هدايا حالية")
                await interaction.response.send_message(embed=embed, ephemeral=False)
                return
            
            embed = self.embed_manager.info(
                "🎉 الهدايا الحالية",
                f"إجمالي الهدايا: {len(giveaways)}"
            )
            
            for gid, gdata in list(giveaways.items())[:5]:
                embed.add_field(
                    name=gdata["prize"],
                    value=f"الفائزون: **{gdata['winners']}**",
                    inline=False
                )
            
            await interaction.response.send_message(embed=embed, ephemeral=False)
        except Exception as e:
            embed = self.embed_manager.error("❌ خطأ", f"```{str(e)[:100]}```")
            await interaction.response.send_message(embed=embed, ephemeral=True)


async def setup(bot):
    await bot.add_cog(Giveaway(bot))
