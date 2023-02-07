from telethon import TelegramClient, events
from telethon.tl.functions.messages import GetBotCallbackAnswerRequest
from telethon.tl.functions.channels import JoinChannelRequest
from telethon.tl.functions.channels import LeaveChannelRequest
from telethon.tl.functions.channels import GetParticipantRequest
import asyncio, time


# DATA
api_id = int(input("APP ID here: ")) 
api_hash = input("API HASH here: ")
acc_name = input("Termux code: ")
iqthon = TelegramClient(acc_name, api_id, api_hash)
iqthon.start()

Waiting_idPart_1 = None
Waiting_idPart_2 = None

collects = []

# COLLECT POINTS
@iqthon.on(events.NewMessage(outgoing=True, pattern=r'.الغاء الجمع ?(.*)'))
async def UnCollectPoints(event):
    bot_username = (event.message.message).replace('.الغاء الجمع', '').strip()        
    reply = await event.reply(f'**تم الغاء الجمع من {bot_username}**')
    
    bot = await event.client.get_entity(bot_username)
    if bot.id in collects:
        collects.remove(bot.id)

# COLLECT POINTS
@iqthon.on(events.NewMessage(outgoing=True, pattern=r'.بدء الجمع ?(.*)'))
async def CollectPoints(event):
    bot_username = (event.message.message).replace('.بدء الجمع', '').strip()        
    reply = await event.reply(f'**جاري التحقق**')
    
    bot = await event.client.get_entity(bot_username)
    if bot.id not in collects:
        collects.append(bot.id)
    
    # WHICH BOT
    check = await CheckStart(event, bot_username)
    if check != True:
        await event.client.edit_message(event.chat_id, reply.id, "**حدث خطأ. تأكد من تفعيل البوت و سرعة استجابته**")
    else:
        await event.client.edit_message(event.chat_id, reply.id, "**تم بدأ الجمع النقاط, سيتم تنبيهك عند الانتهاء داخل البوت**")
            
        # START COLLECTING
        collect = await Collect_t06bot(event, bot_username)

# CHECK BOTs
async def CheckStart(event, username):
    async with event.client.conversation(username) as conv:
        try:
            await conv.send_message("/start")
            await conv.send_message("/start")
            await conv.send_message("/start")
            await conv.send_message("/start")
            await conv.send_message("/start")
            await conv.send_message("/start")
            await conv.send_message("/start")         
            resp = await conv.get_response()
            if resp.reply_markup != None:
                BalanceButton = resp.reply_markup.rows[0].buttons[0].text
                if "عدد نقاطك" in BalanceButton:
                    return True
        except:
            return False
        
        
# COLLECT BOT 
async def Collect_t06bot(event, username):
    global Waiting_idPart_1
    
    async with event.client.conversation(username) as conv:
        try:
            await conv.send_message("/start")
            resp = await conv.get_response()
            Waiting_idPart_1 = resp.id
            click_collect = await resp.click(2)
        except Exception as e:
            return False
        
# JOIN
async def JoinChannel(event, username):
    try:
        Join = await event.client(JoinChannelRequest(channel=username))
        return True
    except:
        return False

  
# EDITS
@iqthon.on(events.MessageEdited)
async def Edits(event):
    global Waiting_idPart_1, Waiting_idPart_2, collects
    
    if event.chat_id in collects:
        if event.message.id == Waiting_idPart_1:
            click_collect = await event.click(0)
            Waiting_idPart_2 = event.message.id
            Waiting_idPart_1 = None
            
        if event.message.id == Waiting_idPart_2:
            if event.reply_markup != None:
                try:
                    for x in range(1000):
                        channel = event.reply_markup.rows[0].buttons[0].url
                        Join = await JoinChannel(event, channel)
                        time.sleep(2)
                        if Join == True:
                            check_collect = await event.click(2)
                        else:
                            if event.chat_id in collects:
                                collects.remove(event.chat_id)
                            finished = await event.edit("**تم اكمال المهمة. اذا كانت توجد المزيد من القنوات فهذا يعني انك محظور لمدة مؤقته**")
                            break
                except Exception as e:
                    pass
        
        
        
        
        
        
        
iqthon.run_until_disconnected()