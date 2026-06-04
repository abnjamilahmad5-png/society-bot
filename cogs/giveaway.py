import discord
from discord.ext import commands
from discord import app_commands
from main import EmbedManager, DataManager
from datetime import datetime, timedelta, timezone
import random
import asyncio

class Giveaway(commands.Cog):
    """نظام الهدايا والجوائز بالكريديت"""
    
    def __init__(self, bot):
        self.bot = bot
        self.embed_manager = EmbedManager()
        self.data_manager = DataManager()
    
    def get_credits_data(self):
        """الحصول على بيانات الكريديت"""
        return self.data_manager.load_data("credits.json")
    
    def save_credits_data(self, data):
        """حفظ بيانات الكريديت"""
        self.data_manager.save_data("credits.json", data)
    
    def add_user_credits(self, user_id: int, amount: int) -> int:
        """إضافة كريديت للمستخدم"""
        data = self.get_credits_data()
        current = data.get(str(user_id), 0)
        new_amount = max(0, current + amount)
        data[str(user_id)] = new_amount
        self.save_credits_data(data)
        return new_amount
    
    def get_bot_credits(self) -> int:
        """الحصول على كريديت البوت"""
        data = self.get_credits_data()
        return data.get(str(self.bot.user.id), 0)
    
    def get_giveaways(self):
        """الحصول على بيانات الهدايا"""
        return self.data_manager.load_data("giveaways.json")
    
    def save_giveaways(self, data):
        """حفظ بيانات الهدايا"""
        self.data_manager.save_data("giveaways.json", data)
    
    @app_commands.command(name="giveaway-start", description="بدء هدية كريديت")
    @app_commands.checks.has_permissions(administrator=True)
    @app_commands.describe(
        duration="المدة بالدقائق",
        winners="عدد الفائزين",
        prize_amount="عدد الكريديت للفائز الواحد",
        channel="القناة (اختيارية)"
    )
    async def start_giveaway(
        self,
        interaction: discord.Interaction,
        duration: int,
        winners: int,
        prize_amount: int,
        channel: discord.TextChannel = None
    ):
        """بدء هدية كريديت"""
        try:
            # التحقق من كريديت البوت
            bot_credits = self.get_bot_credits()
            total_needed = prize_amount * winners
            
            if bot_credits < total_needed:
                embed = self.embed_manager.error(
                    "❌ كريديت غير كافي",
                    f"كريديت البوت: `{bot_credits:,}` 💳\n"
                    f"الكريديت المطلوب: `{total_needed:,}` 💳"
                )
                await interaction.response.send_message(embed=embed, ephemeral=True)
                return
            
            if channel is None:
                channel = interaction.channel
            
            duration_seconds = duration * 60
            end_time = datetime.now(timezone.utc) + timedelta(seconds=duration_seconds)
            
            embed = self.embed_manager.success(
                "🎉 هدية كريديت جديدة!",
                f"**الجائزة**: `{prize_amount:,}` 💳 لكل فائز\n"
                f"**الفائزون**: {winners}\n"
                f"**الإجمالي**: `{total_needed:,}` 💳\n"
                f"**المدة**: {duration} دقيقة\n"
                f"**ينتهي في**: <t:{int(end_time.timestamp())}:R>"
            )
            embed.set_footer(text="اضغط 🎁 للمشاركة!")
            
            class GiveawayView(discord.ui.View):
                def __init__(view_self):
                    super().__init__(timeout=duration_seconds)
                    view_self.participants = set()
                
                @discord.ui.button(label="اضغط للمشاركة", style=discord.ButtonStyle.primary, emoji="🎁")
                async def participate(view_self, inter: discord.Interaction, btn):
                    await inter.response.defer()
                    if inter.user.bot:
                        return
                    view_self.participants.add(inter.user.id)
                    embed = self.embed_manager.success(
                        "✅ تمت المشاركة",
                        "شكراً لمشاركتك في الهدية!"
                    )
                    await inter.followup.send(embed=embed, ephemeral=True)
                
                async def on_timeout(view_self):
                    if len(view_self.participants) < winners:
                        actual_winners = min(winners, len(view_self.participants))
                    else:
                        actual_winners = winners
                    
                    if view_self.participants:
                        selected = random.sample(list(view_self.participants), actual_winners)
                        winners_text = ", ".join([f"<@{uid}>" for uid in selected])
                        
                        # تحويل الكريديت للفائزين
                        for winner_id in selected:
                            self.add_user_credits(winner_id, prize_amount)
                        
                        result_embed = self.embed_manager.success(
                            "🏆 انتهت الهدية!",
                            f"**الفائزون**: {winners_text}\n"
                            f"**الجائزة**: `{prize_amount:,}` 💳 لكل واحد\n\n"
                            f"تم تحويل الكريديت للفائزين! 🎉"
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
                "prize_amount": prize_amount,
                "winners": winners,
                "end_time": end_time.isoformat()
            }
            self.save_giveaways(giveaways)
            
            response_embed = self.embed_manager.success(
                "✅ تمت البداية",
                f"تم بدء الهدية في {channel.mention}\n"
                f"الكريديت المحتجز: `{total_needed:,}` 💳"
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
