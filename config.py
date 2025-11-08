"""
Dorothy Bot - Configuration Module
Contains all configuration settings, constants, and environment variables
"""

import os
from typing import List

# ==================== BOT CONFIGURATION ====================
BOT_NAME = "Dorothy"
VERSION = "3.0"
PREFIX = "-"

# ==================== OWNER CONFIGURATION ====================
default_owner_id = "1344312732278591500"
owner_id_str = os.getenv('BOT_OWNER_IDS', os.getenv('OWNER_ID', default_owner_id))

# Support multiple owner IDs
if ',' in owner_id_str:
    OWNER_IDS = [int(x.strip()) for x in owner_id_str.split(',') if x.strip().isdigit()]
    OWNER_ID = OWNER_IDS[0] if OWNER_IDS else int(default_owner_id)
else:
    OWNER_ID = int(owner_id_str) if owner_id_str.isdigit() else int(default_owner_id)
    OWNER_IDS = [OWNER_ID]

# ==================== API CONFIGURATION ====================
NVIDIA_API_KEY = os.getenv('NVIDIA_API_KEY', '')
NVIDIA_API_URL = "https://integrate.api.nvidia.com/v1/chat/completions"

# ==================== DORO AI PATTERNS ====================
doro_patterns = {
    "happy": ["doro!", "doro doro!", "doro~!", "doro doro~"],
    "sad": ["doro...", "...doro...", "doro……"],
    "confused": ["doro?", "doro doro?", "...doro?", "doro??"],
    "angry": ["doro!!", "DORO!", "doro doro!!"],
    "scared": ["do...doro...", "doro...!", "do do..."],
    "excited": ["doro doro!", "doro~!", "doro!! doro!!"],
    "neutral": ["doro", "doro~", "doro doro", "doro?"],
    "apologetic": ["doro do...", "do...doro...", "doro... doro..."],
    "sleepy": ["do...ro...", "doro... zzz...", "...doro..."],
    "curious": ["doro?", "doro doro?", "do? doro?"]
}

doro_actions = {
    "happy": ["*Dorothy nhảy nhót vui vẻ*", "*Dorothy vẫy tay hào hứng*", "*Dorothy cười toe toét*"],
    "sad": ["*Dorothy cúi đầu buồn bã*", "*Dorothy lau nước mắt*", "*Dorothy trông có vẻ buồn*"],
    "confused": ["*Dorothy nghiêng đầu*", "*Dorothy nhìn bạn chằm chằm*", "*Dorothy có vẻ bối rối*"],
    "angry": ["*Dorothy phồng má*", "*Dorothy giậm chân*", "*Dorothy trông có vẻ khó chịu*"],
    "scared": ["*Dorothy run rẩy*", "*Dorothy lùi lại*", "*Dorothy ẩn sau lưng bạn*"],
    "excited": ["*Dorothy nhảy lên*", "*Dorothy vỗ tay*", "*Dorothy quay tròn*"],
    "neutral": ["*Dorothy đứng yên*", "*Dorothy nhìn bạn*", "*Dorothy lắng nghe*"],
    "apologetic": ["*Dorothy cúi đầu xin lỗi*", "*Dorothy trông có lỗi*", "*Dorothy nhìn xuống đất*"],
    "sleepy": ["*Dorothy ngáp*", "*Dorothy dụi mắt*", "*Dorothy gục đầu*"],
    "curious": ["*Dorothy nhìn chăm chú*", "*Dorothy tiến lại gần*", "*Dorothy mắt sáng lên*"]
}

# ==================== WARNING SYSTEM ====================
WARNING_LEVELS = {
    1: {"action": "none", "duration": 0, "message": "⚠️ Cảnh báo lần 1: Vui lòng tuân thủ quy định!"},
    2: {"action": "none", "duration": 0, "message": "⚠️ Cảnh báo lần 2: Cẩn thận với hành vi của bạn!"},
    3: {"action": "none", "duration": 0, "message": "⚠️ Cảnh báo lần 3: Đây là lần cảnh báo cuối cùng!"},
    4: {"action": "timeout", "duration": 5, "message": "🔇 Cảnh báo lần 4: Bạn bị mute 5 phút!"},
    5: {"action": "timeout", "duration": 30, "message": "🔇 Cảnh báo lần 5: Bạn bị mute 30 phút!"},
    6: {"action": "timeout", "duration": 60, "message": "🔇 Cảnh báo lần 6: Bạn bị mute 1 giờ!"},
    7: {"action": "timeout", "duration": 180, "message": "🔇 Cảnh báo lần 7: Bạn bị mute 3 giờ!"},
    8: {"action": "kick", "duration": 0, "message": "👢 Cảnh báo lần 8: Bạn bị kick khỏi server!"},
    9: {"action": "ban", "duration": 0, "message": "🔨 Cảnh báo lần 9: Bạn bị ban 1 ngày!"},
    10: {"action": "ban", "duration": 0, "message": "🔨 Cảnh báo lần 10: Bạn bị ban vĩnh viễn!"}
}

# ==================== SECURITY CONFIGURATION ====================
# Anti-Raid Settings
RAID_DETECTION_THRESHOLD = 5  # Number of joins in time window
RAID_DETECTION_WINDOW = 10  # Seconds
RAID_MIN_ACCOUNT_AGE = 7  # Days

# Anti-Spam Settings
SPAM_MESSAGE_THRESHOLD = 5  # Messages in time window
SPAM_TIME_WINDOW = 5  # Seconds
SPAM_MENTION_THRESHOLD = 5  # Mentions in one message
SPAM_DUPLICATE_THRESHOLD = 3  # Same message repeated

# Anti-Nuke Settings
NUKE_BAN_THRESHOLD = 3  # Multiple bans in short time
NUKE_KICK_THRESHOLD = 3  # Multiple kicks in short time
NUKE_DELETE_THRESHOLD = 5  # Multiple channel deletes
NUKE_ROLE_DELETE_THRESHOLD = 3  # Multiple role deletes
NUKE_TIME_WINDOW = 10  # Seconds

# Auto-Moderation Settings
AUTO_MOD_CAPS_THRESHOLD = 70  # Percentage of caps
AUTO_MOD_CAPS_MIN_LENGTH = 10  # Minimum message length to check caps
AUTO_MOD_ENABLED_BY_DEFAULT = True

# Blacklisted words (expandable per server)
DEFAULT_BLACKLIST = [
    "nigga", "nigger", "nazi", "hitler",
    "faggot", "fag", "retard", "kys",
    # Add more as needed
]

# Invite link patterns
INVITE_PATTERNS = [
    r'discord\.gg/\w+',
    r'discord\.com/invite/\w+',
    r'discordapp\.com/invite/\w+',
]
