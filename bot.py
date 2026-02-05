import discord
from discord.ext import commands

TOKEN = "MTQ2OTA5NDMyODY5NjgzNjM3MQ.G3np4j.28-SL8SG2c6Hdbp18_zN8bY33YdWWjOyySY2tk"

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="$", intents=intents)

class MyView(discord.ui.View):
    @discord.ui.button(label="Klick mich", style=discord.ButtonStyle.primary)
    async def button_callback(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message("Button gedrückt!", ephemeral=True)

@bot.event
async def on_ready():
    print(f"Eingeloggt als {bot.user}")

@bot.command()
async def button(ctx):
    await ctx.send("Hier ist dein Button:", view=MyView())

bot.run(TOKEN)
