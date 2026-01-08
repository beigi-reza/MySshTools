import os

from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    BotCommand,
)
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
    ConversationHandler,
    filters,
    MessageHandler,    
)

from TelegramBotFunction import TelegramJsonConfig
from lib.ServiceManagmentCore import ServiceManager
from tunnel import JsonConfig,current_directory
import copy
SERVICE_LIST =JsonConfig.get('services',{})
manager = ServiceManager()

ADMIN_PERMISSION = TelegramJsonConfig.get('primession',{}).get('admin',[])

##############################################################
#### Menu Menu Menu Menu Menu Menu ###########################
##############################################################

def ServiceManagmentMenu(ListOfServices={},Backmenu=True):
    Menulist = [] 
    if len(ListOfServices) == 0:    
        Menulist.append([InlineKeyboardButton("⬅️ No Service Found", callback_data="back_main")])                         
        return InlineKeyboardMarkup(Menulist)
    for _s in ListOfServices:
        service = ListOfServices[_s]
        Status = service.get('status',None)
        active_state = service.get('active_state',None)
        if Status is None:
            EmojiStatus = '⁉️'
            Statusstr = ' ( Unknown )'

        if Status:
            EmojiStatus = '✅'
            Statusstr = ' ( Running )'
        else:
            EmojiStatus = ''
            Statusstr = ''
                    
        Menulist.append([InlineKeyboardButton(f"{EmojiStatus} {service['name']} ( {active_state} )", callback_data=f"SVM.service|{service['name']}")])    
    if Backmenu is True:
        Menulist.append([InlineKeyboardButton("⬅️ Back to Tunnel Menu", callback_data="back_main")])
    return InlineKeyboardMarkup(Menulist)

#async def ServiceActionButtons(ServiceName=""):
#    Menulist = []
#    Menulist.append([InlineKeyboardButton("Show Status", callback_data=f"SVM.action|status|{ServiceName}"),
#                     InlineKeyboardButton("Show Logs", callback_data=f"SVM.action|logs|{ServiceName}")])
#    Menulist.append([InlineKeyboardButton("Create Service", callback_data=f"SVM.action|create|{ServiceName}"),
#                     InlineKeyboardButton("Install Service (reload daemon)", callback_data=f"SVM.action|install|{ServiceName}")])        
#    Menulist.append([InlineKeyboardButton("Enable Service", callback_data=f"SVM.action|enable|{ServiceName}")])  
#    Menulist.append([InlineKeyboardButton("Disable Servive", callback_data=f"SVM.action|disable|{ServiceName}")])  
#    Menulist.append([InlineKeyboardButton("Delete Server", callback_data="SVM.action|delete")])
#    Menulist.append([InlineKeyboardButton("Start Service", callback_data=f"SVM.action|start|{ServiceName}"),                     
#                     InlineKeyboardButton("Stop Service", callback_data=f"SVM.action|stop|{ServiceName}"),
#                     InlineKeyboardButton("Restart Service", callback_data=f"SVM.action|restart|{ServiceName}")])    
#    Menulist.append([InlineKeyboardButton("⬅️ Back to Service Menu", callback_data="SVM.MainMenu")])
#    return InlineKeyboardMarkup(Menulist)


async def ServiceActionButtons(ServiceName=""):
    Menulist = []
    Menulist.append([InlineKeyboardButton("👁️ Show Status", callback_data=f"SVM.action|status|{ServiceName}")])                     
    Menulist.append([InlineKeyboardButton("📜 Show Logs", callback_data=f"SVM.action|logs|{ServiceName}")])        
    Menulist.append([InlineKeyboardButton("📄 Create Service", callback_data=f"SVM.action|create|{ServiceName}")])                     
    Menulist.append([InlineKeyboardButton("⚡ Install Service (reload daemon)", callback_data=f"SVM.action|install|{ServiceName}")])        
    
    Menulist.append([InlineKeyboardButton("🟢 Enable", callback_data=f"SVM.action|enable|{ServiceName}"),
                    InlineKeyboardButton("🔴 Disable", callback_data=f"SVM.action|disable|{ServiceName}"),
                    InlineKeyboardButton("❌ Delete", callback_data="SVM.action|delete")
                     ])
    Menulist.append([InlineKeyboardButton("▶️ Start", callback_data=f"SVM.action|start|{ServiceName}"),
                     InlineKeyboardButton("⏹️ Stop", callback_data=f"SVM.action|stop|{ServiceName}"),
                     InlineKeyboardButton("🔁 Restart", callback_data=f"SVM.action|restart|{ServiceName}")])    
    Menulist.append([InlineKeyboardButton("⬅️ Back to Service Menu", callback_data="SVM.MainMenu")])
    return InlineKeyboardMarkup(Menulist)


