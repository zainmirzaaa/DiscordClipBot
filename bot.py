import discord
from discord.ext import commands
import requests

@bot.command()
async def transcribe(ctx, url: str):
    """Send an audio URL to transcription microservice."""
    res = requests.post("http://localhost:5001/transcribe",
                        json={"audio_url": url})
    if res.ok:
        data = res.json()
        await ctx.send(f"Transcript: {data['transcript']}")
    else:
        await ctx.send("Transcription failed.")


intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"Bot is online as {bot.user}")

@bot.command()
async def ping(ctx):
    await ctx.send("pong!")

if __name__ == "__main__":
    bot.run("YOUR_DISCORD_BOT_TOKEN")
