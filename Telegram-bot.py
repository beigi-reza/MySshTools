#!/usr/bin/env python3
"""
Telegram Bot with Beautiful Emoji Menu
python-telegram-bot >= 20.x (async)
"""
import re
import copy
import os
from PIL import Image
import lib.BaseFunction as base
import logging
#from tunnel import TUNNEL_LIST,RefreshTunnelList
import TelegramBotFunction as BotFunc
import lib.Edit_or_Create as EditCreateFunc
from tunnel import RefreshTunnelList,DropAllSShTunnel,StartAllTunnel,SSHKEYDir,GetTunnelLogDetails,ClearTunnleLog
from pathlib import Path
import lib.ServiceManagmentHandler as SVM_HandlerFunc
from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    BotCommand,
)
from telegram.ext import (
    ApplicationBuilder,
    Application,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
    ConversationHandler,
    filters,
    MessageHandler,
)
from TelegramBotFunction import TelegramJsonConfig,TUNNEL_LIST



ADMIN_PERMISSION = TelegramJsonConfig.get('primession',{}).get('admin',[])
TELEGRAM_BOT_TOKEN = TelegramJsonConfig.get('bot_token','')
Telegram_STICKER = TelegramJsonConfig.get('stickers','')

TELEGRAM_BOT_TOKEN= '8339475059:AAHcclq2qcA3PLXB388Vqc-q-36q3jx2Y5g'
WAITING_FILE = 1
STANDARD_FIELDS_LIST = ["Name","sship","sshuser","sshport",'SourceServer','Sourceport',"FinalPort","MonitorPort"] 
msgHelp = """
Welcome to the Administration bot Token !
Here are some commands you can use:
/start - Show the main menu
/tunnels - List all SSH Tunnels
/help - Show this help message
"""

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)            

# ===============================================
#                  MENU FUNCTIONS
# ===============================================

def main_menu():   
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🦑 SSh Tunnel Managment", callback_data="tunnel_list")],
        [InlineKeyboardButton("🦡 Service Managment", callback_data="SVM.MainMenu")],
        #[InlineKeyboardButton("Ask Value", callback_data="ask_value")],        
    ])
    

        
    

def DynamicTunnelMenu(Backmenu=True,OnlyCreateNew=False):
    Menulist = []
    
    TunnelList = BotFunc.CreateTunnlListwithStatus()    
    if len(TunnelList) == 0:
        if OnlyCreateNew is True:
            Menulist.append([InlineKeyboardButton("✨ Create New Tunnel", callback_data=f"create_tunnel")])                    
            if Backmenu is True:
                Menulist.append([InlineKeyboardButton("⬅️ Back to Tunnel Menu", callback_data="back_main")])                         
            return InlineKeyboardMarkup(Menulist)
        return False
    
    for _t in TunnelList:
        tunnel = TunnelList[_t]
        Status = tunnel.get('status',None)
        IsActive = tunnel.get('is_active',True)
        if Status is None:
            EmojiStatus = '⁉️'
            Statusstr = ' ( Unknown )'

        if Status:
            EmojiStatus = '✅'
            Statusstr = ' ( Running )'
        else:
            EmojiStatus = ''
            Statusstr = ''
        if IsActive is False:
            EmojiStatus = '🚫'
            Statusstr = ' ( Disabled )'
            
        Menulist.append([InlineKeyboardButton(f"{EmojiStatus} {tunnel['Name']} {Statusstr}", callback_data=f"tunnel|{tunnel['Code']}")])        
    Menulist.append([InlineKeyboardButton("⏫ Start all tunnels", callback_data="StartAllTunnels"),
                    InlineKeyboardButton("⏬ Stop all tunnels", callback_data=f"StopAllTunnels")])
    Menulist.append([InlineKeyboardButton("✨ Create New Tunnel", callback_data=f"create_tunnel")])                    

    if Backmenu is True:
        Menulist.append([InlineKeyboardButton("⬅️ Back to Tunnel Menu", callback_data="back_main")])                         
    return InlineKeyboardMarkup(Menulist)

def TunnelActionMeny(TunnelDict='',_from=''):
    TunnelCode = TunnelDict["Code"]
    TunnelStatus = TunnelDict["status"]
    IsActive= TunnelDict.get('is_active',True)
    if _from == 'live_status':
        Call_BackData_restart = f"RestartTunnel_Live|{TunnelCode}"
    else:
        Call_BackData_restart = f"RestartTunnel_detail|{TunnelCode}"
    Menulist = []
    if IsActive:
        if TunnelStatus: 
            Menulist.append([InlineKeyboardButton(f" ⏹️ Stop Tunnel", callback_data=f"StopTunnel|{TunnelCode}")])
            Menulist.append([InlineKeyboardButton("🔃 Restart Tunnel", callback_data=Call_BackData_restart)])                        
        else:
            Menulist.append([InlineKeyboardButton(f" ▶️ Start Tunnel", callback_data=f"StartTunnel|{TunnelCode}")])
        Menulist.append([InlineKeyboardButton(f" 🚫 Disable Tunnel", callback_data=f"Edit_isActive|{TunnelCode}")])
    else:
         Menulist.append([InlineKeyboardButton(f" 🟢 Enable Tunnel", callback_data=f"Edit_isActive|{TunnelCode}")])
    
    Menulist.append([InlineKeyboardButton("✏️ Edit Tunnel", callback_data=f"EditTunnel|{TunnelCode}"),
                     InlineKeyboardButton("🗑️ Delete Tunnel", callback_data=f"DeleteConfirm|{TunnelCode}")])        
    Menulist.append([InlineKeyboardButton("🐞 Debug Tunnel", callback_data=f"DebugMenu|{TunnelCode}"),
                     InlineKeyboardButton("📄📄 Clone Tunnel", callback_data=f"CloneTunnel|{TunnelCode}")])        
    
    Menulist.append([InlineKeyboardButton("⬅️ Back to Tunnel List", callback_data="tunnel_list"),
                     InlineKeyboardButton("📃 Tunnel Status", callback_data=f"TunnelLiveStatus|{TunnelCode}")])
    return InlineKeyboardMarkup(Menulist)


def DebugTunnelMenu(TunnelCode='',TunnelIsRunning=False):
    Menulist = []
    if TunnelIsRunning:
        Menulist.append([InlineKeyboardButton("🐞 Restart Tunnel on Debug Mode", callback_data=f"DebugTunnel|{TunnelCode}"),
                         InlineKeyboardButton("⏹️ Stop Debug Mode", callback_data=f"StopTunnel|{TunnelCode}")])    
    else:
        Menulist.append([InlineKeyboardButton("🐞 Start Tunnel on Debug Mode", callback_data=f"DebugTunnel|{TunnelCode}")])
    Menulist.append([InlineKeyboardButton("📜 Get the last 20 lines of the log", callback_data=f"Last20Log|{TunnelCode}")])                    
    Menulist.append([InlineKeyboardButton("🐧 Tunnle Command", callback_data=f"TunnelCommand|{TunnelCode}")])                    
    Menulist.append([InlineKeyboardButton("📥 Download Full Tunnel Logs", callback_data=f"DownloadLogFile|{TunnelCode}"),
                     InlineKeyboardButton("🧹 Clear Tunnel Log", callback_data=f"ClearLog|{TunnelCode}")])    
    Menulist.append([InlineKeyboardButton("📥 Download Tunnel Config Json", callback_data=f"DowbloadAsJson|{TunnelCode}")]),
    Menulist.append([InlineKeyboardButton("⬅️ Back to Edit Menu", callback_data=f"tunnel|{TunnelCode}")])
    return InlineKeyboardMarkup(Menulist)

