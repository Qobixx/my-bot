import discord
from discord.ext import commands
from discord.ui import Button, View, Modal, TextInput
import os
from dotenv import load_dotenv

# .env-Datei laden und Token holen
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

# Direkt im Code
FORUM_CHANNEL_ID = 1468258804226330764  # Forum-Channel ID
TAG_ID_OPENED = 1468259772339065071     # Tag-ID für "opened"

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="$", intents=intents)


class SuggestionModal(Modal):
    def __init__(self, forum_channel):
        super().__init__(title="Neue Suggestion")
        self.forum_channel = forum_channel

        self.title_input = TextInput(label="Titel", placeholder="Titel der Suggestion")
        self.description_input = TextInput(
            label="Beschreibung", style=discord.TextStyle.paragraph, placeholder="Beschreibung eingeben"
        )
        self.image_url_input = TextInput(label="Bild-URL", required=False, placeholder="Optional: Bild-URL")

        self.add_item(self.title_input)
        self.add_item(self.description_input)
        self.add_item(self.image_url_input)

    async def on_submit(self, interaction: discord.Interaction):
        embed = discord.Embed(
            title=self.title_input.value,
            description=self.description_input.value,
            color=discord.Color.blue()
        )
        if self.image_url_input.value:
            embed.set_image(url=self.image_url_input.value)

        # Forum-Post erstellen
        post = await self.forum_channel.create_post(
            name=self.title_input.value,
            embed=embed,
            applied_tags=[TAG_ID_OPENED]  # Tag automatisch setzen
        )

        await interaction.response.send_message("Deine Suggestion wurde gepostet!", ephemeral=True)


class SuggestionView(View):
    @discord.ui.button(label="Suggest", style=discord.ButtonStyle.primary)
    async def suggest_button(self, interaction: discord.Interaction, button: Button):
        forum_channel = bot.get_channel
