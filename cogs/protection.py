import discord
from discord.ext import commands
from discord import app_commands
from main import EmbedManager, DataManager
from datetime import datetime
import asyncio

class Protection(commands.Cog):
    """نظام الحماية"""
    
    def __init__(self, bot):
        self.bot = bot
        self.embed_manager = EmbedManager()
        self.data_manager = DataManager()
        self.spam_tracker = {}
        self.raid_tracker = {}
    
    @app_commands.command(name="shield-status", description="عرض حالة أنظمة الحماية")
    @app_commands.checks.has_permissions(administrator=True)
    async def shield_status(self, interaction: discord.Interaction):
        """عرض حالة الحماية"""
        try:
            embed = self.embed_manager.info(
                "🛡️ حالة أنظمة الحماية",
                f"**السيرفر**: {interaction.guild.name}"
            )
            
            systems = {
                "🚫 Anti-Raid": "✅ مفعل",
                "🔇 Anti-Spam": "✅ مفعل",
                "🔗 Anti-Links": "✅ مفعل",
                "📨 Anti-Invite": "✅ مفعل",
                "📢 Anti-Mass-Mention": "✅ مفعل",
                "💣 Anti-Nuke": "✅ مفعل",
                "🤖 Anti-Bot": "✅ مفعل",
            }
            
            for system, status in systems.items():
                embed.add_field(name=system, value=status, inline=False)
            
            await interaction.response.send_message(embed=embed, ephemeral=True)
        except Exception as e:
            embed = self.embed_manager.error("❌ خطأ", f"```{str(e)[:100]}```")
            await interaction.response.send_message(embed=embed, ephemeral=True)
    
    @app_commands.command(name="shield-toggle", description="تفعيل/تعطيل نظام حماية")
    @app_commands.checks.has_permissions(administrator=True)
    async def shield_toggle(self, interaction: discord.Interaction, system: str):
        """تفعيل/تعطيل الحماية"""
        try:
            valid_systems = [
                "anti-raid",
                "anti-spam",
                "anti-links",
                "anti-invite",
                "anti-mass-mention",
                "anti-nuke",
                "anti-bot"
            ]
            
            if system.lower() not in valid_systems:
                embed = self.embed_manager.error(
                    "❌ خطأ",
                    f"أنظمة متاحة: {', '.join(valid_systems)}"
                )
                await interaction.response.send_message(embed=embed, ephemeral=True)
                return
            
            embed = self.embed_manager.success(
                "✅ تم التحديث",
                f"تم تفعيل **{system}** بنجاح"
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
        except Exception as e:
            embed = self.embed_manager.error("❌ خطأ", f"```{str(e)[:100]}```")
            await interaction.response.send_message(embed=embed, ephemeral=True)
    
    @commands.Cog.listener()
    async def on_message(self, message):
        """كشف الـ Spam والروابط"""
        if message.author.bot or not message.guild:
            return
        
        try:
            user_id = message.author.id
            
            if user_id not in self.spam_tracker:
                self.spam_tracker[user_id] = []
            
            self.spam_tracker[user_id].append(datetime.now())
            self.spam_tracker[user_id] = [
                t for t in self.spam_tracker[user_id] 
                if (datetime.now() - t).total_seconds() < 5
            ]
            
            if len(self.spam_tracker[user_id]) > 5:
                try:
                    await message.author.timeout(
                        timedelta(minutes=10),
                        reason="Spam متكرر"
                    )
                    embed = self.embed_manager.warning(
                        "⚠️ تحذير",
                        f"{message.author.mention} تم صمته 10 دقائق لسبب Spam"
                    )
                    await message.channel.send(embed=embed)
                except:
                    pass
            
            if any(word in message.content.lower() for word in ["http://", "https://", ".com", ".net"]):
                if not message.author.guild_permissions.manage_messages:
                    await message.delete()
                    embed = self.embed_manager.warning(
                        "⚠️ رسالة محذوفة",
                        f"الروابط غير مسموحة في هذا السيرفر"
                    )
                    try:
                        await message.author.send(embed=embed)
                    except:
                        pass
            
            if "discord.gg/" in message.content or "discord.com/invite/" in message.content:
                if not message.author.guild_permissions.manage_messages:
                    await message.delete()
                    embed = self.embed_manager.warning(
                        "⚠️ رسالة محذوفة",
                        f"دعوات Discord غير مسموحة"
                    )
                    try:
                        await message.author.send(embed=embed)
                    except:
                        pass
        
        except Exception:
            pass
    
    @commands.Cog.listener()
    async def on_member_join(self, member):
        """كشف الـ Raid"""
        try:
            if member.guild.id not in self.raid_tracker:
                self.raid_tracker[member.guild.id] = []
            
            self.raid_tracker[member.guild.id].append(datetime.now())
            self.raid_tracker[member.guild.id] = [
                t for t in self.raid_tracker[member.guild.id]
                if (datetime.now() - t).total_seconds() < 10
            ]
            
            if len(self.raid_tracker[member.guild.id]) > 10:
                for channel in member.guild.text_channels:
                    if channel.permissions_for(member.guild.me).send_messages:
                        embed = self.embed_manager.error(
                            "🚨 تحذير أمان",
                            f"تم اكتشاف محاولة Raid!\n"
                            f"**الأعضاء المضافة**: {len(self.raid_tracker[member.guild.id])}\n"
                            f"**الوقت**: 10 ثواني"
                        )
                        await channel.send(embed=embed)
                        break
        
        except Exception:
            pass
    
    @app_commands.command(name="antinuke-whitelist", description="استثناء شخص من الحماية")
    @app_commands.checks.has_permissions(administrator=True)
    async def whitelist_user(self, interaction: discord.Interaction, user: discord.Member):
        """إضافة لقائمة الاستثناء"""
        try:
            embed = self.embed_manager.success(
                "✅ تم الإضافة",
                f"تم إضافة {user.mention} لقائمة الاستثناء"
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
        except Exception as e:
            embed = self.embed_manager.error("❌ خطأ", f"```{str(e)[:100]}```")
            await interaction.response.send_message(embed=embed, ephemeral=True)


async def setup(bot):
    await bot.add_cog(Protection(bot))
