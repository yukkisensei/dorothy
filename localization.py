"""
Dorothy Bot - Localization Module
Multi-language support system (English and Vietnamese)
"""

from typing import Dict, Any

# Language translations dictionary
TRANSLATIONS = {
    "en": {
        # Bot messages
        "bot_ready": "✅ Dorothy is ready!",
        "protecting_servers": "📊 Protecting {count} server(s)",
        "synced_commands": "✅ Synced {count} slash command(s)",
        "error_sync": "❌ Error syncing commands: {error}",
        
        # Security alerts
        "raid_detected": "⚠️ **RAID DETECTED!**\n{count} joins in {window}s\nNew account detected (Age: {age} days)",
        "spam_detected": "🚨 Spam Detected",
        "automod_triggered": "🤖 Auto-Mod Triggered",
        "nuke_blocked": "🚨 NUKE ATTEMPT BLOCKED",
        "nuke_alert": "🚨 NUKE ATTEMPT DETECTED!",
        "nuke_description": "**{user}** attempted to nuke the server!",
        "nuke_action_type": "Action Type",
        "nuke_moderator": "Moderator",
        "nuke_auto_response": "Auto-Response",
        "nuke_response_text": "✅ Removed permissions and timed out user",
        "nuke_attempt_mass": "**{user}** attempted mass {action}",
        "nuke_response_action": "Removed permissions and timed out",
        
        # Warning system
        "warning_auto": "⚠️ AUTOMATIC WARNING",
        "warning_title": "⚠️ WARNING",
        "warning_member": "👤 Member",
        "warning_count": "🔢 Warning Count",
        "warning_reason": "📝 Reason",
        "warning_stats": "📊 Warning Statistics",
        "warning_number": "⚠️ Warnings",
        "warning_next": "⏭️ Next Punishment",
        "warning_cleared": "✅ Cleared all warnings for {user}",
        "warning_none": "ℹ️ {user} has no warnings!",
        "warning_excessive": "🔨 {user} exceeded warning limit and has been banned!",
        
        # Moderation actions
        "timeout_title": "🔇 TIMEOUT",
        "kick_title": "👢 KICK",
        "ban_title": "🔨 BAN",
        "unban_title": "✅ UNBAN",
        "clear_success": "✅ Deleted {count} message(s)!",
        "channel_locked": "🔒 Channel {channel} has been locked!",
        "channel_unlocked": "🔓 Channel {channel} has been unlocked!",
        "slowmode_disabled": "✅ Slowmode disabled!",
        "slowmode_set": "✅ Set slowmode: {seconds} seconds!",
        "duration": "⏱️ Duration",
        "user": "👤 User",
        
        # Errors
        "error_self_warn": "❌ You cannot warn yourself!",
        "error_self_timeout": "❌ You cannot timeout yourself!",
        "error_self_kick": "❌ You cannot kick yourself!",
        "error_self_ban": "❌ You cannot ban yourself!",
        "error_bot_action": "❌ Cannot perform action on bots!",
        "error_no_permission": "❌ You don't have permission to use this command!",
        "error_missing_args": "❌ Missing parameters! Use `{prefix}help` for guide.",
        "error_member_not_found": "❌ Member not found!",
        "error_user_not_found": "❌ User not found with this ID!",
        "error_forbidden_timeout": "❌ No permission to timeout this member!",
        "error_forbidden_kick": "❌ No permission to kick this member!",
        "error_forbidden_ban": "❌ No permission to ban this member!",
        "error_forbidden_unban": "❌ No permission to unban!",
        "error_invalid_time": "❌ Invalid time format! Use: 5m, 1h, 2h30m, etc.",
        "error_invalid_amount": "❌ Amount must be between 1 and 100!",
        "error_invalid_slowmode": "❌ Slowmode must be between 0 and 21600 seconds (6 hours)!",
        "error_prefix_long": "❌ Prefix cannot be longer than 5 characters!",
        "error_message_not_found": "❌ Message not found with this ID!",
        "error_invalid_message_id": "❌ Invalid message ID!",
        
        # Info commands
        "help_title": "🛡️ Dorothy - Help Menu",
        "help_description": "Professional security bot with AI Dorothy\n**@Dorothy [message]** - Chat with Dorothy AI (doro doro!)",
        "help_warning_system": "⚠️ **Warning System**",
        "help_warning_desc": "`-warn @user [reason]` - Warn member\n`-warnings [@user]` - Check warnings\n`-clearwarns @user` - Clear warnings\n**Auto system:** 1-3: Warning | 4-7: Mute | 8: Kick | 9-10: Ban",
        "help_timeout": "🔇 **Timeout/Mute**",
        "help_timeout_desc": "`-timeout @user [time] [reason]` - Timeout member\n`-to @user [time]` - Short alias\n`-untimeout @user` - Remove timeout\n`-rto @user` - Short alias",
        "help_kickban": "🔨 **Kick/Ban**",
        "help_kickban_desc": "`-kick @user [reason]` - Kick member\n`-ban @user [reason]` - Ban member\n`-unban <user_id>` - Unban member",
        "help_security": "🛡️ **Security**",
        "help_security_desc": "`-security` - View security status\n`-antinuke [on/off]` - Anti-nuke protection\n`-antiraid [on/off]` - Anti-raid protection\n`-antispam [on/off]` - Anti-spam protection\n`-automod [on/off]` - Auto-moderation\n`-whitelist @user` - Add user to whitelist\n`-whitelistchannel [#channel]` - Add channel to whitelist (immune zone)\n`-blacklist [add/remove] <word>` - Manage blacklist",
        "help_utility": "🛠️ **Utility**",
        "help_utility_desc": "`-clear [amount]` - Delete messages\n`-lock [#channel]` - Lock channel\n`-unlock [#channel]` - Unlock channel\n`-slowmode [seconds]` - Set slowmode",
        "help_info": "📊 **Information**",
        "help_info_desc": "`-serverinfo` - Server info\n`-userinfo [@user]` - User info\n`-ping` - Check latency\n`-setprefix <prefix>` - Change prefix",
        "help_footer": "Dorothy v3.1 | Prefix: {prefix}",
        
        # Server info
        "serverinfo_title": "📊 Information for {name}",
        "serverinfo_id": "🆔 ID",
        "serverinfo_owner": "👑 Owner",
        "serverinfo_created": "📅 Created",
        "serverinfo_members": "👥 Members",
        "serverinfo_channels": "💬 Channels",
        "serverinfo_roles": "📜 Roles",
        "serverinfo_boost": "🎯 Boost Level",
        "serverinfo_boosts": "🚀 Boosts",
        
        # User info
        "userinfo_title": "👤 Information for {name}",
        "userinfo_id": "🆔 ID",
        "userinfo_username": "📛 Username",
        "userinfo_nickname": "🎭 Nickname",
        "userinfo_created": "📅 Account Created",
        "userinfo_joined": "📥 Joined Server",
        "userinfo_color": "🎨 Role Color",
        "userinfo_roles": "📜 Roles",
        "userinfo_warnings": "⚠️ Warnings",
        "userinfo_none": "None",
        
        # Ping
        "ping_title": "🏓 Pong!",
        "ping_latency": "Latency: **{ms}ms**",
        
        # Prefix
        "prefix_current": "📌 Current prefix: `{prefix}`\nUse: `{prefix}setprefix <prefix>` to change",
        "prefix_changed": "✅ Changed prefix to: `{prefix}`",
        
        # Security commands
        "security_title": "🛡️ Security Status",
        "security_antinuke": "🚫 Anti-Nuke",
        "security_antiraid": "🛡️ Anti-Raid",
        "security_antispam": "📢 Anti-Spam",
        "security_automod": "🤖 Auto-Mod",
        "security_on": "✅ On",
        "security_off": "❌ Off",
        "security_logs": "📋 Recent Logs",
        "security_footer": "Use -help to see security commands",
        
        # Security toggles
        "antinuke_current": "🚫 Anti-Nuke is currently: **{status}**\nUse: `-antinuke on/off`",
        "antinuke_enabled": "✅ **ENABLED** Anti-Nuke! Server is protected from nuke attacks.",
        "antinuke_disabled": "⚠️ **DISABLED** Anti-Nuke! Server is no longer protected from nuke attacks.",
        "antiraid_current": "🛡️ Anti-Raid is currently: **{status}**\nUse: `-antiraid on/off`",
        "antiraid_enabled": "✅ **ENABLED** Anti-Raid! Server is protected from raid attacks.",
        "antiraid_disabled": "⚠️ **DISABLED** Anti-Raid! Server is no longer protected from raids.",
        "antispam_current": "📢 Anti-Spam is currently: **{status}**\nUse: `-antispam on/off`",
        "antispam_enabled": "✅ **ENABLED** Anti-Spam! Bot will auto-detect spam.",
        "antispam_disabled": "⚠️ **DISABLED** Anti-Spam!",
        "automod_current": "🤖 Auto-Mod is currently: **{status}**\nUse: `-automod on/off`",
        "automod_enabled": "✅ **ENABLED** Auto-Moderation! Bot will auto-moderate content.",
        "automod_disabled": "⚠️ **DISABLED** Auto-Moderation!",
        "error_invalid_toggle": "❌ Use: `-{command} on` or `-{command} off`",
        
        # Whitelist
        "whitelist_usage": "❌ Use: `-whitelist @user [add/remove]`",
        "whitelist_added": "✅ Added {user} to whitelist! This user will not be affected by auto-mod.",
        "whitelist_removed": "✅ Removed {user} from whitelist!",
        
        # Channel Whitelist
        "whitelist_channel_usage": "❌ Use: `-whitelistchannel [#channel] [add/remove]`",
        "whitelist_channel_added": "✅ Added {channel} to whitelist! This channel is now an immune zone for security checks.",
        "whitelist_channel_removed": "✅ Removed {channel} from whitelist!",
        
        # Blacklist
        "blacklist_title": "📋 Blacklisted Words",
        "blacklist_empty": "ℹ️ No words in blacklist yet!",
        "blacklist_usage": "❌ Use: `-blacklist add/remove <word>`",
        "blacklist_added": "✅ Added word `{word}` to blacklist!",
        "blacklist_removed": "✅ Removed word `{word}` from blacklist!",
        
        # DM notifications
        "dm_title": "⚠️ Violation Notice",
        "dm_description": "You have been **{action}** in server **{server}**",
        "dm_reason": "📝 Reason",
        "dm_info": "ℹ️ Additional Info",
        "dm_footer": "Please follow server rules",
        "dm_no_reason": "No reason provided",
        
        # Action translations
        "action_warned": "warned {count}/10 times",
        "action_kicked": "kicked from server",
        "action_banned": "permanently banned",
        "action_timeout": "timed out for {duration}",
        "action_muted_7days": "muted for 7 days",
        "extra_rejoin": "You can rejoin if you have an invite link",
        "extra_cannot_rejoin": "You cannot rejoin this server",
        "extra_timeout_duration": "Mute duration: {duration}",
        "extra_spam_detected": "Automatic punishment for spam behavior",
        "extra_raid_detected": "Automatic punishment for raid behavior",
        "extra_nuke_detected": "Automatic punishment for nuke attempt",
        
        # Language
        "language_title": "🌐 Language Settings",
        "language_current": "Current language: **{language}**",
        "language_changed": "✅ Language changed to **{language}**!",
        "language_description": "Change the bot's language for this server",
        "language_option_name": "language",
        "language_option_desc": "Choose language",
        "language_english": "English",
        "language_vietnamese": "Tiếng Việt",
        
        # Log Channel
        "logchannel_title": "📋 Log Channel Settings",
        "logchannel_set": "✅ Log channel set to {channel}!\nAll moderation and security logs will be sent here.",
        "logchannel_current": "📋 Current log channel: {channel}\nUse `/logchannel #channel` to change it.",
        "logchannel_none": "ℹ️ No log channel set.\nUse `/logchannel #channel` to set one.",
        "logchannel_invalid": "⚠️ Log channel is set but the channel no longer exists.\nUse `/logchannel #channel` to set a new one.",
    },
    
    "vi": {
        # Bot messages
        "bot_ready": "✅ Dorothy đã sẵn sàng!",
        "protecting_servers": "📊 Đang bảo vệ {count} server",
        "synced_commands": "✅ Đã sync {count} slash command",
        "error_sync": "❌ Lỗi sync commands: {error}",
        
        # Security alerts
        "raid_detected": "⚠️ **PHÁT HIỆN RAID!**\n{count} lần join trong {window}s\nTài khoản mới phát hiện (Tuổi: {age} ngày)",
        "spam_detected": "🚨 Phát hiện Spam",
        "automod_triggered": "🤖 Auto-Mod Kích hoạt",
        "nuke_blocked": "🚨 ĐÃ CHẶN NỖ LỰC NUKE",
        "nuke_alert": "🚨 PHÁT HIỆN NỖ LỰC NUKE!",
        "nuke_description": "**{user}** đã cố phá hoại server!",
        "nuke_action_type": "Loại hành động",
        "nuke_moderator": "Người kiểm duyệt",
        "nuke_auto_response": "Phản hồi tự động",
        "nuke_response_text": "✅ Đã xóa quyền và timeout user",
        "nuke_attempt_mass": "**{user}** đã cố {action} hàng loạt",
        "nuke_response_action": "Đã xóa quyền và timeout",
        
        # Warning system
        "warning_auto": "⚠️ CẢNH BÁO TỰ ĐỘNG",
        "warning_title": "⚠️ CẢNH BÁO",
        "warning_member": "👤 Thành viên",
        "warning_count": "🔢 Lần cảnh báo",
        "warning_reason": "📝 Lý do",
        "warning_stats": "📊 Thống kê cảnh báo",
        "warning_number": "⚠️ Số cảnh báo",
        "warning_next": "⏭️ Hình phạt tiếp theo",
        "warning_cleared": "✅ Đã xóa toàn bộ cảnh báo của {user}",
        "warning_none": "ℹ️ {user} không có cảnh báo nào!",
        "warning_excessive": "🔨 {user} đã vượt quá giới hạn cảnh báo và bị ban!",
        
        # Moderation actions
        "timeout_title": "🔇 TIMEOUT",
        "kick_title": "👢 KICK",
        "ban_title": "🔨 BAN",
        "unban_title": "✅ UNBAN",
        "clear_success": "✅ Đã xóa {count} tin nhắn!",
        "channel_locked": "🔒 Kênh {channel} đã được khóa!",
        "channel_unlocked": "🔓 Kênh {channel} đã được mở khóa!",
        "slowmode_disabled": "✅ Đã tắt slowmode!",
        "slowmode_set": "✅ Đã đặt slowmode: {seconds} giây!",
        "duration": "⏱️ Thời gian",
        "user": "👤 User",
        
        # Errors
        "error_self_warn": "❌ Bạn không thể tự cảnh báo chính mình!",
        "error_self_timeout": "❌ Bạn không thể tự mute chính mình!",
        "error_self_kick": "❌ Bạn không thể tự kick chính mình!",
        "error_self_ban": "❌ Bạn không thể tự ban chính mình!",
        "error_bot_action": "❌ Không thể thực hiện hành động với bot!",
        "error_no_permission": "❌ Bạn không có quyền sử dụng lệnh này!",
        "error_missing_args": "❌ Thiếu tham số! Sử dụng `{prefix}help` để xem hướng dẫn.",
        "error_member_not_found": "❌ Không tìm thấy thành viên này!",
        "error_user_not_found": "❌ Không tìm thấy user với ID này!",
        "error_forbidden_timeout": "❌ Không có quyền timeout thành viên này!",
        "error_forbidden_kick": "❌ Không có quyền kick thành viên này!",
        "error_forbidden_ban": "❌ Không có quyền ban thành viên này!",
        "error_forbidden_unban": "❌ Không có quyền unban!",
        "error_invalid_time": "❌ Format thời gian không hợp lệ! Dùng: 5m, 1h, 2h30m, etc.",
        "error_invalid_amount": "❌ Số lượng phải từ 1 đến 100!",
        "error_invalid_slowmode": "❌ Slowmode phải từ 0 đến 21600 giây (6 giờ)!",
        "error_prefix_long": "❌ Prefix không được dài quá 5 ký tự!",
        "error_message_not_found": "❌ Không tìm thấy tin nhắn với ID này!",
        "error_invalid_message_id": "❌ ID tin nhắn không hợp lệ!",
        
        # Info commands
        "help_title": "🛡️ Dorothy - Menu Trợ giúp",
        "help_description": "Bot bảo mật chuyên nghiệp với AI Dorothy\n**@Dorothy [tin nhắn]** - Chat với Dorothy AI (doro doro!)",
        "help_warning_system": "⚠️ **Hệ thống Cảnh báo**",
        "help_warning_desc": "`-warn @user [lý do]` - Cảnh báo thành viên\n`-warnings [@user]` - Kiểm tra cảnh báo\n`-clearwarns @user` - Xóa cảnh báo\n**Tự động:** 1-3: Cảnh báo | 4-7: Mute | 8: Kick | 9-10: Ban",
        "help_timeout": "🔇 **Timeout/Mute**",
        "help_timeout_desc": "`-timeout @user [time] [lý do]` - Timeout thành viên\n`-to @user [time]` - Viết tắt\n`-untimeout @user` - Gỡ timeout\n`-rto @user` - Viết tắt",
        "help_kickban": "🔨 **Kick/Ban**",
        "help_kickban_desc": "`-kick @user [lý do]` - Kick thành viên\n`-ban @user [lý do]` - Ban thành viên\n`-unban <user_id>` - Unban thành viên",
        "help_security": "🛡️ **Bảo mật**",
        "help_security_desc": "`-security` - Xem trạng thái bảo mật\n`-antinuke [on/off]` - Chống nuke\n`-antiraid [on/off]` - Chống raid\n`-antispam [on/off]` - Chống spam\n`-automod [on/off]` - Tự động kiểm duyệt\n`-whitelist @user` - Thêm user vào whitelist\n`-whitelistchannel [#kênh]` - Thêm kênh vào whitelist (vùng miễn nhiễm)\n`-blacklist [add/remove] <từ>` - Quản lý blacklist",
        "help_utility": "🛠️ **Tiện ích**",
        "help_utility_desc": "`-clear [số]` - Xóa tin nhắn\n`-lock [#kênh]` - Khóa kênh\n`-unlock [#kênh]` - Mở khóa kênh\n`-slowmode [giây]` - Đặt slowmode",
        "help_info": "📊 **Thông tin**",
        "help_info_desc": "`-serverinfo` - Thông tin server\n`-userinfo [@user]` - Thông tin user\n`-ping` - Kiểm tra độ trễ\n`-setprefix <prefix>` - Đổi prefix",
        "help_footer": "Dorothy v3.1 | Prefix: {prefix}",
        
        # Server info
        "serverinfo_title": "📊 Thông tin {name}",
        "serverinfo_id": "🆔 ID",
        "serverinfo_owner": "👑 Chủ sở hữu",
        "serverinfo_created": "📅 Ngày tạo",
        "serverinfo_members": "👥 Thành viên",
        "serverinfo_channels": "💬 Kênh",
        "serverinfo_roles": "📜 Role",
        "serverinfo_boost": "🎯 Cấp Boost",
        "serverinfo_boosts": "🚀 Số Boost",
        
        # User info
        "userinfo_title": "👤 Thông tin {name}",
        "userinfo_id": "🆔 ID",
        "userinfo_username": "📛 Username",
        "userinfo_nickname": "🎭 Nickname",
        "userinfo_created": "📅 Tạo tài khoản",
        "userinfo_joined": "📥 Tham gia server",
        "userinfo_color": "🎨 Màu role",
        "userinfo_roles": "📜 Role",
        "userinfo_warnings": "⚠️ Cảnh báo",
        "userinfo_none": "Không có",
        
        # Ping
        "ping_title": "🏓 Pong!",
        "ping_latency": "Độ trễ: **{ms}ms**",
        
        # Prefix
        "prefix_current": "📌 Prefix hiện tại: `{prefix}`\nSử dụng: `{prefix}setprefix <prefix>` để thay đổi",
        "prefix_changed": "✅ Đã đổi prefix thành: `{prefix}`",
        
        # Security commands
        "security_title": "🛡️ Trạng Thái Bảo Mật",
        "security_antinuke": "🚫 Anti-Nuke",
        "security_antiraid": "🛡️ Anti-Raid",
        "security_antispam": "📢 Anti-Spam",
        "security_automod": "🤖 Auto-Mod",
        "security_on": "✅ Bật",
        "security_off": "❌ Tắt",
        "security_logs": "📋 Nhật ký gần đây",
        "security_footer": "Dùng -help để xem lệnh bảo mật",
        
        # Security toggles
        "antinuke_current": "🚫 Anti-Nuke hiện tại: **{status}**\nDùng: `-antinuke on/off`",
        "antinuke_enabled": "✅ Đã **BẬT** Anti-Nuke! Server được bảo vệ khỏi nuke attacks.",
        "antinuke_disabled": "⚠️ Đã **TẮT** Anti-Nuke! Server không còn được bảo vệ khỏi nuke attacks.",
        "antiraid_current": "🛡️ Anti-Raid hiện tại: **{status}**\nDùng: `-antiraid on/off`",
        "antiraid_enabled": "✅ Đã **BẬT** Anti-Raid! Server được bảo vệ khỏi raid attacks.",
        "antiraid_disabled": "⚠️ Đã **TẮT** Anti-Raid! Server không còn được bảo vệ khỏi raids.",
        "antispam_current": "📢 Anti-Spam hiện tại: **{status}**\nDùng: `-antispam on/off`",
        "antispam_enabled": "✅ Đã **BẬT** Anti-Spam! Bot sẽ tự động phát hiện spam.",
        "antispam_disabled": "⚠️ Đã **TẮT** Anti-Spam!",
        "automod_current": "🤖 Auto-Mod hiện tại: **{status}**\nDùng: `-automod on/off`",
        "automod_enabled": "✅ Đã **BẬT** Auto-Moderation! Bot sẽ tự động kiểm duyệt nội dung.",
        "automod_disabled": "⚠️ Đã **TẮT** Auto-Moderation!",
        "error_invalid_toggle": "❌ Sử dụng: `-{command} on` hoặc `-{command} off`",
        
        # Whitelist
        "whitelist_usage": "❌ Sử dụng: `-whitelist @user [add/remove]`",
        "whitelist_added": "✅ Đã thêm {user} vào whitelist! User này sẽ không bị ảnh hưởng bởi auto-mod.",
        "whitelist_removed": "✅ Đã xóa {user} khỏi whitelist!",
        
        # Channel Whitelist
        "whitelist_channel_usage": "❌ Sử dụng: `-whitelistchannel [#kênh] [add/remove]`",
        "whitelist_channel_added": "✅ Đã thêm {channel} vào whitelist! Kênh này trở thành vùng miễn nhiễm với các kiểm tra bảo mật.",
        "whitelist_channel_removed": "✅ Đã xóa {channel} khỏi whitelist!",
        
        # Blacklist
        "blacklist_title": "📋 Danh sách từ cấm",
        "blacklist_empty": "ℹ️ Chưa có từ nào trong blacklist!",
        "blacklist_usage": "❌ Sử dụng: `-blacklist add/remove <từ>`",
        "blacklist_added": "✅ Đã thêm từ `{word}` vào blacklist!",
        "blacklist_removed": "✅ Đã xóa từ `{word}` khỏi blacklist!",
        
        # DM notifications
        "dm_title": "⚠️ Thông Báo Vi Phạm",
        "dm_description": "Bạn đã bị **{action}** tại server **{server}**",
        "dm_reason": "📝 Lý do",
        "dm_info": "ℹ️ Thông tin thêm",
        "dm_footer": "Vui lòng tuân thủ quy định của server",
        "dm_no_reason": "Không có lý do",
        
        # Action translations
        "action_warned": "cảnh báo lần {count}/10",
        "action_kicked": "kick khỏi server",
        "action_banned": "ban vĩnh viễn",
        "action_timeout": "timeout {duration}",
        "action_muted_7days": "mute 7 ngày",
        "extra_rejoin": "Bạn có thể join lại server nếu có invite link",
        "extra_cannot_rejoin": "Bạn sẽ không thể join lại server này",
        "extra_timeout_duration": "Thời gian mute: {duration}",
        "extra_spam_detected": "Trừng phạt tự động do hành vi spam",
        "extra_raid_detected": "Trừng phạt tự động do hành vi raid",
        "extra_nuke_detected": "Trừng phạt tự động do cố gắng phá hoại server",
        
        # Language
        "language_title": "🌐 Cài đặt Ngôn ngữ",
        "language_current": "Ngôn ngữ hiện tại: **{language}**",
        "language_changed": "✅ Đã đổi ngôn ngữ sang **{language}**!",
        "language_description": "Thay đổi ngôn ngữ của bot cho server này",
        "language_option_name": "ngôn-ngữ",
        "language_option_desc": "Chọn ngôn ngữ",
        "language_english": "English",
        "language_vietnamese": "Tiếng Việt",
        
        # Log Channel
        "logchannel_title": "📋 Cài đặt Kênh Log",
        "logchannel_set": "✅ Đã đặt kênh log thành {channel}!\nTất cả log moderation và bảo mật sẽ được gửi vào đây.",
        "logchannel_current": "📋 Kênh log hiện tại: {channel}\nDùng `/logchannel #kênh` để thay đổi.",
        "logchannel_none": "ℹ️ Chưa đặt kênh log.\nDùng `/logchannel #kênh` để đặt.",
        "logchannel_invalid": "⚠️ Kênh log đã được đặt nhưng kênh không còn tồn tại.\nDùng `/logchannel #kênh` để đặt kênh mới.",
    }
}

def get_text(guild_id: str, key: str, **kwargs) -> str:
    """Get translated text for a guild"""
    from database import DataManager
    
    # Get data manager instance
    dm = DataManager()
    language = dm.get_language(guild_id)
    
    # Get translation
    if language in TRANSLATIONS and key in TRANSLATIONS[language]:
        text = TRANSLATIONS[language][key]
    else:
        # Fallback to English
        text = TRANSLATIONS["en"].get(key, key)
    
    # Format with kwargs if provided
    if kwargs:
        try:
            return text.format(**kwargs)
        except KeyError:
            return text
    return text

def get_language_name(lang_code: str) -> str:
    """Get language display name"""
    names = {
        "en": "English",
        "vi": "Tiếng Việt"
    }
    return names.get(lang_code, "English")