def AuthenticationMenu(TunnelCode=''):
    Menulist = []
    Menulist.append([InlineKeyboardButton("🔓 Usee Defualt Authentication", callback_data=f"Edit_Auth_SetAuthNone|{TunnelCode}")])
    Menulist.append([InlineKeyboardButton("📁 Enter Path of Private Key File", callback_data=f"Edit_Auth_SetAuthKeyfile|{TunnelCode}")])
    Menulist.append([InlineKeyboardButton("🗝️ Enter Private Key", callback_data=f"Edit_Auth_SetAuthPrivateKey|{TunnelCode}"),
                     InlineKeyboardButton("📤 Upload Private Key", callback_data=f"Edit_Auth_UploadKey|{TunnelCode}")])    
    Menulist.append([InlineKeyboardButton("🔐 Password Authentication", callback_data=f"Edit_Auth_SetAuthPass|{TunnelCode}")])    
    Menulist.append([InlineKeyboardButton("⬅️ Back to Edit Menu", callback_data=f"EditTunnel|{TunnelCode}"),
                     InlineKeyboardButton("ℹ️ Help", callback_data=f"HelpAuthMenu")])
    return InlineKeyboardMarkup(Menulist)     

def EditTunnelMenu(TunnelCode='',context=None):
    _tunnleList = RefreshTunnelList()
    changesDict = BotFunc.compare_dicts(dict1=_tunnleList[TunnelCode],dict2=context.user_data["tunnel_list"][TunnelCode],)        
    if context.user_data["tunnel_list"][TunnelCode].get('Keep_Alive',False) is True:
        KeepAliveStr = "❎ Keep Alive is Enabled"
    else:
        KeepAliveStr = "🔲 Keep Alive is Disabled"
    for _t in context.user_data['tunnel_list']:
        if TunnelCode == _t:
            TunnelDict = context.user_data['tunnel_list'][_t]
            break
    SSHIP = f"{TunnelDict.get('ssh_user','N/A')}@{TunnelDict.get('ssh_ip','N/A')}:{TunnelDict.get('ssh_port','N/A')}"
    loIp = f"{TunnelDict.get('Source_Server','N/A')}:{TunnelDict.get('Source_port','N/A')}"
    Menulist = []
    Menulist.append([InlineKeyboardButton(f"💡 Edit Name ({TunnelDict.get('Name','N/A')})", callback_data=f"Edit_Name|{TunnelCode}")])
    Menulist.append([InlineKeyboardButton(f"🔐 Edit Authentication ...", callback_data=f"AuthMenu|{TunnelCode}")])
    Menulist.append([InlineKeyboardButton(f"🔀 Change Type ({TunnelDict.get('Type','N/A')})", callback_data=f"ChageTypeMenu|{TunnelCode}")])
    Menulist.append([InlineKeyboardButton(f"🖥️ Edit SSH Server ({SSHIP})", callback_data=f"SshServerMenu|{TunnelCode}")])
    Menulist.append([InlineKeyboardButton(f"⚙️ Edit Source IP ({loIp})", callback_data=f"SourceServerMenu|{TunnelCode}")])
    Menulist.append([InlineKeyboardButton(f"🏁 Final Port ({TunnelDict.get('FinalPort','N/A')})", callback_data=f"Edit_FinalPort|{TunnelCode}")])    
    Menulist.append([InlineKeyboardButton(f"✨ Advance Configuration ... ", callback_data=f"AdvancedMenu|{TunnelCode}"),
                     InlineKeyboardButton(f"{KeepAliveStr}", callback_data=f"KeepAliveMenu|{TunnelCode}")])
    
    if len(changesDict) > 0:        
        Menulist.append([InlineKeyboardButton("💾 Apply & Save", callback_data=f"SaveChangeMenu")])
        Menulist.append([InlineKeyboardButton("⬅️ Back to Tunnel Details", callback_data=f"tunnel|{TunnelCode}")])
    else:
        Menulist.append([InlineKeyboardButton("⬅️ Back to Tunnel Details", callback_data=f"tunnel|{TunnelCode}")])
    
    return InlineKeyboardMarkup(Menulist)                    
                    
def SSHServerMenu(TunnelCode='',context=None):
    for _t in context.user_data['tunnel_list']:
        if TunnelCode == _t:
            TunnelDict = context.user_data['tunnel_list'][_t]
            break        
    Menulist= []
    Menulist.append([InlineKeyboardButton(f"💻 Change IP Address ({TunnelDict['ssh_ip']})", callback_data=f"Edit_sship|{TunnelCode}")])
    Menulist.append([InlineKeyboardButton(f"👤 Change SSH Username ({TunnelDict['ssh_user']})", callback_data=f"Edit_sshuser|{TunnelCode}")])
    Menulist.append([InlineKeyboardButton(f"🔌 Change SSH Server Port ({TunnelDict['ssh_port']})", callback_data=f"Edit_sshport|{TunnelCode}")])
    Menulist.append([InlineKeyboardButton(f"⬅️ Back to Edit Menu", callback_data=f"EditTunnel|{TunnelCode}")])
    return InlineKeyboardMarkup(Menulist)

def SourceServerMenu(TunnelCode='',context=None):
    for _t in context.user_data['tunnel_list']:
        if TunnelCode == _t:
            TunnelDict = context.user_data['tunnel_list'][_t]
            break        

    Menulist= []
    Menulist.append([InlineKeyboardButton(f"💻 Change Source IP Address\n({TunnelDict['Source_Server']})", callback_data=f"Edit_SourceServer|{TunnelCode}")])    
    Menulist.append([InlineKeyboardButton(f"🔌 Change Source Port\n({TunnelDict['Source_port']})", callback_data=f"Edit_Sourceport|{TunnelCode}")])
    Menulist.append([InlineKeyboardButton("⬅️ Back to Edit Menu", callback_data=f"EditTunnel|{TunnelCode}")])
    return InlineKeyboardMarkup(Menulist)

def AdvancedMenu(TunnelCode='',HighlyRestrictedNetworksDict ={}):
    if HighlyRestrictedNetworksDict.get('Enable',False):
        StatusStr = "❎  Highly Restricted Networks Mode is Enabled"
    else:
        StatusStr = "🔲 Highly Restricted Networks Mode is Disabled"

    if HighlyRestrictedNetworksDict.get('ExitOnForwardFailure',"no") == "yes":
        ExitOnForwardFailure = "❎ Kill tunnel if forward port fail"
 
    else:
        ExitOnForwardFailure = "🔲 Kill tunnel if forward port fail"
    ServerAliveInterval = HighlyRestrictedNetworksDict.get('ServerAliveInterval',1)
    ServerAliveCountMax = HighlyRestrictedNetworksDict.get('ServerAliveCountMax',1)
    MonitorPort = HighlyRestrictedNetworksDict.get('MonitorPort',0)
    
    if ServerAliveInterval == 0:
        ServerAliveIntervalTitle = "⚠️ Send alive packet is Disabled"
    else:
        ServerAliveIntervalTitle = f"Send alive packet every [ {ServerAliveInterval} ] seconds"

    if MonitorPort == 0:
        MonitorPortTitle = "Monitor Tunnel is Disabled"        
    else:
        MonitorPortTitle = f"Monitor Tunnel on port [ {MonitorPort} ]"        
    
    if ServerAliveCountMax == 0:
        ServerAliveCountMaxStr = "⚠️ kill Force tunnel on first alive packet fail"
    else:
        ServerAliveCountMaxStr = f"Kill the tunnel after [ {ServerAliveCountMax} ] Alive packet fails"

    Menulist= []
    Menulist.append([InlineKeyboardButton(StatusStr, callback_data=f"RestrictedMode|{TunnelCode}")])
    Menulist.append([InlineKeyboardButton(ExitOnForwardFailure, callback_data=f"ExitOnForwardFailureSelect|{TunnelCode}")])
    Menulist.append([InlineKeyboardButton(ServerAliveIntervalTitle, callback_data=f"SendAlivePacketMenu|{TunnelCode}")])
    Menulist.append([InlineKeyboardButton(ServerAliveCountMaxStr, callback_data=f"ServerAliveCountMaxMenu|{TunnelCode}")])
    Menulist.append([InlineKeyboardButton(MonitorPortTitle, callback_data=f"Edit_MonitorPort|{TunnelCode}")])
    Menulist.append([InlineKeyboardButton("⬅️ Back to edit menu", callback_data=f"EditTunnel|{TunnelCode}")])
    return InlineKeyboardMarkup(Menulist)

