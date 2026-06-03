import discord
from discord.ext import commands
from discord import app_commands
from main import EmbedManager, DataManager
from datetime import datetime

class Logging(commands.Cog):
    """نظام اللوق"""
    
    def __init__(self, bot):
        self.bot = bot
        self.embed_manager = EmbedManager()
        self.data_manager = DataManager()
    
    @app_commands.command(name="log-set", description="تعيين قناة لوق")
    @app_commands.checks.has_permissions(administrator=True)
    async def log_set(self, interaction: discord.Interaction, channel: discord.TextChannel, log_type: str):
        """تعيين قناة لوق"""
        try:
            valid_types = ["member", "message", "role", "channel", "server", "moderation"]
            
            if log_type.lower() not in valid_types:
                embed = self.embed_manager.error(
                    "❌ خطأ",
                    f"أنواع متاحة: {', '.join(valid_types)}"
                )
                await interaction.response.send_message(embed=embed, ephemeral=True)
                return
            
            embed = self.embed_manager.success(
                "✅ تم التعيين",
                f"تم تعيين قناة لوق **{log_type}** في {channel.mention}"
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
        except Exception as e:
            embed = self.embed_manager.error("❌ خطأ", f"```{str(e)[:100]}```")
            await interaction.response.send_message(embed=embed, ephemeral=True)
    
    @commands.Cog.listener()
    async def on_member_join(self, member):
        """تسجيل انضمام عضو"""
        try:
            embed = self.embed_manager.info(
                "👋 عضو جديد انضم",
                f"**المستخدم**: {member.mention}\n"
                f"**ID**: {member.id}\n"
                f"**عمر الحساب**: {(datetime.now() - member.created_at).days} يوم\n"
                f"**الوقت**: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}"
            )
            embed.set_thumbnail(url=member.avatar.url if member.avatar else "")
            
            for channel in member.guild.text_channels:
                if "log" in channel.name.lower():
                    try:
                        await channel.send(embed=embed)
                        break
                    except:
                        pass
        except Exception:
            pass
    
    @commands.Cog.listener()
    async def on_member_remove(self, member):
        """تسجيل مغادرة عضو"""
        try:
            embed = self.embed_manager.warning(
                "👋 عضو غادر",
                f"**المستخدم**: {member.mention}\n"
                f"**ID**: {member.id}\n"
                f"**الرتب**: {len(member.roles)}\n"
                f"**الوقت**: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}"
            )
            embed.set_thumbnail(url=member.avatar.url if member.avatar else "")
            
            for channel in member.guild.text_channels:
                if "log" in channel.name.lower():
                    try:
                        await channel.send(embed=embed)
                        break
                    except:
                        pass
        except Exception:
            pass
    
    @commands.Cog.listener()
    async def on_message_delete(self, message):
        """تسجيل حذف رسالة"""
        try:
            if message.author.bot or not message.guild:
                return
            
            embed = self.embed_manager.warning(
                "🗑️ رسالة محذوفة",
                f"**المنشئ**: {message.author.mention}\n"
                f"**المحتوى**: {message.content[:100]}\n"
                f"**القناة**: {message.channel.mention}"
            )
            
            for channel in message.guild.text_channels:
                if "log" in channel.name.lower():
                    try:
                        await channel.send(embed=embed)
                        break
                    except:
                        pass
        except Exception:
            pass
    
    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        """تسجيل تعديل رسالة"""
        try:
            if after.author.bot or not after.guild:
                return
            
            if before.content == after.content:
                return
            
            embed = self.embed_manager.info(
                "✏️ رسالة معدلة",
                f"**المنشئ**: {after.author.mention}\n"
                f"**قبل**: {before.content[:100]}\n"
                f"**بعد**: {after.content[:100]}\n"
                f"**القناة**: {after.channel.mention}"
            )
            
            for channel in after.guild.text_channels:
                if "log" in channel.name.lower():
                    try:
                        await channel.send(embed=embed)
                        break
                    except:
                        pass
        except Exception:
            pass
    
    @commands.Cog.listener()
    async def on_member_update(self, before, after):
        """تسجيل تحديثات العضو"""
        try:
            if before.roles != after.roles:
                added_roles = [r for r in after.roles if r not in before.roles]
                removed_roles = [r for r in before.roles if r not in after.roles]
                
                if added_roles or removed_roles:
                    embed = self.embed_manager.info(
                        "📜 تحديث الرتب",
                        f"**المستخدم**: {after.mention}\n"
                    )
                    
                    if added_roles:
                        embed.add_field(name="رتب مضافة", value=", ".join([r.mention for r in added_roles]), inline=False)
                    if removed_roles:
                        embed.add_field(name="رتب محذوفة", value=", ".join([r.mention for r in removed_roles]), inline=False)
                    
                    for channel in after.guild.text_channels:
                        if "log" in channel.name.lower():
                            try:
                                await channel.send(embed=embed)
                                break
                            except:
                                pass
        except Exception:
            pass


async def setup(bot):
    await bot.add_cog(Logging(bot))
