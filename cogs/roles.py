import discord
from discord.ext import commands
from discord import app_commands
from main import EmbedManager, DataManager

class Roles(commands.Cog):
    """نظام الرتب التفاعلية"""
    
    def __init__(self, bot):
        self.bot = bot
        self.embed_manager = EmbedManager()
        self.data_manager = DataManager()
    
    @app_commands.command(name="roles-panel", description="إرسال بانيل الرتب")
    @app_commands.checks.has_permissions(administrator=True)
    async def roles_panel(self, interaction: discord.Interaction):
        """إرسال بانيل الرتب"""
        try:
            embed = self.embed_manager.info(
                "🎭 اختر رتبتك",
                "اختر الرتب التي تريدها من خلال القائمة أدناه"
            )
            
            roles_data = self.data_manager.load_data("guild_settings.json")
            guild_key = str(interaction.guild.id)
            
            if guild_key not in roles_data:
                roles_data[guild_key] = {"selfroles": []}
            
            selfroles = roles_data[guild_key].get("selfroles", [])
            
            if not selfroles:
                embed.add_field(
                    name="ℹ️ معلومة",
                    value="لم يتم تحديد أي رتب للاختيار بعد. اطلب من الأدمن إضافتها.",
                    inline=False
                )
                await interaction.response.send_message(embed=embed, ephemeral=False)
                return
            
            class RolesView(discord.ui.View):
                def __init__(view_self):
                    super().__init__(timeout=None)
                
                @discord.ui.select(
                    placeholder="اختر رتبتك",
                    options=[
                        discord.SelectOption(label=f"رتبة {i+1}", value=f"role_{i}")
                        for i in range(len(selfroles[:25]))
                    ]
                )
                async def select_role(view_self, inter: discord.Interaction, select: discord.ui.Select):
                    await inter.response.defer()
                    try:
                        role_index = int(select.values[0].split("_")[1])
                        role_id = selfroles[role_index]
                        role = inter.guild.get_role(role_id)
                        
                        if role:
                            if role in inter.user.roles:
                                await inter.user.remove_roles(role)
                                result = "تمت إزالة الرتبة ❌"
                            else:
                                await inter.user.add_roles(role)
                                result = "تمت إضافة الرتبة ✅"
                            
                            embed = self.embed_manager.success("✅ تم التحديث", result)
                            await inter.followup.send(embed=embed, ephemeral=True)
                    except Exception as e:
                        embed = self.embed_manager.error("❌ خطأ", f"```{str(e)[:100]}```")
                        await inter.followup.send(embed=embed, ephemeral=True)
            
            await interaction.response.send_message(embed=embed, view=RolesView())
        except Exception as e:
            embed = self.embed_manager.error("❌ خطأ", f"```{str(e)[:100]}```")
            await interaction.response.send_message(embed=embed, ephemeral=True)
    
    @app_commands.command(name="add-selfrole", description="إضافة رتبة للاختيار")
    @app_commands.checks.has_permissions(administrator=True)
    async def add_selfrole(self, interaction: discord.Interaction, role: discord.Role):
        """إضافة رتبة للاختيار"""
        try:
            roles_data = self.data_manager.load_data("guild_settings.json")
            guild_key = str(interaction.guild.id)
            
            if guild_key not in roles_data:
                roles_data[guild_key] = {"selfroles": []}
            
            if role.id not in roles_data[guild_key].get("selfroles", []):
                if "selfroles" not in roles_data[guild_key]:
                    roles_data[guild_key]["selfroles"] = []
                roles_data[guild_key]["selfroles"].append(role.id)
                self.data_manager.save_data("guild_settings.json", roles_data)
            
            embed = self.embed_manager.success(
                "✅ تمت الإضافة",
                f"تمت إضافة {role.mention} لرتب الاختيار"
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
        except Exception as e:
            embed = self.embed_manager.error("❌ خطأ", f"```{str(e)[:100]}```")
            await interaction.response.send_message(embed=embed, ephemeral=True)
    
    @app_commands.command(name="remove-selfrole", description="إزالة رتبة من الاختيار")
    @app_commands.checks.has_permissions(administrator=True)
    async def remove_selfrole(self, interaction: discord.Interaction, role: discord.Role):
        """إزالة رتبة من الاختيار"""
        try:
            roles_data = self.data_manager.load_data("guild_settings.json")
            guild_key = str(interaction.guild.id)
            
            if guild_key in roles_data and role.id in roles_data[guild_key].get("selfroles", []):
                roles_data[guild_key]["selfroles"].remove(role.id)
                self.data_manager.save_data("guild_settings.json", roles_data)
            
            embed = self.embed_manager.success(
                "✅ تمت الإزالة",
                f"تمت إزالة {role.mention} من رتب الاختيار"
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
        except Exception as e:
            embed = self.embed_manager.error("❌ خطأ", f"```{str(e)[:100]}```")
            await interaction.response.send_message(embed=embed, ephemeral=True)
    
    @app_commands.command(name="role-info", description="معلومات عن رتبة")
    async def role_info(self, interaction: discord.Interaction, role: discord.Role):
        """معلومات الرتبة"""
        try:
            embed = self.embed_manager.info(
                f"ℹ️ معلومات الرتبة: {role.name}",
                f"**اللون**: {role.color}\n"
                f"**المنصب**: {role.position}\n"
                f"**الأعضاء**: {len(role.members)}\n"
                f"**قابلة للاختيار**: {'✅ نعم' if role.mentionable else '❌ لا'}\n"
                f"**تاريخ الإنشاء**: {role.created_at.strftime('%d/%m/%Y')}"
            )
            await interaction.response.send_message(embed=embed, ephemeral=False)
        except Exception as e:
            embed = self.embed_manager.error("❌ خطأ", f"```{str(e)[:100]}```")
            await interaction.response.send_message(embed=embed, ephemeral=True)
    
    @app_commands.command(name="role-add", description="إعطاء رتبة لشخص")
    @app_commands.checks.has_permissions(manage_roles=True)
    async def role_add(self, interaction: discord.Interaction, user: discord.Member, role: discord.Role):
        """إعطاء رتبة"""
        try:
            await user.add_roles(role)
            embed = self.embed_manager.success(
                "✅ تمت الإضافة",
                f"تمت إضافة {role.mention} لـ {user.mention}"
            )
            await interaction.response.send_message(embed=embed, ephemeral=False)
        except Exception as e:
            embed = self.embed_manager.error("❌ خطأ", f"```{str(e)[:100]}```")
            await interaction.response.send_message(embed=embed, ephemeral=True)
    
    @app_commands.command(name="role-remove", description="إزالة رتبة من شخص")
    @app_commands.checks.has_permissions(manage_roles=True)
    async def role_remove(self, interaction: discord.Interaction, user: discord.Member, role: discord.Role):
        """إزالة رتبة"""
        try:
            await user.remove_roles(role)
            embed = self.embed_manager.success(
                "✅ تمت الإزالة",
                f"تمت إزالة {role.mention} من {user.mention}"
            )
            await interaction.response.send_message(embed=embed, ephemeral=False)
        except Exception as e:
            embed = self.embed_manager.error("❌ خطأ", f"```{str(e)[:100]}```")
            await interaction.response.send_message(embed=embed, ephemeral=True)


async def setup(bot):
    await bot.add_cog(Roles(bot))
