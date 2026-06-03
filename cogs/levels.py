import discord
from discord.ext import commands
from discord import app_commands
from main import EmbedManager, DataManager
import random

class Levels(commands.Cog):
    """نظام المستويات والـ XP"""
    
    def __init__(self, bot):
        self.bot = bot
        self.embed_manager = EmbedManager()
        self.data_manager = DataManager()
        self.cooldowns = {}
    
    def get_levels(self):
        """الحصول على بيانات المستويات"""
        return self.data_manager.load_data("levels.json")
    
    def save_levels(self, data):
        """حفظ بيانات المستويات"""
        self.data_manager.save_data("levels.json", data)
    
    def calculate_xp_needed(self, level):
        """حساب الـ XP المطلوب للمستوى التالي"""
        return 5 * (level ** 2) + 50 * level + 100
    
    @commands.Cog.listener()
    async def on_message(self, message):
        """إضافة XP عند الرسالة"""
        if message.author.bot or not message.guild:
            return
        
        user_id = str(message.author.id)
        
        if user_id in self.cooldowns:
            if (message.created_at.timestamp() - self.cooldowns[user_id]) < 60:
                return
        
        self.cooldowns[user_id] = message.created_at.timestamp()
        
        try:
            levels = self.get_levels()
            
            if user_id not in levels:
                levels[user_id] = {"xp": 0, "level": 1}
            
            xp_gain = random.randint(15, 25)
            levels[user_id]["xp"] += xp_gain
            
            current_level = levels[user_id]["level"]
            xp_needed = self.calculate_xp_needed(current_level)
            
            if levels[user_id]["xp"] >= xp_needed:
                levels[user_id]["level"] += 1
                levels[user_id]["xp"] = 0
                
                self.save_levels(levels)
                
                embed = self.embed_manager.success(
                    "🎉 تم الترقية!",
                    f"{message.author.mention} وصل إلى المستوى **{levels[user_id]['level']}**"
                )
                
                try:
                    await message.channel.send(embed=embed)
                except:
                    pass
            else:
                self.save_levels(levels)
        except Exception:
            pass
    
    @app_commands.command(name="rank", description="عرض مستوى المستخدم")
    async def rank_command(self, interaction: discord.Interaction, user: discord.Member = None):
        """عرض المستوى"""
        try:
            if user is None:
                user = interaction.user
            
            levels = self.get_levels()
            user_id = str(user.id)
            
            if user_id not in levels:
                levels[user_id] = {"xp": 0, "level": 1}
                self.save_levels(levels)
            
            user_data = levels[user_id]
            current_level = user_data["level"]
            current_xp = user_data["xp"]
            xp_needed = self.calculate_xp_needed(current_level)
            
            progress = int((current_xp / xp_needed) * 100)
            progress_bar = "█" * (progress // 10) + "░" * (10 - progress // 10)
            
            embed = self.embed_manager.info(
                f"📊 مستوى {user.name}",
                f"**المستوى**: {current_level}\n"
                f"**الـ XP**: {current_xp}/{xp_needed}\n"
                f"**التقدم**: [{progress_bar}] {progress}%"
            )
            embed.set_thumbnail(url=user.avatar.url if user.avatar else "")
            
            await interaction.response.send_message(embed=embed, ephemeral=False)
        except Exception as e:
            embed = self.embed_manager.error("❌ خطأ", f"```{str(e)[:100]}```")
            await interaction.response.send_message(embed=embed, ephemeral=True)
    
    @app_commands.command(name="leaderboard", description="أفضل 10 أعضاء")
    async def leaderboard(self, interaction: discord.Interaction):
        """عرض الترتيب"""
        try:
            levels = self.get_levels()
            
            sorted_users = sorted(
                levels.items(),
                key=lambda x: (x[1]["level"], x[1]["xp"]),
                reverse=True
            )[:10]
            
            embed = self.embed_manager.info(
                "🏆 لوحة الصدارة",
                f"أفضل 10 أعضاء في السيرفر"
            )
            
            leaderboard_text = "\n".join([
                f"{i+1}. <@{uid}> - المستوى: **{data['level']}** | الـ XP: **{data['xp']}**"
                for i, (uid, data) in enumerate(sorted_users)
            ])
            
            embed.add_field(name="الترتيب", value=leaderboard_text or "لا توجد بيانات", inline=False)
            
            await interaction.response.send_message(embed=embed, ephemeral=False)
        except Exception as e:
            embed = self.embed_manager.error("❌ خطأ", f"```{str(e)[:100]}```")
            await interaction.response.send_message(embed=embed, ephemeral=True)
    
    @app_commands.command(name="addxp", description="إضافة XP لمستخدم")
    @app_commands.checks.has_permissions(administrator=True)
    async def add_xp(self, interaction: discord.Interaction, user: discord.Member, amount: int):
        """إضافة XP"""
        try:
            levels = self.get_levels()
            user_id = str(user.id)
            
            if user_id not in levels:
                levels[user_id] = {"xp": 0, "level": 1}
            
            levels[user_id]["xp"] += amount
            self.save_levels(levels)
            
            embed = self.embed_manager.success(
                "✅ تمت الإضافة",
                f"تمت إضافة **{amount}** XP لـ {user.mention}\n"
                f"**الـ XP الحالي**: {levels[user_id]['xp']}"
            )
            await interaction.response.send_message(embed=embed, ephemeral=False)
        except Exception as e:
            embed = self.embed_manager.error("❌ خطأ", f"```{str(e)[:100]}```")
            await interaction.response.send_message(embed=embed, ephemeral=True)
    
    @app_commands.command(name="setxp", description="تعيين XP لمستخدم")
    @app_commands.checks.has_permissions(administrator=True)
    async def set_xp(self, interaction: discord.Interaction, user: discord.Member, amount: int):
        """تعيين XP"""
        try:
            levels = self.get_levels()
            user_id = str(user.id)
            
            levels[user_id] = {"xp": amount, "level": 1}
            self.save_levels(levels)
            
            embed = self.embed_manager.success(
                "✅ تم التعيين",
                f"تم تعيين الـ XP إلى **{amount}** لـ {user.mention}"
            )
            await interaction.response.send_message(embed=embed, ephemeral=False)
        except Exception as e:
            embed = self.embed_manager.error("❌ خطأ", f"```{str(e)[:100]}```")
            await interaction.response.send_message(embed=embed, ephemeral=True)


async def setup(bot):
    await bot.add_cog(Levels(bot))
