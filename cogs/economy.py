import discord
from discord.ext import commands
from discord import app_commands
from main import EmbedManager, DataManager, ColorManager
from typing import Optional

class Economy(commands.Cog):
    """نظام كريديت Discord العالمي"""
    
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
    
    def get_user_credits(self, user_id: int) -> int:
        """الحصول على كريديت المستخدم"""
        data = self.get_credits_data()
        return data.get(str(user_id), 0)
    
    def set_user_credits(self, user_id: int, amount: int):
        """تعيين كريديت المستخدم"""
        data = self.get_credits_data()
        data[str(user_id)] = max(0, amount)  # لا يقل عن 0
        self.save_credits_data(data)
    
    def add_user_credits(self, user_id: int, amount: int) -> int:
        """إضافة كريديت للمستخدم"""
        current = self.get_user_credits(user_id)
        new_amount = max(0, current + amount)
        self.set_user_credits(user_id, new_amount)
        return new_amount
    
    @app_commands.command(name="balance", description="عرض رصيدك من الكريديت")
    async def balance(self, interaction: discord.Interaction, user: Optional[discord.Member] = None):
        """عرض رصيد الكريديت"""
        try:
            target_user = user or interaction.user
            credits = self.get_user_credits(target_user.id)
            
            embed = self.embed_manager.info(
                f"💎 كريديت {target_user.name}",
                f"**الرصيد**: `{credits:,}` 💳"
            )
            embed.set_thumbnail(url=target_user.avatar.url if target_user.avatar else "")
            embed.add_field(
                name="ℹ️ معلومة",
                value="الكريديت هو النقود العالمية - استخدمها في الهدايا والفعاليات!",
                inline=False
            )
            
            await interaction.response.send_message(embed=embed)
        except Exception as e:
            embed = self.embed_manager.error("❌ خطأ", f"```{str(e)[:100]}```")
            await interaction.response.send_message(embed=embed, ephemeral=True)
    
    @app_commands.command(name="transfer", description="تحويل كريديت لشخص آخر")
    @app_commands.describe(
        user="المستخدم الذي تريد تحويل له",
        amount="عدد الكريديت"
    )
    async def transfer(self, interaction: discord.Interaction, user: discord.Member, amount: int):
        """تحويل الكريديت بين المستخدمين"""
        try:
            if amount <= 0:
                embed = self.embed_manager.error("❌ خطأ", "يجب أن يكون المبلغ أكبر من 0")
                await interaction.response.send_message(embed=embed, ephemeral=True)
                return
            
            if user.id == interaction.user.id:
                embed = self.embed_manager.error("❌ خطأ", "لا يمكنك تحويل كريديت لنفسك")
                await interaction.response.send_message(embed=embed, ephemeral=True)
                return
            
            sender_credits = self.get_user_credits(interaction.user.id)
            if sender_credits < amount:
                embed = self.embed_manager.error(
                    "❌ كريديت غير كافي",
                    f"رصيدك: `{sender_credits:,}` 💳\nالمبلغ المطلوب: `{amount:,}` 💳"
                )
                await interaction.response.send_message(embed=embed, ephemeral=True)
                return
            
            # تنفيذ التحويل
            self.add_user_credits(interaction.user.id, -amount)
            self.add_user_credits(user.id, amount)
            
            embed = self.embed_manager.success(
                "✅ تم التحويل بنجاح",
                f"**من**: {interaction.user.mention}\n"
                f"**إلى**: {user.mention}\n"
                f"**المبلغ**: `{amount:,}` 💳\n\n"
                f"رصيدك الجديد: `{self.get_user_credits(interaction.user.id):,}` 💳"
            )
            
            await interaction.response.send_message(embed=embed)
        except Exception as e:
            embed = self.embed_manager.error("❌ خطأ", f"```{str(e)[:100]}```")
            await interaction.response.send_message(embed=embed, ephemeral=True)
    
    @app_commands.command(name="credits-info", description="معلومات نظام الكريديت")
    async def credits_info(self, interaction: discord.Interaction):
        """عرض معلومات الكريديت"""
        try:
            embed = self.embed_manager.info(
                "💎 نظام الكريديت العالمي",
                "كريديت Discord العالمي - استخدمه في الفعاليات والهدايا!"
            )
            embed.add_field(
                name="📊 ماذا تفعل بالكريديت؟",
                value="""
                🎁 **الهدايا** - شارك في هدايا الكريديت واربح المزيد
                🎉 **الفعاليات** - شارك في الفعاليات الخاصة
                💸 **التحويل** - حول كريديتك لأصدقائك
                """,
                inline=False
            )
            embed.add_field(
                name="⚡ الأوامر المتاحة",
                value="""
                `/balance` - عرض رصيدك
                `/transfer @user [amount]` - تحويل كريديت
                """,
                inline=False
            )
            
            await interaction.response.send_message(embed=embed)
        except Exception as e:
            embed = self.embed_manager.error("❌ خطأ", f"```{str(e)[:100]}```")
            await interaction.response.send_message(embed=embed, ephemeral=True)
    
    # ═══════════════════════════════════════════════════════════
    # 🔐 أوامر المالك فقط
    # ═══════════════════════════════════════════════════════════
    
    @app_commands.command(name="admin-credits", description="[المالك] إدارة الكريديت")
    @app_commands.checks.has_permissions(administrator=True)
    @app_commands.describe(
        user="المستخدم",
        action="إضافة (+) أم حذف (-)",
        amount="عدد الكريديت"
    )
    async def admin_credits(self, interaction: discord.Interaction, user: discord.Member, action: str, amount: int):
        """إدارة الكريديت من قبل المالك"""
        try:
            # التحقق من صلاحيات المالك
            if interaction.user.id != self.bot.owner_id:
                embed = self.embed_manager.error(
                    "❌ رفض الوصول",
                    "فقط مالك البوت يمكنه استخدام هذا الأمر"
                )
                await interaction.response.send_message(embed=embed, ephemeral=True)
                return
            
            if amount <= 0:
                embed = self.embed_manager.error("❌ خطأ", "المبلغ يجب أن يكون أكبر من 0")
                await interaction.response.send_message(embed=embed, ephemeral=True)
                return
            
            if action not in ["+", "-", "add", "remove"]:
                embed = self.embed_manager.error("❌ خطأ", "استخدم `+` أو `-` أو `add` أو `remove`")
                await interaction.response.send_message(embed=embed, ephemeral=True)
                return
            
            is_add = action in ["+", "add"]
            change = amount if is_add else -amount
            
            new_balance = self.add_user_credits(user.id, change)
            action_text = "إضافة" if is_add else "حذف"
            
            embed = self.embed_manager.success(
                f"✅ تم {action_text} الكريديت",
                f"**المستخدم**: {user.mention}\n"
                f"**العملية**: {action_text} `{amount:,}` 💳\n"
                f"**الرصيد الجديد**: `{new_balance:,}` 💳"
            )
            
            await interaction.response.send_message(embed=embed)
        except Exception as e:
            embed = self.embed_manager.error("❌ خطأ", f"```{str(e)[:100]}```")
            await interaction.response.send_message(embed=embed, ephemeral=True)
    
    @app_commands.command(name="bot-credits", description="[المالك] عرض كريديت البوت")
    @app_commands.checks.has_permissions(administrator=True)
    async def bot_credits(self, interaction: discord.Interaction):
        """عرض كريديت البوت"""
        try:
            bot_credits = self.get_user_credits(self.bot.user.id)
            
            embed = self.embed_manager.info(
                "💎 كريديت البوت",
                f"**الرصيد الإجمالي**: `{bot_credits:,}` 💳\n\n"
                f"هذا الكريديت يُستخدم في:\n"
                f"🎁 الهدايا والفعاليات\n"
                f"🎉 المكافئات الخاصة"
            )
            
            await interaction.response.send_message(embed=embed)
        except Exception as e:
            embed = self.embed_manager.error("❌ خطأ", f"```{str(e)[:100]}```")
            await interaction.response.send_message(embed=embed, ephemeral=True)


async def setup(bot):
    await bot.add_cog(Economy(bot))
