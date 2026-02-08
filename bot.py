import discord
from discord.ext import commands
from dotenv import load_dotenv
import os

# .env-Datei laden
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

# Hier deine Forum-Channel-ID einfügen
FORUM_CHANNEL_ID = 1468258804226330764  # <--- ersetzen
# Vordefinierte Tags
FORUM_TAGS = ["Open"]

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="$", intents=intents)

# ---------------- Modal für Suggestion ----------------
class SuggestionModal(discord.ui.Modal, title="Neue Suggestion"):
    title_input = discord.ui.TextInput(label="Titel", placeholder="Gib hier den Titel ein", max_length=100)
    description_input = discord.ui.TextInput(label="Beschreibung", style=discord.TextStyle.paragraph, placeholder="Beschreibe deine Suggestion hier...")
    image_url_input = discord.ui.TextInput(label="Bild URL (optional)", required=False, placeholder="https://...")

    def __init__(self, forum_channel: discord.ForumChannel):
        super().__init__()
        self.forum_channel = forum_channel

    async def on_submit(self, interaction: discord.Interaction):
        # Erstelle Embed
        embed = discord.Embed(title=self.title_input.value, description=self.description_input.value, color=discord.Color.blue())
        if self.image_url_input.value:
            embed.set_image(url=self.image_url_input.value)

        # Poste in Forum Channel
        await self.forum_channel.create_post(
            name=self.title_input.value,
            content=self.description_input.value,
            embed=embed,
            tags=FORUM_TAGS
        )

        await interaction.response.send_message("Deine Suggestion wurde gepostet!", ephemeral=True)

# ---------------- Button View ----------------
class SuggestionView(discord.ui.View):
    def __init__(self, forum_channel: discord.ForumChannel):
        super().__init__()
        self.forum_channel = forum_channel

    @discord.ui.button(label="Erstelle Suggestion", style=discord.ButtonStyle.primary)
    async def suggestion_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        modal = SuggestionModal(self.forum_channel)
        await interaction.response.send_modal(modal)

# ---------------- Events & Commands ----------------
@bot.event
async def on_ready():
    print(f"Eingeloggt als {bot.user}")

@bot.command()
async def button_suggest(ctx):
    forum_channel = bot.get_channel(FORUM_CHANNEL_ID)
    if not isinstance(forum_channel, discord.ForumChannel):
        await ctx.send("Fehler: Der Channel ist kein Forum-Channel!")
        return

    view = SuggestionView(forum_channel)
    await ctx.send("Klicke auf den Button, um eine Suggestion zu erstellen:", view=view)

bot.run(TOKEN)
