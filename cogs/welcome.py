import discord
from discord.ext import commands
from discord import app_commands
from main import EmbedManager, DataManager
from datetime import datetime

class Welcome(commands.Cog):
    """نظام الترحيب والوداع"""
    
    def __init__(self, bot):
        self.bot = bot
        self.embed_manager = EmbedManager()
        self.data_manager = DataManager()
    
    def get_guild_settings(self, guild_id):
        """الحصول على إعدادات السيرفر"""
        settings = self.data_manager.load_data("guild_settings.json")
        if str(guild_id) not in settings:
            settings[str(guild_id)] = {}
        return settings
    
    @app_commands.command(name="set-welcome", description="تعيين قناة الترحيب")
    @app_commands.checks.has_permissions(administrator=True)
    async def set_welcome(self, interaction: discord.Interaction, channel: discord.TextChannel):
        """تعيين قناة الترحيب"""
        try:
            settings = self.get_guild_settings(interaction.guild.id)
            settings[str(interaction.guild.id)]["welcome_channel"] = channel.id
            self.data_manager.save_data("guild_settings.json", settings)
            
            embed = self.embed_manager.success(
                "✅ تم التعيين",
                f"تم تعيين قناة الترحيب: {channel.mention}"
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
        except Exception as e:
            embed = self.embed_manager.error("❌ خطأ", f"```{str(e)[:100]}```")
            await interaction.response.send_message(embed=embed, ephemeral=True)
    
    @app_commands.command(name="set-goodbye", description="تعيين قناة الوداع")
    @app_commands.checks.has_permissions(administrator=True)
    async def set_goodbye(self, interaction: discord.Interaction, channel: discord.TextChannel):
        """تعيين قناة الوداع"""
        try:
            settings = self.get_guild_settings(interaction.guild.id)
            settings[str(interaction.guild.id)]["goodbye_channel"] = channel.id
            self.data_manager.save_data("guild_settings.json", settings)
            
            embed = self.embed_manager.success(
                "✅ تم التعيين",
                f"تم تعيين قناة الوداع: {channel.mention}"
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
        except Exception as e:
            embed = self.embed_manager.error("❌ خطأ", f"```{str(e)[:100]}```")
            await interaction.response.send_message(embed=embed, ephemeral=True)
    
    @app_commands.command(name="set-autorole", description="تعيين رتبة تلقائية")
    @app_commands.checks.has_permissions(administrator=True)
    async def set_autorole(self, interaction: discord.Interaction, role: discord.Role):
        """تعيين رتبة تلقائية"""
        try:
            settings = self.get_guild_settings(interaction.guild.id)
            settings[str(interaction.guild.id)]["autorole"] = role.id
            self.data_manager.save_data("guild_settings.json", settings)
            
            embed = self.embed_manager.success(
                "✅ تم التعيين",
                f"تم تعيين الرتبة التلقائية: {role.mention}"
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
        except Exception as e:
            embed = self.embed_manager.error("❌ خطأ", f"```{str(e)[:100]}```")
            await interaction.response.send_message(embed=embed, ephemeral=True)
    
    @commands.Cog.listener()
    async def on_member_join(self, member):
        """ترحيب بالعضو الجديد"""
        try:
            settings = self.get_guild_settings(member.guild.id)
            guild_settings = settings.get(str(member.guild.id), {})
            
            welcome_channel_id = guild_settings.get("welcome_channel")
            autorole_id = guild_settings.get("autorole")
            
            if welcome_channel_id:
                channel = member.guild.get_channel(welcome_channel_id)
                if channel:
                    embed = self.embed_manager.success(
                        f"👋 مرحباً {member.name}",
                        f"**المستخدم**: {member.mention}\n"
                        f"**عدد الأعضاء**: {member.guild.member_count}\n"
                        f"**عمر الحساب**: {(datetime.now() - member.created_at).days} يوم\n"
                        f"**وقت الانضمام**: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}"
                    )
                    embed.set_thumbnail(url=member.avatar.url if member.avatar else "")
                    embed.set_footer(text=f"𝑆𝑜𝑐𝑖𝑒𝑡𝑦 ✦ {datetime.now().strftime('%d/%m/%Y • %H:%M:%S')}")
                    
                    try:
                        await channel.send(embed=embed)
                    except:
                        pass
            
            if autorole_id:
                role = member.guild.get_role(autorole_id)
                if role:
                    try:
                        await member.add_roles(role)
                    except:
                        pass
            
            try:
                dm_embed = self.embed_manager.info(
                    f"مرحباً في {member.guild.name}",
                    f"نتمنى أن تستمتع بوقتك في السيرفر!\n\n"
                    f"اقرأ القوانين وتمتع بالتواصل مع الأعضاء الآخرين."
                )
                await member.send(embed=dm_embed)
            except:
                pass
        except Exception:
            pass
    
    @commands.Cog.listener()
    async def on_member_remove(self, member):
        """وداع العضو"""
        try:
            settings = self.get_guild_settings(member.guild.id)
            guild_settings = settings.get(str(member.guild.id), {})
            
            goodbye_channel_id = guild_settings.get("goodbye_channel")
            
            if goodbye_channel_id:
                channel = member.guild.get_channel(goodbye_channel_id)
                if channel:
                    embed = self.embed_manager.warning(
                        f"👋 وداعاً {member.name}",
                        f"**المستخدم**: {member.mention}\n"
                        f"**الرتب**: {len(member.roles)}\n"
                        f"**مدة البقاء**: {(datetime.now() - member.joined_at).days} يوم"
                    )
                    embed.set_thumbnail(url=member.avatar.url if member.avatar else "")
                    
                    try:
                        await channel.send(embed=embed)
                    except:
                        pass
        except Exception:
            pass


async def setup(bot):
    await bot.add_cog(Welcome(bot))
