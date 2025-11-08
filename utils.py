"""
Dorothy Bot - Utility Functions
Helper functions used throughout the bot
"""

import discord
import re
from datetime import datetime, timedelta
from typing import Optional
from discord.ext import commands
from config import OWNER_IDS

def parse_time_string(time_str: str) -> Optional[int]:
    """Parse time string like '1h', '30m', '1h30m' to minutes"""
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
    """Check if user has moderation permissions"""
    def predicate(ctx):
        return (ctx.author == ctx.guild.owner or 
                ctx.author.guild_permissions.manage_messages or 
                ctx.author.guild_permissions.administrator or
                ctx.author.id in OWNER_IDS)
    return commands.check(predicate)

def has_admin_permissions():
    """Check if user has administrator permissions"""
    def predicate(ctx):
        return (ctx.author == ctx.guild.owner or 
                ctx.author.guild_permissions.administrator or
                ctx.author.id in OWNER_IDS)
    return commands.check(predicate)

async def send_dm_notification(member: discord.Member, action: str, reason: str, server_name: str, extra_info: str = None) -> bool:
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
        return False
    except Exception:
        return False

async def log_moderation_action(guild: discord.Guild, action: str, target: discord.Member, moderator: discord.Member, reason: str = None):
    """Log moderation actions to a log channel if exists"""
    log_channel = discord.utils.get(guild.text_channels, name="mod-log")
    if log_channel:
        try:
            embed = discord.Embed(
                title=f"🔒 {action}",
                color=discord.Color.red(),
                timestamp=datetime.now()
            )
            embed.add_field(name="👮 Moderator", value=moderator.mention, inline=True)
            embed.add_field(name="👤 Target", value=target.mention, inline=True)
            embed.add_field(name="📝 Lý do", value=reason or "Không có lý do", inline=False)
            embed.set_footer(text=f"ID: {target.id}")
            await log_channel.send(embed=embed)
        except:
            pass

async def log_security_event(guild: discord.Guild, event_title: str, description: str, color: discord.Color = discord.Color.orange()):
    """Log security events to security-log channel"""
    log_channel = discord.utils.get(guild.text_channels, name="security-log")
    if log_channel:
        try:
            embed = discord.Embed(
                title=event_title,
                description=description,
                color=color,
                timestamp=datetime.now()
            )
            embed.set_footer(text="Dorothy Security System")
            await log_channel.send(embed=embed)
        except:
            pass
