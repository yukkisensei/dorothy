"""
Dorothy Bot - Main Entry Point
Discord security bot with AI features
Version 3.0
"""

import sys
import io

# Fix Windows console encoding for Unicode characters
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

# Check Python version - require 3.12.x
if sys.version_info < (3, 12, 0) or sys.version_info >= (3, 13, 0):
    detected = f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
    raise RuntimeError(
        "Dorothy bot requires Python 3.12.x (tested on 3.12.10). "
        f"Detected Python {detected}. Please install Python 3.12.10."
    )

if sys.version_info[:3] != (3, 12, 10):
    detected = f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
    try:
        print(
            "⚠️  Dorothy bot is validated on Python 3.12.10. "
            f"Current interpreter is {detected}. Consider switching to 3.12.10 for stability"
        )
    except UnicodeEncodeError:
        print(
            "[WARNING] Dorothy bot is validated on Python 3.12.10. "
            f"Current interpreter is {detected}. Consider switching to 3.12.10 for stability"
        )

import discord
import os
from discord.ext import commands
from dotenv import load_dotenv

# Import modules
from config import PREFIX, OWNER_IDS, BOT_NAME, VERSION, DISCORD_BOT_TOKEN
from database import DataManager
from security import SecurityManager
import moderation
import info_commands
import security_commands
import doro_ai
import events

# ==================== BOT INITIALIZATION ====================
def get_prefix(bot, message):
    """Dynamic prefix function"""
    if message.guild:
        return data_manager.get_prefix(message.guild.id)
    return PREFIX

# Initialize intents
intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.moderation = True

# Initialize bot
bot = commands.Bot(command_prefix=get_prefix, intents=intents, help_command=None)

# Initialize data manager
data_manager = DataManager()

# Initialize security manager
security_manager = SecurityManager(bot, data_manager)

# ==================== SETUP MODULES ====================
def setup_bot():
    """Setup all bot modules and commands"""
    try:
        print("🔧 Initializing modules...")
    except UnicodeEncodeError:
        print("[INFO] Initializing modules...")
    
    # Setup moderation module
    moderation.setup_moderation(data_manager)
    moderation.setup_commands(bot)
    
    # Initialize modules
    config.init_config()
    database.init_database(data_manager)
    security.init_security(data_manager)
    moderation.init_moderation(data_manager)
    utils.init_utils(data_manager)
    info_commands.init_info_commands(data_manager)
    security_commands.init_security_commands(data_manager)
    doro_ai.init_doro_ai()
    
    events.setup_events(bot, data_manager, security_manager)
    
    try:
        print("✅ All modules initialized!")
    except UnicodeEncodeError:
        print("[OK] All modules initialized!")

# ==================== RUN BOT ====================
if __name__ == "__main__":
    # Load environment variables
    load_dotenv()
    
    TOKEN = os.getenv('DISCORD_BOT_TOKEN')
    if not TOKEN:
        raise ValueError("Missing DISCORD_BOT_TOKEN in .env file")
    
    # Print startup info
    try:
        print(f"🚀 Starting {BOT_NAME} v{VERSION}...")
        print(f"👑 Owner IDs: {OWNER_IDS}")
    except UnicodeEncodeError:
        print(f"[INFO] Starting {BOT_NAME} v{VERSION}...")
        print(f"[INFO] Owner IDs: {OWNER_IDS}")
    
    # Setup bot modules
    setup_bot()
    
    # Run bot
    try:
        bot.run(TOKEN)
    except Exception as e:
        try:
            print(f"❌ Error: {e}")
        except UnicodeEncodeError:
            print(f"[ERROR] {e}")