##############################################################
##############################################################
##############################################################

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




#####

async def ListOfServicesWithStatus():    
    List_of_servive = copy.deepcopy(SERVICE_LIST)
    for _s in List_of_servive:
        service = List_of_servive[_s]
        Name = service.get('name',None)
        if Name is None:
            continue            
        _rst = manager.status_service(Name,ReturnLog=False)
        IsActive = _rst[0]
        _Status = _rst[1]
        List_of_servive[_s]['status'] = IsActive
        List_of_servive[_s]['active_state'] = _Status["active_state"]
        List_of_servive[_s]['enabled_state'] = _Status["enabled_state"]


    return List_of_servive


async def ServriceInfo(ServerDict = {}):
    MSGList = []
    MSGList.append(f"🛠️ Service Information 🛠️\n\n")
    Name = ServerDict.get('name','Unknown')
    Description = ServerDict.get('description','Unknown')
    MSGList.append(f"Name: {Name}\n")
    MSGList.append(f"   • Description: {Description}\n")
    Status = ServerDict.get('status',None)
    active_state = ServerDict.get('active_state',None)
    enabled_state = ServerDict.get('enabled_state',None)
    _res = manager.status_service(Name,ReturnLog=False)
    if Status is None:
        MSGList.append(f"   •  Active State: ⚫ Unknown\n")
    else:
        if Status:
            MSGList.append(f"   •  Active State: 🟢 Running ( {active_state} )\n")
        else:
            MSGList.append(f"   •  Active State: 🔴 Stopped ( {active_state} )\n")
    if enabled_state is None:
        MSGList.append(f"   •  Enable State: ⚫ Unknown\n")
    else:
        MSGList.append(f"   •  Enable State: {enabled_state}\n")
    return ''.join(MSGList)

async def ServiceStatus(ServiceName=""):
    _res = manager.status_service(ServiceName,ReturnLog=True)    
    ServerDict = _res[1]
    active_state = ServerDict.get('active_state',None)
    enabled_state = ServerDict.get('enabled_state',None)
    log = ServerDict.get('log','No log available')
    MsgList = []
    MsgList.append(f"🛠️ Service Status for '{ServiceName}' 🛠️\n\n")
    MsgList.append(f"Active State: {active_state}\n")
    MsgList.append(f"Enable State: {enabled_state}\n\n")
    MsgList.append(f"{'▫️'*13}\n\n")
    MsgList.append(f"{log}\n")
    MsgList.append(f"\n\n{'▫️'*13}")
    return  ''.join(MsgList) 

async def ServiceLogs(ServiceName=""):    
    _res = manager.status_service(ServiceName,ReturnLog=True)    
    ServerDict = _res[1]
    active_state = ServerDict.get('active_state',None)
    enabled_state = ServerDict.get('enabled_state',None)
    Logs = manager.get_log(ServiceName,lines=30)
    LogsList = []
    LogsList.append(f"🛠️ Logs for Service '{ServiceName}' 🛠️\n\n")
    LogsList.append(f"Active State: {active_state}\n")
    LogsList.append(f"Enable State: {enabled_state}\n\n")
    LogsList.append(f"{'▫️'*13}\n\n")
    LogsList.append(f"{Logs}\n")
    LogsList.append(f"\n\n{'▫️'*13}")
    log = ''.join(LogsList)
    return  ''.join(log)
##############################################################
##############################################################
#
#     handler
#
##############################################################
##############################################################

async def SVM_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):    
    query = update.callback_query
    UserId = query.from_user.id
    if await has_permission(context=context,user_id=UserId) is False:
        return
    await query.answer()
    data = query.data
    command, Action = data.split(".", 1)
    List_of_service =await ListOfServicesWithStatus()
    if command == "SVM":
        if Action == "MainMenu":            
            list_of_service = List_of_service
