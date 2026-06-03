import discord
from discord.ext import commands
from discord import app_commands
from main import EmbedManager
import random

class Fun(commands.Cog):
    """نظام الترفيه والألعاب"""
    
    def __init__(self, bot):
        self.bot = bot
        self.embed_manager = EmbedManager()
    
    @app_commands.command(name="8ball", description="كرة السحر")
    async def eightball(self, interaction: discord.Interaction, question: str):
        """كرة السحر"""
        try:
            answers = [
                "نعم، بكل تأكيد ✅",
                "لا، أبداً ❌",
                "قد يكون 🤷",
                "بالتأكيد! 🎯",
                "غير محتمل 😕",
                "نعم، سيحدث بسرعة ⚡",
                "لا يبدو جيداً 😞",
                "قد تحتاج لانتظار أطول ⏳",
            ]
            
            answer = random.choice(answers)
            
            embed = self.embed_manager.info(
                "🔮 كرة السحر",
                f"**السؤال**: {question}\n"
                f"**الإجابة**: {answer}"
            )
            
            await interaction.response.send_message(embed=embed, ephemeral=False)
        except Exception as e:
            embed = self.embed_manager.error("❌ خطأ", f"```{str(e)[:100]}```")
            await interaction.response.send_message(embed=embed, ephemeral=True)
    
    @app_commands.command(name="roll", description="رمي نرد")
    async def roll_dice(self, interaction: discord.Interaction, max_num: int = 6):
        """رمي نرد"""
        try:
            result = random.randint(1, max_num)
            
            embed = self.embed_manager.success(
                "🎲 رمي النرد",
                f"**النتيجة**: {result} من {max_num}"
            )
            
            await interaction.response.send_message(embed=embed, ephemeral=False)
        except Exception as e:
            embed = self.embed_manager.error("❌ خطأ", f"```{str(e)[:100]}```")
            await interaction.response.send_message(embed=embed, ephemeral=True)
    
    @app_commands.command(name="coinflip", description="قلب عملة")
    async def coinflip(self, interaction: discord.Interaction):
        """قلب عملة"""
        try:
            result = random.choice(["صورة 🪙", "كتابة 📜"])
            
            embed = self.embed_manager.success(
                "💰 قلب العملة",
                f"**النتيجة**: {result}"
            )
            
            await interaction.response.send_message(embed=embed, ephemeral=False)
        except Exception as e:
            embed = self.embed_manager.error("❌ خطأ", f"```{str(e)[:100]}```")
            await interaction.response.send_message(embed=embed, ephemeral=True)
    
    @app_commands.command(name="rps", description="حجر ورقة مقص")
    async def rock_paper_scissors(self, interaction: discord.Interaction, choice: str):
        """حجر ورقة مقص"""
        try:
            valid_choices = ["حجر", "ورقة", "مقص", "rock", "paper", "scissors"]
            
            if choice.lower() not in valid_choices:
                embed = self.embed_manager.error(
                    "❌ خطأ",
                    "اختيارات صحيحة: حجر، ورقة، مقص"
                )
                await interaction.response.send_message(embed=embed, ephemeral=True)
                return
            
            bot_choice = random.choice(["حجر", "ورقة", "مقص"])
            
            if choice.lower() in ["حجر", "rock"]:
                user_choice = "حجر"
            elif choice.lower() in ["ورقة", "paper"]:
                user_choice = "ورقة"
            else:
                user_choice = "مقص"
            
            if user_choice == bot_choice:
                result = "تعادل 🤝"
            elif (user_choice == "حجر" and bot_choice == "مقص") or \
                 (user_choice == "ورقة" and bot_choice == "حجر") or \
                 (user_choice == "مقص" and bot_choice == "ورقة"):
                result = "فزت! 🎉"
            else:
                result = "خسرت 😢"
            
            embed = self.embed_manager.info(
                "🎮 حجر ورقة مقص",
                f"**اختيارك**: {user_choice}\n"
                f"**اختياري**: {bot_choice}\n"
                f"**النتيجة**: {result}"
            )
            
            await interaction.response.send_message(embed=embed, ephemeral=False)
        except Exception as e:
            embed = self.embed_manager.error("❌ خطأ", f"```{str(e)[:100]}```")
            await interaction.response.send_message(embed=embed, ephemeral=True)
    
    @app_commands.command(name="joke", description="نكتة عشوائية")
    async def joke(self, interaction: discord.Interaction):
        """نكتة"""
        try:
            jokes = [
                "لماذا الموز أصفر؟ لأنه لم يكن أحمر! 🍌",
                "ما الفرق بين السيارة والبرتقالة؟ اللون! 🚗🍊",
                "كم بيدك؟ 10 أصابع! 🖐️",
                "لماذا تحب الدجاجة الطريق؟ لأنها تحب العبور! 🐔",
                "ما اسم أطول فنان موسيقي؟ الموجة الطويلة! 🎵",
            ]
            
            joke_text = random.choice(jokes)
            
            embed = self.embed_manager.success(
                "😂 نكتة عشوائية",
                joke_text
            )
            
            await interaction.response.send_message(embed=embed, ephemeral=False)
        except Exception as e:
            embed = self.embed_manager.error("❌ خطأ", f"```{str(e)[:100]}```")
            await interaction.response.send_message(embed=embed, ephemeral=True)
    
    @app_commands.command(name="say", description="البوت يقول رسالة")
    async def say(self, interaction: discord.Interaction, message: str):
        """البوت يقول رسالة"""
        try:
            embed = self.embed_manager.info(
                f"💬 {interaction.user.name} يقول",
                message
            )
            
            await interaction.response.send_message(embed=embed, ephemeral=False)
        except Exception as e:
            embed = self.embed_manager.error("❌ خطأ", f"```{str(e)[:100]}```")
            await interaction.response.send_message(embed=embed, ephemeral=True)
    
    @app_commands.command(name="pp", description="قياس عشوائي 😆")
    async def pp_command(self, interaction: discord.Interaction, user: discord.Member = None):
        """قياس مضحك"""
        try:
            if user is None:
                user = interaction.user
            
            size = random.randint(1, 20)
            bar = "=" * size
            
            embed = self.embed_manager.success(
                f"📏 قياس {user.name}",
                f"[{bar}]\n**الحجم**: {size}%"
            )
            
            await interaction.response.send_message(embed=embed, ephemeral=False)
        except Exception as e:
            embed = self.embed_manager.error("❌ خطأ", f"```{str(e)[:100]}```")
            await interaction.response.send_message(embed=embed, ephemeral=True)
    
    @app_commands.command(name="iq", description="اختبار الذكاء 🧠")
    async def iq_command(self, interaction: discord.Interaction, user: discord.Member = None):
        """اختبار ذكاء"""
        try:
            if user is None:
                user = interaction.user
            
            iq = random.randint(1, 200)
            
            if iq > 150:
                description = "عبقري جداً! 🧠✨"
            elif iq > 100:
                description = "ذكي جداً! 🧠"
            elif iq > 70:
                description = "متوسط الذكاء 🤔"
            else:
                description = "قد تحتاج لبعض الوقت 😄"
            
            embed = self.embed_manager.success(
                f"🧠 اختبار ذكاء {user.name}",
                f"**النتيجة**: {iq} IQ\n**الوصف**: {description}"
            )
            
            await interaction.response.send_message(embed=embed, ephemeral=False)
        except Exception as e:
            embed = self.embed_manager.error("❌ خطأ", f"```{str(e)[:100]}```")
            await interaction.response.send_message(embed=embed, ephemeral=True)
    
    @commands.command(name="joke", aliases=["j"])
    async def joke_prefix(self, ctx):
        """نكتة (prefix version)"""
        try:
            jokes = [
                "لماذا الموز أصفر؟ لأنه لم يكن أحمر! 🍌",
                "ما الفرق بين السيارة والبرتقالة؟ اللون! 🚗🍊",
            ]
            
            embed = self.embed_manager.success("😂 نكتة", random.choice(jokes))
            await ctx.send(embed=embed)
        except Exception as e:
            embed = self.embed_manager.error("❌ خطأ", f"```{str(e)[:100]}```")
            await ctx.send(embed=embed)


async def setup(bot):
    await bot.add_cog(Fun(bot))
