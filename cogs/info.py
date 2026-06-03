import discord
from discord.ext import commands
from discord import app_commands
from main import EmbedManager
from datetime import datetime

class Info(commands.Cog):
    """أوامر المعلومات"""
    
    def __init__(self, bot):
        self.bot = bot
        self.embed_manager = EmbedManager()
    
    @app_commands.command(name="userinfo", description="معلومات مستخدم")
    async def userinfo(self, interaction: discord.Interaction, user: discord.Member = None):
        """معلومات مستخدم"""
        try:
            if user is None:
                user = interaction.user
            
            roles = ", ".join([r.mention for r in user.roles[1:5]]) or "بدون رتب"
            
            embed = self.embed_manager.info(
                f"ℹ️ معلومات {user.name}",
                f"**الـ ID**: {user.id}\n"
                f"**الحالة**: {user.status}\n"
                f"**تاريخ الإنشاء**: {user.created_at.strftime('%d/%m/%Y')}\n"
                f"**تاريخ الانضمام**: {user.joined_at.strftime('%d/%m/%Y')}\n"
                f"**الرتب**: {roles}"
            )
            embed.set_thumbnail(url=user.avatar.url if user.avatar else "")
            
            await interaction.response.send_message(embed=embed, ephemeral=False)
        except Exception as e:
            embed = self.embed_manager.error("❌ خطأ", f"```{str(e)[:100]}```")
            await interaction.response.send_message(embed=embed, ephemeral=True)
    
    @app_commands.command(name="serverinfo", description="معلومات السيرفر")
    async def serverinfo(self, interaction: discord.Interaction):
        """معلومات السيرفر"""
        try:
            guild = interaction.guild
            
            embed = self.embed_manager.info(
                f"ℹ️ معلومات {guild.name}",
                f"**الـ ID**: {guild.id}\n"
                f"**المالك**: {guild.owner.mention}\n"
                f"**الأعضاء**: {guild.member_count}\n"
                f"**القنوات**: {len(guild.channels)}\n"
                f"**الرتب**: {len(guild.roles)}\n"
                f"**تاريخ الإنشاء**: {guild.created_at.strftime('%d/%m/%Y')}"
            )
            embed.set_thumbnail(url=guild.icon.url if guild.icon else "")
            
            await interaction.response.send_message(embed=embed, ephemeral=False)
        except Exception as e:
            embed = self.embed_manager.error("❌ خطأ", f"```{str(e)[:100]}```")
            await interaction.response.send_message(embed=embed, ephemeral=True)
    
    @app_commands.command(name="botinfo", description="معلومات البوت")
    async def botinfo(self, interaction: discord.Interaction):
        """معلومات البوت"""
        try:
            bot_user = self.bot.user
            
            embed = self.embed_manager.info(
                f"ℹ️ معلومات {bot_user.name}",
                f"**الـ ID**: {bot_user.id}\n"
                f"**الإصدار**: discord.py 2.3.2\n"
                f"**السيرفرات**: {len(self.bot.guilds)}\n"
                f"**الأعضاء**: {sum(g.member_count for g in self.bot.guilds)}\n"
                f"**تاريخ الإنشاء**: {bot_user.created_at.strftime('%d/%m/%Y')}"
            )
            embed.set_thumbnail(url=bot_user.avatar.url if bot_user.avatar else "")
            
            await interaction.response.send_message(embed=embed, ephemeral=False)
        except Exception as e:
            embed = self.embed_manager.error("❌ خطأ", f"```{str(e)[:100]}```")
            await interaction.response.send_message(embed=embed, ephemeral=True)
    
    @app_commands.command(name="avatar", description="صورة المستخدم")
    async def avatar(self, interaction: discord.Interaction, user: discord.Member = None):
        """عرض الصورة"""
        try:
            if user is None:
                user = interaction.user
            
            embed = self.embed_manager.info(
                f"🖼️ صورة {user.name}",
                f"[اضغط لتحميل الصورة]({user.avatar.url})" if user.avatar else "بدون صورة"
            )
            embed.set_image(url=user.avatar.url if user.avatar else "")
            
            await interaction.response.send_message(embed=embed, ephemeral=False)
        except Exception as e:
            embed = self.embed_manager.error("❌ خطأ", f"```{str(e)[:100]}```")
            await interaction.response.send_message(embed=embed, ephemeral=True)
    
    @app_commands.command(name="ping", description="اختبار الاتصال")
    async def ping(self, interaction: discord.Interaction):
        """اختبار Ping"""
        try:
            latency = round(self.bot.latency * 1000)
            
            embed = self.embed_manager.success(
                "🏓 Ping",
                f"**التأخير**: {latency}ms"
            )
            
            await interaction.response.send_message(embed=embed, ephemeral=False)
        except Exception as e:
            embed = self.embed_manager.error("❌ خطأ", f"```{str(e)[:100]}```")
            await interaction.response.send_message(embed=embed, ephemeral=True)
    
    @app_commands.command(name="uptime", description="وقت التشغيل")
    async def uptime(self, interaction: discord.Interaction):
        """عرض وقت التشغيل"""
        try:
            if hasattr(self.bot, 'start_time') and self.bot.start_time:
                uptime_delta = datetime.now() - self.bot.start_time
                days = uptime_delta.days
                hours = uptime_delta.seconds // 3600
                minutes = (uptime_delta.seconds % 3600) // 60
                
                embed = self.embed_manager.info(
                    "⏱️ وقت التشغيل",
                    f"**المدة**: {days} يوم، {hours} ساعة، {minutes} دقيقة"
                )
            else:
                embed = self.embed_manager.warning(
                    "⏱️ وقت التشغيل",
                    "البوت بدأ للتو"
                )
            
            await interaction.response.send_message(embed=embed, ephemeral=False)
        except Exception as e:
            embed = self.embed_manager.error("❌ خطأ", f"```{str(e)[:100]}```")
            await interaction.response.send_message(embed=embed, ephemeral=True)
    
    @app_commands.command(name="id", description="الحصول على ID")
    async def get_id(self, interaction: discord.Interaction, target: str = None):
        """الحصول على ID"""
        try:
            if target:
                try:
                    user = await self.bot.fetch_user(int(target))
                    embed = self.embed_manager.info("🆔 ID", f"**ID المستخدم**: {user.id}")
                except:
                    embed = self.embed_manager.error("❌ خطأ", "لم أستطع العثور على المستخدم")
            else:
                embed = self.embed_manager.info(
                    "🆔 معلومات ID",
                    f"**ID المستخدم**: {interaction.user.id}\n"
                    f"**ID السيرفر**: {interaction.guild.id}\n"
                    f"**ID القناة**: {interaction.channel.id}"
                )
            
            await interaction.response.send_message(embed=embed, ephemeral=False)
        except Exception as e:
            embed = self.embed_manager.error("❌ خطأ", f"```{str(e)[:100]}```")
            await interaction.response.send_message(embed=embed, ephemeral=True)


async def setup(bot):
    await bot.add_cog(Info(bot))
