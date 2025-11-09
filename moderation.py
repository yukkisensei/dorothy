"""
Dorothy Bot - Moderation Module
All moderation commands and functions
"""

import discord
from datetime import datetime, timedelta
from discord.ext import commands
from typing import Optional
from config import WARNING_LEVELS
from database import DataManager
from utils import (
    parse_time_string, format_duration, has_mod_permissions, has_admin_permissions,
    send_dm_notification, log_moderation_action
)

# Global data manager reference (will be set in main.py)
data_manager: Optional[DataManager] = None

def setup_moderation(dm: DataManager):
    """Initialize moderation module with data manager"""
    global data_manager
    data_manager = dm

# ==================== AUTO WARNING SYSTEM ====================
async def add_auto_warning(guild: discord.Guild, member: discord.Member, channel: discord.TextChannel, reason: str):
    """Add automatic warning from security system"""
    from localization import get_text
    
    if not data_manager:
        return
    
    guild_id = str(guild.id)
    warning_count = data_manager.add_warning(guild.id, member.id, reason)
    
    # Get warning level configuration
    if warning_count in WARNING_LEVELS:
        level_config = WARNING_LEVELS[warning_count]
        
        # Create embed
        embed = discord.Embed(
            title=get_text(guild_id, "warning_auto"),
            description=level_config["message"],
            color=discord.Color.orange() if warning_count < 6 else discord.Color.red(),
            timestamp=datetime.now()
        )
        embed.add_field(name=get_text(guild_id, "warning_member"), value=member.mention, inline=True)
        embed.add_field(name=get_text(guild_id, "warning_count"), value=f"{warning_count}/10", inline=True)
        embed.add_field(name=get_text(guild_id, "warning_reason"), value=reason, inline=False)
        embed.set_footer(text="Auto-Moderation System")
        
        await channel.send(embed=embed)
        
        # Send DM notification
        action_text = get_text(guild_id, "action_warned", count=warning_count)
        await send_dm_notification(
            member,
            action_text,
            reason,
            guild.name,
            level_config["message"],
            guild_id
        )
        
        # Apply action based on warning level
        if level_config["action"] == "timeout":
            try:
                duration = timedelta(minutes=level_config["duration"])
                await member.timeout(duration, reason=f"[AUTO] Warning #{warning_count}: {reason}")
            except:
                pass
        
        elif level_config["action"] == "kick":
            try:
                action_text = get_text(guild_id, "action_kicked")
                extra_text = get_text(guild_id, "extra_rejoin")
                await send_dm_notification(
                    member,
                    action_text,
                    reason,
                    guild.name,
                    extra_text,
                    guild_id
                )
                await member.kick(reason=f"[AUTO] Warning #{warning_count}: {reason}")
            except:
                pass
        
        elif level_config["action"] == "ban":
            try:
                action_text = get_text(guild_id, "action_banned")
                extra_text = get_text(guild_id, "extra_cannot_rejoin")
                await send_dm_notification(
                    member,
                    action_text,
                    reason,
                    guild.name,
                    extra_text,
                    guild_id
                )
                await member.ban(reason=f"[AUTO] Warning #{warning_count}: {reason}")
            except:
                pass

