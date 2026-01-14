import discord
from discord.ext import commands
import os

# ===== CONFIG =====
# These channel IDs are already provided by you
WELCOME_CHANNEL_ID = 1367850216459599965  # Welcome channel
APPLY_CHANNEL_ID = 1368138036071763968    # Apply channel

# Your Discord User ID (to be mentioned)
OWNER_ID = 933323420714827777

# Token from Render Environment Variables
TOKEN = os.getenv("TOKEN")

if not TOKEN:
    raise RuntimeError("TOKEN not found. Set it in Render Environment Variables.")

# ===== INTENTS =====
intents = discord.Intents.default()
intents.members = True
intents.message_content = True

# ===== BOT SETUP =====
bot = commands.Bot(command_prefix="!", intents=intents)

# ===== EVENTS =====
@bot.event
async def on_ready():
    print(f"🜂 Bot online as {bot.user}")

@bot.event
async def on_member_join(member):
    channel = bot.get_channel(WELCOME_CHANNEL_ID)
    apply_channel = bot.get_channel(APPLY_CHANNEL_ID)

    if channel and apply_channel:
        await channel.send(
            f"Welcome {member.mention} to **Eternal Phoenix** 🜂\n"
            f"Please proceed to {apply_channel.mention} to complete your application."
        )

@bot.event
async def on_member_remove(member):
    channel = bot.get_channel(WELCOME_CHANNEL_ID)
    owner = bot.get_user(OWNER_ID)

    if channel and owner:
        await channel.send(
            f"{owner.mention} — **{member.name}** left the server. Loser detected 🜂"
        )

# ===== COMMANDS =====
@bot.command()
async def ping(ctx):
    await ctx.send("🜂 Eternal Phoenix systems online.")

# ===== RUN BOT =====
bot.run(TOKEN)
