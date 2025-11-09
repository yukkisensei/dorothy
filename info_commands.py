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
from config import BOT_NAME, VERSION, VERSION, PREFIX, OWNER_IDS

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
    
    @bot.command(name='dmblocklist', aliases=['dmbl'])
    async def dm_blocklist(ctx):
        """Show list of DM blocked users (Owner only)"""
        if ctx.author.id not in OWNER_IDS:
            return await ctx.send("❌ This command is owner-only!")
        
        blocked_users = data_manager.data.get("dm_blocked_users", {})
        
        if not blocked_users:
            return await ctx.send("✅ No users are currently blocked from DMing the bot!")
        
        embed = discord.Embed(
            title="🚫 DM Blocked Users",
            description=f"Total: {len(blocked_users)} users",
            color=discord.Color.red()
        )
        
        for user_id, info in list(blocked_users.items())[:10]:
            try:
                user = await bot.fetch_user(int(user_id))
                user_name = f"{user.name}#{user.discriminator if user.discriminator != '0' else ''}"
            except:
                user_name = f"Unknown User ({user_id})"
            
            embed.add_field(
                name=user_name,
                value=f"Reason: {info.get('reason', 'Unknown')}\nBlocked: {info.get('timestamp', 'Unknown')[:10]}",
                inline=False
            )
        
        if len(blocked_users) > 10:
            embed.set_footer(text=f"... and {len(blocked_users) - 10} more users")
        
        await ctx.send(embed=embed)
    
    @bot.command(name='dmunblock', aliases=['dmub'])
    async def dm_unblock(ctx, user_id: str):
        """Unblock a user from DMing the bot (Owner only)"""
        if ctx.author.id not in OWNER_IDS:
            return await ctx.send("❌ This command is owner-only!")
        
        if not data_manager.is_dm_blocked(user_id):
            return await ctx.send(f"❌ User `{user_id}` is not blocked!")
        
        data_manager.unblock_dm_user(user_id)
        
        try:
            user = await bot.fetch_user(int(user_id))
            await ctx.send(f"✅ Unblocked {user.mention} from DMing Dorothy!")
        except:
            await ctx.send(f"✅ Unblocked user `{user_id}` from DMing Dorothy!")

    @bot.command(name='serverinfo', aliases=['server'])
    async def server_info(ctx):
        """Để hiển thị thông tin server"""
        from localization import get_text
        guild_id = str(ctx.guild.id)
        guild = ctx.guild
        
        embed = discord.Embed(
            title=get_text(guild_id, "serverinfo_title", name=guild.name),
            color=discord.Color.blue(),
            timestamp=datetime.now()
        )
        
        embed.set_thumbnail(url=guild.icon.url if guild.icon else None)
        embed.add_field(name=get_text(guild_id, "serverinfo_id"), value=guild.id, inline=True)
        embed.add_field(name=get_text(guild_id, "serverinfo_owner"), value=guild.owner.mention, inline=True)
        embed.add_field(name=get_text(guild_id, "serverinfo_created"), value=guild.created_at.strftime("%d/%m/%Y"), inline=True)
        embed.add_field(name=get_text(guild_id, "serverinfo_members"), value=guild.member_count, inline=True)
        embed.add_field(name=get_text(guild_id, "serverinfo_channels"), value=len(guild.channels), inline=True)
        embed.add_field(name=get_text(guild_id, "serverinfo_roles"), value=len(guild.roles), inline=True)
        embed.add_field(name=get_text(guild_id, "serverinfo_boost"), value=guild.premium_tier, inline=True)
        embed.add_field(name=get_text(guild_id, "serverinfo_boosts"), value=guild.premium_subscription_count or 0, inline=True)
        
        await ctx.send(embed=embed)

    @bot.command(name='userinfo', aliases=['user', 'whois'])
    async def user_info(ctx, member: discord.Member = None):
        """Để hiển thị thông tin thành viên"""
        from localization import get_text
        guild_id = str(ctx.guild.id)
        member = member or ctx.author
        
        embed = discord.Embed(
            title=get_text(guild_id, "userinfo_title", name=member.display_name),
            color=member.color,
            timestamp=datetime.now()
        )
        
        none_text = get_text(guild_id, "userinfo_none")
        embed.set_thumbnail(url=member.avatar.url if member.avatar else member.default_avatar.url)
        embed.add_field(name=get_text(guild_id, "userinfo_id"), value=member.id, inline=True)
        embed.add_field(name=get_text(guild_id, "userinfo_username"), value=str(member), inline=True)
        embed.add_field(name=get_text(guild_id, "userinfo_nickname"), value=member.nick or none_text, inline=True)
        embed.add_field(name=get_text(guild_id, "userinfo_created"), value=member.created_at.strftime("%d/%m/%Y"), inline=True)
        embed.add_field(name=get_text(guild_id, "userinfo_joined"), value=member.joined_at.strftime("%d/%m/%Y") if member.joined_at else "Unknown", inline=True)
        embed.add_field(name=get_text(guild_id, "userinfo_color"), value=str(member.color), inline=True)
        embed.add_field(name=get_text(guild_id, "userinfo_roles"), value=" ".join([r.mention for r in member.roles[1:]]) or none_text, inline=False)
        embed.add_field(name=get_text(guild_id, "userinfo_warnings"), value=f"{data_manager.get_warnings(ctx.guild.id, member.id)}/10", inline=True)
        
        await ctx.send(embed=embed)

    @bot.command(name='ping')
    async def ping(ctx):
        """Kiểm tra độ trễ của bot"""
        from localization import get_text
        guild_id = str(ctx.guild.id) if ctx.guild else "0"
        
        latency = round(bot.latency * 1000)
        embed = discord.Embed(
            title=get_text(guild_id, "ping_title"),
            description=get_text(guild_id, "ping_latency", ms=latency),
            color=discord.Color.green() if latency < 100 else discord.Color.orange()
        )
        await ctx.send(embed=embed)

    @bot.command(name='setprefix', aliases=['prefix'])
    @has_mod_permissions()
    async def set_prefix_command(ctx, new_prefix: str = None):
        """Đặt prefix tùy chỉnh cho server"""
        from localization import get_text
        guild_id = str(ctx.guild.id)
        
        if new_prefix is None:
            current = data_manager.get_prefix(ctx.guild.id)
            await ctx.send(get_text(guild_id, "prefix_current", prefix=current))
            return
        
        if len(new_prefix) > 5:
            await ctx.send(get_text(guild_id, "error_prefix_long"))
            return
        
        data_manager.set_prefix(ctx.guild.id, new_prefix)
        await ctx.send(get_text(guild_id, "prefix_changed", prefix=new_prefix))

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
