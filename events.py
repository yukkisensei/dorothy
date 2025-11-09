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
        
        # Check DM spam
        if not message.guild:  # DM message
            user_id = str(message.author.id)
            
            # Check if user is blocked
            if data_manager.is_dm_blocked(user_id):
                return  # Ignore silently
            
            # Track DM
            from config import DM_SPAM_THRESHOLD, DM_SPAM_WINDOW
            dm_history = data_manager.track_message("0", user_id, message.content)
            
            # Check DM spam
            from datetime import datetime, timedelta
            now = datetime.now()
            window_start = now - timedelta(seconds=DM_SPAM_WINDOW)
            
            dm_count = 0
            for msg in dm_history:
                msg_time = datetime.fromisoformat(msg["timestamp"])
                if msg_time >= window_start:
                    dm_count += 1
            
            if dm_count >= DM_SPAM_THRESHOLD:
                # Block user permanently
                data_manager.block_dm_user(user_id, "DM Spam")
                try:
                    await message.author.send(
                        "⛔ **You have been blocked from DMing Dorothy**\n"
                        "Reason: Spam detected\n"
                        "\"Chúng ta không thuộc về nhau\" 💔"
                    )
                except:
                    pass
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
        
        # Check command spam before processing
        if message.content.startswith(data_manager.get_prefix(message.guild.id) if message.guild else '-'):
            from config import COMMAND_SPAM_THRESHOLD, COMMAND_SPAM_WINDOW
            from datetime import datetime, timedelta
            
            user_id = str(message.author.id)
            command_name = message.content.split()[0] if message.content.split() else ""
            
            # Track command
            cmd_history = data_manager.track_command(user_id, command_name)
            
            # Check command spam
            now = datetime.now()
            window_start = now - timedelta(seconds=COMMAND_SPAM_WINDOW)
            
            cmd_count = 0
            for cmd in cmd_history:
                cmd_time = datetime.fromisoformat(cmd["timestamp"])
                if cmd_time >= window_start:
                    cmd_count += 1
            
            if cmd_count >= COMMAND_SPAM_THRESHOLD:
                # Mute 7 days for command spam (KHÔNG BLOCK, chỉ mute trong server)
                if message.guild:
                    try:
                        from datetime import timedelta
                        mute_duration = timedelta(days=7)
                        await message.author.timeout(mute_duration, reason="[AUTO] Command Spam")
                        await message.channel.send(
                            f"🚨 {message.author.mention} đã bị mute 7 ngày do spam commands!"
                        )
                        data_manager.clear_command_tracking(user_id)
                    except:
                        pass
                return
        
        # Process commands
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
    
    # Command spam check decorator for slash commands
    async def check_slash_spam(interaction: discord.Interaction) -> bool:
        """Check if user is spamming slash commands"""
        from config import COMMAND_SPAM_THRESHOLD, COMMAND_SPAM_WINDOW
        from datetime import datetime, timedelta
        
        user_id = str(interaction.user.id)
        command_name = f"/{interaction.command.name}"
        
        # Track command
        cmd_history = data_manager.track_command(user_id, command_name)
        
        # Check command spam
        now = datetime.now()
        window_start = now - timedelta(seconds=COMMAND_SPAM_WINDOW)
        
        cmd_count = sum(1 for cmd in cmd_history if datetime.fromisoformat(cmd["timestamp"]) >= window_start)
        
        if cmd_count >= COMMAND_SPAM_THRESHOLD:
            # Mute 7 days for slash command spam (KHÔNG BLOCK, chỉ mute trong server)
            if interaction.guild:
                try:
                    mute_duration = timedelta(days=7)
                    await interaction.user.timeout(mute_duration, reason="[AUTO] Slash Command Spam")
                    await interaction.response.send_message(
                        f"🚨 Bạn đã bị mute 7 ngày do spam commands!",
                        ephemeral=True
                    )
                    data_manager.clear_command_tracking(user_id)
                    return True
                except:
                    pass
        return False
    
    # Slash commands
    @bot.tree.command(name="help", description="Show help menu / Hiển thị menu trợ giúp")
    async def slash_help(interaction: discord.Interaction):
        if await check_slash_spam(interaction):
            return
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
        if await check_slash_spam(interaction):
            return
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
    
    @bot.tree.command(name="logchannel", description="Set log channel for moderation & security / Đặt kênh log cho moderation & bảo mật")
    @discord.app_commands.describe(channel="Channel to send logs / Kênh để gửi log")
    async def set_log_channel(interaction: discord.Interaction, channel: discord.TextChannel = None):
        if await check_slash_spam(interaction):
            return
        from localization import get_text
        from config import OWNER_IDS
        
        # Check if user is admin
        owner_ids = OWNER_IDS if OWNER_IDS else []
        if not (interaction.user.guild_permissions.administrator or 
                interaction.user.id == interaction.guild.owner_id or
                interaction.user.id in owner_ids):
            await interaction.response.send_message(
                "❌ **English:** Only administrators can set log channel!\n"
                "❌ **Tiếng Việt:** Chỉ quản trị viên mới có thể đặt kênh log!",
                ephemeral=True
            )
            return
        
        guild_id = str(interaction.guild.id)
        
        # If no channel provided, show current setting
        if channel is None:
            current_channel_id = data_manager.get_log_channel(guild_id)
            if current_channel_id:
                current_channel = interaction.guild.get_channel(current_channel_id)
                if current_channel:
                    await interaction.response.send_message(
                        get_text(guild_id, "logchannel_current", channel=current_channel.mention),
                        ephemeral=True
                    )
                else:
                    await interaction.response.send_message(
                        get_text(guild_id, "logchannel_invalid"),
                        ephemeral=True
                    )
            else:
                await interaction.response.send_message(
                    get_text(guild_id, "logchannel_none"),
                    ephemeral=True
                )
            return
        
        # Set the log channel
        data_manager.set_log_channel(guild_id, channel.id)
        
        embed = discord.Embed(
            title=get_text(guild_id, "logchannel_title"),
            description=get_text(guild_id, "logchannel_set", channel=channel.mention),
            color=discord.Color.green()
        )
        await interaction.response.send_message(embed=embed)
