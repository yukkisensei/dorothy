import sys
import io

# Fix Windows console encoding for Unicode characters
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

# Check Python version - require 3.12.10
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
import json
import os
import asyncio
import random
import aiohttp
from datetime import datetime, timedelta
from discord.ext import commands, tasks
from discord import app_commands
from typing import Optional, Dict, List

# ==================== CONFIGURATION ====================
BOT_NAME = "DoSecurity"
PREFIX = "-"

# Load owner ID từ env với default
default_owner_id = "1344312732278591500"  # ID Discord của bạn
owner_id_str = os.getenv('BOT_OWNER_IDS', os.getenv('OWNER_ID', default_owner_id))

# Support nhiều owner IDs nếu cần
if ',' in owner_id_str:
    OWNER_IDS = [int(x.strip()) for x in owner_id_str.split(',') if x.strip().isdigit()]
    OWNER_ID = OWNER_IDS[0] if OWNER_IDS else int(default_owner_id)
else:
    OWNER_ID = int(owner_id_str) if owner_id_str.isdigit() else int(default_owner_id)
    OWNER_IDS = [OWNER_ID]

print(f"👑 Dorothy Owner ID loaded: {OWNER_ID}")
print(f"👑 All Owner IDs: {OWNER_IDS}")

# NVIDIA API config - load from env
NVIDIA_API_KEY = os.getenv('NVIDIA_API_KEY', '')  # Load from env, don't hardcode!
NVIDIA_API_URL = "https://integrate.api.nvidia.com/v1/chat/completions"

# Doro response patterns
doro_patterns = {
    "happy": ["doro!", "doro doro!", "doro~!", "doro doro~"],
    "sad": ["doro...", "...doro...", "doro……"],
    "confused": ["doro?", "doro doro?", "...doro?", "doro??"],
    "angry": ["doro!!", "DORO!", "doro doro!!"],
    "scared": ["do...doro...", "doro...!", "do do..."],
    "excited": ["doro doro!", "doro~!", "doro!! doro!!"],
    "neutral": ["doro", "doro~", "doro doro", "doro?"],
    "apologetic": ["doro do...", "do...doro...", "doro... doro..."],
    "sleepy": ["do...ro...", "doro... zzz...", "...doro..."],
    "curious": ["doro?", "doro doro?", "do? doro?"]
}

doro_actions = {
    "happy": ["*Dorothy nhảy nhót vui vẻ*", "*Dorothy vẫy tay hào hứng*", "*Dorothy cười toe toét*"],
    "sad": ["*Dorothy cúi đầu buồn bã*", "*Dorothy lau nước mắt*", "*Dorothy trông có vẻ buồn*"],
    "confused": ["*Dorothy nghiêng đầu*", "*Dorothy nhìn bạn chằm chằm*", "*Dorothy có vẻ bối rối*"],
    "angry": ["*Dorothy phồng má*", "*Dorothy giậm chân*", "*Dorothy trông có vẻ khó chịu*"],
    "scared": ["*Dorothy run rẩy*", "*Dorothy lùi lại*", "*Dorothy ẩn sau lưng bạn*"],
    "excited": ["*Dorothy nhảy lên*", "*Dorothy vỗ tay*", "*Dorothy quay tròn*"],
    "neutral": ["*Dorothy đứng yên*", "*Dorothy nhìn bạn*", "*Dorothy lắng nghe*"],
    "apologetic": ["*Dorothy cúi đầu xin lỗi*", "*Dorothy trông có lỗi*", "*Dorothy nhìn xuống đất*"],
    "sleepy": ["*Dorothy ngáp*", "*Dorothy dụi mắt*", "*Dorothy gục đầu*"],
    "curious": ["*Dorothy nhìn chăm chú*", "*Dorothy tiến lại gần*", "*Dorothy mắt sáng lên*"]
}