# ==================== MODERATION COMMANDS ====================
def setup_commands(bot: commands.Bot):
    """Register all moderation commands"""
    
    @bot.command(name='warn', aliases=['w', 'warning'])
    @has_mod_permissions()
    async def warn_user(ctx, member: discord.Member, *, reason: str = None):
        """Cảnh báo một thành viên"""
        from localization import get_text
        guild_id = str(ctx.guild.id)
        
        if reason is None:
            reason = get_text(guild_id, "dm_no_reason")
        
        if member == ctx.author:
            return await ctx.send(get_text(guild_id, "error_self_warn"))
        
        if member.bot:
            return await ctx.send(get_text(guild_id, "error_bot_action"))
        
        # Add warning
        warning_count = data_manager.add_warning(ctx.guild.id, member.id, reason)
        
        # Get warning level configuration
        if warning_count in WARNING_LEVELS:
            level_config = WARNING_LEVELS[warning_count]
            
            # Create embed
            embed = discord.Embed(
                title=get_text(guild_id, "warning_title"),
                description=level_config["message"],
                color=discord.Color.orange() if warning_count < 6 else discord.Color.red(),
                timestamp=datetime.now()
            )
            embed.add_field(name=get_text(guild_id, "warning_member"), value=member.mention, inline=True)
            embed.add_field(name=get_text(guild_id, "warning_count"), value=f"{warning_count}/10", inline=True)
            embed.add_field(name=get_text(guild_id, "warning_reason"), value=reason, inline=False)
            embed.set_footer(text=f"Moderator: {ctx.author.name}")
            
            await ctx.send(embed=embed)
            
            # Send DM notification
            action_text = get_text(guild_id, "action_warned", count=warning_count)
            await send_dm_notification(
                member,
                action_text,
                reason,
                ctx.guild.name,
                level_config["message"],
                guild_id
            )
            
            # Apply action based on warning level
            if level_config["action"] == "timeout":
                try:
                    duration = timedelta(minutes=level_config['duration'])
                    await member.timeout(duration, reason=f"Warning #{warning_count}: {reason}")
                    await ctx.send(get_text(guild_id, "timeout_success", user=member.mention, duration=level_config['duration']))
                except discord.Forbidden:
                    await ctx.send(get_text(guild_id, "error_forbidden_timeout"))
            
            elif level_config["action"] == "kick":
                try:
                    action_text = get_text(guild_id, "action_kicked")
                    extra_text = get_text(guild_id, "extra_rejoin")
                    await send_dm_notification(
                        member, action_text, reason, ctx.guild.name,
                        extra_text, guild_id
                    )
                    await member.kick(reason=f"Warning #{warning_count}: {reason}")
                    await ctx.send(f"👢 {member.mention} đã bị kick khỏi server!")
                except discord.Forbidden:
                    await ctx.send(get_text(guild_id, "error_forbidden_kick"))
            
            elif level_config["action"] == "ban":
                try:
                    action_text = get_text(guild_id, "action_banned")
                    extra_text = get_text(guild_id, "extra_cannot_rejoin")
                    await send_dm_notification(
                        member, action_text, reason, ctx.guild.name,
                        extra_text, guild_id
                    )
                    await member.ban(reason=f"Warning #{warning_count}: {reason}")
                    await ctx.send(f"🔨 {member.mention} đã bị ban vĩnh viễn!")
                except discord.Forbidden:
                    await ctx.send(get_text(guild_id, "error_forbidden_ban"))
            
            # Log action
            await log_moderation_action(ctx.guild, f"Warning #{warning_count}", member, ctx.author, reason)
        else:
            # Beyond level 10, auto-ban
            try:
                await member.ban(reason=f"Excessive warnings: {warning_count}")
                await ctx.send(get_text(guild_id, "warning_excessive", user=member.mention))
            except:
                pass

    @bot.command(name='warnings', aliases=['warns', 'checkwarn'])
    @has_mod_permissions()
    async def check_warnings(ctx, member: discord.Member = None):
        """Kiểm tra số lần cảnh báo"""
        from localization import get_text
        guild_id = str(ctx.guild.id)
        
        member = member or ctx.author
        warning_count = data_manager.get_warnings(ctx.guild.id, member.id)
        
        embed = discord.Embed(
            title=get_text(guild_id, "warning_stats"),
            color=discord.Color.blue()
        )
        embed.add_field(name=get_text(guild_id, "warning_member"), value=member.mention, inline=True)
        embed.add_field(name=get_text(guild_id, "warning_number"), value=f"{warning_count}/10", inline=True)
        
        if warning_count > 0 and warning_count < 10:
            next_level = min(warning_count + 1, 10)
            next_action = WARNING_LEVELS[next_level]["action"]
            embed.add_field(name=get_text(guild_id, "warning_next"), value=next_action.upper(), inline=False)
        
        await ctx.send(embed=embed)

    @bot.command(name='clearwarns', aliases=['resetwarns'])
    @has_mod_permissions()
    async def clear_warnings(ctx, member: discord.Member):
        """Xóa toàn bộ cảnh báo của một thành viên"""
        from localization import get_text
        guild_id = str(ctx.guild.id)
        
        if data_manager.clear_warnings(ctx.guild.id, member.id):
            await ctx.send(get_text(guild_id, "warning_cleared", user=member.mention))
            await log_moderation_action(ctx.guild, "Clear Warnings", member, ctx.author, "Reset warnings to 0")
        else:
            await ctx.send(get_text(guild_id, "warning_none", user=member.mention))

    # ==================== TIMEOUT COMMANDS ====================
    @bot.command(name='timeout', aliases=['mute'])
    @has_mod_permissions()
    async def timeout_member(ctx, member: discord.Member, duration: Optional[str] = None, *, reason: Optional[str] = None):
        """Timeout (mute) một thành viên"""
        timeout_minutes = 5
        if duration:
            if any(c in duration for c in ['h', 'm', 's', 'd']):
                timeout_minutes = parse_time_string(duration)
                if timeout_minutes is None:
                    return await ctx.send(get_text(guild_id, "error_invalid_time"))
            else:
                try:
                    timeout_minutes = int(duration)
                except ValueError:
                    reason = duration if not reason else f"{duration} {reason}"
                    timeout_minutes = 5
        
        from localization import get_text
        guild_id = str(ctx.guild.id)
        
        if member == ctx.author:
            return await ctx.send(get_text(guild_id, "error_self_timeout"))
        if member.bot:
            return await ctx.send(get_text(guild_id, "error_bot_action"))
        
        try:
            timeout_duration = timedelta(minutes=timeout_minutes)
            reason = reason or get_text(guild_id, "dm_no_reason")
            
            await send_dm_notification(
                member, f"timeout {format_duration(timeout_minutes)}", reason,
                ctx.guild.name, f"Thời gian mute: {format_duration(timeout_minutes)}"
            )
            
            await member.timeout(timeout_duration, reason=reason)
            
            embed = discord.Embed(
                title=get_text(guild_id, "timeout_title"),
                color=discord.Color.orange(),
                timestamp=datetime.now()
            )
            embed.add_field(name=get_text(guild_id, "warning_member"), value=member.mention, inline=True)
            embed.add_field(name=get_text(guild_id, "duration"), value=format_duration(timeout_minutes), inline=True)
            embed.add_field(name=get_text(guild_id, "warning_reason"), value=reason, inline=False)
            embed.set_footer(text=f"Moderator: {ctx.author.name}")
            
            await ctx.send(embed=embed)
            await log_moderation_action(ctx.guild, f"Timeout {timeout_minutes}m", member, ctx.author, reason)
        except discord.Forbidden:
            await ctx.send(get_text(guild_id, "error_forbidden_timeout"))

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
            await log_moderation_action(ctx.guild, "Remove Timeout", member, ctx.author)
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
    async def kick_member(ctx, member: discord.Member, *, reason: str = None):
        """Kick một thành viên khỏi server"""
        from localization import get_text
        guild_id = str(ctx.guild.id)
        
        if reason is None:
            reason = get_text(guild_id, "dm_no_reason")
        
        if member == ctx.author:
            return await ctx.send(get_text(guild_id, "error_self_kick"))
        if member.bot:
            return await ctx.send(get_text(guild_id, "error_bot_action"))
        
        try:
            action_text = get_text(guild_id, "action_kicked")
            extra_text = get_text(guild_id, "extra_rejoin")
            await send_dm_notification(
                member, action_text, reason, ctx.guild.name,
                extra_text, guild_id
            )
            
            await member.kick(reason=reason)
            
            embed = discord.Embed(
                title=get_text(guild_id, "kick_title"),
                color=discord.Color.orange(),
                timestamp=datetime.now()
            )
            embed.add_field(name=get_text(guild_id, "warning_member"), value=f"{member.mention} ({member.id})", inline=True)
            embed.add_field(name=get_text(guild_id, "warning_reason"), value=reason, inline=False)
            embed.set_footer(text=f"Moderator: {ctx.author.name}")
            
            await ctx.send(embed=embed)
            await log_moderation_action(ctx.guild, "Kick", member, ctx.author, reason)
        except discord.Forbidden:
            await ctx.send(get_text(guild_id, "error_forbidden_kick"))

    @bot.command(name='ban', aliases=['b'])
    @has_mod_permissions()
    async def ban_member(ctx, member: discord.Member, *, reason: str = None):
        """Ban một thành viên khỏi server"""
        from localization import get_text
        guild_id = str(ctx.guild.id)
        
        if reason is None:
            reason = get_text(guild_id, "dm_no_reason")
        
        if member == ctx.author:
            return await ctx.send(get_text(guild_id, "error_self_ban"))
        if member.bot:
            return await ctx.send(get_text(guild_id, "error_bot_action"))
        
        try:
            action_text = get_text(guild_id, "action_banned")
            extra_text = get_text(guild_id, "extra_cannot_rejoin")
            await send_dm_notification(
                member, action_text, reason, ctx.guild.name,
                extra_text, guild_id
            )
            
            await member.ban(reason=reason)
            
            embed = discord.Embed(
                title=get_text(guild_id, "ban_title"),
                color=discord.Color.red(),
                timestamp=datetime.now()
            )
            embed.add_field(name=get_text(guild_id, "warning_member"), value=f"{member.mention} ({member.id})", inline=True)
            embed.add_field(name=get_text(guild_id, "warning_reason"), value=reason, inline=False)
            embed.set_footer(text=f"Moderator: {ctx.author.name}")
            
            await ctx.send(embed=embed)
            await log_moderation_action(ctx.guild, "Ban", member, ctx.author, reason)
        except discord.Forbidden:
            await ctx.send(get_text(guild_id, "error_forbidden_ban"))

    @bot.command(name='unban', aliases=['ub', 'rban'])
    @has_mod_permissions()
    async def unban_member(ctx, user_id: int, *, reason: str = None):
        """Unban một thành viên"""
        from localization import get_text
        guild_id = str(ctx.guild.id)
        
        if reason is None:
            reason = get_text(guild_id, "dm_no_reason")
        
        try:
            user = await bot.fetch_user(user_id)
            await ctx.guild.unban(user, reason=reason)
            
            embed = discord.Embed(
                title=get_text(guild_id, "unban_title"),
                color=discord.Color.green(),
                timestamp=datetime.now()
            )
            embed.add_field(name=get_text(guild_id, "user"), value=f"{user.mention} ({user.id})", inline=True)
            embed.add_field(name=get_text(guild_id, "warning_reason"), value=reason, inline=False)
            embed.set_footer(text=f"Moderator: {ctx.author.name}")
            
            await ctx.send(embed=embed)
        except discord.NotFound:
            await ctx.send(get_text(guild_id, "error_user_not_found"))
        except discord.Forbidden:
            await ctx.send(get_text(guild_id, "error_forbidden_unban"))

    # ==================== UTILITY COMMANDS ====================
    @bot.command(name='clear', aliases=['purge', 'clean'])
    @has_mod_permissions()
    async def clear_messages(ctx, amount: int = 10):
        """Xóa tin nhắn trong channel"""
        from localization import get_text
        guild_id = str(ctx.guild.id)
        
        if amount < 1 or amount > 100:
            return await ctx.send(get_text(guild_id, "error_invalid_amount"))
        
        deleted = await ctx.channel.purge(limit=amount + 1)
        msg = await ctx.send(get_text(guild_id, "clear_success", count=len(deleted) - 1))
        
        import asyncio
        await asyncio.sleep(3)
        await msg.delete()

    @bot.command(name='lock')
    @has_mod_permissions()
    async def lock_channel(ctx, channel: discord.TextChannel = None):
        """Khóa channel"""
        from localization import get_text
        guild_id = str(ctx.guild.id)
        
        channel = channel or ctx.channel
        await channel.set_permissions(ctx.guild.default_role, send_messages=False)
        await ctx.send(get_text(guild_id, "channel_locked", channel=channel.mention))

    @bot.command(name='unlock')
    @has_mod_permissions()
    async def unlock_channel(ctx, channel: discord.TextChannel = None):
        """Mở khóa channel"""
        from localization import get_text
        guild_id = str(ctx.guild.id)
        
        channel = channel or ctx.channel
        await channel.set_permissions(ctx.guild.default_role, send_messages=True)
        await ctx.send(get_text(guild_id, "channel_unlocked", channel=channel.mention))

    @bot.command(name='slowmode', aliases=['slow'])
    @has_mod_permissions()
    async def set_slowmode(ctx, seconds: int = 0):
        """Đặt slowmode cho channel (0 = tắt)"""
        from localization import get_text
        guild_id = str(ctx.guild.id)
        
        if seconds < 0 or seconds > 21600:
            return await ctx.send(get_text(guild_id, "error_invalid_slowmode"))
        
        await ctx.channel.edit(slowmode_delay=seconds)
        if seconds == 0:
            await ctx.send(get_text(guild_id, "slowmode_disabled"))
        else:
            await ctx.send(get_text(guild_id, "slowmode_set", seconds=seconds))
