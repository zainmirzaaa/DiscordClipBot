import discord
from discord.ext import commands
import requests
from llama_agent import highlight_clips

@bot.command()
async def highlight(ctx, *, text: str):
    """Run transcript text through LLaMA stub for highlights."""
    picks = highlight_clips(text)
    msg = "\n".join([f"- {p}" for p in picks])
    await ctx.send(f"Highlights:\n{msg}")


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

@bot.command()
async def clips(ctx):
    res = requests.get("http://localhost:8080/clips")
    if res.ok:
        data = res.json()
        links = "\n".join([c["link"] for c in data])
        await ctx.send(f"Available Clips:\n{links}")
    else:
        await ctx.send("Failed to fetch clips.")