# ===============================================
#                  FUNCTIONS
# ===============================================

async def has_permission(context: ContextTypes.DEFAULT_TYPE,user_id=None):
    Access_Denied = True
    if user_id in ['',None]:
        Access_Denied = True
        
    for uid in ADMIN_PERMISSION:
        if str(user_id) == str(uid):
            Access_Denied = False
            break
    if Access_Denied is True:
        await context.bot.send_message(
            chat_id=user_id,
            text="🔐 Access is Denied. 🔐"
        )
        return False
    else:
        return True

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):    
            
        if 'tunnel_list' not in context.user_data:        
            context.user_data['tunnel_list'] = copy.deepcopy(BotFunc.CreateTunnlListwithStatus())
        
        userId = update.effective_user.id            
        if await has_permission(context=context,user_id=userId) is False:
            return
        await update.message.reply_text(
            "🦄 **Welcom To SSH Tunnel Managment**\n\n"
            "Select one of the menu options:",
            reply_markup=main_menu(),
            parse_mode="Markdown"
        )

async def helpmenu(update: Update, context: ContextTypes.DEFAULT_TYPE):    
    UserId = update.message.chat_id
    if await has_permission(context=context,user_id=UserId) is False:
        return
    await update.message.reply_text(msgHelp)


async def Fn_TunnelList(update: Update, context: ContextTypes.DEFAULT_TYPE,backmenu=False,UserId=''):

    if 'tunnel_list' not in context.user_data:        
        context.user_data['tunnel_list'] = copy.deepcopy(BotFunc.CreateTunnlListwithStatus())

    if UserId == '':
        UserId = update.effective_user.id
    if await has_permission(context=context,user_id=UserId) is False:
        return
    TunnelList = DynamicTunnelMenu(Backmenu=backmenu)
    if type(TunnelList) is bool and TunnelList is False:
        TunnelList = DynamicTunnelMenu(Backmenu=backmenu,OnlyCreateNew=True)
        StikerID = BotFunc.GetTelegramStickerID(StikerName='tunnel_not_found')
        await context.bot.send_sticker(
            chat_id=UserId,
            sticker=StikerID
        )
        await context.bot.send_message(
            chat_id=UserId,
            text="Create New Tunnel:\n\n",
            reply_markup=TunnelList,
            parse_mode="Markdown"
        )
        return
    StikerID = BotFunc.GetTelegramStickerID(StikerName='ssh-tunnel-boss')
    await context.bot.send_sticker(
        chat_id=UserId,
        sticker=StikerID
    )    
    await context.bot.send_message(
        chat_id=UserId,
        text="Select Tunnel or Create New Tunnel:\n\n",
        reply_markup=TunnelList,
        parse_mode="Markdown"
    )

async def FuEditMenu(query=None,context=None,TunnelInEdit='',UserId=''):
    StikerID = BotFunc.GetTelegramStickerID(StikerName='Edit_tunnel')
    if StikerID != None:
        await context.bot.send_sticker(
            chat_id=UserId,
            sticker=StikerID)

    await query.message.reply_text("Select one of the menu options:",
                                    reply_markup=EditTunnelMenu(TunnelCode=TunnelInEdit,context=context),
                                    parse_mode="Markdown")


async def FnAdvancedMenuHandler(update: Update, context: ContextTypes.DEFAULT_TYPE,query=None,data='',UserId=''):
        TunnelCode = data.split('|')[1]        
        StikerID = BotFunc.GetTelegramStickerID(StikerName='advanced_config')
        if StikerID != None:
            await context.bot.send_sticker(
                chat_id=UserId,
                sticker=StikerID)
        MsgLine = []
        MsgLine.append(f"🖥️ *تنظیمات پیشرفته تونل {TunnelCode} *\n\n")
        MsgLine.append(f"⚠️ با تنظبم درست  این پارامتر ها می توانید کارایی تونل را افزایش دهد و از رفتن اتصال به حالت روح 👻 جلوگیری کنید\n\n")
        MsgLine.append(f"ℹ️ حالت روح 👻 زمانی اتفاق می افتد که اتصال از نظر مبدا و مقصد باز است ولی در واقع ارتباط شبکه قطع شده است\n\n")
        MsgLine.append(f"ℹ️ اگر ارتباط تونل صدمه دیده باشد و پکت ها به درستی به مقصد نرسند می توانید با کنترل پکت های بررسی سلامت وضعیت تونل را کنترل کنید \n\n")
        Msg = ''.join(MsgLine)
        #Send Msg
        #await context.bot.send_message(text=Msg,chat_id=UserId,parse_mode="Markdown")
        HighlyRestrictedNetworksDict = context.user_data["tunnel_list"][TunnelCode].get('Highly_Restricted_Networks',{})            
        await query.message.reply_text(                       
            Msg,            
            reply_markup=AdvancedMenu(TunnelCode=TunnelCode,HighlyRestrictedNetworksDict=HighlyRestrictedNetworksDict),
            parse_mode="Markdown"
        )


async def Fn_GetTunnelLog(data='',context=None,UserId='',query=None):    
    TunnelCode = data.split('|')[1]    
    for _t in context.user_data['tunnel_list']:
        if TunnelCode == _t:
            TunnelDict = context.user_data['tunnel_list'][_t]
            break
    rst = BotFunc.getTunnelLogs(TunnelCode=TunnelCode)
    if TunnelDict.get('is_active',True) is True:
        if rst[0] is True:
            StikerID = BotFunc.GetTelegramStickerID(StikerName='SSH_Tunnel_Start')            
        else:
            StikerID = BotFunc.GetTelegramStickerID(StikerName='SSH_Tunnel_Stop')
    else:
        StikerID = BotFunc.GetTelegramStickerID(StikerName='SSH_Tunnel_Disabled')
    if StikerID != None:
        await context.bot.send_sticker(
            chat_id=UserId,
            sticker=StikerID)
    await query.message.reply_text(                        
        f"{rst[1]}\n",
        reply_markup=TunnelActionMeny(TunnelDict=TunnelDict,_from='live_status'),
        parse_mode="Markdown"
    )


async def Fn_DebugMenu(update: Update, context: ContextTypes.DEFAULT_TYPE,query=None,data='',UserId='',Massege='',TunnelIsRunning=False):
        TunnelCode = data.split('|')[1]
        TunnelName = context.user_data['tunnel_list'][TunnelCode]['Name']
        StikerID = BotFunc.GetTelegramStickerID(StikerName='SSH_debug_Tunnel')
        if StikerID != None:
            await context.bot.send_sticker(
                chat_id=UserId,
                sticker=StikerID)
        if Massege == '':
            Msg = f"🟥 Debug Menu for Tunnel ( {TunnelName} ) "
        else:
            Msg = Massege        
        await query.message.reply_text(                                   
            f"{Msg}",
            reply_markup=DebugTunnelMenu(TunnelCode=TunnelCode,TunnelIsRunning=TunnelIsRunning),
            parse_mode="Markdown"
        )

#
#async def TunnelListCommand(update: Update, context: ContextTypes.DEFAULT_TYPE):       
#    ## /OnIssue command handler
#    chat_id = update.message.chat_id
#    if await has_permission(user_id=chat_id,context=context) is False:
#        return
#    await Fn_TunnelListCommand(chat_id, context)