# Warning system configuration
WARNING_LEVELS = {
    1: {"action": "none", "duration": 0, "message": "⚠️ Cảnh báo lần 1: Vui lòng tuân thủ quy định!"},
    2: {"action": "none", "duration": 0, "message": "⚠️ Cảnh báo lần 2: Cẩn thận với hành vi của bạn!"},
    3: {"action": "none", "duration": 0, "message": "⚠️ Cảnh báo lần 3: Đây là lần cảnh báo cuối cùng!"},
    4: {"action": "timeout", "duration": 5, "message": "🔇 Cảnh báo lần 4: Bạn bị mute 5 phút!"},
    5: {"action": "timeout", "duration": 30, "message": "🔇 Cảnh báo lần 5: Bạn bị mute 30 phút!"},
    6: {"action": "timeout", "duration": 60, "message": "🔇 Cảnh báo lần 6: Bạn bị mute 1 giờ!"},
    7: {"action": "timeout", "duration": 180, "message": "🔇 Cảnh báo lần 7: Bạn bị mute 3 giờ!"},
    8: {"action": "kick", "duration": 0, "message": "👢 Cảnh báo lần 8: Bạn bị kick khỏi server!"},
    9: {"action": "ban", "duration": 0, "message": "🔨 Cảnh báo lần 9: Bạn bị ban 1 ngày!"},
    10: {"action": "ban", "duration": 0, "message": "🔨 Cảnh báo lần 10: Bạn bị ban vĩnh viễn!"}
}

