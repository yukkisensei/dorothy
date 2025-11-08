"""
Dorothy Bot - Events Module
Handles all Discord events and security monitoring
"""

import discord
import os
from datetime import datetime
from discord.ext import commands, tasks
from typing import Optional
from database import DataManager
from security import SecurityManager
from doro_ai import analyze_simple, generate_doro_response
from utils import log_security_event
from config import BOT_NAME

# Global references
bot: Optional[commands.Bot] = None
data_manager: Optional[DataManager] = None
security_manager: Optional[SecurityManager] = None

def setup_events(bot_instance: commands.Bot, dm: DataManager, sm: SecurityManager):
    """Initialize events module with bot and managers"""
    global bot, data_manager, security_manager
    bot = bot_instance
    data_manager = dm
    security_manager = sm
    
    # Register events
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
        
        # Start presence update
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
                
                # Quick response with simple analysis
                sentiment = analyze_simple(content)
                response = generate_doro_response(sentiment, include_action=False)
                
                await message.channel.send(response)
                return
        
        # Security checks for guild messages
        if message.guild:
            # Check spam
            spam_info = await security_manager.check_spam(message)
            if spam_info:
                await security_manager.handle_spam(message, spam_info)
                await log_security_event(
                    message.guild,
                    "🚨 Spam Detected",
                    f"{message.author.mention} - {spam_info['reason']}",
                    discord.Color.orange()
                )
                return
            
            # Check auto-moderation
            mod_info = await security_manager.check_auto_mod(message)
            if mod_info:
                await security_manager.handle_auto_mod(message, mod_info)
                await log_security_event(
                    message.guild,
                    "🤖 Auto-Mod Triggered",
                    f"{message.author.mention} - {mod_info['reason']}",
                    discord.Color.red() if mod_info['severity'] == 'high' else discord.Color.orange()
                )
                return
        
        await bot.process_commands(message)
    
    @bot.event
    async def on_member_join(member: discord.Member):
        """Handle member join - check for raids"""
        raid_alert = await security_manager.check_raid(member)
        
        if raid_alert:
            # Potential raid detected
            await security_manager.handle_raid_member(member, raid_alert)
            
            # Alert in security log
            await log_security_event(
                member.guild,
                "🚨 RAID ALERT",
                f"Kicked {member.mention}\n{raid_alert}",
                discord.Color.red()
            )
    
    @bot.event
    async def on_member_ban(guild: discord.Guild, user: discord.User):
        """Monitor bans for nuke detection"""
        # Get ban entry to find who banned
        try:
            async for entry in guild.audit_logs(limit=1, action=discord.AuditLogAction.ban):
                if entry.target.id == user.id:
                    moderator = entry.user
                    
                    # Check for nuke attempt
                    is_nuke = await security_manager.check_nuke_action(guild, moderator, "ban")
                    
                    if is_nuke:
                        await security_manager.handle_nuke_attempt(guild, moderator, "ban")
                        await log_security_event(
                            guild,
                            "🚨 NUKE ATTEMPT BLOCKED",
                            f"{moderator.mention} attempted mass bans!",
                            discord.Color.dark_red()
                        )
                    break
        except:
            pass
    
    @bot.event
    async def on_member_remove(member: discord.Member):
        """Monitor kicks for nuke detection"""
        try:
            async for entry in member.guild.audit_logs(limit=1, action=discord.AuditLogAction.kick):
                if entry.target.id == member.id:
                    moderator = entry.user
                    
                    # Check for nuke attempt
                    is_nuke = await security_manager.check_nuke_action(member.guild, moderator, "kick")
                    
                    if is_nuke:
                        await security_manager.handle_nuke_attempt(member.guild, moderator, "kick")
                        await log_security_event(
                            member.guild,
                            "🚨 NUKE ATTEMPT BLOCKED",
                            f"{moderator.mention} attempted mass kicks!",
                            discord.Color.dark_red()
                        )
                    break
        except:
            pass
    
    @bot.event
    async def on_guild_channel_delete(channel: discord.abc.GuildChannel):
        """Monitor channel deletions for nuke detection"""
        try:
            async for entry in channel.guild.audit_logs(limit=1, action=discord.AuditLogAction.channel_delete):
                if entry.target.id == channel.id:
                    moderator = entry.user
                    
                    # Check for nuke attempt
                    is_nuke = await security_manager.check_nuke_action(channel.guild, moderator, "channel_delete")
                    
                    if is_nuke:
                        await security_manager.handle_nuke_attempt(channel.guild, moderator, "channel_delete")
                        await log_security_event(
                            channel.guild,
                            "🚨 NUKE ATTEMPT BLOCKED",
                            f"{moderator.mention} attempted mass channel deletion!",
                            discord.Color.dark_red()
                        )
                    break
        except:
            pass
    
    @bot.event
    async def on_guild_role_delete(role: discord.Role):
        """Monitor role deletions for nuke detection"""
        try:
            async for entry in role.guild.audit_logs(limit=1, action=discord.AuditLogAction.role_delete):
                if entry.target.id == role.id:
                    moderator = entry.user
                    
                    # Check for nuke attempt
                    is_nuke = await security_manager.check_nuke_action(role.guild, moderator, "role_delete")
                    
                    if is_nuke:
                        await security_manager.handle_nuke_attempt(role.guild, moderator, "role_delete")
                        await log_security_event(
                            role.guild,
                            "🚨 NUKE ATTEMPT BLOCKED",
                            f"{moderator.mention} attempted mass role deletion!",
                            discord.Color.dark_red()
                        )
                    break
        except:
            pass
    
    @bot.event
    async def on_command_error(ctx, error):
        """Handle command errors"""
        from localization import get_text
        guild_id = str(ctx.guild.id) if ctx.guild else "0"
        
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(get_text(guild_id, "error_missing_args", prefix=ctx.prefix))
        elif isinstance(error, commands.MemberNotFound):
            await ctx.send(get_text(guild_id, "error_member_not_found"))
        elif isinstance(error, commands.CheckFailure):
            await ctx.send(get_text(guild_id, "error_no_permission"))
        elif isinstance(error, commands.CommandNotFound):
            pass
        else:
            print(f"Error: {error}")
    
    @tasks.loop(seconds=30)
    async def update_presence():
        """Update bot presence with server count"""
        activity = discord.Activity(
            type=discord.ActivityType.watching,
            name=f"{len(bot.guilds)} servers",
            state="Protecting..."
        )
        await bot.change_presence(
            status=discord.Status.do_not_disturb,
            activity=activity
        )
    
    # Slash commands
    @bot.tree.command(name="help", description="Show help menu / Hiển thị menu trợ giúp")
    async def slash_help(interaction: discord.Interaction):
        from localization import get_text
        guild_id = str(interaction.guild.id) if interaction.guild else "0"
        
        embed = discord.Embed(
            title=get_text(guild_id, 'help_title'),
            description=get_text(guild_id, 'help_description'),
            color=discord.Color.blue()
        )
        
        if data_manager.get_language(guild_id) == "vi":
            cmd_text = "Gõ `-help` trong chat để xem chi tiết"
        else:
            cmd_text = "Type `-help` in chat for details"
        
        embed.add_field(name="📋 Commands / Lệnh", value=cmd_text, inline=False)
        await interaction.response.send_message(embed=embed, ephemeral=True)
    
    @bot.tree.command(name="setlanguage", description="Change bot language / Đổi ngôn ngữ bot")
    @discord.app_commands.describe(language="Choose language / Chọn ngôn ngữ")
    @discord.app_commands.choices(language=[
        discord.app_commands.Choice(name="🇬🇧 English", value="en"),
        discord.app_commands.Choice(name="🇻🇳 Tiếng Việt", value="vi")
    ])
    async def set_language(interaction: discord.Interaction, language: discord.app_commands.Choice[str]):
        from localization import get_text, get_language_name
        from config import OWNER_IDS
        
        # Check if user is admin
        owner_ids = OWNER_IDS if OWNER_IDS else []
        if not (interaction.user.guild_permissions.administrator or 
                interaction.user.id == interaction.guild.owner_id or
                interaction.user.id in owner_ids):
            await interaction.response.send_message(
                "❌ **English:** Only administrators can change the language!\n"
                "❌ **Tiếng Việt:** Chỉ quản trị viên mới có thể đổi ngôn ngữ!",
                ephemeral=True
            )
            return
        
        # Set language FIRST, then get text in new language
        guild_id = str(interaction.guild.id)
        data_manager.set_language(guild_id, language.value)
        
        # Send confirmation in new language
        lang_name = get_language_name(language.value)
        embed = discord.Embed(
            title=get_text(guild_id, "language_title"),
            description=get_text(guild_id, "language_changed", language=lang_name),
            color=discord.Color.green()
        )
        await interaction.response.send_message(embed=embed)