# ===============================================
#                  END FUNCTIONS
# ===============================================


async def Fn_TunnelDetailsMsg(TunnelCode='',context=None,update=None,query=None,UserId=''):
    #TunnelCode = data.split('|')[1]
    UserData = context.user_data
    Msg = BotFunc.GenerateTunnelStatusSummary(TunnelCode=TunnelCode,UserData=UserData)
    
    TunnelDict= BotFunc.GetTunnelStatusByCode(TunnelCode=TunnelCode)
    if TunnelDict.get('is_active',True) is True:
        StikerID = BotFunc.GetTelegramStickerID(StikerName='ssh_tunnel_details')    
    else:
        StikerID = BotFunc.GetTelegramStickerID(StikerName='SSH_Tunnel_Disabled')    
    await context.bot.send_sticker(
        chat_id=UserId,
        sticker=StikerID)
    await query.message.reply_text(
                        Msg,
                        reply_markup=TunnelActionMeny(TunnelDict=TunnelDict,_from="Details"),
                    )        


# ===============================================
#     HANDLERS (button_handler)
# ===============================================

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if 'tunnel_list' not in context.user_data:        
        context.user_data['tunnel_list'] = copy.deepcopy(BotFunc.CreateTunnlListwithStatus())

    query = update.callback_query
    await query.answer()
    data = query.data
    UserId = query.from_user.id
    if await has_permission(context=context,user_id=UserId) is False:
        return
    if data == "tunnel_list":
        query = update.callback_query
        await query.answer()        
        await Fn_TunnelList(update, context,backmenu=True)
    elif data == "back_main":        
        await query.edit_message_text("Select one of the menu options:", reply_markup=main_menu())        
    elif data.split('|')[0] == "EditTunnel":
        #await query.edit_message_text("", reply_markup=EditTunnelMenu(TunnelCode=data.split('|')[1]))
        await FuEditMenu(query=query,context=context,TunnelInEdit=data.split('|')[1],UserId=UserId)
    elif data.split('|')[0] == "tunnel":
        ###
        await Fn_TunnelDetailsMsg(context=context,update=update,query=query,TunnelCode=data.split('|')[1],UserId=UserId)

    elif data.split('|')[0] == "StartTunnel":
        ######### START TUNNEL ##############
        TunnelCode = data.split('|')[1]
        rst = BotFunc.GetTunnelStatusByCode(TunnelCode=TunnelCode)
        if rst.get('status',False) is True:
            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text=f"❌ Tunnel {rst.get('Name','')} is already running ❌")
            return
        rst = BotFunc.StartTunnelByCode(TunnelCode=TunnelCode)
        if rst[0] is True:
            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text=f"{rst[1]}")
            await Fn_TunnelDetailsMsg(context=context,update=update,query=query,TunnelCode=data.split('|')[1],UserId=UserId)
        else:
            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text=f"❌ Failed to start tunnel: ❌ \n ------\n{rst[1]}❌")
    elif data.split('|')[0] == "StopTunnel":
        ######### STOP TUNNEL ##############
        TunnelCode = data.split('|')[1]
        rst = BotFunc.GetTunnelStatusByCode(TunnelCode=TunnelCode)
        if rst.get('status',False) is False:
            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text=f"❌ Tunnel {rst.get('Name','')} is already stopped ❌")
            return
        rst = BotFunc.StopTunnelByCode(TunnelCode=TunnelCode)        
        if rst[0] is True:
            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text=f"{rst[1]}")
            await Fn_TunnelDetailsMsg(context=context,update=update,query=query,TunnelCode=data.split('|')[1],UserId=UserId)
        else:
            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text=f"❌ Failed to stop tunnel: ❌ \n ------\n{rst[1]}❌")
    
    elif data.split('|')[0] == "DeleteConfirm":
        ######### DELETE CONFIRM ##############
        StikerID = BotFunc.GetTelegramStickerID(StikerName='ssh_tunnel_delete')
        await context.bot.send_sticker(
            chat_id=UserId,
            sticker=StikerID)

        TunnelCode = data.split('|')[1]
        await query.message.reply_text(
            f"Are you sure you want to delete this tunnel?",
            reply_markup=EditCreateFunc.ConfirmationMenu(
                YesCallbackData=f"DeleteTunnel|{TunnelCode}",
                NoCallbackData=f"tunnel|{TunnelCode}",
                YesText="✅ Yes, Delete Tunnel ",
                NoText="❌ No, Cancel"                
            ),
            parse_mode="Markdown"
        )
    elif data.split('|')[0] == "AuthMenu":
        ######### AUTH MENU ##############
        TunnelCode = data.split('|')[1]        
        StikerID = BotFunc.GetTelegramStickerID(StikerName='change_authentication')
        await context.bot.send_sticker(
            chat_id=UserId,
            sticker=StikerID)
        await query.message.reply_text(                        
            f"🔐 Select Authentication Method for Tunnel ( {TunnelCode} ) ",
            reply_markup=AuthenticationMenu(TunnelCode=TunnelCode),
            parse_mode="Markdown"
        )
    elif data.split('|')[0] == "DeleteTunnel":
        ######### DELETE TUNNEL ##############
        TunnelCode = data.split('|')[1]        
        rst = BotFunc.DeleteTunnelByCode(TunnelCode=TunnelCode,UserData=context.user_data)
        if rst[0] is True:
            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text=f"{rst[1]}")
            await Fn_TunnelList(update, context,backmenu=True,UserId=UserId)
        else:
            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text=f"❌ Failed to delete tunnel: ❌")                
    elif data == 'HelpAuthMenu':
        ######### HELP AUTH MENU ##############
        HelpTextList = []
        HelpTextList.append("🔐 Authentication Methods:\n\n")
        HelpTextList.append("1. 🔓 Default Authentication\n")
        HelpTextList.append("   - Uses the system's default SSH keys or settings.\n\n")
        HelpTextList.append("2. 📁 Enter Path of Private Key File\n")
        HelpTextList.append("   - Specify the path to a private key file for authentication.\n")
        HelpTextList.append("   - Key file must exist on the server.\n\n")
        HelpTextList.append("3. 🗝️ Enter Private Key\n")
        HelpTextList.append("   - Directly enter the private key for authentication.\n")
        HelpTextList.append("   - Key file Saved in Server.\n\n")
        HelpTextList.append("4. 📤 Upload Private Key: Upload   \n")
        HelpTextList.append("   - Upload Private keyFile   \n")
        HelpTextList.append("   - Key file Saved in Server.\n\n")        
        HelpTextList.append("5. 🔐 Password Authentication")
        HelpTextList.append("   - Use a password for SSH authentication.\n")
        Msg = ''.join(HelpTextList)
        await context.bot.send_message(
            chat_id=UserId,
            text=Msg
        )
    elif data.split('|')[0] == "ResetAuth":
        TunnelInEdit = data.split('|')[1]
        context.user_data["awaiting_value"] = False  # Reset the flag                
        if context.user_data["tunnel_list"][TunnelInEdit].get('authentication',None) is not None:
            del context.user_data["tunnel_list"][TunnelInEdit]['authentication']
        if context.user_data["tunnel_list"][TunnelInEdit].get('password',None) is not None:
            del context.user_data["tunnel_list"][TunnelInEdit]['password']
        if context.user_data["tunnel_list"][TunnelInEdit].get('key_file',None) is not None:
            del context.user_data["tunnel_list"][TunnelInEdit]['key_file']                            
        context.user_data["FieldToEdit"] = ""  # Clear the field to edit                    
        #FiledChange = EditCreateFunc.DetectUserTunnelChanges(TunnelCode=TunnelInEdit,Fileds2Edit='authentication',New_Value=None)
        #if FiledChange is True:
        #    context.user_data["tunnel_list"][TunnelInEdit]['tunel_changed'] = True
        Msg = BotFunc.GenerateTunnelStatusSummary(TunnelCode=TunnelInEdit,UserData=context.user_data)            
        await context.bot.send_message(
            chat_id=UserId,
            text=Msg)
        #await context.bot.send_message(text="Select one of the menu options:"
        #                                    ,chat_id=UserId
        #                                    , reply_markup=EditTunnelMenu(TunnelCode=TunnelInEdit,context=context)
        #                                    ,parse_mode="Markdown")
        await FuEditMenu(query=query,context=context,TunnelInEdit=TunnelInEdit,UserId=UserId)        
        return
    elif data.split('|')[0].split('_')[0] == "Edit":
        ################# EDIT ###################
        tunnelCode= data.split('|')[1]
        FieldToEdit = data.split('|')[0].split('_')[1]
        context.user_data["awaiting_value"] = True
        context.user_data["FieldToEdit"] = FieldToEdit
        context.user_data["TunnelInEdit"] = tunnelCode
        if FieldToEdit == "Auth": # Handle Authentication Menu
            Action = data.split('_')[2].split('|')[0]    
            if Action != 'SetAuthNone':                
                if Action == 'UploadKey':                    
                    context.user_data["state"] = WAITING_FILE
                await EditCreateFunc.AuthenticateUserChange(user_id=UserId
                                                            ,context=context
                                                            ,DataInput=data
                                                            ,query=query)
            else:
                await context.bot.send_message(
                    chat_id=UserId,
                    text=f"Are you sure you want to reset Authentication ?",
                    reply_markup=EditCreateFunc.ConfirmationMenu(
                        YesCallbackData=f"ResetAuth|{tunnelCode}",
                        NoCallbackData="AuthMenu",
                        YesText="✅ Reset Authentication ",
                        NoText="❌ Cancel "


                    ),
                    parse_mode="Markdown"
                )
                context.user_data["awaiting_value"] = False  # Reset the flag
        elif FieldToEdit in STANDARD_FIELDS_LIST:
            await EditCreateFunc.StandardFieldUserChange(user_id=UserId
                                                        ,context=context
                                                        ,DataInput=data
                                                        ,query=query
                                                        ,tunnelCode=tunnelCode)    
        elif FieldToEdit == "isActive":            
            await EditCreateFunc.Edit_isActive(context=context,query=query,TunnelInEdit=tunnelCode,UserId=UserId)
            
        return
    elif data.split('|')[0]== "ChageTypeMenu":
        ######### CHANGE TYPE ##############
        await EditCreateFunc.ChangeTunnelType(data=data,context=context,UserId=UserId,query=query)
        return
    elif data.split('|')[0].split('_')[0] == "TypeMode":
        ######### SET TUNNEL TYPE ##############
        #EditCreateFunc.TunnelModeHandler(update=update,contex''t=context,DataInput=data,UserId=UserId,query=query)
        FileldToEdit = 'Type'
        TunnelInEdit = data.split('|')[1]
        Mode = data.split('|')[0].split('_')[1]
        if Mode == 'local':
            NewType = 'local'
        elif Mode == 'Remote':
            NewType = 'remote'
        elif Mode == 'Dynamic': 
            NewType = 'dynamic' 
        context.user_data["tunnel_list"][TunnelInEdit][FileldToEdit] = NewType  # Save the value
        context.user_data["FieldToEdit"] = ""  # Clear the field to edit            
        #await query.edit_message_text("Select one of the menu options:", reply_markup=EditTunnelMenu(TunnelCode=TunnelInEdit))            
        #FiledChange = EditCreateFunc.DetectUserTunnelChanges(TunnelCode=TunnelInEdit,Fileds2Edit=FileldToEdit,New_Value=NewType)
        #if FiledChange is True:
        #    context.user_data["tunnel_list"][TunnelInEdit]['tunel_changed'] = True
        Msg = BotFunc.GenerateTunnelStatusSummary(TunnelCode=TunnelInEdit,UserData=context.user_data)            
        await context.bot.send_message(
            chat_id=UserId,
            text=Msg)
        #await query.message.reply_text("Select one of the menu options:", reply_markup=EditTunnelMenu(TunnelCode=TunnelInEdit,context=context),parse_mode="Markdown")
        await FuEditMenu(query=query,context=context,TunnelInEdit=TunnelInEdit,UserId=UserId)                
        return
    elif data.split('|')[0] == "SshServerMenu":    
        ######### SSH SERVER MENU ##############
        TunnelCode = data.split('|')[1]        
        StikerID = BotFunc.GetTelegramStickerID(StikerName='change_ssh_config')
        if StikerID != None:
            await context.bot.send_sticker(
                chat_id=UserId,
                sticker=StikerID)
        await query.message.reply_text(                        
            f"🖥️ Edit SSH Server Settings for Tunnel ( {TunnelCode} )\n\n",            
            reply_markup=SSHServerMenu(TunnelCode=TunnelCode,context=context),
            parse_mode="Markdown"
        )
        return
    elif data.split('|')[0] == "SourceServerMenu":
        ######### SOURCE SERVER MENU ##############
        TunnelCode = data.split('|')[1]        
        StikerID = BotFunc.GetTelegramStickerID(StikerName='change_Source_config')
        if StikerID != None:
            await context.bot.send_sticker(
                chat_id=UserId,
                sticker=StikerID)
        await query.message.reply_text(                        
            f"🖥️ Edit Source Address Settings for Tunnel ( {TunnelCode} )\n\n",
            reply_markup=SourceServerMenu(TunnelCode=TunnelCode,context=context),
            parse_mode="Markdown"
        )
        return
    elif data.split('|')[0] == "AdvancedMenu":
        # SOURCE SERVER MENU
        await FnAdvancedMenuHandler(update=update,context=context,query=query,data=data,UserId=UserId)
        return
    elif data.split('|')[0] == "RestrictedMode":
        # RESTRICTED MODE Chahe Status Select
        await EditCreateFunc.RestrictedModeConfirm(user_id=UserId,context=context,query=query,TunnelCode=data.split('|')[1])
    elif data.split('|')[0].split('_')[0] == "RestrictedMode":        
        await EditCreateFunc.RestrictedModeChange(data=data,context=context)
        await FnAdvancedMenuHandler(update=update,context=context,query=query,data=data,UserId=UserId)
    elif data.split('|')[0] == "ExitOnForwardFailureSelect":
        # EXIT ON FORWARD FAILURE CHANGE CONFIRM
        await EditCreateFunc.ExitOnForwardFailureConfirm(data=data,context=context,query=query)
    elif data.split('|')[0].split('_')[0] == "ExitOnForwardFailure":
        # EXIT ON FORWARD FAILURE CHANGE CONFIRM
        await EditCreateFunc.ExitOnForwardFailureChange(data=data,context=context)
        await FnAdvancedMenuHandler(update=update,context=context,query=query,data=data,UserId=UserId)
    elif data.split('|')[0] == "SendAlivePacketMenu":
        # SEND ALIVE PACKET MENU
        await EditCreateFunc.SendAlivePacketMenuHandler(data=data,context=context,query=query,UserId=UserId)
    elif data.split('|')[0].split('_')[0] == "SetExitOnForwardFailure":
        TunnelCode = data.split('|')[1]
        # Get All Send Alive Packet Value
        Value = data.split('|')[0].split('_')[1]        
        ValueInt = int(Value)
        context.user_data["tunnel_list"][TunnelCode]["Highly_Restricted_Networks"]["ServerAliveInterval"] = ValueInt        
        SuccessMsg = f"✅ Send Alive Packet Interval set to [ {ValueInt} ] seconds successfully. for Tunnel ( {data.split('|')[1]} )"
        await query.message.reply_text(SuccessMsg,parse_mode="Markdown")        
        await FnAdvancedMenuHandler(update=update,context=context,query=query,data=data,UserId=UserId)
    elif data.split('|')[0] == "ServerAliveCountMaxMenu":
        # SERVER ALIVE COUNT MAX MENU
        await EditCreateFunc.ServerAliveCountMaxMenuHandler(data=data,context=context,query=query,UserId=UserId)
    elif data.split('|')[0].split('_')[0] == "SetServerAliveCountMax":
        TunnelCode = data.split('|')[1]
        # Get All Send Alive Packet Value
        Value = data.split('|')[0].split('_')[1]        
        ValueInt = int(Value)
        context.user_data["tunnel_list"][TunnelCode]["Highly_Restricted_Networks"]["ServerAliveCountMax"] = ValueInt        
        SuccessMsg = f"✅ Send Alive Packet Interval set to [ {ValueInt} ] seconds successfully. for Tunnel ( {data.split('|')[1]} )"
        await query.message.reply_text(SuccessMsg,parse_mode="Markdown")        
        await FnAdvancedMenuHandler(update=update,context=context,query=query,data=data,UserId=UserId)
    elif data.split('|')[0] == "KeepAliveMenu":
        ######### KEEP ALIVE MENU ##############
        TunnelCode = data.split('|')[1]        
        StikerID = BotFunc.GetTelegramStickerID(StikerName='Keep_Alive_Service')
        if StikerID != None:
            await context.bot.send_sticker(
                chat_id=UserId,
                sticker=StikerID)
        await EditCreateFunc.KeepAliveToggleHandler(context=context,query=query,data=data,UserId=UserId)    
    elif data.split('|')[0].split('_')[0] == "KeepAliveServer":
        ######### KEEP ALIVE SET ##############
        TunnelCode = data.split('|')[1]        
        NewValue = data.split('|')[0].split('_')[1]        
        UserId = query.from_user.id
        if NewValue.lower() == 'enable':
            KeepAliveValue = True
        else:
            KeepAliveValue = False
        context.user_data["tunnel_list"][TunnelCode]["Keep_Alive"] = KeepAliveValue        
        SuccessMsg = f"✅ Keep Alive set to [ {NewValue} ] successfully. for Tunnel ( {data.split('|')[1]} )"
        await query.message.reply_text(SuccessMsg,parse_mode="Markdown")        
        #await FnAdvancedMenuHandler(update=update,context=context,query=query,data=data,UserId=UserId)        
