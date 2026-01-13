import discord
from discord.ext import commands
import requests
import os

# ===== CONFIG =====
TOKEN = os.getenv("TOKEN")

WELCOME_CHANNEL_ID = 1367850216459599965
APPLY_CHANNEL_ID = 1368138036071763968

DISCORD_ID = 1426437331291734118
NATION_ID = 726130
PNW_API_KEY = "cfe0cf1ff736684026e2"

# ===== INTENTS =====
intents = discord.Intents.default()
intents.members = True
intents.message_content = True

# ===== BOT SETUP =====
bot = commands.Bot(command_prefix="!", intents=intents)

# ===== EVENTS =====
@bot.event
async def on_ready():
    print(f"EP Bot online as {bot.user}")

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
    except Exception as e:
        print(f"ERROR sending welcome: {e}")

# ===== HELPER FUNCTION =====
def should_respond(ctx, command_name):
    """Return True if bot should respond to a command"""
    message = ctx.message.content.lower()
    # Slash command or bot mention + !command
    return (
        message.startswith(f"/{command_name}") or
        (bot.user in ctx.message.mentions and message.startswith(f"!{command_name}"))
    )

# ===== COMMANDS =====
@bot.command()
async def ping(ctx):
    if should_respond(ctx, "ping"):
        await ctx.send("🜂 Bot is alive.")

@bot.command()
async def who(ctx, user: discord.User = None):
    if not should_respond(ctx, "who"):
        return

    try:
        if user is None or user.id == DISCORD_ID:
            nation_id = NATION_ID
        else:
            nation_id = NATION_ID  # Placeholder for other users

        query = f"""
        {{
          nations(id: {nation_id}) {{
            nation_name
            balance
            population
            networth
            land
            is_vacation
          }}
        }}
        """
        headers = {"X-Api-Key": PNW_API_KEY}
        response = requests.post("https://api.politicsandwar.com/graphql", json={"query": query}, headers=headers)
        data = response.json()
        nation = data.get("data", {}).get("nations", [{}])[0]

        if nation:
            await ctx.send(
                f"📊 Nation Info for {nation.get('nation_name')}:\n"
                f"💰 Balance: {nation.get('balance')}\n"
                f"🌍 Land: {nation.get('land')}\n"
                f"👥 Population: {nation.get('population')}\n"
                f"🏛️ Networth: {nation.get('networth')}\n"
                f"🛡 Vacation Mode: {nation.get('is_vacation')}"
            )
        else:
            await ctx.send("❌ Could not fetch nation data.")
    except Exception as e:
        await ctx.send(f"❌ Error fetching nation info: {e}")

# ===== RUN BOT =====
bot.run(TOKEN)
