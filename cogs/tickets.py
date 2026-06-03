import discord
from discord.ext import commands
from discord import app_commands
from main import EmbedManager, DataManager
import random
from datetime import datetime

class Tickets(commands.Cog):
    """نظام التكتات"""
    
    def __init__(self, bot):
        self.bot = bot
        self.embed_manager = EmbedManager()
        self.data_manager = DataManager()
    
    def get_tickets(self):
        """الحصول على بيانات التكتات"""
        return self.data_manager.load_data("tickets.json")
    
    def save_tickets(self, data):
        """حفظ بيانات التكتات"""
        self.data_manager.save_data("tickets.json", data)
    
    @app_commands.command(name="ticket-panel", description="إرسال بانيل فتح التكتات")
    @app_commands.checks.has_permissions(administrator=True)
    async def ticket_panel(self, interaction: discord.Interaction):
        """إرسال بانيل التكتات"""
        try:
            embed = self.embed_manager.info(
                "🎫 نظام الدعم الفني",
                "اضغط على الزر أدناه لفتح تكت دعم جديد"
            )
            embed.set_thumbnail(url=interaction.guild.icon.url if interaction.guild.icon else "")
            
            class TicketView(discord.ui.View):
                def __init__(view_self):
                    super().__init__(timeout=None)
                    view_self.cog = self
                
                @discord.ui.button(label="فتح تكت", style=discord.ButtonStyle.primary, emoji="🎫")
                async def open_ticket(view_self, inter: discord.Interaction, button):
                    await inter.response.defer()
                    try:
                        tickets = self.get_tickets()
                        user_id = str(inter.user.id)
                        
                        if user_id in tickets:
                            embed = self.embed_manager.error(
                                "❌ خطأ",
                                "لديك تكت مفتوح بالفعل"
                            )
                            await inter.followup.send(embed=embed, ephemeral=True)
                            return
                        
                        category = inter.guild.get_channel(123456789) or inter.guild.categories[0]
                        
                        channel = await inter.guild.create_text_channel(
                            name=f"تكت-{inter.user.name}",
                            category=category
                        )
                        
                        tickets[user_id] = {
                            "channel_id": channel.id,
                            "user_id": inter.user.id,
                            "created_at": datetime.now().isoformat(),
                            "claimed_by": None,
                        }
                        self.save_tickets(tickets)
                        
                        embed = self.embed_manager.success(
                            "✅ تم فتح التكت",
                            f"تم فتح التكت في {channel.mention}"
                        )
                        await inter.followup.send(embed=embed, ephemeral=True)
                        
                        ticket_embed = self.embed_manager.info(
                            "🎫 تكت دعم جديد",
                            f"**المستخدم**: {inter.user.mention}\n"
                            f"**الوقت**: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n"
                            f"**الحالة**: مفتوح"
                        )
                        
                        class TicketChannelView(discord.ui.View):
                            def __init__(view_self):
                                super().__init__(timeout=None)
                            
                            @discord.ui.button(label="إغلاق", style=discord.ButtonStyle.danger, emoji="🔒")
                            async def close_ticket(view_self, close_inter: discord.Interaction, btn):
                                await close_inter.response.defer()
                                await channel.delete()
                        
                        await channel.send(embed=ticket_embed, view=TicketChannelView())
                        
                    except Exception as e:
                        embed = self.embed_manager.error("❌ خطأ", f"```{str(e)[:100]}```")
                        await inter.followup.send(embed=embed, ephemeral=True)
            
            await interaction.response.send_message(embed=embed, view=TicketView())
        except Exception as e:
            embed = self.embed_manager.error("❌ خطأ", f"```{str(e)[:100]}```")
            await interaction.response.send_message(embed=embed, ephemeral=True)
    
    @app_commands.command(name="ticket-close", description="إغلاق التكت الحالي")
    async def ticket_close(self, interaction: discord.Interaction):
        """إغلاق التكت"""
        try:
            tickets = self.get_tickets()
            user_id = str(interaction.user.id)
            
            if user_id not in tickets:
                embed = self.embed_manager.error("❌ خطأ", "أنت لا تملك أي تكت مفتوح")
                await interaction.response.send_message(embed=embed, ephemeral=True)
                return
            
            channel_id = tickets[user_id]["channel_id"]
            channel = interaction.guild.get_channel(channel_id)
            
            if channel:
                await channel.delete()
            
            del tickets[user_id]
            self.save_tickets(tickets)
            
            embed = self.embed_manager.success("✅ تم إغلاق التكت", "تم حذف قناة التكت بنجاح")
            await interaction.response.send_message(embed=embed, ephemeral=True)
        except Exception as e:
            embed = self.embed_manager.error("❌ خطأ", f"```{str(e)[:100]}```")
            await interaction.response.send_message(embed=embed, ephemeral=True)
    
    @app_commands.command(name="ticket-stats", description="إحصائيات التكتات")
    @app_commands.checks.has_permissions(administrator=True)
    async def ticket_stats(self, interaction: discord.Interaction):
        """عرض إحصائيات التكتات"""
        try:
            tickets = self.get_tickets()
            
            embed = self.embed_manager.info(
                "📊 إحصائيات التكتات",
                f"إجمالي التكتات المفتوحة: **{len(tickets)}**"
            )
            
            if tickets:
                ticket_list = "\n".join([
                    f"• <@{ticket['user_id']}> - {ticket.get('created_at', 'تاريخ غير متاح')}"
                    for ticket in tickets.values()
                ])
                embed.add_field(name="التكتات المفتوحة", value=ticket_list, inline=False)
            
            await interaction.response.send_message(embed=embed, ephemeral=True)
        except Exception as e:
            embed = self.embed_manager.error("❌ خطأ", f"```{str(e)[:100]}```")
            await interaction.response.send_message(embed=embed, ephemeral=True)
    
    @commands.command(name="ticket-close", aliases=["tc"])
    async def ticket_close_prefix(self, ctx):
        """نسخة الـ prefix من إغلاق التكت"""
        try:
            tickets = self.get_tickets()
            user_id = str(ctx.author.id)
            
            if user_id not in tickets:
                embed = self.embed_manager.error("❌ خطأ", "أنت لا تملك أي تكت مفتوح")
                await ctx.send(embed=embed)
                return
            
            channel_id = tickets[user_id]["channel_id"]
            channel = ctx.guild.get_channel(channel_id)
            
            if channel:
                await channel.delete()
            
            del tickets[user_id]
            self.save_tickets(tickets)
            
            embed = self.embed_manager.success("✅ تم إغلاق التكت", "تم حذف قناة التكت بنجاح")
            await ctx.send(embed=embed)
        except Exception as e:
            embed = self.embed_manager.error("❌ خطأ", f"```{str(e)[:100]}```")
            await ctx.send(embed=embed)


async def setup(bot):
    await bot.add_cog(Tickets(bot))
