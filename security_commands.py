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
        """Hiển thị trạng thái bảo mật của server"""
        guild_id = str(ctx.guild.id)
        
        embed = discord.Embed(
            title="🛡️ Trạng Thái Bảo Mật",
            description=f"**{ctx.guild.name}**",
            color=discord.Color.blue(),
            timestamp=datetime.now()
        )
        
        # Get security settings
        anti_nuke = "✅ Bật" if data_manager.get_security_setting(guild_id, "anti_nuke_enabled", True) else "❌ Tắt"
        anti_raid = "✅ Bật" if data_manager.get_security_setting(guild_id, "anti_raid_enabled", True) else "❌ Tắt"
        anti_spam = "✅ Bật" if data_manager.get_security_setting(guild_id, "anti_spam_enabled", True) else "❌ Tắt"
        auto_mod = "✅ Bật" if data_manager.get_security_setting(guild_id, "auto_mod_enabled", True) else "❌ Tắt"
        
        embed.add_field(name="🚫 Anti-Nuke", value=anti_nuke, inline=True)
        embed.add_field(name="🛡️ Anti-Raid", value=anti_raid, inline=True)
        embed.add_field(name="📢 Anti-Spam", value=anti_spam, inline=True)
        embed.add_field(name="🤖 Auto-Mod", value=auto_mod, inline=True)
        
        # Get recent logs
        recent_logs = data_manager.get_security_logs(guild_id, limit=5)
        if recent_logs:
            log_text = "\n".join([f"• {log['type']}: {log['timestamp'][:10]}" for log in recent_logs])
            embed.add_field(name="📋 Nhật ký gần đây", value=log_text, inline=False)
        
        embed.set_footer(text="Sử dụng -help để xem các lệnh bảo mật")
        await ctx.send(embed=embed)
    
    @bot.command(name='antinuke', aliases=['an'])
    @has_admin_permissions()
    async def toggle_antinuke(ctx, status: str = None):
        """Bật/tắt Anti-Nuke"""
        if status is None:
            current = data_manager.get_security_setting(str(ctx.guild.id), "anti_nuke_enabled", True)
            await ctx.send(f"🚫 Anti-Nuke hiện tại: {'**BẬT**' if current else '**TẮT**'}\nDùng: `-antinuke on/off`")
            return
        
        if status.lower() in ['on', 'enable', 'bật', '1']:
            data_manager.set_security_setting(str(ctx.guild.id), "anti_nuke_enabled", True)
            await ctx.send("✅ Đã **BẬT** Anti-Nuke! Server được bảo vệ khỏi nuke attacks.")
        elif status.lower() in ['off', 'disable', 'tắt', '0']:
            data_manager.set_security_setting(str(ctx.guild.id), "anti_nuke_enabled", False)
            await ctx.send("⚠️ Đã **TẮT** Anti-Nuke! Server không còn được bảo vệ khỏi nuke attacks.")
        else:
            await ctx.send("❌ Sử dụng: `-antinuke on` hoặc `-antinuke off`")
    
    @bot.command(name='antiraid', aliases=['ar'])
    @has_admin_permissions()
    async def toggle_antiraid(ctx, status: str = None):
        """Bật/tắt Anti-Raid"""
        if status is None:
            current = data_manager.get_security_setting(str(ctx.guild.id), "anti_raid_enabled", True)
            await ctx.send(f"🛡️ Anti-Raid hiện tại: {'**BẬT**' if current else '**TẮT**'}\nDùng: `-antiraid on/off`")
            return
        
        if status.lower() in ['on', 'enable', 'bật', '1']:
            data_manager.set_security_setting(str(ctx.guild.id), "anti_raid_enabled", True)
            await ctx.send("✅ Đã **BẬT** Anti-Raid! Server được bảo vệ khỏi raid attacks.")
        elif status.lower() in ['off', 'disable', 'tắt', '0']:
            data_manager.set_security_setting(str(ctx.guild.id), "anti_raid_enabled", False)
            await ctx.send("⚠️ Đã **TẮT** Anti-Raid! Server không còn được bảo vệ khỏi raids.")
        else:
            await ctx.send("❌ Sử dụng: `-antiraid on` hoặc `-antiraid off`")
    
    @bot.command(name='antispam', aliases=['as'])
    @has_admin_permissions()
    async def toggle_antispam(ctx, status: str = None):
        """Bật/tắt Anti-Spam"""
        if status is None:
            current = data_manager.get_security_setting(str(ctx.guild.id), "anti_spam_enabled", True)
            await ctx.send(f"📢 Anti-Spam hiện tại: {'**BẬT**' if current else '**TẮT**'}\nDùng: `-antispam on/off`")
            return
        
        if status.lower() in ['on', 'enable', 'bật', '1']:
            data_manager.set_security_setting(str(ctx.guild.id), "anti_spam_enabled", True)
            await ctx.send("✅ Đã **BẬT** Anti-Spam! Bot sẽ tự động phát hiện spam.")
        elif status.lower() in ['off', 'disable', 'tắt', '0']:
            data_manager.set_security_setting(str(ctx.guild.id), "anti_spam_enabled", False)
            await ctx.send("⚠️ Đã **TẮT** Anti-Spam!")
        else:
            await ctx.send("❌ Sử dụng: `-antispam on` hoặc `-antispam off`")
    
    @bot.command(name='automod', aliases=['am'])
    @has_admin_permissions()
    async def toggle_automod(ctx, status: str = None):
        """Bật/tắt Auto-Moderation"""
        if status is None:
            current = data_manager.get_security_setting(str(ctx.guild.id), "auto_mod_enabled", True)
            await ctx.send(f"🤖 Auto-Mod hiện tại: {'**BẬT**' if current else '**TẮT**'}\nDùng: `-automod on/off`")
            return
        
        if status.lower() in ['on', 'enable', 'bật', '1']:
            data_manager.set_security_setting(str(ctx.guild.id), "auto_mod_enabled", True)
            await ctx.send("✅ Đã **BẬT** Auto-Moderation! Bot sẽ tự động kiểm duyệt nội dung.")
        elif status.lower() in ['off', 'disable', 'tắt', '0']:
            data_manager.set_security_setting(str(ctx.guild.id), "auto_mod_enabled", False)
            await ctx.send("⚠️ Đã **TẮT** Auto-Moderation!")
        else:
            await ctx.send("❌ Sử dụng: `-automod on` hoặc `-automod off`")
    
    @bot.command(name='whitelist', aliases=['wl'])
    @has_admin_permissions()
    async def whitelist_user(ctx, member: discord.Member = None, action: str = "add"):
        """Thêm/xóa user khỏi whitelist"""
        if member is None:
            await ctx.send("❌ Sử dụng: `-whitelist @user [add/remove]`")
            return
        
        guild_id = str(ctx.guild.id)
        user_id = str(member.id)
        
        if action.lower() in ['add', 'thêm', '+']:
            data_manager.add_whitelist(guild_id, user_id)
            await ctx.send(f"✅ Đã thêm {member.mention} vào whitelist! User này sẽ không bị ảnh hưởng bởi auto-mod.")
        elif action.lower() in ['remove', 'xóa', '-', 'rm']:
            data_manager.remove_whitelist(guild_id, user_id)
            await ctx.send(f"✅ Đã xóa {member.mention} khỏi whitelist!")
        else:
            # Toggle
            if data_manager.is_whitelisted(guild_id, user_id):
                data_manager.remove_whitelist(guild_id, user_id)
                await ctx.send(f"✅ Đã xóa {member.mention} khỏi whitelist!")
            else:
                data_manager.add_whitelist(guild_id, user_id)
                await ctx.send(f"✅ Đã thêm {member.mention} vào whitelist!")
    
    @bot.command(name='blacklist', aliases=['bl'])
    @has_admin_permissions()
    async def blacklist_word(ctx, action: str = None, *, word: str = None):
        """Quản lý danh sách từ cấm"""
        guild_id = str(ctx.guild.id)
        
        if action is None:
            # Show current blacklist
            blacklist = data_manager.get_blacklist_words(guild_id)
            if blacklist:
                word_list = ", ".join([f"`{w}`" for w in blacklist[:20]])
                if len(blacklist) > 20:
                    word_list += f"\n...và {len(blacklist) - 20} từ khác"
                embed = discord.Embed(
                    title="📋 Danh sách từ cấm",
                    description=word_list,
                    color=discord.Color.orange()
                )
                await ctx.send(embed=embed)
            else:
                await ctx.send("ℹ️ Chưa có từ nào trong blacklist!")
            return
        
        if not word:
            await ctx.send("❌ Sử dụng: `-blacklist add/remove <word>`")
            return
        
        if action.lower() in ['add', 'thêm', '+']:
            data_manager.add_blacklist_word(guild_id, word)
            await ctx.send(f"✅ Đã thêm từ `{word}` vào blacklist!")
        elif action.lower() in ['remove', 'xóa', '-', 'rm']:
            data_manager.remove_blacklist_word(guild_id, word)
            await ctx.send(f"✅ Đã xóa từ `{word}` khỏi blacklist!")
        else:
            await ctx.send("❌ Sử dụng: `-blacklist add/remove <word>`")