#        await context.bot.send_message(
#            chat_id=UserId,
#            text=Msg)
        #await query.message.reply_text("Select one of the menu options:", reply_markup=EditTunnelMenu(TunnelCode=TunnelCode,context=context),parse_mode="Markdown")
        await FuEditMenu(query=query,context=context,TunnelInEdit=TunnelCode,UserId=UserId)        
    elif data == 'SaveChangeMenu':
        await EditCreateFunc.SaveUserTunnelChangesConfim(update=update,context=context,query=query,UserId=UserId)
    elif data == 'YesSaveUserTunnelChanges':
        _rst = BotFunc.SaveUserTunnelChange(UserDataTunnels=context.user_data['tunnel_list'])
        if _rst[0] is True:
            await context.bot.send_message(
                chat_id=UserId,
                text=_rst[1])
            #query = update.callback_query
            #await query.answer()        
            await Fn_TunnelList(update, context,backmenu=True)                        
    elif data.split('|')[0] == "TunnelLiveStatus":
        await Fn_GetTunnelLog(data=data,context=context,UserId=UserId,query=query)
        ######### TUNNEL LIVE STATUS ##############

#        await query.message.reply_text(rst[1])
#        await query.message.reply_text(                        
#            f'🖥️ Live Tunnel Logs for Tunnel ( {TunnelCode} )\n\n',
#            reply_markup=RefreshTunnelogs(TunnelCode=TunnelCode),
#            parse_mode="Markdown"
#        )
    elif data.split('|')[0].split('_')[0] == "RestartTunnel":
        _mode =  data.split('|')[0].split('_')[1]
        tunnelCode = data.split('|')[1]
        if _mode.lower().strip() == 'live':
            logmod = True
        else:
            logmod = False
            
        rst = BotFunc.StopTunnelByCode(TunnelCode=tunnelCode)
        await context.bot.send_message(text=rst[1],chat_id=UserId)
        rst = BotFunc.StartTunnelByCode(TunnelCode=tunnelCode)
        await context.bot.send_message(text=rst[1],chat_id=UserId)

        
        if logmod is True:
            await Fn_GetTunnelLog(data=data,context=context,UserId=UserId,query=query)
        else:
            await Fn_TunnelDetailsMsg(context=context,update=update,query=query,TunnelCode=tunnelCode,UserId=UserId)
    elif data.split('|')[0] ==  "StopAllTunnels":
        ######### STOP ALL TUNNELS ##############
        rstDict = DropAllSShTunnel(ReturnResualt=True)
        if len(rstDict) > 0:
            for _l in rstDict:
                line = rstDict[_l].get('msg','')
                await context.bot.send_message(
                    chat_id=UserId,
                    text=line
                )
        else:
            await context.bot.send_message(
                chat_id=UserId,
                text="❕ No active tunnels to stop ❕"
            )
        await Fn_TunnelList(update, context,backmenu=True)            
    elif data.split('|')[0] ==  "StartAllTunnels":
        ######### STOP ALL TUNNELS ##############
        rstDic = StartAllTunnel(ReturnResualt=True)        
        if len(rstDic) > 0:
            for _m in rstDic:
                line = rstDic[_m].get('msg','')
                await context.bot.send_message(
                    chat_id=UserId,
                    text=line
                )                
