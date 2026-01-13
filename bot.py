import os
import discord
from discord.ext import commands

# ===== CONFIG =====
# Pull token from Render environment variable
TOKEN = os.getenv("TOKEN")

if not TOKEN:
    raise ValueError("ERROR: No TOKEN found. Did you set it in Render environment variables?")

# Your Discord channel IDs
WELCOME_CHANNEL_ID = 1367850216459599965  # Where the welcome message goes
APPLY_CHANNEL_ID = 1368138036071763968    # #apply channel

# ===== INTENTS =====
intents = discord.Intents.default()
intents.members = True          # Required to detect new members
intents.message_content = True  # Required to read commands

# ===== BOT SETUP =====
bot = commands.Bot(command_prefix="!", intents=intents)

# ===== EVENTS =====
@bot.event
async def on_ready():
    print(f"EP Bot online as {bot.user}")
    print("✅ Bot token successfully loaded from environment variable.")

# ===== AUTO-WELCOME =====
@bot.event
async def on_member_join(member):
    try:
        welcome_channel = bot.get_channel(WELCOME_CHANNEL_ID)
        apply_channel = bot.get_channel(APPLY_CHANNEL_ID)
        if welcome_channel and apply_channel:
            await welcome_channel.send(
                f"Welcome {member.mention} to **Eternal Phoenix**!\n"
                f"Open a ticket in {apply_channel.mention}"
            )
            print(f"DEBUG: Welcome message sent to {member}")
        else:
            print("ERROR: Channels not found.")
    except Exception as e:
        print(f"ERROR: Failed to send welcome message: {e}")

# ===== COMMANDS =====
@bot.command()
async def ping(ctx):
    await ctx.send("🜂 Bot is alive.")

# ===== RUN BOT =====
bot.run(TOKEN)
