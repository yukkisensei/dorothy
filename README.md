# Dorothy Discord Bot 🛡️

A professional security and moderation bot for Discord servers with AI-powered features and comprehensive protection systems.

## 🌟 Features

### 🤖 AI-Powered Dorothy Assistant
- Chat with Dorothy using AI sentiment analysis
- Natural "doro doro" responses with emotions
- Context-aware reactions based on message sentiment
- Powered by NVIDIA API with intelligent fallback

### 🛡️ Advanced Security Systems

#### Anti-Nuke Protection
- Detects and prevents server destruction attempts
- Monitors mass bans, kicks, channel deletions, and role deletions
- Automatic removal of permissions from attackers
- Real-time alerts to server owner
- Configurable thresholds for detection

#### Anti-Raid Protection
- Detects suspicious join patterns
- Monitors account age and join frequency
- Automatic kick of potential raiders
- Configurable detection windows and thresholds
- Whitelist system for trusted users

#### Anti-Spam Protection
- Message frequency monitoring
- Duplicate message detection
- Mention spam prevention
- Automatic warnings and punishments
- Smart tracking per user

#### Auto-Moderation
- Blacklisted word filtering
- Discord invite link blocking
- Excessive caps detection
- Customizable per-server blacklist
- Severity-based automatic actions

### ⚠️ Advanced Warning System
- Progressive punishment system (10 levels)
- Automatic actions based on warning count:
  - Level 1-3: Warning only
  - Level 4: 5-minute timeout
  - Level 5: 30-minute timeout
  - Level 6: 1-hour timeout
  - Level 7: 3-hour timeout
  - Level 8: Kick from server
  - Level 9-10: Permanent ban
- Warning history tracking with reasons
- Clear warnings command for second chances
- DM notifications to users

### 🔨 Moderation Tools
- **Timeout/Mute**: Temporary silence members with custom duration (supports 1h, 30m, 1h30m formats)
- **Kick**: Remove disruptive members from server
- **Ban/Unban**: Permanent removal with unban capability
- **Clear Messages**: Bulk delete messages (1-100)
- **Channel Lock/Unlock**: Emergency channel control
- **Slowmode**: Control message frequency
- **Say Command**: Bot speaks with optional reply function

### 📊 Information Commands
- Comprehensive server statistics
- Detailed user profiles with warning status
- Real-time ping monitoring
- Custom prefix per server
- Mod-log and security-log channel integration

### 🌐 Multi-Language Support
- Full English and Vietnamese language support
- Per-server language preferences
- Slash command `/setlanguage` for easy switching
- Admin-only language control
- All commands, messages, and embeds adapt to selected language

## 🚀 Quick Start

### Prerequisites
- Python 3.12.x (tested on 3.12.10)
- Discord Bot Token
- Administrator permissions in target server
- (Optional) NVIDIA API Key for AI features

### Installation

1. Clone or download the bot files
2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Create a `.env` file with your configuration:
```env
DISCORD_BOT_TOKEN=your_bot_token_here
OWNER_ID=your_discord_id_here
NVIDIA_API_KEY=your_nvidia_api_key_here  # Optional
```

4. Run the bot:
```bash
python main.py
```

### File Structure
```
dorothy/
├── main.py              # Main entry point
├── config.py            # Configuration and constants
├── database.py          # Data management and persistence
├── localization.py      # Multi-language support system
├── security.py          # Security features (anti-nuke, anti-raid, etc.)
├── moderation.py        # Moderation commands
├── info_commands.py     # Info and utility commands
├── security_commands.py # Security management commands
├── doro_ai.py          # AI sentiment analysis
├── events.py           # Discord event handlers
└── utils.py            # Helper functions
```

## 📝 Commands

### 🤖 AI Commands
- `@Dorothy [message]` - Chat with Dorothy AI (responds with "doro doro!")

### 🛡️ Security Commands
- `-security` - View security status and recent logs
- `-antinuke [on/off]` - Toggle anti-nuke protection
- `-antiraid [on/off]` - Toggle anti-raid protection
- `-antispam [on/off]` - Toggle anti-spam protection
- `-automod [on/off]` - Toggle auto-moderation
- `-whitelist @user [add/remove]` - Manage whitelist
- `-blacklist [add/remove] <word>` - Manage blacklisted words

### ⚠️ Warning System
- `-warn @user [reason]` - Issue warning
- `-warnings [@user]` - Check warning count
- `-clearwarns @user` - Reset warnings

### 🔇 Timeout Commands  
- `-timeout @user [time] [reason]` - Mute user (e.g., 5m, 1h, 2h30m)
- `-to @user [time]` - Short alias
- `-untimeout @user` - Remove timeout
- `-rto @user` - Short unmute alias

### 🔨 Kick/Ban Commands
- `-kick @user [reason]` - Kick member
- `-ban @user [reason]` - Ban member
- `-unban <user_id> [reason]` - Unban user
- `-rban <user_id>` - Short unban alias

### 🛠️ Utility Commands
- `-clear [amount]` - Delete messages (1-100)
- `-lock [#channel]` - Lock channel
- `-unlock [#channel]` - Unlock channel
- `-slowmode [seconds]` - Set slowmode (0-21600)
- `-say <content>` - Bot speaks
- `-say -r <msg_id> <content>` - Bot replies to message

