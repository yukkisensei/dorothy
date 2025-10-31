# DoSecurity Discord Bot 🛡️

A professional security and moderation bot for Discord servers with comprehensive management features.

## 🌟 Features

### ⚠️ Advanced Warning System
- Progressive punishment system (7 levels)
- Automatic actions based on warning count:
  - Level 1-2: Warning only
  - Level 3: 2-minute timeout
  - Level 4: 5-minute timeout 
  - Level 5: 10-minute timeout
  - Level 6: Kick from server
  - Level 7: Permanent ban
- Warning history tracking
- Clear warnings command for second chances

### 🔨 Moderation Tools
- **Timeout/Mute**: Temporary silence members with custom duration
- **Kick**: Remove disruptive members from server
- **Ban/Unban**: Permanent removal with unban capability
- **Clear Messages**: Bulk delete messages (1-100)
- **Channel Lock/Unlock**: Emergency channel control
- **Slowmode**: Control message frequency

### 📊 Information Commands
- Server statistics and information
- User profiles with warning status
- Real-time ping monitoring
- Mod-log channel integration

## 🚀 Quick Start

### Prerequisites
- Python 3.12+
- Discord Bot Token
- Administrator permissions in target server

### Installation

1. Clone or download the bot files
2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Configure your bot token in the main file or environment variable:
```python
TOKEN = 'YOUR_BOT_TOKEN_HERE'
```

4. Run the bot:
```bash
python dosecurity.py
```

## 📝 Commands

### Warning System
- `-warn @user [reason]` - Issue warning
- `-warnings [@user]` - Check warning count
- `-clearwarns @user` - Reset warnings

### Timeout Commands  
- `-timeout @user [minutes] [reason]` - Mute user
- `-to @user [minutes]` - Short alias
- `-untimeout @user` - Remove timeout
- `-rto @user` - Short unmute alias

### Kick/Ban Commands
- `-kick @user [reason]` - Kick member
- `-ban @user [reason]` - Ban member
- `-unban <user_id> [reason]` - Unban user
- `-rban <user_id>` - Short unban alias

### Utility Commands
- `-clear [amount]` - Delete messages
- `-lock [#channel]` - Lock channel
- `-unlock [#channel]` - Unlock channel
- `-slowmode [seconds]` - Set slowmode

### Information
- `-help` - Show all commands
- `-serverinfo` - Server details
- `-userinfo [@user]` - User information
- `-ping` - Check bot latency

## ⚙️ Configuration

### Setting Owner ID
Edit the `OWNER_ID` variable in the main file:
```python
OWNER_ID = 1344312732278591500  # Your Discord ID
```

### Customizing Warning Levels
Modify the `WARNING_LEVELS` dictionary to adjust punishments:
```python
WARNING_LEVELS = {
    1: {"action": "none", "duration": 0, "message": "Warning message"},
    # ... more levels
}
```

### Setting Mod Log Channel
Create a channel named `mod-log` for automatic logging of all moderation actions.

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

1. **Set up mod-log channel** for action tracking
2. **Configure role hierarchy** - Bot role should be above managed roles
3. **Test commands** in a private channel first
4. **Regular warning reviews** - Consider clearing old warnings periodically
5. **Staff training** - Ensure moderators understand the warning system

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

---

> **Note:** I've already modified this bot to be easily customizable. If you don't know how to customize it further, just give it to AI. If that fails... well, tough luck! 😈

## 📄 License

This bot is provided as-is for personal and commercial use. Modify and distribute freely.

---
*DoSecurity - Professional Discord Moderation*