#        else:
#            await context.bot.send_message(
#                chat_id=UserId,
#                text="❕ No active tunnels to stop ❕"
#            )
        await Fn_TunnelList(update, context,backmenu=True)            
    elif data.split('|')[0] == "DowbloadAsJson":
        ######### DOWNLOAD AS JSON ##############
        TunnelCode = data.split('|')[1]        
        rst = await EditCreateFunc.ExportTunnelAsJson(TunnelCode=TunnelCode,context=context,UserId=UserId)
        return
    elif data.split('|')[0] == "CloneTunnel":
        ######### CLONE TUNNEL ##############
        TunnelCode = data.split('|')[1]        
        context.user_data["awaiting_value"] = True
        context.user_data["FieldToEdit"] = "CloneTunnel"        
        context.user_data["TunnelforCloned"] = TunnelCode
        await EditCreateFunc.CloneTunnelHandler(tunnelCode=TunnelCode,context=context,user_id=UserId,query=query)
        return
    elif data.split('|')[0] == "IsActive_Change":
        ######### TOGGLE IS ACTIVE ##############
        TunnelInEdit = data.split('|')[1]
        IsActiveValue = context.user_data["tunnel_list"][TunnelInEdit].get('is_active',True)
        if IsActiveValue is True:
            context.user_data["tunnel_list"][TunnelInEdit]['is_active'] = False
        else:
            Rst = BotFunc.TunnelIsValidForActive(TunnelDict=context.user_data["tunnel_list"][TunnelInEdit])
            if Rst[0] is False:
                keyboard = [
                    [InlineKeyboardButton("✏️ Edit Tunnel", callback_data=f"EditTunnel|{TunnelInEdit}")],
                ]
                await context.bot.send_message(
                    chat_id=UserId,
                    reply_markup=InlineKeyboardMarkup(keyboard),
                    text=f"❌ Cannot Enable Tunnel {TunnelInEdit} ❌ \n\nReason:\n{Rst[1]}")
                return
            context.user_data["tunnel_list"][TunnelInEdit]['is_active'] = True
        
        await EditCreateFunc.SaveUserTunnelChangesConfim(update=update,context=context,query=query,UserId=UserId)
        #await Fn_TunnelDetailsMsg(context=context,update=update,query=query,TunnelCode=data.split('|')[1],UserId=UserId)


