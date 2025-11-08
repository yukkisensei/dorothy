"""
Dorothy Bot - Database Module
Handles all data persistence and management
"""

import json
import os
from datetime import datetime
from typing import Dict, List, Optional, Any

class DataManager:
    """Manages all bot data including warnings, security settings, and configurations"""
    
    def __init__(self, filename="dorothy_data.json"):
        self.filename = filename
        self.data = self.load_data()
        # Create initial save if file doesn't exist
        if not os.path.exists(self.filename):
            self.save_data()
    
    def load_data(self) -> Dict:
        """Load data from JSON file"""
        if os.path.exists(self.filename):
            try:
                with open(self.filename, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                print(f"Error loading data: {e}")
                return self._get_default_structure()
        return self._get_default_structure()
    
    def _get_default_structure(self) -> Dict:
        """Return default data structure"""
        return {
            "warnings": {},
            "kicks": {},
            "bans": {},
            "mutes": {},
            "prefixes": {},
            "languages": {},
            "security": {
                "anti_raid_enabled": {},
                "anti_spam_enabled": {},
                "anti_nuke_enabled": {},
                "auto_mod_enabled": {},
                "whitelisted_users": {},
                "blacklisted_words": {},
                "trusted_roles": {},
                "security_logs": {}
            },
            "spam_tracking": {},
            "raid_tracking": {},
            "nuke_tracking": {},
            "dm_blocked_users": {},
            "command_spam_tracking": {}
        }
    
    def save_data(self):
        """Save data to JSON file"""
        try:
            with open(self.filename, 'w', encoding='utf-8') as f:
                json.dump(self.data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"Error saving data: {e}")
    
    # ==================== WARNING SYSTEM ====================
    def add_warning(self, guild_id: str, user_id: str, reason: str = "") -> int:
        """Add warning to user and return total warning count"""
        guild_id, user_id = str(guild_id), str(user_id)
        if guild_id not in self.data["warnings"]:
            self.data["warnings"][guild_id] = {}
        if user_id not in self.data["warnings"][guild_id]:
            self.data["warnings"][guild_id][user_id] = []
        
        warning_entry = {
            "timestamp": datetime.now().isoformat(),
            "count": len(self.data["warnings"][guild_id][user_id]) + 1,
            "reason": reason
        }
        self.data["warnings"][guild_id][user_id].append(warning_entry)
        self.save_data()
        return len(self.data["warnings"][guild_id][user_id])
    
    def get_warnings(self, guild_id: str, user_id: str) -> int:
        """Get total warning count for user"""
        guild_id, user_id = str(guild_id), str(user_id)
        if guild_id in self.data["warnings"] and user_id in self.data["warnings"][guild_id]:
            return len(self.data["warnings"][guild_id][user_id])
        return 0
    
    def clear_warnings(self, guild_id: str, user_id: str) -> bool:
        """Clear all warnings for user"""
        guild_id, user_id = str(guild_id), str(user_id)
        if guild_id in self.data["warnings"] and user_id in self.data["warnings"][guild_id]:
            del self.data["warnings"][guild_id][user_id]
            self.save_data()
            return True
        return False
    
    # ==================== PREFIX SYSTEM ====================
    def set_prefix(self, guild_id: str, prefix: str):
        """Set custom prefix for server"""
        guild_id = str(guild_id)
        self.data["prefixes"][guild_id] = prefix
        self.save_data()
    
    def get_prefix(self, guild_id: str) -> str:
        """Get custom prefix for server"""
        from config import PREFIX
        guild_id = str(guild_id)
        return self.data["prefixes"].get(guild_id, PREFIX)
    
    # ==================== SECURITY SETTINGS ====================
    def set_security_setting(self, guild_id: str, setting: str, enabled: bool):
        """Enable/disable security feature for server"""
        guild_id = str(guild_id)
        if guild_id not in self.data["security"][setting]:
            self.data["security"][setting][guild_id] = {}
        self.data["security"][setting][guild_id] = enabled
        self.save_data()
    
    def get_security_setting(self, guild_id: str, setting: str, default: bool = True) -> bool:
        """Get security setting for server"""
        guild_id = str(guild_id)
        if guild_id in self.data["security"][setting]:
            return self.data["security"][setting][guild_id]
        return default
    
    # ==================== WHITELIST SYSTEM ====================
    def add_whitelist(self, guild_id: str, user_id: str):
        """Add user to whitelist"""
        guild_id, user_id = str(guild_id), str(user_id)
        if guild_id not in self.data["security"]["whitelisted_users"]:
            self.data["security"]["whitelisted_users"][guild_id] = []
        if user_id not in self.data["security"]["whitelisted_users"][guild_id]:
            self.data["security"]["whitelisted_users"][guild_id].append(user_id)
            self.save_data()
    
    def remove_whitelist(self, guild_id: str, user_id: str):
        """Remove user from whitelist"""
        guild_id, user_id = str(guild_id), str(user_id)
        if guild_id in self.data["security"]["whitelisted_users"]:
            if user_id in self.data["security"]["whitelisted_users"][guild_id]:
                self.data["security"]["whitelisted_users"][guild_id].remove(user_id)
                self.save_data()
    
    def is_whitelisted(self, guild_id: str, user_id: str) -> bool:
        """Check if user is whitelisted"""
        guild_id, user_id = str(guild_id), str(user_id)
        if guild_id in self.data["security"]["whitelisted_users"]:
            return user_id in self.data["security"]["whitelisted_users"][guild_id]
        return False
    
    # ==================== BLACKLIST WORDS ====================
    def add_blacklist_word(self, guild_id: str, word: str):
        """Add word to server blacklist"""
        guild_id = str(guild_id)
        if guild_id not in self.data["security"]["blacklisted_words"]:
            self.data["security"]["blacklisted_words"][guild_id] = []
        word_lower = word.lower()
        if word_lower not in self.data["security"]["blacklisted_words"][guild_id]:
            self.data["security"]["blacklisted_words"][guild_id].append(word_lower)
            self.save_data()
    
    def remove_blacklist_word(self, guild_id: str, word: str):
        """Remove word from server blacklist"""
        guild_id = str(guild_id)
        if guild_id in self.data["security"]["blacklisted_words"]:
            word_lower = word.lower()
            if word_lower in self.data["security"]["blacklisted_words"][guild_id]:
                self.data["security"]["blacklisted_words"][guild_id].remove(word_lower)
                self.save_data()
    
    def get_blacklist_words(self, guild_id: str) -> List[str]:
        """Get all blacklisted words for server"""
        from config import DEFAULT_BLACKLIST
        guild_id = str(guild_id)
        server_blacklist = self.data["security"]["blacklisted_words"].get(guild_id, [])
        return list(set(DEFAULT_BLACKLIST + server_blacklist))
    
    # ==================== SPAM TRACKING ====================
    def track_message(self, guild_id: str, user_id: str, content: str) -> List[Dict]:
        """Track user message for spam detection"""
        guild_id, user_id = str(guild_id), str(user_id)
        
        if guild_id not in self.data["spam_tracking"]:
            self.data["spam_tracking"][guild_id] = {}
        if user_id not in self.data["spam_tracking"][guild_id]:
            self.data["spam_tracking"][guild_id][user_id] = []
        
        message_data = {
            "content": content,
            "timestamp": datetime.now().isoformat()
        }
        
        self.data["spam_tracking"][guild_id][user_id].append(message_data)
        
        # Keep only last 10 messages
        self.data["spam_tracking"][guild_id][user_id] = \
            self.data["spam_tracking"][guild_id][user_id][-10:]
        
        return self.data["spam_tracking"][guild_id][user_id]
    
    def clear_spam_tracking(self, guild_id: str, user_id: str):
        """Clear spam tracking for user"""
        guild_id, user_id = str(guild_id), str(user_id)
        if guild_id in self.data["spam_tracking"]:
            if user_id in self.data["spam_tracking"][guild_id]:
                del self.data["spam_tracking"][guild_id][user_id]
    
    # ==================== RAID TRACKING ====================
    def track_join(self, guild_id: str, user_id: str) -> List[Dict]:
        """Track user join for raid detection"""
        guild_id, user_id = str(guild_id), str(user_id)
        
        if guild_id not in self.data["raid_tracking"]:
            self.data["raid_tracking"][guild_id] = []
        
        join_data = {
            "user_id": user_id,
            "timestamp": datetime.now().isoformat()
        }
        
        self.data["raid_tracking"][guild_id].append(join_data)
        
        # Keep only last 50 joins
        self.data["raid_tracking"][guild_id] = \
            self.data["raid_tracking"][guild_id][-50:]
        
        return self.data["raid_tracking"][guild_id]
    
    # ==================== NUKE TRACKING ====================
    def track_moderation_action(self, guild_id: str, action_type: str, moderator_id: str) -> List[Dict]:
        """Track moderation actions for nuke detection"""
        guild_id, moderator_id = str(guild_id), str(moderator_id)
        
        if guild_id not in self.data["nuke_tracking"]:
            self.data["nuke_tracking"][guild_id] = {}
        if moderator_id not in self.data["nuke_tracking"][guild_id]:
            self.data["nuke_tracking"][guild_id][moderator_id] = []
        
        action_data = {
            "action": action_type,
            "timestamp": datetime.now().isoformat()
        }
        
        self.data["nuke_tracking"][guild_id][moderator_id].append(action_data)
        
        # Keep only last 20 actions
        self.data["nuke_tracking"][guild_id][moderator_id] = \
            self.data["nuke_tracking"][guild_id][moderator_id][-20:]
        
        return self.data["nuke_tracking"][guild_id][moderator_id]
    
    # ==================== SECURITY LOGS ====================
    def add_security_log(self, guild_id: str, log_type: str, details: Dict):
        """Add security log entry"""
        guild_id = str(guild_id)
        
        if guild_id not in self.data["security"]["security_logs"]:
            self.data["security"]["security_logs"][guild_id] = []
        
        log_entry = {
            "type": log_type,
            "timestamp": datetime.now().isoformat(),
            "details": details
        }
        
        self.data["security"]["security_logs"][guild_id].append(log_entry)
        
        # Keep only last 100 logs per server
        self.data["security"]["security_logs"][guild_id] = \
            self.data["security"]["security_logs"][guild_id][-100:]
        
        self.save_data()
    
    def get_security_logs(self, guild_id: str, limit: int = 10) -> List[Dict]:
        """Get recent security logs"""
        guild_id = str(guild_id)
        if guild_id in self.data["security"]["security_logs"]:
            return self.data["security"]["security_logs"][guild_id][-limit:]
        return []
    
    # ==================== LANGUAGE SYSTEM ====================
    def set_language(self, guild_id: str, language: str):
        """Set language for server"""
        guild_id = str(guild_id)
        self.data["languages"][guild_id] = language
        self.save_data()
    
    def get_language(self, guild_id: str) -> str:
        """Get language for server (default: en)"""
        guild_id = str(guild_id)
        return self.data["languages"].get(guild_id, "en")
    
    # ==================== DM BLOCK SYSTEM ====================
    def block_dm_user(self, user_id: str, reason: str = "DM Spam"):
        """Block user from DMing bot"""
        user_id = str(user_id)
        self.data["dm_blocked_users"][user_id] = {
            "timestamp": datetime.now().isoformat(),
            "reason": reason
        }
        self.save_data()
    
    def is_dm_blocked(self, user_id: str) -> bool:
        """Check if user is blocked from DMing bot"""
        user_id = str(user_id)
        return user_id in self.data["dm_blocked_users"]
    
    def unblock_dm_user(self, user_id: str):
        """Unblock user from DMing bot"""
        user_id = str(user_id)
        if user_id in self.data["dm_blocked_users"]:
            del self.data["dm_blocked_users"][user_id]
            self.save_data()
    
    # ==================== COMMAND SPAM TRACKING ====================
    def track_command(self, user_id: str, command_name: str) -> List[Dict]:
        """Track user command for spam detection"""
        user_id = str(user_id)
        
        if user_id not in self.data["command_spam_tracking"]:
            self.data["command_spam_tracking"][user_id] = []
        
        command_data = {
            "command": command_name,
            "timestamp": datetime.now().isoformat()
        }
        
        self.data["command_spam_tracking"][user_id].append(command_data)
        
        # Keep only last 10 commands
        self.data["command_spam_tracking"][user_id] = \
            self.data["command_spam_tracking"][user_id][-10:]
        
        return self.data["command_spam_tracking"][user_id]
    
    def clear_command_tracking(self, user_id: str):
        """Clear command tracking for user"""
        user_id = str(user_id)
        if user_id in self.data["command_spam_tracking"]:
            del self.data["command_spam_tracking"][user_id]
