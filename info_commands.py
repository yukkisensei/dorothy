"""
Dorothy Bot - Info Commands Module
Server info, user info, and utility commands
"""

import discord
import asyncio
from datetime import datetime
from typing import Optional
from discord.ext import commands
from database import DataManager
from utils import has_mod_permissions
from config import BOT_NAME, VERSION, PREFIX

# Global data manager reference
data_manager: Optional[DataManager] = None

def setup_info(dm: DataManager):
    """Initialize info module with data manager"""
    global data_manager
    data_manager = dm

def setup_commands(bot: commands.Bot):
    """Register all info commands"""
    
    @bot.command(name='help', aliases=['h'])
    async def help_command(ctx):
        """Show help menu / Hiển thị menu trợ giúp"""
        from localization import get_text
        
        guild_id = str(ctx.guild.id) if ctx.guild else "0"
        current_prefix = data_manager.get_prefix(ctx.guild.id) if ctx.guild else PREFIX
        
        embed = discord.Embed(
            title=get_text(guild_id, "help_title"),
            description=get_text(guild_id, "help_description"),
            color=discord.Color.blue()
        )
        
        embed.add_field(
            name=get_text(guild_id, "help_warning_system"),
            value=get_text(guild_id, "help_warning_desc"),
            inline=False
        )
        
        embed.add_field(
            name=get_text(guild_id, "help_timeout"),
            value=get_text(guild_id, "help_timeout_desc"),
            inline=False
        )
        
        embed.add_field(
            name=get_text(guild_id, "help_kickban"),
            value=get_text(guild_id, "help_kickban_desc"),
            inline=False
        )
        
        embed.add_field(
            name=get_text(guild_id, "help_security"),
            value=get_text(guild_id, "help_security_desc"),
            inline=False
        )
        
        embed.add_field(
            name=get_text(guild_id, "help_utility"),
            value=get_text(guild_id, "help_utility_desc"),
            inline=False
        )
        
        embed.add_field(
            name=get_text(guild_id, "help_info"),
            value=get_text(guild_id, "help_info_desc"),
            inline=False
        )
        
        embed.set_footer(text=get_text(guild_id, "help_footer", prefix=current_prefix))
        await ctx.send(embed=embed)

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
        embed.add_field(name="🚀 Số Boost", value=guild.premium_subscription_count or 0, inline=True)
        
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
        embed.add_field(name="📥 Tham gia server", value=member.joined_at.strftime("%d/%m/%Y") if member.joined_at else "Unknown", inline=True)
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

    @bot.command(name='setprefix', aliases=['prefix'])
    @has_mod_permissions()
    async def set_prefix_command(ctx, new_prefix: str = None):
        """Đặt prefix tùy chỉnh cho server"""
        if new_prefix is None:
            current = data_manager.get_prefix(ctx.guild.id)
            await ctx.send(f"📌 Prefix hiện tại: `{current}`\nSử dụng: `{current}setprefix <prefix>` để thay đổi")
            return
        
        if len(new_prefix) > 5:
            await ctx.send("❌ Prefix không được dài quá 5 ký tự!")
            return
        
        data_manager.set_prefix(ctx.guild.id, new_prefix)
        await ctx.send(f"✅ Đã đổi prefix thành: `{new_prefix}`")

    @bot.command(name='say')
    @has_mod_permissions()
    async def say_command(ctx, *, content: str = None):
        """Bot nói thay bạn. Dùng -say -r <message_id> <content> để reply"""
        try:
            await ctx.message.delete()
        except:
            pass
        
        if not content:
            return
        
        # Check if reply mode
        if content.startswith('-r '):
            parts = content[3:].split(None, 1)
            if len(parts) < 2:
                temp_msg = await ctx.send("❌ Sử dụng: `-say -r <message_id> <content>`")
                await asyncio.sleep(3)
                try:
                    await temp_msg.delete()
                except:
                    pass
                return
            
            try:
                message_id = int(parts[0])
                reply_content = parts[1]
                target_message = await ctx.channel.fetch_message(message_id)
                await target_message.reply(reply_content)
            except discord.NotFound:
                temp_msg = await ctx.send("❌ Không tìm thấy tin nhắn với ID này!")
                await asyncio.sleep(3)
                try:
                    await temp_msg.delete()
                except:
                    pass
            except ValueError:
                temp_msg = await ctx.send("❌ ID tin nhắn không hợp lệ!")
                await asyncio.sleep(3)
                try:
                    await temp_msg.delete()
                except:
                    pass
        else:
            await ctx.send(content)
