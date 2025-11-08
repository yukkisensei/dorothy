"""
Dorothy Bot - Security Module
Comprehensive security features including anti-nuke, anti-raid, anti-spam, and auto-moderation
"""

import discord
import re
from datetime import datetime, timedelta
from typing import Optional, List, Dict
from config import (
    RAID_DETECTION_THRESHOLD, RAID_DETECTION_WINDOW, RAID_MIN_ACCOUNT_AGE,
    SPAM_MESSAGE_THRESHOLD, SPAM_TIME_WINDOW, SPAM_MENTION_THRESHOLD, SPAM_DUPLICATE_THRESHOLD,
    NUKE_BAN_THRESHOLD, NUKE_KICK_THRESHOLD, NUKE_DELETE_THRESHOLD, NUKE_ROLE_DELETE_THRESHOLD, NUKE_TIME_WINDOW,
    AUTO_MOD_CAPS_THRESHOLD, AUTO_MOD_CAPS_MIN_LENGTH, INVITE_PATTERNS, OWNER_IDS
)
from database import DataManager

class SecurityManager:
    """Manages all security features for the bot"""
    
    def __init__(self, bot, data_manager: DataManager):
        self.bot = bot
        self.data = data_manager
        
    # ==================== ANTI-RAID SYSTEM ====================
    async def check_raid(self, member: discord.Member) -> Optional[str]:
        """Check for potential raid attempts"""
        guild_id = str(member.guild.id)
        
        # Skip if anti-raid is disabled
        if not self.data.get_security_setting(guild_id, "anti_raid_enabled", True):
            return None
        
        # Track the join
        recent_joins = self.data.track_join(guild_id, str(member.id))
        
        # Count joins in the detection window
        now = datetime.now()
        window_start = now - timedelta(seconds=RAID_DETECTION_WINDOW)
        
        recent_count = 0
        for join in recent_joins:
            join_time = datetime.fromisoformat(join["timestamp"])
            if join_time >= window_start:
                recent_count += 1
        
        # Check if raid threshold exceeded
        if recent_count >= RAID_DETECTION_THRESHOLD:
            # Check account age
            account_age = (now - member.created_at).days
            
            if account_age < RAID_MIN_ACCOUNT_AGE:
                self.data.add_security_log(
                    guild_id,
                    "raid_detected",
                    {
                        "joins_in_window": recent_count,
                        "member_id": str(member.id),
                        "account_age_days": account_age
                    }
                )
                return f"⚠️ **RAID DETECTED!**\n{recent_count} joins in {RAID_DETECTION_WINDOW}s\nNew account detected (Age: {account_age} days)"
        
        return None
    
    async def handle_raid_member(self, member: discord.Member, reason: str):
        """Handle a member flagged as potential raider - Mute 7 days and notify admins"""
        from localization import get_text
        from utils import send_dm_notification
        from datetime import timedelta
        
        try:
            guild_id = str(member.guild.id)
            
            # Auto-mute for 7 days instead of kick
            try:
                mute_duration = timedelta(days=7)
                await member.timeout(mute_duration, reason=f"[AUTO] Raid Protection: {reason}")
                
                # Send DM to user
                action_text = get_text(guild_id, "action_muted_7days")
                extra_text = get_text(guild_id, "extra_raid_detected")
                await send_dm_notification(
                    member,
                    action_text,
                    f"[AUTO-RAID] {reason}",
                    member.guild.name,
                    extra_text,
                    guild_id
                )
            except Exception as e:
                print(f"Failed to mute raider: {e}")
            
            # Notify highest role members
            await self.notify_highest_role(
                member.guild,
                f"🛡️ **Raid Detected**\n"
                f"User: {member.mention} (`{member.id}`)\n"
                f"Reason: {reason}\n"
                f"Action: Auto-muted for 7 days"
            )
            
            return True
        except Exception as e:
            print(f"Failed to handle raid member: {e}")
            return False
    
    # ==================== ANTI-SPAM SYSTEM ====================
    async def check_spam(self, message: discord.Message) -> Optional[Dict]:
        """Check message for spam patterns"""
        if message.author.bot or not message.guild:
            return None
        
        guild_id = str(message.guild.id)
        user_id = str(message.author.id)
        
        # Skip if anti-spam is disabled or user is whitelisted
        if not self.data.get_security_setting(guild_id, "anti_spam_enabled", True):
            return None
        if self.data.is_whitelisted(guild_id, user_id):
            return None
        
        # Track the message
        recent_messages = self.data.track_message(guild_id, user_id, message.content)
        
        # Check mention spam
        if len(message.mentions) >= SPAM_MENTION_THRESHOLD:
            return {
                "type": "mention_spam",
                "reason": f"Mentioned {len(message.mentions)} users in one message",
                "severity": "high"
            }
        
        # Check message spam (frequency)
        now = datetime.now()
        window_start = now - timedelta(seconds=SPAM_TIME_WINDOW)
        
        spam_count = 0
        for msg in recent_messages:
            msg_time = datetime.fromisoformat(msg["timestamp"])
            if msg_time >= window_start:
                spam_count += 1
        
        if spam_count >= SPAM_MESSAGE_THRESHOLD:
            return {
                "type": "message_spam",
                "reason": f"Sent {spam_count} messages in {SPAM_TIME_WINDOW} seconds",
                "severity": "medium"
            }
        
        # Check duplicate messages
        if len(recent_messages) >= SPAM_DUPLICATE_THRESHOLD:
            last_messages = [msg["content"] for msg in recent_messages[-SPAM_DUPLICATE_THRESHOLD:]]
            if len(set(last_messages)) == 1 and message.content == last_messages[0]:
                return {
                    "type": "duplicate_spam",
                    "reason": f"Repeated the same message {SPAM_DUPLICATE_THRESHOLD} times",
                    "severity": "medium"
                }
        
        return None
    
    async def handle_spam(self, message: discord.Message, spam_info: Dict):
        """Handle detected spam - Auto mute 7 days and notify admins"""
        from localization import get_text
        from utils import send_dm_notification
        from datetime import timedelta
        
        try:
            guild_id = str(message.guild.id)
            
            # Delete the spam message
            await message.delete()
            
            # Auto-mute for 7 days
            try:
                mute_duration = timedelta(days=7)
                await message.author.timeout(mute_duration, reason=f"[AUTO-MOD] Spam detected: {spam_info['reason']}")
                
                # Send DM to user
                action_text = get_text(guild_id, "action_muted_7days")
                extra_text = get_text(guild_id, "extra_spam_detected")
                await send_dm_notification(
                    message.author,
                    action_text,
                    f"[AUTO-MOD] Spam: {spam_info['reason']}",
                    message.guild.name,
                    extra_text,
                    guild_id
                )
            except Exception as e:
                print(f"Failed to mute spammer: {e}")
            
            # Notify highest role members
            await self.notify_highest_role(
                message.guild,
                f"🚨 **Spam Detected**\n"
                f"User: {message.author.mention} (`{message.author.id}`)\n"
                f"Type: {spam_info['type']}\n"
                f"Reason: {spam_info['reason']}\n"
                f"Action: Auto-muted for 7 days"
            )
            
            # Log the spam
            self.data.add_security_log(
                guild_id,
                "spam_detected",
                {
                    "user_id": str(message.author.id),
                    "type": spam_info["type"],
                    "reason": spam_info["reason"],
                    "severity": spam_info["severity"],
                    "action": "muted_7days"
                }
            )
            
            # Clear spam tracking after punishment
            self.data.clear_spam_tracking(guild_id, str(message.author.id))
            
            return True
        except Exception as e:
            print(f"Failed to handle spam: {e}")
            return False
    
    # ==================== ANTI-NUKE SYSTEM ====================
    async def check_nuke_action(self, guild: discord.Guild, moderator: discord.Member, action_type: str) -> bool:
        """Check if moderation action is part of nuke attempt"""
        guild_id = str(guild.id)
        moderator_id = str(moderator.id)
        
        # Skip if anti-nuke is disabled
        if not self.data.get_security_setting(guild_id, "anti_nuke_enabled", True):
            return False
        
        # Skip if moderator is owner or whitelisted
        if moderator.id == guild.owner_id or moderator.id in OWNER_IDS:
            return False
        if self.data.is_whitelisted(guild_id, moderator_id):
            return False
        
        # Track the action
        recent_actions = self.data.track_moderation_action(guild_id, action_type, moderator_id)
        
        # Count actions in the detection window
        now = datetime.now()
        window_start = now - timedelta(seconds=NUKE_TIME_WINDOW)
        
        action_count = 0
        for action in recent_actions:
            if action["action"] == action_type:
                action_time = datetime.fromisoformat(action["timestamp"])
                if action_time >= window_start:
                    action_count += 1
        
        # Check thresholds based on action type
        threshold = 0
        if action_type == "ban":
            threshold = NUKE_BAN_THRESHOLD
        elif action_type == "kick":
            threshold = NUKE_KICK_THRESHOLD
        elif action_type == "channel_delete":
            threshold = NUKE_DELETE_THRESHOLD
        elif action_type == "role_delete":
            threshold = NUKE_ROLE_DELETE_THRESHOLD
        
        if action_count >= threshold:
            # NUKE DETECTED!
            self.data.add_security_log(
                guild_id,
                "nuke_attempt",
                {
                    "moderator_id": moderator_id,
                    "action_type": action_type,
                    "action_count": action_count,
                    "time_window": NUKE_TIME_WINDOW
                }
            )
            return True
        
        return False
    
    async def handle_nuke_attempt(self, guild: discord.Guild, moderator: discord.Member, action_type: str):
        """Handle detected nuke attempt"""
        try:
            # Remove all permissions from the nuker
            for role in moderator.roles:
                if role.permissions.administrator or role.permissions.ban_members or role.permissions.kick_members:
                    try:
                        await moderator.remove_roles(role, reason="[AUTO] Nuke attempt detected")
                    except:
                        pass
            
            # Timeout the nuker
            try:
                await moderator.timeout(timedelta(days=28), reason="[AUTO] Nuke attempt detected")
            except:
                pass
            
            # Send alert to owner
            owner = guild.owner
            if owner:
                try:
                    embed = discord.Embed(
                        title="🚨 NUKE ATTEMPT DETECTED!",
                        description=f"**{moderator.mention}** attempted to nuke the server!",
                        color=discord.Color.red(),
                        timestamp=datetime.now()
                    )
                    embed.add_field(name="Action Type", value=action_type, inline=True)
                    embed.add_field(name="Moderator", value=f"{moderator.mention} ({moderator.id})", inline=True)
                    embed.add_field(name="Auto-Response", value="✅ Removed permissions and timed out user", inline=False)
                    embed.set_footer(text="Dorothy Security System")
                    await owner.send(embed=embed)
                except:
                    pass
            
            # Send to security log channel if exists
            log_channel = discord.utils.get(guild.text_channels, name="security-log")
            if log_channel:
                embed = discord.Embed(
                    title="🚨 NUKE ATTEMPT BLOCKED",
                    description=f"**{moderator.mention}** attempted mass {action_type}",
                    color=discord.Color.red(),
                    timestamp=datetime.now()
                )
                embed.add_field(name="User", value=f"{moderator.mention} ({moderator.id})", inline=False)
                embed.add_field(name="Action", value=f"Attempted mass {action_type}", inline=False)
                embed.add_field(name="Response", value="Removed permissions and timed out", inline=False)
                await log_channel.send(embed=embed)
            
            return True
        except Exception as e:
            print(f"Failed to handle nuke attempt: {e}")
            return False
    
    # ==================== AUTO-MODERATION SYSTEM ====================
    async def check_auto_mod(self, message: discord.Message) -> Optional[Dict]:
        """Check message for auto-moderation triggers"""
        if message.author.bot or not message.guild:
            return None
        
        guild_id = str(message.guild.id)
        user_id = str(message.author.id)
        
        # Skip if auto-mod is disabled or user is whitelisted
        if not self.data.get_security_setting(guild_id, "auto_mod_enabled", True):
            return None
        if self.data.is_whitelisted(guild_id, user_id):
            return None
        
        content = message.content
        
        # Check for blacklisted words
        blacklist = self.data.get_blacklist_words(guild_id)
        content_lower = content.lower()
        for word in blacklist:
            if word in content_lower:
                return {
                    "type": "blacklisted_word",
                    "reason": f"Used blacklisted word: {word}",
                    "severity": "high"
                }
        
        # Check for invite links
        for pattern in INVITE_PATTERNS:
            if re.search(pattern, content):
                return {
                    "type": "invite_link",
                    "reason": "Posted Discord invite link",
                    "severity": "medium"
                }
        
        # Check for excessive caps
        if len(content) >= AUTO_MOD_CAPS_MIN_LENGTH:
            caps_count = sum(1 for c in content if c.isupper())
            caps_percentage = (caps_count / len(content)) * 100
            
            if caps_percentage >= AUTO_MOD_CAPS_THRESHOLD:
                return {
                    "type": "excessive_caps",
                    "reason": f"Message is {int(caps_percentage)}% caps",
                    "severity": "low"
                }
        
        return None
    
    async def handle_auto_mod(self, message: discord.Message, mod_info: Dict):
        """Handle auto-moderation trigger"""
        try:
            # Delete the message
            await message.delete()
            
            # Send warning
            warning_msg = await message.channel.send(
                f"⚠️ {message.author.mention} {mod_info['reason']}"
            )
            
            # Auto-delete warning after 5 seconds
            import asyncio
            await asyncio.sleep(5)
            try:
                await warning_msg.delete()
            except:
                pass
            
            # Give automatic warning for high severity
            if mod_info["severity"] == "high":
                from moderation import add_auto_warning
                await add_auto_warning(
                    message.guild,
                    message.author,
                    message.channel,
                    f"[AUTO-MOD] {mod_info['reason']}"
                )
            
            # Log the violation
            self.data.add_security_log(
                str(message.guild.id),
                "auto_mod_trigger",
                {
                    "user_id": str(message.author.id),
                    "type": mod_info["type"],
                    "reason": mod_info["reason"],
                    "severity": mod_info["severity"]
                }
            )
            
            return True
        except Exception as e:
            print(f"Failed to handle auto-mod: {e}")
            return False
    
    async def notify_highest_role(self, guild: discord.Guild, message: str):
        """Notify members with highest role about security event"""
        try:
            # Send to security-log channel
            security_channel = discord.utils.get(guild.text_channels, name="security-log")
            if security_channel:
                embed = discord.Embed(
                    title="🚨 Security Alert",
                    description=message,
                    color=discord.Color.red(),
                    timestamp=datetime.now()
                )
                embed.set_footer(text=f"Server: {guild.name}")
                try:
                    await security_channel.send(embed=embed)
                except:
                    pass
            
            # Get the highest role (excluding @everyone and bot roles)
            highest_role = None
            for role in sorted(guild.roles, key=lambda r: r.position, reverse=True):
                if role.name != "@everyone" and not role.is_bot_managed() and len(role.members) > 0:
                    highest_role = role
                    break
            
            if not highest_role:
                return
            
            # Send DM to all members with the highest role
            embed = discord.Embed(
                title="🚨 Security Alert",
                description=message,
                color=discord.Color.red(),
                timestamp=datetime.now()
            )
            embed.set_footer(text=f"Server: {guild.name}")
            
            for member in highest_role.members:
                if not member.bot:
                    try:
                        await member.send(embed=embed)
                    except:
                        pass  # Ignore if DM fails
        except Exception as e:
            print(f"Failed to notify highest role: {e}")
