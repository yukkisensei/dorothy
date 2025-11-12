"""
Dorothy Bot - Security Commands Module
Commands for managing security features
"""

import discord
from datetime import datetime
from typing import Optional
from discord.ext import commands
from database import DataManager
from utils import has_admin_permissions, has_mod_permissions

# Global data manager reference
data_manager: Optional[DataManager] = None

def setup_security_commands(dm: DataManager):
    """Initialize security commands module with data manager"""
    global data_manager
    data_manager = dm

def setup_commands(bot: commands.Bot):
    """Register all security commands"""
    
    @bot.command(name='security', aliases=['sec'])
    @has_mod_permissions()
    async def security_status(ctx):
        """Show security status / Hiển thị trạng thái bảo mật"""
        from localization import get_text
        guild_id = str(ctx.guild.id)
        
        embed = discord.Embed(
            title=get_text(guild_id, "security_title"),
            description=f"**{ctx.guild.name}**",
            color=discord.Color.blue(),
            timestamp=datetime.now()
        )
        
        # Get security settings
        on_text = get_text(guild_id, "security_on")
        off_text = get_text(guild_id, "security_off")
        
        anti_nuke = on_text if data_manager.get_security_setting(guild_id, "anti_nuke_enabled", True) else off_text
        anti_raid = on_text if data_manager.get_security_setting(guild_id, "anti_raid_enabled", True) else off_text
        anti_spam = on_text if data_manager.get_security_setting(guild_id, "anti_spam_enabled", True) else off_text
        auto_mod = on_text if data_manager.get_security_setting(guild_id, "auto_mod_enabled", True) else off_text
        
        embed.add_field(name=get_text(guild_id, "security_antinuke"), value=anti_nuke, inline=True)
        embed.add_field(name=get_text(guild_id, "security_antiraid"), value=anti_raid, inline=True)
        embed.add_field(name=get_text(guild_id, "security_antispam"), value=anti_spam, inline=True)
        embed.add_field(name=get_text(guild_id, "security_automod"), value=auto_mod, inline=True)
        
        # Get recent logs
        recent_logs = data_manager.get_security_logs(guild_id, limit=5)
        if recent_logs:
            log_text = "\n".join([f"• {log['type']}: {log['timestamp'][:10]}" for log in recent_logs])
            embed.add_field(name=get_text(guild_id, "security_logs"), value=log_text, inline=False)
        
        embed.set_footer(text=get_text(guild_id, "security_footer"))
        await ctx.send(embed=embed)
    
    @bot.command(name='antinuke', aliases=['an'])
    @has_admin_permissions()
    async def toggle_antinuke(ctx, status: str = None):
        """Toggle Anti-Nuke / Bật/tắt Anti-Nuke"""
        from localization import get_text
        guild_id = str(ctx.guild.id)
        
        if status is None:
            current = data_manager.get_security_setting(guild_id, "anti_nuke_enabled", True)
            status_text = get_text(guild_id, "security_on") if current else get_text(guild_id, "security_off")
            await ctx.send(get_text(guild_id, "antinuke_current", status=status_text))
            return
        
        if status.lower() in ['on', 'enable', 'bật', '1']:
            data_manager.set_security_setting(guild_id, "anti_nuke_enabled", True)
            await ctx.send(get_text(guild_id, "antinuke_enabled"))
        elif status.lower() in ['off', 'disable', 'tắt', '0']:
            data_manager.set_security_setting(guild_id, "anti_nuke_enabled", False)
            await ctx.send(get_text(guild_id, "antinuke_disabled"))
        else:
            await ctx.send(get_text(guild_id, "error_invalid_toggle", command="antinuke"))
    
    @bot.command(name='antiraid', aliases=['ar'])
    @has_admin_permissions()
    async def toggle_antiraid(ctx, status: str = None):
        """Toggle Anti-Raid / Bật/tắt Anti-Raid"""
        from localization import get_text
        guild_id = str(ctx.guild.id)
        
        if status is None:
            current = data_manager.get_security_setting(guild_id, "anti_raid_enabled", True)
            status_text = get_text(guild_id, "security_on") if current else get_text(guild_id, "security_off")
            await ctx.send(get_text(guild_id, "antiraid_current", status=status_text))
            return
        
        if status.lower() in ['on', 'enable', 'bật', '1']:
            data_manager.set_security_setting(guild_id, "anti_raid_enabled", True)
            await ctx.send(get_text(guild_id, "antiraid_enabled"))
        elif status.lower() in ['off', 'disable', 'tắt', '0']:
            data_manager.set_security_setting(guild_id, "anti_raid_enabled", False)
            await ctx.send(get_text(guild_id, "antiraid_disabled"))
        else:
            await ctx.send(get_text(guild_id, "error_invalid_toggle", command="antiraid"))
    
    @bot.command(name='antispam', aliases=['as'])
    @has_admin_permissions()
    async def toggle_antispam(ctx, status: str = None):
        """Toggle Anti-Spam / Bật/tắt Anti-Spam"""
        from localization import get_text
        guild_id = str(ctx.guild.id)
        
        if status is None:
            current = data_manager.get_security_setting(guild_id, "anti_spam_enabled", True)
            status_text = get_text(guild_id, "security_on") if current else get_text(guild_id, "security_off")
            await ctx.send(get_text(guild_id, "antispam_current", status=status_text))
            return
        
        if status.lower() in ['on', 'enable', 'bật', '1']:
            data_manager.set_security_setting(guild_id, "anti_spam_enabled", True)
            await ctx.send(get_text(guild_id, "antispam_enabled"))
        elif status.lower() in ['off', 'disable', 'tắt', '0']:
            data_manager.set_security_setting(guild_id, "anti_spam_enabled", False)
            await ctx.send(get_text(guild_id, "antispam_disabled"))
        else:
            await ctx.send(get_text(guild_id, "error_invalid_toggle", command="antispam"))
    
    @bot.command(name='automod', aliases=['am'])
    @has_admin_permissions()
    async def toggle_automod(ctx, status: str = None):
        """Toggle Auto-Mod / Bật/tắt Auto-Moderation"""
        from localization import get_text
        guild_id = str(ctx.guild.id)
        
        if status is None:
            current = data_manager.get_security_setting(guild_id, "auto_mod_enabled", True)
            status_text = get_text(guild_id, "security_on") if current else get_text(guild_id, "security_off")
            await ctx.send(get_text(guild_id, "automod_current", status=status_text))
            return
        
        if status.lower() in ['on', 'enable', 'bật', '1']:
            data_manager.set_security_setting(guild_id, "auto_mod_enabled", True)
            await ctx.send(get_text(guild_id, "automod_enabled"))
        elif status.lower() in ['off', 'disable', 'tắt', '0']:
            data_manager.set_security_setting(guild_id, "auto_mod_enabled", False)
            await ctx.send(get_text(guild_id, "automod_disabled"))
        else:
            await ctx.send(get_text(guild_id, "error_invalid_toggle", command="automod"))
    
    @bot.command(name='whitelist', aliases=['wl'])
    @has_admin_permissions()
    async def whitelist_user(ctx, member: discord.Member = None, action: str = "add"):
        """Add/remove user from whitelist / Thêm/xóa user khỏi whitelist"""
        from localization import get_text
        guild_id = str(ctx.guild.id)
        
        if member is None:
            await ctx.send(get_text(guild_id, "whitelist_usage"))
            return
        
        user_id = str(member.id)
        
        if action.lower() in ['add', 'thêm', '+']:
            data_manager.add_whitelist(guild_id, user_id)
            await ctx.send(get_text(guild_id, "whitelist_added", user=member.mention))
        elif action.lower() in ['remove', 'xóa', '-', 'rm']:
            data_manager.remove_whitelist(guild_id, user_id)
            await ctx.send(get_text(guild_id, "whitelist_removed", user=member.mention))
        else:
            # Toggle
            if data_manager.is_whitelisted(guild_id, user_id):
                data_manager.remove_whitelist(guild_id, user_id)
                await ctx.send(get_text(guild_id, "whitelist_removed", user=member.mention))
            else:
                data_manager.add_whitelist(guild_id, user_id)
                await ctx.send(get_text(guild_id, "whitelist_added", user=member.mention))
                
    @bot.command(name='whitelistchannel', aliases=['wlc'])
    @has_admin_permissions()
    async def whitelist_channel(ctx, channel: discord.TextChannel = None, action: str = "add"):
        """Add/remove channel from whitelist / Thêm/xóa kênh khỏi whitelist"""
        from localization import get_text
        guild_id = str(ctx.guild.id)
        
        if channel is None:
            channel = ctx.channel
        
        channel_id = str(channel.id)
        
        if action.lower() in ['add', 'thêm', '+']:
            data_manager.add_whitelist_channel(guild_id, channel_id)
            await ctx.send(get_text(guild_id, "whitelist_channel_added", channel=channel.mention))
        elif action.lower() in ['remove', 'xóa', '-', 'rm']:
            data_manager.remove_whitelist_channel(guild_id, channel_id)
            await ctx.send(get_text(guild_id, "whitelist_channel_removed", channel=channel.mention))
        else:
            # Toggle
            if data_manager.is_channel_whitelisted(guild_id, channel_id):
                data_manager.remove_whitelist_channel(guild_id, channel_id)
                await ctx.send(get_text(guild_id, "whitelist_channel_removed", channel=channel.mention))
            else:
                data_manager.add_whitelist_channel(guild_id, channel_id)
                await ctx.send(get_text(guild_id, "whitelist_channel_added", channel=channel.mention))
    
    @bot.command(name='blacklist', aliases=['bl'])
    @has_admin_permissions()
    async def blacklist_word(ctx, action: str = None, *, word: str = None):
        """Manage blacklisted words / Quản lý danh sách từ cấm"""
        from localization import get_text
        guild_id = str(ctx.guild.id)
        
        if action is None:
            # Show current blacklist
            blacklist = data_manager.get_blacklist_words(guild_id)
            if blacklist:
                word_list = ", ".join([f"`{w}`" for w in blacklist[:20]])
                if len(blacklist) > 20:
                    word_list += f"\n...{len(blacklist) - 20} more words" if data_manager.get_language(guild_id) == "en" else f"\n...và {len(blacklist) - 20} từ khác"
                embed = discord.Embed(
                    title=get_text(guild_id, "blacklist_title"),
                    description=word_list,
                    color=discord.Color.orange()
                )
                await ctx.send(embed=embed)
            else:
                await ctx.send(get_text(guild_id, "blacklist_empty"))
            return
        
        if not word:
            await ctx.send(get_text(guild_id, "blacklist_usage"))
            return
        
        if action.lower() in ['add', 'thêm', '+']:
            data_manager.add_blacklist_word(guild_id, word)
            await ctx.send(get_text(guild_id, "blacklist_added", word=word))
        elif action.lower() in ['remove', 'xóa', '-', 'rm']:
            data_manager.remove_blacklist_word(guild_id, word)
            await ctx.send(get_text(guild_id, "blacklist_removed", word=word))
        else:
            await ctx.send(get_text(guild_id, "blacklist_usage"))
