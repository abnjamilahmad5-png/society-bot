import discord
from discord.ext import commands
from discord import app_commands
from main import EmbedManager, DataManager
from datetime import timedelta
import asyncio

class Moderation(commands.Cog):
    """نظام الإشراف والإدارة"""
    
    def __init__(self, bot):
        self.bot = bot
        self.embed_manager = EmbedManager()
        self.data_manager = DataManager()
    
    def get_warnings(self):
        """الحصول على الإنذارات"""
        return self.data_manager.load_data("warnings.json")
    
    def save_warnings(self, data):
        """حفظ الإنذارات"""
        self.data_manager.save_data("warnings.json", data)
    
    @app_commands.command(name="ban", description="حظر مستخدم")
    @app_commands.checks.has_permissions(ban_members=True)
    async def ban_user(self, interaction: discord.Interaction, user: discord.User, reason: str = "بدون سبب"):
        """حظر مستخدم"""
        try:
            await interaction.guild.ban(user, reason=reason)
            
            embed = self.embed_manager.success(
                "✅ تم الحظر",
                f"**المستخدم**: {user.mention}\n"
                f"**السبب**: {reason}\n"
                f"**الموظف**: {interaction.user.mention}"
            )
            await interaction.response.send_message(embed=embed, ephemeral=False)
            
            try:
                dm_embed = self.embed_manager.error(
                    "❌ تم حظرك",
                    f"**السيرفر**: {interaction.guild.name}\n"
                    f"**السبب**: {reason}"
                )
                await user.send(embed=dm_embed)
            except:
                pass
        except Exception as e:
            embed = self.embed_manager.error("❌ خطأ", f"```{str(e)[:100]}```")
            await interaction.response.send_message(embed=embed, ephemeral=True)
    
    @app_commands.command(name="kick", description="طرد مستخدم")
    @app_commands.checks.has_permissions(kick_members=True)
    async def kick_user(self, interaction: discord.Interaction, user: discord.Member, reason: str = "بدون سبب"):
        """طرد مستخدم"""
        try:
            await interaction.guild.kick(user, reason=reason)
            
            embed = self.embed_manager.success(
                "✅ تم الطرد",
                f"**المستخدم**: {user.mention}\n"
                f"**السبب**: {reason}\n"
                f"**الموظف**: {interaction.user.mention}"
            )
            await interaction.response.send_message(embed=embed, ephemeral=False)
            
            try:
                dm_embed = self.embed_manager.error(
                    "❌ تم طردك",
                    f"**السيرفر**: {interaction.guild.name}\n"
                    f"**السبب**: {reason}"
                )
                await user.send(embed=dm_embed)
            except:
                pass
        except Exception as e:
            embed = self.embed_manager.error("❌ خطأ", f"```{str(e)[:100]}```")
            await interaction.response.send_message(embed=embed, ephemeral=True)
    
    @app_commands.command(name="warn", description="إنذار مستخدم")
    @app_commands.checks.has_permissions(moderate_members=True)
    async def warn_user(self, interaction: discord.Interaction, user: discord.Member, reason: str = "بدون سبب"):
        """إنذار مستخدم"""
        try:
            warnings = self.get_warnings()
            user_id = str(user.id)
            
            if user_id not in warnings:
                warnings[user_id] = []
            
            warnings[user_id].append({
                "reason": reason,
                "moderator": interaction.user.name,
                "date": discord.utils.utcnow().isoformat()
            })
            
            self.save_warnings(warnings)
            
            warn_count = len(warnings[user_id])
            
            embed = self.embed_manager.warning(
                "⚠️ تم الإنذار",
                f"**المستخدم**: {user.mention}\n"
                f"**السبب**: {reason}\n"
                f"**عدد الإنذارات**: {warn_count}/3"
            )
            await interaction.response.send_message(embed=embed, ephemeral=False)
            
            if warn_count >= 3:
                await interaction.guild.ban(user, reason="تم الحظر تلقائياً: 3 إنذارات")
                embed = self.embed_manager.error(
                    "🚫 تم الحظر التلقائي",
                    f"{user.mention} تم حظره تلقائياً بعد 3 إنذارات"
                )
                await interaction.channel.send(embed=embed)
        except Exception as e:
            embed = self.embed_manager.error("❌ خطأ", f"```{str(e)[:100]}```")
            await interaction.response.send_message(embed=embed, ephemeral=True)
    
    @app_commands.command(name="warnings", description="عرض إنذارات مستخدم")
    async def check_warnings(self, interaction: discord.Interaction, user: discord.Member):
        """عرض الإنذارات"""
        try:
            warnings = self.get_warnings()
            user_id = str(user.id)
            
            if user_id not in warnings or not warnings[user_id]:
                embed = self.embed_manager.info(
                    "ℹ️ الإنذارات",
                    f"{user.mention} لا يملك أي إنذارات"
                )
            else:
                warn_list = "\n".join([
                    f"{i+1}. **{w['reason']}** - {w['moderator']}\n   {w['date']}"
                    for i, w in enumerate(warnings[user_id])
                ])
                embed = self.embed_manager.info(
                    f"⚠️ إنذارات {user.name}",
                    f"**العدد الكلي**: {len(warnings[user_id])}\n\n{warn_list}"
                )
            
            await interaction.response.send_message(embed=embed, ephemeral=False)
        except Exception as e:
            embed = self.embed_manager.error("❌ خطأ", f"```{str(e)[:100]}```")
            await interaction.response.send_message(embed=embed, ephemeral=True)
    
    @app_commands.command(name="purge", description="حذف رسائل من القناة")
    @app_commands.checks.has_permissions(manage_messages=True)
    async def purge_messages(self, interaction: discord.Interaction, count: int):
        """حذف رسائل"""
        try:
            await interaction.response.defer()
            deleted = await interaction.channel.purge(limit=count)
            
            embed = self.embed_manager.success(
                "✅ تم الحذف",
                f"تم حذف **{len(deleted)}** رسالة من {interaction.channel.mention}"
            )
            await interaction.followup.send(embed=embed, ephemeral=False)
        except Exception as e:
            embed = self.embed_manager.error("❌ خطأ", f"```{str(e)[:100]}```")
            await interaction.followup.send(embed=embed, ephemeral=True)
    
    @app_commands.command(name="lock", description="قفل القناة")
    @app_commands.checks.has_permissions(manage_channels=True)
    async def lock_channel(self, interaction: discord.Interaction, reason: str = "بدون سبب"):
        """قفل القناة"""
        try:
            await interaction.channel.set_permissions(
                interaction.guild.default_role,
                send_messages=False
            )
            
            embed = self.embed_manager.warning(
                "🔒 تم قفل القناة",
                f"**السبب**: {reason}"
            )
            await interaction.response.send_message(embed=embed, ephemeral=False)
        except Exception as e:
            embed = self.embed_manager.error("❌ خطأ", f"```{str(e)[:100]}```")
            await interaction.response.send_message(embed=embed, ephemeral=True)
    
    @app_commands.command(name="unlock", description="فتح القناة")
    @app_commands.checks.has_permissions(manage_channels=True)
    async def unlock_channel(self, interaction: discord.Interaction):
        """فتح القناة"""
        try:
            await interaction.channel.set_permissions(
                interaction.guild.default_role,
                send_messages=True
            )
            
            embed = self.embed_manager.success(
                "🔓 تم فتح القناة",
                "القناة مفتوحة الآن للجميع"
            )
            await interaction.response.send_message(embed=embed, ephemeral=False)
        except Exception as e:
            embed = self.embed_manager.error("❌ خطأ", f"```{str(e)[:100]}```")
            await interaction.response.send_message(embed=embed, ephemeral=True)
    
    @commands.command(name="ban", aliases=["b"])
    @commands.has_permissions(ban_members=True)
    async def ban_prefix(self, ctx, user: discord.User, *, reason="بدون سبب"):
        """نسخة الـ prefix من Ban"""
        try:
            await ctx.guild.ban(user, reason=reason)
            embed = self.embed_manager.success(
                "✅ تم الحظر",
                f"**المستخدم**: {user.mention}\n**السبب**: {reason}"
            )
            await ctx.send(embed=embed)
        except Exception as e:
            embed = self.embed_manager.error("❌ خطأ", f"```{str(e)[:100]}```")
            await ctx.send(embed=embed)
    
    @commands.command(name="kick", aliases=["k"])
    @commands.has_permissions(kick_members=True)
    async def kick_prefix(self, ctx, user: discord.Member, *, reason="بدون سبب"):
        """نسخة الـ prefix من Kick"""
        try:
            await ctx.guild.kick(user, reason=reason)
            embed = self.embed_manager.success(
                "✅ تم الطرد",
                f"**المستخدم**: {user.mention}\n**السبب**: {reason}"
            )
            await ctx.send(embed=embed)
        except Exception as e:
            embed = self.embed_manager.error("❌ خطأ", f"```{str(e)[:100]}```")
            await ctx.send(embed=embed)
    
    @commands.command(name="warn", aliases=["w"])
    @commands.has_permissions(moderate_members=True)
    async def warn_prefix(self, ctx, user: discord.Member, *, reason="بدون سبب"):
        """نسخة الـ prefix من Warn"""
        try:
            warnings = self.get_warnings()
            user_id = str(user.id)
            
            if user_id not in warnings:
                warnings[user_id] = []
            
            warnings[user_id].append({
                "reason": reason,
                "moderator": ctx.author.name,
                "date": discord.utils.utcnow().isoformat()
            })
            
            self.save_warnings(warnings)
            
            warn_count = len(warnings[user_id])
            embed = self.embed_manager.warning(
                "⚠️ تم الإنذار",
                f"**المستخدم**: {user.mention}\n**السبب**: {reason}\n**العدد**: {warn_count}/3"
            )
            await ctx.send(embed=embed)
        except Exception as e:
            embed = self.embed_manager.error("❌ خطأ", f"```{str(e)[:100]}```")
            await ctx.send(embed=embed)


async def setup(bot):
    await bot.add_cog(Moderation(bot))