### 📊 Information
- `-help` - Show all commands
- `-serverinfo` - Server details
- `-userinfo [@user]` - User information with warning status
- `-ping` - Check bot latency
- `-setprefix <prefix>` - Set custom prefix for server

### 🌐 Language (Slash Commands)
- `/setlanguage` - Change bot language (Admin only)
  - 🇬🇧 English
  - 🇻🇳 Tiếng Việt

## ⚙️ Configuration

### Environment Variables
Create a `.env` file in the root directory:
```env
DISCORD_BOT_TOKEN=your_token_here
OWNER_ID=your_discord_id
BOT_OWNER_IDS=id1,id2,id3  # Multiple owners (optional)
NVIDIA_API_KEY=your_nvidia_key  # Optional for AI features
DISCORD_WEBHOOK_URL=your_status_webhook  # Bot status notifications
DISCORD_WEBHOOK_SECURITY_URL=your_security_webhook  # Security alerts
```

### GitHub Actions Secrets
For deployment on GitHub Actions, add these secrets:
- `DISCORD_BOT_TOKEN` - Your bot token
- `OWNER_ID` - Your Discord user ID
- `DISCORD_WEBHOOK_URL` - Webhook for bot status (started/stopped/error)
- `DISCORD_WEBHOOK_SECURITY_URL` - Webhook for security alerts (spam/raid/nuke)

### Security Settings
All security features are enabled by default and can be toggled per server:
- Anti-Nuke: Prevents mass bans/kicks/deletions
- Anti-Raid: Blocks suspicious join patterns
- Anti-Spam: Monitors message frequency and duplicates
- Auto-Mod: Filters blacklisted words and links

### Customizing Security Thresholds
Edit `config.py` to adjust detection thresholds:
```python
RAID_DETECTION_THRESHOLD = 5  # Joins in time window
SPAM_MESSAGE_THRESHOLD = 5    # Messages in time window
NUKE_BAN_THRESHOLD = 3        # Multiple bans detected
```

### Customizing Warning Levels
Modify `WARNING_LEVELS` in `config.py`:
```python
WARNING_LEVELS = {
    1: {"action": "none", "duration": 0, "message": "Warning message"},
    # ... 10 levels total
}
```

### Log Channels
Create these channels for automatic logging:
- `mod-log` - Moderation actions (warns, kicks, bans)
- `security-log` - Security events (raids, spam, nuke attempts)

## 🔒 Permissions Required

The bot requires these Discord permissions:
- Manage Messages
- Manage Roles
- Kick Members
- Ban Members
- Timeout Members
- View Channels
- Send Messages
- Embed Links

## 🎯 Best Practices

1. **Set up log channels** - Create `mod-log` and `security-log` channels
2. **Configure role hierarchy** - Bot role must be above all managed roles
3. **Whitelist trusted staff** - Add moderators to whitelist to prevent false positives
4. **Test security features** - Test in a private server before production use
5. **Review security logs** - Regularly check `-security` command for alerts
6. **Configure thresholds** - Adjust detection thresholds based on server size
7. **Staff training** - Ensure moderators understand all security systems
8. **Regular maintenance** - Clear old warnings and review blacklist periodically

## 🐛 Troubleshooting

### Bot not responding to commands
- Check bot has message content intent enabled
- Verify correct command prefix (`-`)
- Ensure bot has necessary permissions

### Cannot timeout/kick/ban members
- Bot role must be higher than target member's highest role
- Bot cannot moderate server owner or members with admin permissions

### Commands showing permission errors
- User needs Manage Messages permission or be bot owner
- Some commands are owner-only (check documentation)

## 📚 Support

For issues or questions:
1. Check command syntax with `-help`
2. Verify bot permissions in server settings
3. Review error messages in console
4. Check Discord API status

## 🎨 Customization

This bot is designed for easy customization:
- Modify embed colors in command responses
- Change command prefixes in bot initialization
- Add custom commands by following existing patterns
- Adjust timeout durations and warning messages

## 🔧 Advanced Features

### Modular Architecture
Dorothy uses a modular design for easy maintenance and customization:
- **config.py** - All configuration constants
- **database.py** - JSON-based data persistence
- **security.py** - Core security algorithms
- **moderation.py** - Moderation command logic
- **doro_ai.py** - AI sentiment analysis
- **events.py** - Discord event monitoring

### Security Logging
All security events are logged with timestamps and details:
- Raid detection with account age
- Spam patterns and user tracking
- Nuke attempts with action counts
- Auto-mod triggers with severity levels

### Data Persistence
All data is stored in `dorothy_data.json`:
- Warning history per user
- Security settings per server
- Custom prefixes
- Whitelisted users
- Blacklisted words
- Security event logs

---

> **Note:** Dorothy is built with a modular architecture for easy customization. If you need help modifying features, AI assistants can help you navigate the codebase efficiently!

## 📄 License

This bot is provided as-is for personal and commercial use. Modify and distribute freely.

---
*Dorothy - Advanced Discord Security & Moderation Bot v3.0*
