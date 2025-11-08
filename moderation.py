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
    if not data_manager:
        return
    
    warning_count = data_manager.add_warning(guild.id, member.id, reason)
    
    # Get warning level configuration
    if warning_count in WARNING_LEVELS:
        level_config = WARNING_LEVELS[warning_count]
        
        # Create embed
        embed = discord.Embed(
            title="⚠️ CẢNH BÁO TỰ ĐỘNG",
            description=level_config["message"],
            color=discord.Color.orange() if warning_count < 6 else discord.Color.red(),
            timestamp=datetime.now()
        )
        embed.add_field(name="👤 Thành viên", value=member.mention, inline=True)
        embed.add_field(name="🔢 Lần cảnh báo", value=f"{warning_count}/10", inline=True)
        embed.add_field(name="📝 Lý do", value=reason, inline=False)
        embed.set_footer(text="Auto-Moderation System")
        
        await channel.send(embed=embed)
        
        # Send DM notification
        await send_dm_notification(
            member,
            f"cảnh báo lần {warning_count}/10",
            reason,
            guild.name,
            level_config["message"]
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
                await send_dm_notification(
                    member,
                    "kick khỏi server",
                    reason,
                    guild.name,
                    "Bạn có thể join lại server nếu có invite link"
                )
                await member.kick(reason=f"[AUTO] Warning #{warning_count}: {reason}")
            except:
                pass
        
        elif level_config["action"] == "ban":
            try:
                await send_dm_notification(
                    member,
                    "ban vĩnh viễn",
                    reason,
                    guild.name,
                    "Bạn sẽ không thể join lại server này"
                )
                await member.ban(reason=f"[AUTO] Warning #{warning_count}: {reason}")
            except:
                pass

# ==================== MODERATION COMMANDS ====================
def setup_commands(bot: commands.Bot):
    """Register all moderation commands"""
    
    @bot.command(name='warn', aliases=['w', 'warning'])
    @has_mod_permissions()
    async def warn_user(ctx, member: discord.Member, *, reason: str = "Không có lý do"):
        """Cảnh báo một thành viên"""
        if member == ctx.author:
            return await ctx.send("❌ Bạn không thể tự cảnh báo chính mình!")
        
        if member.bot:
            return await ctx.send("❌ Không thể cảnh báo bot!")
        
        # Add warning
        warning_count = data_manager.add_warning(ctx.guild.id, member.id, reason)
        
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
            
            # Send DM notification
            await send_dm_notification(
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
                except discord.Forbidden:
                    await ctx.send("❌ Không có quyền timeout thành viên này!")
            
            elif level_config["action"] == "kick":
                try:
                    await send_dm_notification(
                        member, "kick khỏi server", reason, ctx.guild.name,
                        "Bạn có thể join lại server nếu có invite link"
                    )
                    await member.kick(reason=f"Warning #{warning_count}: {reason}")
                    await ctx.send(f"👢 {member.mention} đã bị kick khỏi server!")
                except discord.Forbidden:
                    await ctx.send("❌ Không có quyền kick thành viên này!")
            
            elif level_config["action"] == "ban":
                try:
                    await send_dm_notification(
                        member, "ban vĩnh viễn", reason, ctx.guild.name,
                        "Bạn sẽ không thể join lại server này"
                    )
                    await member.ban(reason=f"Warning #{warning_count}: {reason}")
                    await ctx.send(f"🔨 {member.mention} đã bị ban vĩnh viễn!")
                except discord.Forbidden:
                    await ctx.send("❌ Không có quyền ban thành viên này!")
            
            # Log action
            await log_moderation_action(ctx.guild, f"Warning #{warning_count}", member, ctx.author, reason)
        else:
            # Beyond level 10, auto-ban
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
        
        if warning_count > 0 and warning_count < 10:
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
            await log_moderation_action(ctx.guild, "Clear Warnings", member, ctx.author, "Reset warnings to 0")
        else:
            await ctx.send(f"ℹ️ {member.mention} không có cảnh báo nào!")

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
                    return await ctx.send("❌ Format thời gian không hợp lệ! Dùng: 5m, 1h, 2h30m, etc.")
            else:
                try:
                    timeout_minutes = int(duration)
                except ValueError:
                    reason = duration if not reason else f"{duration} {reason}"
                    timeout_minutes = 5
        
        if member == ctx.author:
            return await ctx.send("❌ Bạn không thể tự mute chính mình!")
        if member.bot:
            return await ctx.send("❌ Không thể mute bot!")
        
        try:
            timeout_duration = timedelta(minutes=timeout_minutes)
            reason = reason or "Không có lý do"
            
            await send_dm_notification(
                member, f"timeout {format_duration(timeout_minutes)}", reason,
                ctx.guild.name, f"Thời gian mute: {format_duration(timeout_minutes)}"
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
            await log_moderation_action(ctx.guild, f"Timeout {timeout_minutes}m", member, ctx.author, reason)
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
    async def kick_member(ctx, member: discord.Member, *, reason: str = "Không có lý do"):
        """Kick một thành viên khỏi server"""
        if member == ctx.author:
            return await ctx.send("❌ Bạn không thể tự kick chính mình!")
        if member.bot:
            return await ctx.send("❌ Không thể kick bot!")
        
        try:
            await send_dm_notification(
                member, "kick khỏi server", reason, ctx.guild.name,
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
            await log_moderation_action(ctx.guild, "Kick", member, ctx.author, reason)
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
            await send_dm_notification(
                member, "ban vĩnh viễn", reason, ctx.guild.name,
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
            await log_moderation_action(ctx.guild, "Ban", member, ctx.author, reason)
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

    # ==================== UTILITY COMMANDS ====================
    @bot.command(name='clear', aliases=['purge', 'clean'])
    @has_mod_permissions()
    async def clear_messages(ctx, amount: int = 10):
        """Xóa tin nhắn trong channel"""
        if amount < 1 or amount > 100:
            return await ctx.send("❌ Số lượng phải từ 1 đến 100!")
        
        deleted = await ctx.channel.purge(limit=amount + 1)
        msg = await ctx.send(f"✅ Đã xóa {len(deleted) - 1} tin nhắn!")
        
        import asyncio
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