#    await query.message.reply_text(                        
#        f"{rst[1]}\n",
#        reply_markup=TunnelActionMeny(TunnelDict=TunnelDict,_from='live_status'),
#        parse_mode="Markdown"
#    )

            await query.message.reply_text(
                text="🛠️ Service Management Menu 🛠️",
                reply_markup=ServiceManagmentMenu(ListOfServices=list_of_service,Backmenu=True)
            )
        elif Action.split("|")[0] == "service":
            ServiceName = Action.split("|")[1]
            ServiceDict = List_of_service.get(ServiceName,{})
            if ServiceDict == {}:
                await query.edit_message_text(
                    text=f"❌ Service '{ServiceName}' not found ❌",
                    reply_markup=ServiceManagmentMenu(ListOfServices=List_of_service,Backmenu=True)
                )
                return
            ServiceInfoMSG = await ServriceInfo(ServerDict=ServiceDict)
            await query.edit_message_text(
                text=ServiceInfoMSG,
                reply_markup=await ServiceActionButtons(ServiceName=ServiceName),                
            )
        elif Action.split("|")[0] == "action":
            SubAction = Action.split("|")[1]
            ServiceName = Action.split("|")[2]
            ServiceDict = List_of_service.get(ServiceName,{})
            if ServiceDict == {}:
                await query.edit_message_text(
                    text=f"❌ Service '{ServiceName}' not found ❌",
                    reply_markup=ServiceManagmentMenu(ListOfServices=List_of_service,Backmenu=True)
                )
                return
            if SubAction == "start":
                _res = manager.start_service(ServiceName)
            elif SubAction == "stop":
                _res = manager.stop_service(ServiceName)
            elif SubAction == "restart":
                _res = manager.restart_service(ServiceName)
            elif SubAction == "create":            
                Name = ServiceDict.get('name','')
                Description = ServiceDict.get('description','My Service Description')
                Exec = ServiceDict.get('exec','')
                ExecStart = f"/usr/bin/python3 {current_directory}/{Exec}"
                User = ServiceDict.get('user','root')
                WorkingDir = ServiceDict.get('working_dir',current_directory)
                if Name == '' or Exec == '':
                    await query.answer()
                    await context.bot.send_message(
                        chat_id=UserId,
                        text=f"❌ Service '{ServiceName}' configuration is invalid. Name and ExecStart are required. ❌\n",                        
                        parse_mode="Markdown"
                    )
                    return                
                #
                _res = manager.create_service(Name,Description,ExecStart,User,WorkingDir)                
            elif SubAction == "install":
                _res = manager.install_service(ServiceName)
            elif SubAction == "enable":
                _res = manager.enable_service(ServiceName)
            elif SubAction == "disable":                
                _res = manager.disable_service(ServiceName)
            elif SubAction == "delete":
                _res = manager.delete_service(ServiceName)            
            elif SubAction == "status":
                details = await ServiceStatus(ServiceName=ServiceName)
                await query.answer()
                await context.bot.send_message(
                    chat_id=UserId,
                    text=details,
                    #reply_markup=TunnelList,                    
                )
                return
            elif SubAction == "logs":
                Logs = await ServiceLogs(ServiceName=ServiceName)
                keyboard = [
                    [InlineKeyboardButton("❌ Cancel", callback_data=f"SVM.service|{ServiceName}")],
                    [InlineKeyboardButton("♻️ Refresh", callback_data=f"SVM.action|logs|{ServiceName}")]
                ]    
                await query.answer()
                await context.bot.send_message(
                    chat_id=UserId,
                    text=Logs,
                    reply_markup=InlineKeyboardMarkup(keyboard),
                    parse_mode="Markdown"
                )
                return


            if _res[0] is True:
                ActionMSG = f"✅ Successfully performed '{SubAction}' on service '{ServiceName}'. ✅\n"
            else:
                ActionMSG = f"❌ Failed to perform '*{SubAction}*' on service '*{ServiceName}*'. ❌\n\nError: {_res[1]}\n"
            
            await query.answer()
            await context.bot.send_message(
                chat_id=UserId,
                text=ActionMSG,
                #reply_markup=TunnelList,
                parse_mode="Markdown"
            )

#            List_of_service = await ListOfServicesWithStatus()
#            ServiceDict = List_of_service.get(ServiceName,{})
#            ServiceInfoMSG = await ServriceInfo(ServerDict=ServiceDict)
#
#
#            await query.edit_message_text(
#                text=ServiceInfoMSG,
#                reply_markup=await ServiceActionButtons(ServiceName=ServiceName)
#            )
#        
#        

        

    
    



if __name__ == "__main__":           
    print(f"You should not run this file directly")
