import discord
from discord.ext import commands
from discord import app_commands
from main import EmbedManager, DataManager
from datetime import datetime, timedelta
import random

class Economy(commands.Cog):
    """نظام الاقتصاد والعملات"""
    
    def __init__(self, bot):
        self.bot = bot
        self.embed_manager = EmbedManager()
        self.data_manager = DataManager()
    
    def get_economy(self):
        """الحصول على بيانات الاقتصاد"""
        return self.data_manager.load_data("economy.json")
    
    def save_economy(self, data):
        """حفظ بيانات الاقتصاد"""
        self.data_manager.save_data("economy.json", data)
    
    def get_user_balance(self, user_id):
        """الحصول على رصيد المستخدم"""
        economy = self.get_economy()
        user_id = str(user_id)
        
        if user_id not in economy:
            economy[user_id] = {"wallet": 1000, "bank": 0, "last_daily": None}
            self.save_economy(economy)
        
        return economy[user_id]
    
    @app_commands.command(name="balance", description="عرض الرصيد")
    async def balance(self, interaction: discord.Interaction, user: discord.Member = None):
        """عرض الرصيد"""
        try:
            if user is None:
                user = interaction.user
            
            balance_data = self.get_user_balance(user.id)
            
            embed = self.embed_manager.info(
                f"💰 رصيد {user.name}",
                f"**المحفظة**: 💎 {balance_data['wallet']}\n"
                f"**البنك**: 🏦 {balance_data['bank']}\n"
                f"**المجموع**: 💎 {balance_data['wallet'] + balance_data['bank']}"
            )
            embed.set_thumbnail(url=user.avatar.url if user.avatar else "")
            
            await interaction.response.send_message(embed=embed, ephemeral=False)
        except Exception as e:
            embed = self.embed_manager.error("❌ خطأ", f"```{str(e)[:100]}```")
            await interaction.response.send_message(embed=embed, ephemeral=True)
    
    @app_commands.command(name="daily", description="مكافأة يومية")
    async def daily_reward(self, interaction: discord.Interaction):
        """مكافأة يومية"""
        try:
            balance_data = self.get_user_balance(interaction.user.id)
            
            if balance_data["last_daily"]:
                last_daily = datetime.fromisoformat(balance_data["last_daily"])
                if (datetime.now() - last_daily) < timedelta(hours=24):
                    hours_left = 24 - int((datetime.now() - last_daily).total_seconds() / 3600)
                    embed = self.embed_manager.warning(
                        "⏳ انتظر",
                        f"يمكنك الحصول على مكافأة يومية جديدة بعد **{hours_left}** ساعة"
                    )
                    await interaction.response.send_message(embed=embed, ephemeral=True)
                    return
            
            reward = 100
            economy = self.get_economy()
            economy[str(interaction.user.id)]["wallet"] += reward
            economy[str(interaction.user.id)]["last_daily"] = datetime.now().isoformat()
            self.save_economy(economy)
            
            embed = self.embed_manager.success(
                "✅ تم استلام المكافأة",
                f"حصلت على **💎 {reward}**"
            )
            await interaction.response.send_message(embed=embed, ephemeral=False)
        except Exception as e:
            embed = self.embed_manager.error("❌ خطأ", f"```{str(e)[:100]}```")
            await interaction.response.send_message(embed=embed, ephemeral=True)
    
    @app_commands.command(name="work", description="العمل للحصول على عملات")
    async def work(self, interaction: discord.Interaction):
        """العمل"""
        try:
            jobs = [
                {"name": "برمجة", "reward": (50, 100)},
                {"name": "تصميم", "reward": (40, 80)},
                {"name": "كتابة", "reward": (30, 60)},
                {"name": "تدريس", "reward": (45, 90)},
            ]
            
            job = random.choice(jobs)
            reward = random.randint(job["reward"][0], job["reward"][1])
            
            economy = self.get_economy()
            economy[str(interaction.user.id)]["wallet"] += reward
            self.save_economy(economy)
            
            embed = self.embed_manager.success(
                "💼 عملت بنجاح",
                f"عملت في **{job['name']}** وحصلت على **💎 {reward}**"
            )
            await interaction.response.send_message(embed=embed, ephemeral=False)
        except Exception as e:
            embed = self.embed_manager.error("❌ خطأ", f"```{str(e)[:100]}```")
            await interaction.response.send_message(embed=embed, ephemeral=True)
    
    @app_commands.command(name="deposit", description="إيداع أموال في البنك")
    async def deposit(self, interaction: discord.Interaction, amount: int):
        """إيداع"""
        try:
            balance_data = self.get_user_balance(interaction.user.id)
            
            if amount > balance_data["wallet"]:
                embed = self.embed_manager.error(
                    "❌ أموال غير كافية",
                    f"رصيدك في المحفظة: **💎 {balance_data['wallet']}**"
                )
                await interaction.response.send_message(embed=embed, ephemeral=True)
                return
            
            economy = self.get_economy()
            economy[str(interaction.user.id)]["wallet"] -= amount
            economy[str(interaction.user.id)]["bank"] += amount
            self.save_economy(economy)
            
            embed = self.embed_manager.success(
                "✅ تم الإيداع",
                f"تم إيداع **💎 {amount}** في البنك"
            )
            await interaction.response.send_message(embed=embed, ephemeral=False)
        except Exception as e:
            embed = self.embed_manager.error("❌ خطأ", f"```{str(e)[:100]}```")
            await interaction.response.send_message(embed=embed, ephemeral=True)
    
    @app_commands.command(name="withdraw", description="سحب أموال من البنك")
    async def withdraw(self, interaction: discord.Interaction, amount: int):
        """سحب"""
        try:
            balance_data = self.get_user_balance(interaction.user.id)
            
            if amount > balance_data["bank"]:
                embed = self.embed_manager.error(
                    "❌ أموال غير كافية",
                    f"رصيدك في البنك: **💎 {balance_data['bank']}**"
                )
                await interaction.response.send_message(embed=embed, ephemeral=True)
                return
            
            economy = self.get_economy()
            economy[str(interaction.user.id)]["wallet"] += amount
            economy[str(interaction.user.id)]["bank"] -= amount
            self.save_economy(economy)
            
            embed = self.embed_manager.success(
                "✅ تم السحب",
                f"تم سحب **💎 {amount}** من البنك"
            )
            await interaction.response.send_message(embed=embed, ephemeral=False)
        except Exception as e:
            embed = self.embed_manager.error("❌ خطأ", f"```{str(e)[:100]}```")
            await interaction.response.send_message(embed=embed, ephemeral=True)
    
    @app_commands.command(name="transfer", description="تحويل أموال لشخص")
    async def transfer(self, interaction: discord.Interaction, user: discord.Member, amount: int):
        """تحويل"""
        try:
            if user == interaction.user:
                embed = self.embed_manager.error(
                    "❌ خطأ",
                    "لا يمكنك تحويل أموال لنفسك"
                )
                await interaction.response.send_message(embed=embed, ephemeral=True)
                return
            
            balance_data = self.get_user_balance(interaction.user.id)
            
            if amount > balance_data["wallet"]:
                embed = self.embed_manager.error(
                    "❌ أموال غير كافية",
                    f"رصيدك: **💎 {balance_data['wallet']}**"
                )
                await interaction.response.send_message(embed=embed, ephemeral=True)
                return
            
            economy = self.get_economy()
            economy[str(interaction.user.id)]["wallet"] -= amount
            self.get_user_balance(user.id)
            economy[str(user.id)]["wallet"] += amount
            self.save_economy(economy)
            
            embed = self.embed_manager.success(
                "✅ تم التحويل",
                f"تم تحويل **💎 {amount}** إلى {user.mention}"
            )
            await interaction.response.send_message(embed=embed, ephemeral=False)
        except Exception as e:
            embed = self.embed_manager.error("❌ خطأ", f"```{str(e)[:100]}```")
            await interaction.response.send_message(embed=embed, ephemeral=True)
    
    @app_commands.command(name="rich", description="أغنى 10 أشخاص")
    async def rich_leaderboard(self, interaction: discord.Interaction):
        """لوحة الأغنياء"""
        try:
            economy = self.get_economy()
            
            sorted_users = sorted(
                economy.items(),
                key=lambda x: x[1]["wallet"] + x[1]["bank"],
                reverse=True
            )[:10]
            
            embed = self.embed_manager.info(
                "💎 أغنى 10 أشخاص",
                "أعلى الأرصدة في السيرفر"
            )
            
            rich_text = "\n".join([
                f"{i+1}. <@{uid}> - 💎 {data['wallet'] + data['bank']}"
                for i, (uid, data) in enumerate(sorted_users)
            ])
            
            embed.add_field(name="الترتيب", value=rich_text or "لا توجد بيانات", inline=False)
            
            await interaction.response.send_message(embed=embed, ephemeral=False)
        except Exception as e:
            embed = self.embed_manager.error("❌ خطأ", f"```{str(e)[:100]}```")
            await interaction.response.send_message(embed=embed, ephemeral=True)


async def setup(bot):
    await bot.add_cog(Economy(bot))
