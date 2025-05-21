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

@bot.command()
async def auto_highlight(ctx, url: str):
    """Fetch transcript + highlights from backend."""
    res = requests.post("http://localhost:5001/transcribe",
                        json={"audio_url": url})
    if not res.ok:
        return await ctx.send("Transcription failed.")

    transcript = res.json()["transcript"]
    res2 = requests.post("http://localhost:5001/highlight",
                         json={"transcript": transcript})
    picks = res2.json().get("highlights", [])
    await ctx.send("Highlights:\n" + "\n".join([f"- {h}" for h in picks]))

@bot.command()
async def transcripts(ctx):
    res = requests.get("http://localhost:5001/all")
    if res.ok:
        docs = res.json().get("items", [])
        msg = "\n".join([f"{i+1}. {d['url']}" for i, d in enumerate(docs)])
        await ctx.send("Saved transcripts:\n" + msg)
    else:
        await ctx.send("Could not fetch transcripts.")


@bot.command()
async def addclip(ctx, link: str):
    payload = {"id": "botclip", "link": link}
    res = requests.post("http://localhost:8080/clip", json=payload)
    if res.ok:
        await ctx.send("Clip saved ✅")
    else:
        await ctx.send("Failed to save clip ❌")


@bot.command()
async def searchtext(ctx, *, keyword: str):
    res = requests.get(f"http://localhost:5001/search?q={keyword}")
    if res.ok:
        hits = res.json().get("results", [])
        msg = "\n".join([f"{i+1}. {h['url']}" for i, h in enumerate(hits)])
        await ctx.send("Matches:\n" + msg if hits else "No matches found.")
    else:
        await ctx.send("Search failed.")