# ==================== DATA MANAGEMENT ====================
class DataManager:
    def __init__(self, filename="security_data.json"):
        self.filename = filename
        self.data = self.load_data()
    
    def load_data(self):
        if os.path.exists(self.filename):
            with open(self.filename, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {"warnings": {}, "kicks": {}, "bans": {}, "mutes": {}}
    
    def save_data(self):
        with open(self.filename, 'w', encoding='utf-8') as f:
            json.dump(self.data, f, ensure_ascii=False, indent=2)
    
    def add_warning(self, guild_id: str, user_id: str):
        guild_id, user_id = str(guild_id), str(user_id)
        if guild_id not in self.data["warnings"]:
            self.data["warnings"][guild_id] = {}
        if user_id not in self.data["warnings"][guild_id]:
            self.data["warnings"][guild_id][user_id] = []
        
        warning_entry = {
            "timestamp": datetime.now().isoformat(),
            "count": len(self.data["warnings"][guild_id][user_id]) + 1
        }
        self.data["warnings"][guild_id][user_id].append(warning_entry)
        self.save_data()
        return len(self.data["warnings"][guild_id][user_id])
    
    def get_warnings(self, guild_id: str, user_id: str):
        guild_id, user_id = str(guild_id), str(user_id)
        if guild_id in self.data["warnings"] and user_id in self.data["warnings"][guild_id]:
            return len(self.data["warnings"][guild_id][user_id])
        return 0
    
    def clear_warnings(self, guild_id: str, user_id: str):
        guild_id, user_id = str(guild_id), str(user_id)
        if guild_id in self.data["warnings"] and user_id in self.data["warnings"][guild_id]:
            del self.data["warnings"][guild_id][user_id]
            self.save_data()
            return True
        return False

# ==================== BOT SETUP ====================
intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.moderation = True

bot = commands.Bot(command_prefix=PREFIX, intents=intents, help_command=None)
data_manager = DataManager()

# ==================== DORO AI FUNCTIONS ====================
async def analyze_sentiment(message: str) -> str:
    """Analyze message sentiment using NVIDIA API or fallback"""
    try:
        # Try NVIDIA API first
        prompt = f"""Analyze sentiment of this message and return ONE word:
happy, sad, confused, angry, scared, excited, neutral, apologetic, sleepy, or curious.

Message: "{message}"

Return only the sentiment word."""

        headers = {
            "Authorization": f"Bearer {NVIDIA_API_KEY}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": "meta/llama-3.1-8b-instruct",
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.5,
            "max_tokens": 5
        }
        
        async with aiohttp.ClientSession() as session:
            async with session.post(NVIDIA_API_URL, json=payload, headers=headers, timeout=2) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    sentiment = data['choices'][0]['message']['content'].strip().lower()
                    if sentiment in doro_patterns:
                        return sentiment
    except:
        pass
    
    # Fallback analysis
    return analyze_simple(message)

def analyze_simple(message: str) -> str:
    """Simple keyword-based sentiment analysis"""
    message_lower = message.lower()
    
    if any(word in message_lower for word in ["chết", "đánh", "giết", "ngu", "fuck", "damn"]):
        return "angry"
    elif any(word in message_lower for word in ["buồn", "khóc", "sad", "cry"]):
        return "sad"
    elif any(word in message_lower for word in ["sợ", "ma", "scared", "afraid"]):
        return "scared"
    elif any(word in message_lower for word in ["xin lỗi", "sorry"]):
        return "apologetic"
    elif any(word in message_lower for word in ["ngủ", "mệt", "sleep", "tired"]):
        return "sleepy"
    elif any(word in message_lower for word in ["vui", "happy", "haha", "yay"]):
        return "happy"
    elif any(word in message_lower for word in ["wow", "amazing", "tuyệt"]):
        return "excited"
    elif "?" in message:
        return "curious"
    elif "!" in message:
        return "excited"
    else:
        return "neutral"

def generate_doro_response(sentiment: str, include_action: bool = True) -> str:
    """Generate Doro response based on sentiment"""
    sentiment = sentiment if sentiment in doro_patterns else "neutral"
    
    # Choose response pattern
    response = random.choice(doro_patterns[sentiment])
    
    # 20% chance to add action
    if include_action and random.random() < 0.2:
        action = random.choice(doro_actions[sentiment])
        response = f"{response}\n{action}"
    
    return response

# ==================== HELPER FUNCTIONS ====================
def parse_time_string(time_str: str) -> Optional[int]:
    """Parse time string like '1h', '30m', '1h30m' to minutes"""
    import re
    
    time_str = time_str.lower().strip()
    total_minutes = 0
    
    # Match patterns like 1d, 2h, 30m, 45s
    patterns = {
        'd': 1440,  # days to minutes
        'h': 60,    # hours to minutes  
        'm': 1,     # minutes
        's': 1/60   # seconds to minutes
    }
    
    for unit, multiplier in patterns.items():
        match = re.search(f'(\\d+){unit}', time_str)
        if match:
            value = int(match.group(1))
            total_minutes += value * multiplier
    
    # If no patterns matched, try to parse as plain number (assume minutes)
    if total_minutes == 0:
        try:
            total_minutes = int(time_str)
        except ValueError:
            return None
    
    # Cap at 28 days (Discord limit)
    return min(int(total_minutes), 40320)

def format_duration(minutes: int) -> str:
    """Format minutes to readable string"""
    if minutes < 60:
        return f"{minutes} phút"
    elif minutes < 1440:
        hours = minutes // 60
        mins = minutes % 60
        if mins > 0:
            return f"{hours} giờ {mins} phút"
        return f"{hours} giờ"
    else:
        days = minutes // 1440
        remaining = minutes % 1440
        hours = remaining // 60
        if hours > 0:
            return f"{days} ngày {hours} giờ"
        return f"{days} ngày"

def has_mod_permissions():
    def predicate(ctx):
        return (ctx.author == ctx.guild.owner or 
                ctx.author.guild_permissions.manage_messages or 
                ctx.author.guild_permissions.administrator or
                ctx.author.id in OWNER_IDS)
    return commands.check(predicate)

async def send_dm_notification(member: discord.Member, action: str, reason: str, server_name: str, extra_info: str = None):
    """Send DM notification to user about moderation action"""
    try:
        embed = discord.Embed(
            title=f"⚠️ Thông Báo Vi Phạm",
            description=f"Bạn đã bị **{action}** tại server **{server_name}**",
            color=discord.Color.red(),
            timestamp=datetime.now()
        )
        embed.add_field(name="📝 Lý do", value=reason or "Không có lý do", inline=False)
        if extra_info:
            embed.add_field(name="ℹ️ Thông tin thêm", value=extra_info, inline=False)
        embed.set_footer(text="Vui lòng tuân thủ quy định của server")
        
        await member.send(embed=embed)
        return True
    except discord.Forbidden:
        # User has DMs disabled
        return False
    except Exception:
        return False

async def log_moderation_action(ctx, action: str, target: discord.Member, reason: str = None):
    """Log moderation actions to a log channel if exists"""
    log_channel = discord.utils.get(ctx.guild.text_channels, name="mod-log")
    if log_channel:
        embed = discord.Embed(
            title=f"🔒 {action}",
            color=discord.Color.red(),
            timestamp=datetime.now()
        )
        embed.add_field(name="👮 Moderator", value=ctx.author.mention, inline=True)
        embed.add_field(name="👤 Target", value=target.mention, inline=True)
        embed.add_field(name="📝 Lý do", value=reason or "Không có lý do", inline=False)
        embed.set_footer(text=f"ID: {target.id}")
        await log_channel.send(embed=embed)

# ==================== EVENTS ====================
@bot.event
async def on_ready():
    try:
        print(f'✅ {BOT_NAME} đã sẵn sàng!')
        print(f'📊 Đang bảo vệ {len(bot.guilds)} server(s)')
    except UnicodeEncodeError:
        print(f'[OK] {BOT_NAME} is ready!')
        print(f'[OK] Protecting {len(bot.guilds)} server(s)')
    
    # Sync slash commands
    try:
        synced = await bot.tree.sync()
        try:
            print(f'✅ Đã sync {len(synced)} slash command(s)')
        except UnicodeEncodeError:
            print(f'[OK] Synced {len(synced)} slash command(s)')
    except Exception as e:
        try:
            print(f'❌ Lỗi sync commands: {e}')
        except UnicodeEncodeError:
            print(f'[ERROR] Failed to sync commands: {e}')
    
    # Update presence
    update_presence.start()

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    
    # Check if bot is mentioned
    if bot.user.mentioned_in(message) and not message.mention_everyone:
        if bot.user in message.mentions:
            # Get message content without mentions
            content = message.content
            for mention in message.mentions:
                content = content.replace(f'<@{mention.id}>', '').replace(f'<@!{mention.id}>', '')
            content = content.strip()
            
            if not content:
                content = "hello"
            
            # Quick response - no typing indicator for speed
            # Use simple analysis for faster response
            sentiment = analyze_simple(content)
            response = generate_doro_response(sentiment, include_action=False)
            
            await message.channel.send(response)
            return
    
    await bot.process_commands(message)

@tasks.loop(seconds=30)
async def update_presence():
    """Update bot status showing number of servers"""
    activity = discord.Activity(
        type=discord.ActivityType.watching,
        name=f"{len(bot.guilds)} server",
        state="Đang kiểm tra..."
    )
    await bot.change_presence(
        status=discord.Status.do_not_disturb,
        activity=activity
    )

# ==================== WARNING SYSTEM ====================
@bot.command(name='warn', aliases=['w', 'warning'])
@has_mod_permissions()
async def warn_user(ctx, member: discord.Member, *, reason: str = "Không có lý do"):
    """Cảnh báo một thành viên"""
    if member == ctx.author:
        return await ctx.send("❌ Bạn không thể tự cảnh báo chính mình!")
    
    if member.bot:
        return await ctx.send("❌ Không thể cảnh báo bot!")
    
    # Add warning
    warning_count = data_manager.add_warning(ctx.guild.id, member.id)
    
    # Get warning level configuration
    if warning_count in WARNING_LEVELS:
        level_config = WARNING_LEVELS[warning_count]
        
        # Create embed
        embed = discord.Embed(
            title="⚠️ CẢNH BÁO",
            description=level_config["message"],
            color=discord.Color.orange() if warning_count < 6 else discord.Color.red(),
            timestamp=datetime.now()
        )
        embed.add_field(name="👤 Thành viên", value=member.mention, inline=True)
        embed.add_field(name="🔢 Lần cảnh báo", value=f"{warning_count}/10", inline=True)
        embed.add_field(name="📝 Lý do", value=reason, inline=False)
        embed.set_footer(text=f"Moderator: {ctx.author.name}")
        
        await ctx.send(embed=embed)
        
        # Send DM notification to user
        dm_sent = await send_dm_notification(
            member,
            f"cảnh báo lần {warning_count}/10",
            reason,
            ctx.guild.name,
            level_config["message"]
        )
        
        # Apply action based on warning level
        if level_config["action"] == "timeout":
            try:
                duration = timedelta(minutes=level_config["duration"])
                await member.timeout(duration, reason=f"Warning #{warning_count}: {reason}")
                await ctx.send(f"🔇 {member.mention} đã bị mute {level_config['duration']} phút!")
                # Send mute notification
                await send_dm_notification(
                    member,
                    f"mute {level_config['duration']} phút",
                    reason,
                    ctx.guild.name,
                    f"Thời gian mute: {level_config['duration']} phút"
                )
            except discord.Forbidden:
                await ctx.send("❌ Không có quyền timeout thành viên này!")
        
        elif level_config["action"] == "kick":
            try:
                # Send DM before kicking
                await send_dm_notification(
                    member,
                    "kick khỏi server",
                    reason,
                    ctx.guild.name,
                    "Bạn có thể join lại server nếu có invite link"
                )
                await member.kick(reason=f"Warning #{warning_count}: {reason}")
                await ctx.send(f"👢 {member.mention} đã bị kick khỏi server!")
            except discord.Forbidden:
                await ctx.send("❌ Không có quyền kick thành viên này!")
        
        elif level_config["action"] == "ban":
            try:
                # Send DM before banning
                await send_dm_notification(
                    member,
                    "ban vĩnh viễn",
                    reason,
                    ctx.guild.name,
                    "Bạn sẽ không thể join lại server này"
                )
                await member.ban(reason=f"Warning #{warning_count}: {reason}")
                await ctx.send(f"🔨 {member.mention} đã bị ban vĩnh viễn!")
            except discord.Forbidden:
                await ctx.send("❌ Không có quyền ban thành viên này!")
        
        # Log action
        await log_moderation_action(ctx, f"Warning #{warning_count}", member, reason)
    else:
        # Beyond level 7, auto-ban
        try:
            await member.ban(reason=f"Excessive warnings: {warning_count}")
            await ctx.send(f"🔨 {member.mention} đã vượt quá giới hạn cảnh báo và bị ban!")
        except:
            pass

@bot.command(name='warnings', aliases=['warns', 'checkwarn'])
@has_mod_permissions()
async def check_warnings(ctx, member: discord.Member = None):
    """Kiểm tra số lần cảnh báo"""
    member = member or ctx.author
    warning_count = data_manager.get_warnings(ctx.guild.id, member.id)
    
    embed = discord.Embed(
        title="📊 Thống kê cảnh báo",
        color=discord.Color.blue()
    )
    embed.add_field(name="👤 Thành viên", value=member.mention, inline=True)
    embed.add_field(name="⚠️ Số cảnh báo", value=f"{warning_count}/10", inline=True)
    
    if warning_count > 0:
        next_level = min(warning_count + 1, 10)
        next_action = WARNING_LEVELS[next_level]["action"]
        embed.add_field(name="⏭️ Hình phạt tiếp theo", value=next_action.upper(), inline=False)
    
    await ctx.send(embed=embed)

@bot.command(name='clearwarns', aliases=['resetwarns'])
@has_mod_permissions()
async def clear_warnings(ctx, member: discord.Member):
    """Xóa toàn bộ cảnh báo của một thành viên"""
    if data_manager.clear_warnings(ctx.guild.id, member.id):
        await ctx.send(f"✅ Đã xóa toàn bộ cảnh báo của {member.mention}")
        await log_moderation_action(ctx, "Clear Warnings", member, "Reset warnings to 0")
    else:
        await ctx.send(f"ℹ️ {member.mention} không có cảnh báo nào!")

# ==================== TIMEOUT COMMANDS ====================
@bot.command(name='timeout', aliases=['mute'])
@has_mod_permissions()
async def timeout_member(ctx, member: discord.Member, duration: Optional[str] = None, *, reason: Optional[str] = None):
    """Timeout (mute) một thành viên
    Usage: -timeout @user [time] [reason]
    Time formats: 5, 5m, 1h, 2h30m
    """
    # Parse duration
    timeout_minutes = 5  # default
    if duration:
        # Check if duration looks like a time format
        if any(c in duration for c in ['h', 'm', 's', 'd']):
            # Parse time string
            timeout_minutes = parse_time_string(duration)
            if timeout_minutes is None:
                return await ctx.send("❌ Format thời gian không hợp lệ! Dùng: 5m, 1h, 2h30m, etc.")
        else:
            # Try to parse as number
            try:
                timeout_minutes = int(duration)
            except ValueError:
                # It's not a number, treat as reason
                reason = duration if not reason else f"{duration} {reason}"
                timeout_minutes = 5
    if member == ctx.author:
        return await ctx.send("❌ Bạn không thể tự mute chính mình!")
    
    if member.bot:
        return await ctx.send("❌ Không thể mute bot!")
    
    try:
        timeout_duration = timedelta(minutes=timeout_minutes)
        reason = reason or "Không có lý do"
        
        # Send DM before timeout
        await send_dm_notification(
            member,
            f"timeout {format_duration(timeout_minutes)}",
            reason,
            ctx.guild.name,
            f"Thời gian mute: {format_duration(timeout_minutes)}"
        )
        
        await member.timeout(timeout_duration, reason=reason)
        
        embed = discord.Embed(
            title="🔇 TIMEOUT",
            color=discord.Color.orange(),
            timestamp=datetime.now()
        )
        embed.add_field(name="👤 Thành viên", value=member.mention, inline=True)
        embed.add_field(name="⏱️ Thời gian", value=format_duration(timeout_minutes), inline=True)
        embed.add_field(name="📝 Lý do", value=reason, inline=False)
        embed.set_footer(text=f"Moderator: {ctx.author.name}")
        
        await ctx.send(embed=embed)
        await log_moderation_action(ctx, f"Timeout {timeout_minutes}m", member, reason)
    except discord.Forbidden:
        await ctx.send("❌ Không có quyền timeout thành viên này!")

@bot.command(name='to')
@has_mod_permissions()
async def to_alias(ctx, member: discord.Member, duration: Optional[str] = None, *, reason: Optional[str] = None):
    """Alias for timeout command"""
    await timeout_member(ctx, member, duration, reason=reason)

@bot.command(name='untimeout', aliases=['unmute'])
@has_mod_permissions()
async def remove_timeout(ctx, member: discord.Member):
    """Gỡ timeout (unmute) cho thành viên"""
    try:
        await member.timeout(None)
        await ctx.send(f"✅ Đã gỡ timeout cho {member.mention}")
        await log_moderation_action(ctx, "Remove Timeout", member)
    except discord.Forbidden:
        await ctx.send("❌ Không có quyền gỡ timeout cho thành viên này!")

@bot.command(name='rto')
@has_mod_permissions()
async def rto_alias(ctx, member: discord.Member):
    """Alias for untimeout command"""
    await remove_timeout(ctx, member)

# ==================== KICK/BAN COMMANDS ====================
@bot.command(name='kick', aliases=['k'])
@has_mod_permissions()
async def kick_member(ctx, member: discord.Member, *, reason: str = "Không có lý do"):
    """Kick một thành viên khỏi server"""
    if member == ctx.author:
        return await ctx.send("❌ Bạn không thể tự kick chính mình!")
    
    if member.bot:
        return await ctx.send("❌ Không thể kick bot!")
    
    try:
        # Send DM before kicking
        await send_dm_notification(
            member,
            "kick khỏi server",
            reason,
            ctx.guild.name,
            "Bạn có thể join lại server nếu có invite link"
        )
        
        await member.kick(reason=reason)
        
        embed = discord.Embed(
            title="👢 KICK",
            color=discord.Color.orange(),
            timestamp=datetime.now()
        )
        embed.add_field(name="👤 Thành viên", value=f"{member.mention} ({member.id})", inline=True)
        embed.add_field(name="📝 Lý do", value=reason, inline=False)
        embed.set_footer(text=f"Moderator: {ctx.author.name}")
        
        await ctx.send(embed=embed)
        await log_moderation_action(ctx, "Kick", member, reason)
    except discord.Forbidden:
        await ctx.send("❌ Không có quyền kick thành viên này!")

@bot.command(name='ban', aliases=['b'])
@has_mod_permissions()
async def ban_member(ctx, member: discord.Member, *, reason: str = "Không có lý do"):
    """Ban một thành viên khỏi server"""
    if member == ctx.author:
        return await ctx.send("❌ Bạn không thể tự ban chính mình!")
    
    if member.bot:
        return await ctx.send("❌ Không thể ban bot!")
    
    try:
        # Send DM before banning
        await send_dm_notification(
            member,
            "ban vĩnh viễn",
            reason,
            ctx.guild.name,
            "Bạn sẽ không thể join lại server này"
        )
        
        await member.ban(reason=reason)
        
        embed = discord.Embed(
            title="🔨 BAN",
            color=discord.Color.red(),
            timestamp=datetime.now()
        )
        embed.add_field(name="👤 Thành viên", value=f"{member.mention} ({member.id})", inline=True)
        embed.add_field(name="📝 Lý do", value=reason, inline=False)
        embed.set_footer(text=f"Moderator: {ctx.author.name}")
        
        await ctx.send(embed=embed)
        await log_moderation_action(ctx, "Ban", member, reason)
    except discord.Forbidden:
        await ctx.send("❌ Không có quyền ban thành viên này!")

@bot.command(name='unban', aliases=['ub', 'rban'])
@has_mod_permissions()
async def unban_member(ctx, user_id: int, *, reason: str = "Đã được tha thứ"):
    """Unban một thành viên"""
    try:
        user = await bot.fetch_user(user_id)
        await ctx.guild.unban(user, reason=reason)
        
        embed = discord.Embed(
            title="✅ UNBAN",
            color=discord.Color.green(),
            timestamp=datetime.now()
        )
        embed.add_field(name="👤 User", value=f"{user.mention} ({user.id})", inline=True)
        embed.add_field(name="📝 Lý do", value=reason, inline=False)
        embed.set_footer(text=f"Moderator: {ctx.author.name}")
        
        await ctx.send(embed=embed)
    except discord.NotFound:
        await ctx.send("❌ Không tìm thấy user với ID này!")
    except discord.Forbidden:
        await ctx.send("❌ Không có quyền unban!")

# ==================== MODERATION UTILITIES ====================
@bot.command(name='clear', aliases=['purge', 'clean'])
@has_mod_permissions()
async def clear_messages(ctx, amount: int = 10):
    """Xóa tin nhắn trong channel"""
    if amount < 1 or amount > 100:
        return await ctx.send("❌ Số lượng phải từ 1 đến 100!")
    
    deleted = await ctx.channel.purge(limit=amount + 1)
    msg = await ctx.send(f"✅ Đã xóa {len(deleted) - 1} tin nhắn!")
    await asyncio.sleep(3)
    await msg.delete()

@bot.command(name='lock')
@has_mod_permissions()
async def lock_channel(ctx, channel: discord.TextChannel = None):
    """Khóa channel"""
    channel = channel or ctx.channel
    await channel.set_permissions(ctx.guild.default_role, send_messages=False)
    await ctx.send(f"🔒 Channel {channel.mention} đã được khóa!")

@bot.command(name='unlock')
@has_mod_permissions()
async def unlock_channel(ctx, channel: discord.TextChannel = None):
    """Mở khóa channel"""
    channel = channel or ctx.channel
    await channel.set_permissions(ctx.guild.default_role, send_messages=True)
    await ctx.send(f"🔓 Channel {channel.mention} đã được mở khóa!")

@bot.command(name='slowmode', aliases=['slow'])
@has_mod_permissions()
async def set_slowmode(ctx, seconds: int = 0):
    """Đặt slowmode cho channel (0 = tắt)"""
    if seconds < 0 or seconds > 21600:
        return await ctx.send("❌ Slowmode phải từ 0 đến 21600 giây (6 giờ)!")
    
    await ctx.channel.edit(slowmode_delay=seconds)
    if seconds == 0:
        await ctx.send("✅ Đã tắt slowmode!")
    else:
        await ctx.send(f"✅ Đã đặt slowmode: {seconds} giây!")

# ==================== HELP COMMAND ====================
@bot.command(name='help', aliases=['h'])
async def help_command(ctx):
    """Hiển thị menu trợ giúp"""
    embed = discord.Embed(
        title=f"🛡️ {BOT_NAME} - Menu Trợ giúp",
        description="Bot bảo mật chuyên nghiệp với AI Dorothy\n" +
                    "**@DoSecurity [tin nhắn]** - Chat với Dorothy AI (doro doro!)",
        color=discord.Color.blue()
    )
    
    embed.add_field(
        name="⚠️ **Hệ thống Cảnh báo**",
        value=(
            "`-warn @user [lý do]` - Cảnh báo thành viên\n"
            "`-warnings [@user]` - Kiểm tra số cảnh báo\n"
            "`-clearwarns @user` - Xóa cảnh báo\n"
            "**Hệ thống tự động:**\n"
            "• Lần 1-2: Chỉ cảnh báo\n"
            "• Lần 3: Cảnh báo cuối\n"
            "• Lần 4: Mute 5 phút\n"
            "• Lần 5: Mute 30 phút\n"
            "• Lần 6: Mute 1 giờ\n"
            "• Lần 7: Mute 3 giờ\n"
            "• Lần 8: Kick\n"
            "• Lần 9: Ban tạm thời\n"
            "• Lần 10: Ban vĩnh viễn"
        ),
        inline=False
    )
    
    embed.add_field(
        name="🔇 **Timeout/Mute**",
        value=(
            "`-timeout @user [phút] [lý do]` - Timeout thành viên\n"
            "`-to @user [phút] [lý do]` - Viết tắt của timeout\n"
            "`-untimeout @user` - Gỡ timeout\n"
            "`-rto @user` - Viết tắt của untimeout"
        ),
        inline=False
    )
    
    embed.add_field(
        name="🔨 **Kick/Ban**",
        value=(
            "`-kick @user [lý do]` - Kick thành viên\n"
            "`-ban @user [lý do]` - Ban thành viên\n"
            "`-unban <user_id> [lý do]` - Unban thành viên\n"
            "`-rban <user_id>` - Viết tắt của unban"
        ),
        inline=False
    )
    
    embed.add_field(
        name="🛠️ **Tiện ích Quản lý**",
        value=(
            "`-clear [số]` - Xóa tin nhắn (1-100)\n"
            "`-lock [#channel]` - Khóa channel\n"
            "`-unlock [#channel]` - Mở khóa channel\n"
            "`-slowmode [giây]` - Đặt slowmode (0 = tắt)"
        ),
        inline=False
    )
    
    embed.add_field(
        name="📊 **Thông tin**",
        value=(
            "`-serverinfo` - Thông tin server\n"
            "`-userinfo [@user]` - Thông tin thành viên\n"
            "`-ping` - Kiểm tra độ trễ"
        ),
        inline=False
    )
    
    embed.set_footer(text=f"{BOT_NAME} v2.0 | Prefix: {PREFIX}")
    await ctx.send(embed=embed)

# ==================== INFO COMMANDS ====================
@bot.command(name='serverinfo', aliases=['server'])
async def server_info(ctx):
    """Hiển thị thông tin server"""
    guild = ctx.guild
    
    embed = discord.Embed(
        title=f"📊 Thông tin {guild.name}",
        color=discord.Color.blue(),
        timestamp=datetime.now()
    )
    
    embed.set_thumbnail(url=guild.icon.url if guild.icon else None)
    embed.add_field(name="🆔 ID", value=guild.id, inline=True)
    embed.add_field(name="👑 Chủ sở hữu", value=guild.owner.mention, inline=True)
    embed.add_field(name="📅 Ngày tạo", value=guild.created_at.strftime("%d/%m/%Y"), inline=True)
    embed.add_field(name="👥 Thành viên", value=guild.member_count, inline=True)
    embed.add_field(name="💬 Channels", value=len(guild.channels), inline=True)
    embed.add_field(name="📜 Roles", value=len(guild.roles), inline=True)
    embed.add_field(name="🎯 Boost Level", value=guild.premium_tier, inline=True)
    embed.add_field(name="🚀 Số Boost", value=guild.premium_subscription_count, inline=True)
    
    await ctx.send(embed=embed)

@bot.command(name='userinfo', aliases=['user', 'whois'])
async def user_info(ctx, member: discord.Member = None):
    """Hiển thị thông tin thành viên"""
    member = member or ctx.author
    
    embed = discord.Embed(
        title=f"👤 Thông tin {member.display_name}",
        color=member.color,
        timestamp=datetime.now()
    )
    
    embed.set_thumbnail(url=member.avatar.url if member.avatar else member.default_avatar.url)
    embed.add_field(name="🆔 ID", value=member.id, inline=True)
    embed.add_field(name="📛 Username", value=str(member), inline=True)
    embed.add_field(name="🎭 Nickname", value=member.nick or "Không có", inline=True)
    embed.add_field(name="📅 Tạo tài khoản", value=member.created_at.strftime("%d/%m/%Y"), inline=True)
    embed.add_field(name="📥 Tham gia server", value=member.joined_at.strftime("%d/%m/%Y"), inline=True)
    embed.add_field(name="🎨 Màu role", value=str(member.color), inline=True)
    embed.add_field(name="📜 Roles", value=" ".join([r.mention for r in member.roles[1:]]) or "Không có", inline=False)
    embed.add_field(name="⚠️ Cảnh báo", value=f"{data_manager.get_warnings(ctx.guild.id, member.id)}/10", inline=True)
    
    await ctx.send(embed=embed)

@bot.command(name='ping')
async def ping(ctx):
    """Kiểm tra độ trễ của bot"""
    latency = round(bot.latency * 1000)
    embed = discord.Embed(
        title="🏓 Pong!",
        description=f"Độ trễ: **{latency}ms**",
        color=discord.Color.green() if latency < 100 else discord.Color.orange()
    )
    await ctx.send(embed=embed)

# ==================== SLASH COMMANDS ====================
@bot.tree.command(name="help", description="Hiển thị menu trợ giúp")
async def slash_help(interaction: discord.Interaction):
    embed = discord.Embed(
        title=f"🛡️ {BOT_NAME} - Menu Trợ giúp",
        description="Sử dụng prefix `-` cho các lệnh\nVí dụ: `-help`, `-warn @user`",
        color=discord.Color.blue()
    )
    embed.add_field(name="📋 Danh sách lệnh", value="Gõ `-help` trong chat để xem chi tiết", inline=False)
    await interaction.response.send_message(embed=embed, ephemeral=True)

# ==================== ERROR HANDLING ====================
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(f"❌ Thiếu tham số! Sử dụng: `{ctx.prefix}help` để xem hướng dẫn.")
    elif isinstance(error, commands.MemberNotFound):
        await ctx.send("❌ Không tìm thấy thành viên này!")
    elif isinstance(error, commands.CheckFailure):
        await ctx.send("❌ Bạn không có quyền sử dụng lệnh này!")
    elif isinstance(error, commands.CommandNotFound):
        pass  # Ignore command not found errors
    else:
        print(f"Error: {error}")

# ==================== RUN BOT ====================
if __name__ == "__main__":
    from dotenv import load_dotenv
    load_dotenv()
    
    TOKEN = os.getenv('DISCORD_BOT_TOKEN')
    if not TOKEN:
        raise ValueError("Missing DISCORD_BOT_TOKEN in .env file")
    
    try:
        print("🚀 Starting Dorothy bot...")
    except UnicodeEncodeError:
        print("[INFO] Starting Dorothy bot...")
    
    bot.run(TOKEN)
