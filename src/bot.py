from dotenv import load_dotenv
import os
import discord
from discord.ext import commands

from db import init_db, add_user_to_db, get_all_users, remove_user_from_db

# Init DB
init_db()

# Load token
load_dotenv()
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')

# Bot setup
intents = discord.Intents.default()
intents.message_content = True
intents.members = True
bot = commands.Bot(command_prefix='RP!', intents=intents)


# ---------------------------
# ADD USER
# ---------------------------

@bot.command(name='add_user')
async def add_user(ctx, member: discord.Member = None, name: str = None):
    if member is None:
        await ctx.send("Please mention a valid Discord user.")
        return

    if name is None:
        await ctx.send("Please provide a name.")
        return

    user_id = str(member.id)

    users = get_all_users()
    for user in users:
        if user["id"] == user_id:
            await ctx.send(f"{member.mention} is already in the championship as **{user['name']}**.")
            return

    try:
        add_user_to_db(user_id, name)
        await ctx.send(f"{name} ({member.mention}) has been added to the championship!")
    except Exception as e:
        await ctx.send(f"Error adding user: {e}")


# ---------------------------
# REMOVE USER
# ---------------------------

@bot.command(name='remove_user')
async def remove_user(ctx):
    users = get_all_users()

    if not users:
        await ctx.send("No users found in the championship.")
        return

    message = "What user to delete from the championship:\n"

    for i, user in enumerate(users, start=1):
        discord_id = user['id']

        try:
            member = await ctx.guild.fetch_member(discord_id)
            mention = member.mention
        except discord.NotFound:
            mention = "(not in server)"
        except:
            mention = "(unknown)"

        message += f"{i}. {user['name']} / {mention}\n"

    await ctx.send(message)

    def check(msg):
        return msg.author == ctx.author and msg.channel == ctx.channel

    try:
        response = await bot.wait_for('message', check=check, timeout=30)
        index = int(response.content) - 1

        if index < 0 or index >= len(users):
            await ctx.send("Invalid index. Please try again.")
            return

        user_to_remove = users[index]
        remove_user_from_db(user_to_remove['id'])

        await ctx.send(f"User {user_to_remove['name']} has been removed from the championship!")

    except ValueError:
        await ctx.send("Please enter a valid number.")
    except Exception:
        await ctx.send(f"Error removing user")


# ---------------------------
# OTHER COMMANDS
# ---------------------------

@bot.command(name='upload_letterboxd')
async def upload_letterboxd(ctx, username: str, letterboxd_url: str):
    await ctx.send(f"Letterboxd URL for user {username} has been uploaded: {letterboxd_url}")


@bot.command(name='scoreboard')
async def scoreboard(ctx):
    await ctx.send("Here's the current scoreboard!")


@bot.command(name='finals')
async def finals(ctx):
    await ctx.send("The finals are coming up soon!")


# Start bot
bot.run(DISCORD_TOKEN)