#        await query.message.reply_text(                       
#            f"🖥️ Advanced Tunnel Config\n\n For Highly Restricted Networks ( {TunnelCode} )\n\n",            
#            reply_markup=AdvancedMenu(TunnelCode=TunnelCode,HighlyRestrictedNetworksDict=HighlyRestrictedNetworksDict),
#            parse_mode="Markdown"
#        )
    elif data ==  "create_tunnel":
        ######### CREATE NEW TUNNEL ##############
        context.user_data["state"] = WAITING_FILE
        context.user_data["WaitingFor"] = "NewTunnelTemplateFile"
        context.user_data["awaiting_value"] = True
        await EditCreateFunc.CreateNewTunnelHandler(context=context,query=query,UserId=UserId)
    elif data ==  "Download TunnelTemplate":
        ######### DOWNLOAD TUNNEL TEMPLATE ##############
        await EditCreateFunc.DownloadTemplateTunnelAsJson(context=context,UserId=UserId)
        pass
    elif data.split('|')[0] == "DebugMenu":
        ######### DEBUG MENU ##############
        await Fn_DebugMenu(update=update,context=context,query=query,data=data,UserId=UserId)
        return
    elif data.split('|')[0] == "DebugTunnel":
        TunnelCode= data.split('|')[1]
        Tunnelname = context.user_data['tunnel_list'][TunnelCode]['Name']
        rst = BotFunc.GetTunnelStatusByCode(TunnelCode=TunnelCode)
        if rst.get('status',False) is True:
            rst = BotFunc.StopTunnelByCode(TunnelCode=TunnelCode)
            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text=f"❕ Stopping Tunnel *{Tunnelname}* for Debugging... ❕\n",
                parse_mode="Markdown")
                        
        rst = BotFunc.StartTunnelByCode(TunnelCode=TunnelCode,DEBUG=True)
        if rst[0] is True:
            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text=f"{rst[1]}\n\n *Note:* Debug mode is enabled. Logs will be more verbose.",
                parse_mode="Markdown")
        else:
            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text=f"❌ Failed to start tunnel: ❌ \n ------\n{rst[1]}❌\n\n *Note:* Debug mode is enabled.",)
        TunneDict = context.user_data['tunnel_list'][TunnelCode]
        RsrLog = GetTunnelLogDetails(TunnelDict=TunneDict)
        if RsrLog[0] is True:
            MassageHeader = f"🛠️ Debug Logs for Tunnel ( {Tunnelname} (Last 20 lines)) 🛠️\n\n"
            FUllLog = f"{MassageHeader}{RsrLog[1]}\n"
            await Fn_DebugMenu(update=update,context=context,query=query,data=data,UserId=UserId,Massege=FUllLog,TunnelIsRunning=True)
        else:
            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text=f"❌ Failed to get debug logs: ❌ \n ------\n{RsrLog[1]}❌\n")
    elif data.split('|')[0] == "DownloadLogFile":
        TunnelCode= data.split('|')[1]
        await EditCreateFunc.DownloadTunnelLogs(TunnelCode=TunnelCode,context=context,UserId=UserId)
        return
    elif data.split('|')[0] == 'TunnelCommand':
        TunnelCode= data.split('|')[1]
        CommandMsg = BotFunc.GetTunnelCommand(TunnelCode=TunnelCode)
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=CommandMsg)
    elif data.split('|')[0] == 'ClearLog':
        TunnelCode= data.split('|')[1]
        rst = ClearTunnleLog(TunnelCode=TunnelCode)
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=f"*{rst[1]}*\n",
            parse_mode="Markdown")
    elif data.split('|')[0] == 'Last20Log':    
        TunnelCode = TunnelCode= data.split('|')[1]
        TunneDict = context.user_data['tunnel_list'][TunnelCode]
        Tunnelname = context.user_data['tunnel_list'][TunnelCode]['Name']
        RsrLog = GetTunnelLogDetails(TunnelDict=TunneDict,NumLines=20)
        keyboard = [
            [InlineKeyboardButton("❌ Cancel", callback_data=f"DebugMenu|{TunnelCode}")],
            [InlineKeyboardButton("♻️ Refresh", callback_data=f"Last20Log|{TunnelCode}")]
        ]        
        if RsrLog[0] is True:
            MassageHeader = f"🛠️ Debug Logs for Tunnel ( {Tunnelname} (Last 20 lines)) 🛠️\n\n"
            FUllLog = f"{MassageHeader}{RsrLog[1]}\n"
            await query.message.reply_text(
                FUllLog,
                reply_markup=InlineKeyboardMarkup(keyboard)
            )

#            await context.bot.send_message(
#                chat_id=update.effective_chat.id,
#                text=FUllLog)                                                
            #await Fn_DebugMenu(update=update,context=context,query=query,data=data,UserId=UserId,Massege=FUllLog,TunnelIsRunning=False)



    





####################
# TEXT HANDLER        
####################
async def text_handler(update, context):
    if context.user_data.get("awaiting_value"):        
        UserId = update.effective_chat.id
        value = update.message.text        
        WaitingFor = context.user_data.get("WaitingFor","")
        if WaitingFor == "NewTunnelTemplateFile":
            NewTunnel = await EditCreateFunc.HandleNewTunnelTemplateFileUpload(context=context,
                                                                                UserId=UserId,
                                                                                update=update,
                                                                                UserInput=value,
                                                                                LocadJsonFrom='InputText')
            if NewTunnel[0] is False:
                return
            ImpMsg = f"✅ Tunnel Import successfully\n\n*Note:* New tunnel is 🚫 Disabled by default. Please Enable it from the tunnel list."
            await context.bot.send_message(
                chat_id=UserId,
                text=ImpMsg,
                parse_mode="Markdown"
            )
            context.user_data["awaiting_value"] = False  # Reset the flag                            
            context.user_data["FieldToEdit"] = ""  # Clear the field to edit            
            context.user_data["WaitingFor"] = ""

            _rst = BotFunc.SaveUserTunnelChange(UserDataTunnels=context.user_data['tunnel_list'])
            if _rst[0] is False:
                await context.bot.send_message(
                    chat_id=UserId,
                    text="❌ Failed to save imported tunnel ❌")    


            await Fn_TunnelList(update, context,backmenu=True)
            return
            

        FileldToEdit = context.user_data.get("FieldToEdit","")        
        TunnelInEdit = context.user_data.get("TunnelInEdit","")
        if FileldToEdit in ['password', 'authentication','key_path','private_key','UploadKey']:
            _rst = await EditCreateFunc.HandleAuthValueInput(update=update
                                                                ,context=context
                                                                ,value=value
                                                                ,FileldToEdit=FileldToEdit
                                                                ,TunnelInEdit=TunnelInEdit
                                                                )
#            if _rst is False:
#                await update.message.reply_text("Password cannot be empty. Please send a valid password.")
        elif FileldToEdit in STANDARD_FIELDS_LIST:
            _rst = await EditCreateFunc.EditStandardField(update=update
                                                            ,context=context
                                                            ,value=value
                                                            ,FileldToEdit=FileldToEdit
                                                            ,TunnelInEdit=TunnelInEdit
                                                            )
        elif FileldToEdit == 'CloneTunnel':
            TunnelforCloned = context.user_data.get("TunnelforCloned","")            
            CodeStatus =  await EditCreateFunc.CLoneCodeTextHandler(Tunnel4Cloned=TunnelforCloned,
                                                                    context=context,
                                                                    update=update,
                                                                    UserId=UserId,
                                                                    Value=value)
            if CodeStatus:
                _rst = BotFunc.SaveUserTunnelChange(UserDataTunnels=context.user_data['tunnel_list'])
                if _rst[0] is True:
                    await context.bot.send_message(
                        chat_id=UserId,
                        text=_rst[1])
                    context.user_data["awaiting_value"] = False  # Reset the flag                                    
                    context.user_data["FieldToEdit"] = ""  # Clear the field to edit            
                    context.user_data["TunnelforCloned"] = ""
                    context.user_data.pop("state", None)
                    #query = update.callback_query
                    #await query.answer()        
                    CloneMsg = f"✅ Tunnel cloned successfully with new code: {value.strip()}\n\n*Note:* New tunnel is 🚫 Disabled by default. Please Enable it from the tunnel list."
                    await context.bot.send_message(
                        chat_id=UserId,
                        text=CloneMsg,
                        parse_mode="Markdown"
                    )
                    #await Fn_TunnelDetailsMsg(context=context,update=update,query=query,TunnelCode=data.split('|')[1],UserId=UserId)                    
                    await Fn_TunnelList(update, context,backmenu=True)
                    return
            else:
                return            
        if _rst:            
            context.user_data["awaiting_value"] = False  # Reset the flag                
            #context.user_data["tunnel_list"][TunnelInEdit][FileldToEdit] = value.strip()  # Save the value
            context.user_data["FieldToEdit"] = ""  # Clear the field to edit            
            #await query.edit_message_text("Select one of the menu options:", reply_markup=EditTunnelMenu(TunnelCode=TunnelInEdit))            
#            FiledChange = EditCreateFunc.DetectUserTunnelChanges(TunnelCode=TunnelInEdit,Fileds2Edit=FileldToEdit,New_Value=value)
#            if FiledChange is True:
#                context.user_data["tunnel_list"][TunnelInEdit]['tunel_changed'] = True

            Msg = BotFunc.GenerateTunnelStatusSummary(TunnelCode=TunnelInEdit,UserData=context.user_data)            
            await context.bot.send_message(
                chat_id=UserId,
                text=Msg)

            StikerID = BotFunc.GetTelegramStickerID(StikerName='Edit_tunnel')
            if StikerID != None:
                await context.bot.send_sticker(
                    chat_id=UserId,
                    sticker=StikerID)

            await update.message.reply_text("Select one of the menu options:", reply_markup=EditTunnelMenu(TunnelCode=TunnelInEdit,context=context),parse_mode="Markdown")

####################
# DOCUMENT HANDLER
####################

async def document_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    a = context.user_data.get("state")
    if context.user_data.get("state") != WAITING_FILE:
        return  # No WAITING_FILE state, ignore the document

    document = update.message.document
    if not document:
        await update.message.reply_text("❌ Please upload a valid File")
        return
    
    # Process the uploaded file
    file = await context.bot.get_file(document.file_id)
    await file.download_to_drive(f"/tmp/{document.file_name}")
    RealFilePath = '/tmp/' + document.file_name
    

    
    if context.user_data.get("WaitingFor") == "NewTunnelTemplateFile":        
        # Handle New Tunnel Template File Upload
        UserId = update.effective_chat.id
        NewTunnel = await EditCreateFunc.HandleNewTunnelTemplateFileUpload(context=context,UserId=UserId,FilePath=RealFilePath,update=update)
        if NewTunnel[0] is False:
            return
        _rst = BotFunc.SaveUserTunnelChange(UserDataTunnels=context.user_data['tunnel_list'])
        if _rst[0] is False:
            await context.bot.send_message(
                chat_id=UserId,
                text="❌ Failed to save imported tunnel ❌")    
            
            #context.user_data["awaiting_value"] = False  # Reset the flag                                    
            #context.user_data["FieldToEdit"] = ""  # Clear the field to edit            
            #context.user_data["TunnelforCloned"] = ""
            
            context.user_data["awaiting_value"] = False  # Reset the flag                                    
            context.user_data["FieldToEdit"] = ""  # Clear the field to edit            
            context.user_data["TunnelforCloned"] = ""
            context.user_data.pop("state", None)

            #query = update.callback_query
            #await query.answer()        
            ImpMsg = f"✅ Tunnel Import successfully\n\n*Note:* New tunnel is 🚫 Disabled by default. Please Enable it from the tunnel list."
            await context.bot.send_message(
                chat_id=UserId,
                text=ImpMsg,
                parse_mode="Markdown"
            )
            #await Fn_TunnelDetailsMsg(context=context,update=update,query=query,TunnelCode=data.split('|')[1],UserId=UserId)                    
            await Fn_TunnelList(update, context,backmenu=True)
            return
            
    # Save the private key to a temporary file
    TunnelInEdit = context.user_data.get("TunnelInEdit","")
    KeyFilePath = f"{SSHKEYDir}/{TunnelInEdit}_private_key.pem"        
    SrcPth = Path(RealFilePath)
    DscTpath = Path(KeyFilePath)    
    SrcPth.rename(DscTpath)

    try:
        os.chmod(KeyFilePath, 0o600)  # Set file permissions to read/write for owner only
    except Exception as e:
        await update.message.reply_text(f"❌ Failed to Change Premission: {str(e)}\nPlease try again.")
        return False

    await update.message.reply_text(f"📤 File Uploaded Successfully in \n\n📁 : {KeyFilePath}")

    # Finish the waiting state
    context.user_data.pop("state", None)

    FileldToEdit = context.user_data.get("FieldToEdit","")
    TunnelInEdit = context.user_data.get("TunnelInEdit","")

    context.user_data["awaiting_value"] = False  # Reset the flag                
    context.user_data["tunnel_list"][TunnelInEdit]['key_path'] = KeyFilePath  # Save the value
    context.user_data['tunnel_list'][TunnelInEdit]['authentication'] = 'key_path'
    context.user_data["FieldToEdit"] = ""  # Clear the field to edit            
    UserId = update.effective_chat.id

    #await query.edit_message_text("Select one of the menu options:", reply_markup=EditTunnelMenu(TunnelCode=TunnelInEdit))            
    #FiledChange = EditCreateFunc.DetectUserTunnelChanges(TunnelCode=TunnelInEdit,Fileds2Edit=FileldToEdit,New_Value=RealFilePath)
    #if FiledChange is True:
    #    context.user_data["tunnel_list"][TunnelInEdit]['tunel_changed'] = True
    Msg = BotFunc.GenerateTunnelStatusSummary(TunnelCode=TunnelInEdit,UserData=context.user_data)            
    await context.bot.send_message(
        chat_id=UserId,
        text=Msg)
    
    StikerID = BotFunc.GetTelegramStickerID(StikerName='Edit_tunnel')
    if StikerID != None:
        await context.bot.send_sticker(
            chat_id=UserId,
            sticker=StikerID)

    await update.message.reply_text("Select one of the menu options:", reply_markup=EditTunnelMenu(TunnelCode=TunnelInEdit,context=context),parse_mode="Markdown")
    


    #ConversationHandler.END

# ===============================================
#               SVM SVM TSVM SVM HANDLERS
# ===============================================






# ===============================================
#               END HANDLERS
# ===============================================

def main():
    app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()

    app.bot.set_my_commands([
        BotCommand("start", "Start the bot"),        
        BotCommand("tunnels_menu", " Manage SSH Tunnels"),
        BotCommand("tunnels", "List of Tunnels"),
    ])
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", helpmenu))    
    app.add_handler(CommandHandler("tunnels", Fn_TunnelList))    
    app.add_handler(CallbackQueryHandler(SVM_HandlerFunc.SVM_handler,pattern=r"^SVM\."))
    app.add_handler(CallbackQueryHandler(button_handler))    
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, text_handler))
    app.add_handler(MessageHandler(filters.Document.ALL, document_handler))


    print("Bot is running… 😤")
    app.run_polling()
    

if __name__ == "__main__":    
    main()