
import time
from collections import defaultdict
from pyrogram import Client, filters
from pyrogram.types import Message,InlineKeyboardMarkup, InlineKeyboardButton
import os
from deep_translator import GoogleTranslator
from datetime import datetime
import asyncio
import random
from pyrogram.enums import ChatMembersFilter # type: ignore
from pyrogram.errors import ChatAdminRequired, UserAdminInvalid,UserAlreadyParticipant, ChatAdminRequired, UserPrivacyRestricted, PeerIdInvalid
from pyrogram.raw import functions, types # type: ignore
from telethon import TelegramClient
from telethon.tl.functions.messages import CreateChatRequest



API_ID = "28561434"
API_HASH = "2f15b7d182207603d3062d10e5a62200"
phone_number = '+994515524320'

app = Client("my_account", api_id=API_ID, api_hash=API_HASH, phone_number=phone_number)


# Komutlar siyahısı
commands_list = [
    "** ↪ active:** Userbotu yoxla",
    "** ↪ version:** Userbot versiyası",
    "** ↪ yuxu:** AFK moduna keç",
    "** ↪ oyan:** AFK modundan çıx",
    "** ↪ userinfo:** Reply atmasan öz hesabının, reply atsan həmin istifadəçinin hesab informasiyası",
    "** ↪ translate:** Bütün dilləri tərcümə et",
    "** ↪ botlist:** Qrupdakı bot listini gətir",
    "** ↪ reverse:** Sözləri tərs çevir",
    "** ↪ alist:** Qrupdakı admins listini gətir",
    "** ↪ userlab:** Userləri etiketlə",
    "** ↪ stoplab:** Etiketləməni dayandır",
    "** ↪ siu:** Ronaldo gol sevinci",
    "** ↪ userban:** Reply ataraq istifadəçiyə ban ver",
    "** ↪ unuserban:** İstifadəçinin banını aç",
    "** ↪ add:** (.add (@username)) qrupa istifadəçi əlavə et",
    "** ↪ comlist:** Userbot komut listini gətir",
    "** ↪ setusername:** (. setusername (yoxlanış)) İstifadəçi adını dəyiş",
    "** ↪ setuserpic:** Hər hansı bir şəkilə reply ataraq profil şəklini dəyiş",
    "** ↪ ury:** Ürəklər içində istədiyin adı yazdır",
    "** ↪ pm:** İstifadəçiyə Şəxsi mesaj göndər",
    "** ↪ block:** İstifadəçini şəxsidən əngəllə",
    "** ↪ unblock:** İstifadəçinin şəxsidən əngəlini aç",
    "** ↪ joindate:** İstifadəçinin Qrupa qatılma zamanı",
    "** ↪ createqrup:** Gizli qrup yarat",
    "** ↪ hava:** Hava haqqında məlumat al",
]

# .comlist komandası
@app.on_message(filters.command("comlist", "."))
async def commands_list_command(client, message):
    response_message = "📜 **Mövcud Komandalar:**\n\n" + "\n".join(commands_list)
    response_message += f"\n\n**Komutların sayı**: {len(commands_list)}"
    await message.edit_text(response_message, disable_web_page_preview=True)


# .active komandası
@app.on_message(filters.command("active", "."))
async def active_command(client, message):
    cold_userbot_fancy = "𝓒𝓸𝓵𝓭 𝓾𝓼𝓮𝓻𝓫𝓸𝓽 "
    response_message = (
        "✧･ﾟ: *✧･ﾟ:*  *:･ﾟ✧*:･ﾟ✧\n"
       f"🔥 **{cold_userbot_fancy} aktivdir...** 🔥\n"
        "✧･ﾟ: *✧･ﾟ:*  *:･ﾟ✧*:･ﾟ✧"
    )
    await message.edit_text(response_message, disable_web_page_preview=True)


class AFKHandler:
    def __init__(self):
        self.afk_status = False
        self.afk_start_time = 0

afk_handler = AFKHandler()

@app.on_message(filters.command("yuxu", ".") & filters.me, group=3)
async def go_afk(client, message):
    afk_handler.afk_status = True
    afk_handler.afk_start_time = time.time()
    await message.edit_text(f"{message.from_user.first_name} **hal hazırda yuxu modundadı!**")

@app.on_message(filters.command("oyan", ".") & filters.me, group=3)
async def back_from_afk(client, message):
    afk_handler.afk_status = False
    afk_duration = time.time() - afk_handler.afk_start_time
    await message.edit_text(f"{message.from_user.first_name} **Yuxu modundan çıxıldı! AFK vaxtı: {afk_duration:.2f} saniye**")

@app.on_message(filters.private & filters.text & filters.incoming & ~filters.me)
async def auto_reply(client, message):
    if afk_handler.afk_status:
        await message.reply_text("**Hal hazırda yuxudayam**")


@app.on_message(filters.command("userinfo", "."))
async def id_command(client: Client, message: Message):
    target = message.reply_to_message.from_user if message.reply_to_message else message.from_user

    # Get user information
    user = await client.get_users(target.id)
    chat = await client.get_chat(target.id)
    chat_member = await client.get_chat_member(message.chat.id, target.id)

    # Get profile photo URL (if available)
    if chat.photo:
        profile_photo_path = await client.download_media(chat.photo.big_file_id)
    else:
        profile_photo_path = None

    # Get user's first name, username, id
    first_name = user.first_name
    username = user.username if user.username else "No username"
    user_id = user.id

    # Determine if user is an admin and get role/title
    if chat_member.status in ("administrator", "creator"):
        role = "Admin"
        custom_title = chat_member.custom_title if chat_member.custom_title else "No custom title"
    else:
        role = "User"
        custom_title = "N/A"

    # Example to fetch user join date (for simplicity, assuming you track this separately)
    join_date = "Not Available"

    # Example to count number of times user has left the group (for simplicity, assuming you track this separately)
    times_left_group = "Not Available"

    # Construct the response message
    response = (
        f"**User Information:**\n"
        f"**First Name:** {first_name}\n"
        f"**Username:** @{username}\n"
        f"**User ID:** `{user_id}`\n"
        f"**Join Date in Group:** {join_date}\n"
        f"**Role in Group:** {role}\n"
        f"**Custom Title:** {custom_title}\n"
        f"**Times Left Group:** {times_left_group}\n"
    )

    # Send the response message
    await message.edit_text(response)

    # Send the profile photo if available
    if profile_photo_path:
        await message.reply_photo(photo=profile_photo_path)
        os.remove(profile_photo_path)  # Remove the photo after sending it to free up space

@app.on_message(filters.command("translate", prefixes=".") & filters.reply)
async def translate_command(client: Client, message: Message):

    original_text = message.reply_to_message.text

    translator = GoogleTranslator(target='az')
    translated_text = translator.translate(text=original_text)

    await message.reply_text(f"**Translated Text:**\n{translated_text}")


@app.on_message(filters.command("botlist", ".") & filters.group)
async def botlist_command(client, message):
    chat = message.chat
    bot_list = []

    async for member in client.get_chat_members(chat.id, filter=ChatMembersFilter.BOTS):
        bot_info = f"⎿ [{member.user.first_name}](tg://user?id={member.user.id})" if member.user.username else f"{member.user.first_name}"
        bot_list.append(bot_info)

    if bot_list:
        bot_info_message = "✨ **Qrupdakı Botlar:**\n" + "\n".join(bot_list)
        bot_info_message += f"\n\n**Bot Sayı:** {len(bot_list)}"
    else:
        bot_info_message = "**Bu grupta bot yoxdu**"

    await message.edit_text(bot_info_message)

    
@app.on_message(filters.command("reverse", ".") & filters.me)
async def reverse_command(client, message):
    if message.reply_to_message and message.reply_to_message.text:
        text = message.reply_to_message.text
        reversed_text = text[::-1]
        await message.edit_text(reversed_text)
    else:
        await message.reply_text("Reply ataraq komutu ver")

@app.on_message(filters.command("alist", ".") & filters.group)
async def adminlist_command(client, message):
    chat = message.chat

    admin_list = []

    async for member in client.get_chat_members(chat.id, filter=ChatMembersFilter.ADMINISTRATORS):
        if member.user.is_bot:
            continue
        admin_info = f"➤ [{member.user.first_name}](tg://user?id={member.user.id})"
        admin_list.append(admin_info)

    if admin_list:
        admin_info_message = "✨ **Qrupdakı Adminlər:**\n\n" + "\n".join(admin_list)
        admin_info_message += f"\n\n🜲 **Admin Sayısı:** {len(admin_list)}"
    else:
        admin_info_message = "🚫 Bu grupta admin yok."

    await message.edit_text(admin_info_message, disable_web_page_preview=True)



tagging_active = {}
tag_message = {}
tagged_counts = {}

@app.on_message(filters.command("userlab", ".") & filters.group)
async def start_tagging(client, message):
    global tagging_active, tag_message, tagged_counts

    chat_id = message.chat.id

    if chat_id in tagging_active and tagging_active[chat_id]:
        await message.reply_text("**Etiketləmə prosesi zatən işləyir**")
        return

    if len(message.command) < 2:
        await message.reply_text("Mesajla etiketleyin")
        return

    tag_message[chat_id] = " ".join(message.command[1:])
    tagging_active[chat_id] = True
    tagged_counts[chat_id] = 0

@app.on_message(filters.text & filters.group & ~filters.me)
async def tag_users(client, message):
    global tagging_active, tag_message, tagged_counts

    chat_id = message.chat.id

    if chat_id in tagging_active and tagging_active[chat_id] and chat_id in tag_message:
        async for member in app.get_chat_members(chat_id):
            if not member.user.is_bot:
                username = f"@{member.user.username}" if member.user.username else f"[{member.user.first_name}](tg://user?id={member.user.id})"
                await client.send_message(chat_id, f"{username} {tag_message[chat_id]}", disable_web_page_preview=True)
                tagged_counts[chat_id] += 1
                await asyncio.sleep(2)  

                if tagged_counts[chat_id] >= 50:
                    tagging_active[chat_id] = False
                    break

            if not tagging_active[chat_id]:
                break

@app.on_message(filters.command("stoplab", ".") & filters.group)
async def stop_tagging(client, message):
    global tagging_active, tag_message, tagged_counts

    chat_id = message.chat.id

    if chat_id in tagging_active and tagging_active[chat_id]:
        tagging_active[chat_id] = False
    else:
        await message.reply_text("Etiketləmə prosesi aktiv deyil")


ronaldo_siu_frames = [
    "SIU!",
    "SIUU!",
    "SIUUU!",
    "SIUUUU!",
    "SIUUUUU!",
    "SIUUUUUU!",
    "SIUUUUUUU!",
    "SIUUUUUUUU!",
    "SIUUUUUUUUU!",
    "SIUUUUUUUUUU!",
    "SIUUUUUUUUUUU!",
]


gif_urls = [
    "https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExZDc0cTV0OWdqb2EyN2xyOWpjemZsMXI3Zm5pMzhkNmNid2NhNGZnZyZlcD12MV9naWZzX3NlYXJjaCZjdD1n/r1IMdmkhUcpzy/giphy.gif",
    "https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExZDc0cTV0OWdqb2EyN2xyOWpjemZsMXI3Zm5pMzhkNmNid2NhNGZnZyZlcD12MV9naWZzX3NlYXJjaCZjdD1n/8EoCZQ7lDDVKNMvNzL/giphy.gif",
    "https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExZDc0cTV0OWdqb2EyN2xyOWpjemZsMXI3Zm5pMzhkNmNid2NhNGZnZyZlcD12MV9naWZzX3NlYXJjaCZjdD1n/xT1XGVp95GDPgFYmUE/giphy.gif",
    "https://media.giphy.com/media/8mnn2DHlkSKIQI0D5v/giphy.gif?cid=790b7611d74q5t9gjoa27lr9jczfl1r7fni38d6cbwca4fgg&ep=v1_gifs_search&rid=giphy.gif&ct=g",
    "https://media.giphy.com/media/v3DdWOdnizRw4/giphy.gif?cid=ecf05e473dutsipfzl2zcsuh1w1xsqyywap4fkwwjz6yft31&ep=v1_gifs_search&rid=giphy.gif&ct=g",
]

@app.on_message(filters.command("siu", ".") & filters.group)
async def send_ronaldo_animation(client, message):
    for frame in ronaldo_siu_frames:
        await message.edit_text(frame)
        await asyncio.sleep(0.3)  
        
    if gif_urls:
        gif_to_send = random.choice(gif_urls)
        await client.send_animation(chat_id=message.chat.id, animation=gif_to_send)


@app.on_message(filters.command("userban", ".") & filters.reply & filters.group)
async def ban_user(client, message):
    target_user = message.reply_to_message.from_user
    chat_id = message.chat.id

    try:
        await client.ban_chat_member(chat_id, target_user.id)
        
        ban_message = f"🚫 [{target_user.first_name}](tg://user?id={target_user.id}) **adlı istifadəçi qrupu tərk etmək məcburiyyətində qaldı.XAXA**"
        await message.edit_text(ban_message, disable_web_page_preview=True)
        
    except ChatAdminRequired:
        await message.edit_text("YETƏRLİ İZNİM YOXDUR")
    except UserAdminInvalid:
        await message.edit_text("**o bir admindi.Banlayabilmərəm**")
       
@app.on_message(filters.command("unuserban", ".") & filters.reply & filters.group)
async def unban_user(client, message):
    target_user = message.reply_to_message.from_user
    chat_id = message.chat.id

    try:
        await client.unban_chat_member(chat_id, target_user.id)
        unban_message = f"✅ [{target_user.first_name}](tg://user?id={target_user.id}) **adlı istifadəçinin qrupdan banı açıldı**"
        await message.edit_text(unban_message, disable_web_page_preview=True)
        
    except ChatAdminRequired:
        await message.edit_text("**Yetərli iznim yoxdur**")
    except UserAdminInvalid:
        await message.edit_text("**BU İSTİFADƏÇİ BİR ADMİNDİR**")


@app.on_message(filters.command("add", ".") & filters.group)
async def add_user_to_group(client, message: Message):
    if len(message.command) < 2:
        await message.reply_text("**Lütfən bir istifadəçi etiketini verin.**")
        return

    
    username = message.command[1]
    source_chat_id = message.chat.id

    try:
        
        user = await client.get_users(username)
        
        try:
            
            await client.add_chat_members(source_chat_id, user.id)
            await message.reply_text(f"**{user.first_name} əlavə olundu.**")
        except UserAlreadyParticipant:
            await message.reply_text(f"**{user.first_name} artıq qrupda.**")
        except UserPrivacyRestricted:
            await message.reply_text(f"**{user.first_name} istifadəçi məxfilik ayarları səbəbindən əlavə oluna bilmədi.**")
        except ChatAdminRequired:
            await message.reply_text(f"**Qrupda istifadəçi əlavə etmək üçün kifayət qədər səlahiyyətim yoxdur.**")
        except Exception as e:
            await message.reply_text(f"**{user.first_name} əlavə oluna bilmədi: {str(e)}**")

    except PeerIdInvalid:
        await message.reply_text("**Keçərsiz istifadəçi etiketi.**")
    except Exception as e:
        await message.reply_text(f"**Bir səhv baş verdi: {str(e)}**")

@app.on_message(filters.command("ury", ".") & filters.me)
async def heart_command(client, message: Message):
    if len(message.command) < 2:
        await message.edit_text("Lütfen bir mesaj girerek `.ury` komutunu kullanın.")
        return
    
    message_text = " ".join(message.command[1:])
    heart = (
        " ❤️ ❤️ ❤️ ❤️ ❤️ ❤️ ❤️ ❤️ ❤️ ❤️ ❤️ ❤️ ❤️ ❤️ ❤️ ❤️ ❤️ ❤️ ❤️ ❤️ ❤️ ❤️ ❤️ \n"
        " ❤️                                                                          ❤️ \n"
        f"❤️                      **{message_text}**                                  ❤️ \n"
        " ❤️                                                                          ❤️ \n"
        " ❤️ ❤️ ❤️ ❤️ ❤️ ❤️ ❤️ ❤️ ❤️ ❤️ ❤️ ❤️ ❤️ ❤️ ❤️ ❤️ ❤️ ❤️ ❤️ ❤️ ❤️ ❤️ ❤️ \n"
    )

    
    await message.edit_text(heart)

@app.on_message(filters.command("setuserpic", prefixes=".") & filters.reply)
async def set_user_pic(client: Client, message: Message):
    reply = message.reply_to_message

    
    if not reply.photo:
        await message.edit_text("**Lütfen bir resim ile yanıtlayın**")
        return

    try:
        
        file_id = reply.photo.file_id
        file_path = await client.download_media(file_id)

       
        await client.set_profile_photo(photo=file_path)
        await message.edit_text("**Profil resmi başarıyla değiştirildi**")

    except Exception as e:
        await message.edit_text(f"**Hata oluştu:** {str(e)}")

@app.on_message(filters.command("setusername", prefixes="."))
async def set_user_name(client: Client, message: Message):
   
    if len(message.command) < 2:
        await message.edit_text("**Xahis edirəm yeni adınızı '.setusername (Adınız)' olaraq yazın**")
        return

    new_name = " ".join(message.command[1:])

    try:
        
        await client.update_profile(first_name=new_name)
        await message.edit_text(f"**İstifadəçi adı uğurla '{new_name}' olaraq dəyişdirildi **")

    except Exception as e:
        await message.edit_text(f"**Hata oluştu:** {str(e)}")

@app.on_message(filters.new_chat_members)
async def welcome(client: Client, message: Message):
    print("Yeni bir user qatıldı!")  
    for new_member in message.new_chat_members:
        username = f"@{new_member.username}" if new_member.username else new_member.first_name
        print(f"Xoş gəldin mesajı göndərilir: {username}")  
        await message.reply_text(f"Xoş gəldin {username}!")


@app.on_message(filters.command("pm", ".") & filters.me)
async def pm(client, message):
    try:
        if message.reply_to_message:
            target_user = message.reply_to_message.from_user.id
            text = " ".join(message.command[1:])
        else:
            target_user = int(message.command[1]) if message.command[1].isdigit() else message.command[1]
            text = " ".join(message.command[2:])
        
        sent_message = await client.send_message(target_user, text)
        
        if isinstance(target_user, int): 
            user = await client.get_users(target_user)
        else: 
            user = await client.get_users(target_user)

        first_name = user.first_name
        user_id = user.id

        confirmation_text = f"**PM mesaj göndərildi:** [{first_name}](tg://user?id={user_id})"
        await message.edit_text(confirmation_text)
        
    except Exception as e:
        await message.reply_text(f"Hata oluştu: {str(e)}")


@app.on_message(filters.command("block", ".") & filters.me)
async def block(client, message):
    try:
        if message.reply_to_message:
            target_user = message.reply_to_message.from_user.id
        else:
            target_user = int(message.command[1]) if message.command[1].isdigit() else message.command[1]

        await client.block_user(target_user)

        if isinstance(target_user, int):  
            user = await client.get_users(target_user)
        else:  
            user = await client.get_users(target_user)

        first_name = user.first_name
        user_id = user.id

        confirmation_text = f"**İstifadəçi PM'dan bloklandı:** [{first_name}](tg://user?id={user_id})"
        await message.edit_text(confirmation_text)
        
    except Exception as e:
        await message.reply_text(f"Hata oluştu: {str(e)}")

@app.on_message(filters.command("unblock", ".") & filters.me)
async def unblock(client, message):
    try:
        if message.reply_to_message:
            target_user = message.reply_to_message.from_user.id
        else:
            target_user = int(message.command[1]) if message.command[1].isdigit() else message.command[1]

        await client.unblock_user(target_user)

        if isinstance(target_user, int):  
            user = await client.get_users(target_user)
        else:  
            user = await client.get_users(target_user)

        first_name = user.first_name
        user_id = user.id

        confirmation_text = f"İstifadəçinin PM'dan bloku açıldı: [{first_name}](tg://user?id={user_id})"
        await message.edit_text(confirmation_text)
        
    except Exception as e:
        await message.reply_text(f"Hata oluştu: {str(e)}")

@app.on_message(filters.command("version", "."))
async def bot_version(client, message):
    cold_userbot_version_fancy = "𝓒𝓸𝓵𝓭 𝓾𝓼𝓮𝓻𝓫𝓸𝓽 𝓼𝓾𝓻𝓾𝓶𝓾:  1.0.0"
    response_message = (
        "✧･ﾟ: *✧･ﾟ:*  *:･ﾟ✧*:･ﾟ✧\n"
       f"🔥 **{cold_userbot_version_fancy}** 🔥\n"
        "✧･ﾟ: *✧･ﾟ:*  *:･ﾟ✧*:･ﾟ✧"
    )
    await message.edit_text(response_message, disable_web_page_preview=True)

@app.on_message(filters.command("leave", ".") & filters.group)
async def leave(client, message):
    await client.leave_chat(message.chat.id)
    await message.edit_text("**Sağolun.Mən qrupdan çıxdım**")

@app.on_message(filters.command("join", ".") & filters.me)
async def join(client, message):
    try:
        chat_identifier = message.command[1]
        if chat_identifier.startswith('@'):
            chat = await client.get_chat(chat_identifier)
            chat_id = chat.id
        else:
            chat_id = int(chat_identifier)

        await client.join_chat(chat_id)
        await message.edit_text("🟢 𝓠𝓻𝓾𝓹𝓪 𝓺𝓪𝓽𝓲𝓵𝓭𝓲𝓶. 🟢")
    except Exception as e:
        await message.edit_text(f"Hata: {str(e)}")

@app.on_message(filters.command("joindate", ".") & filters.group)
async def joindate(client, message):
    if message.reply_to_message:
        user = message.reply_to_message.from_user
    else:
        user_input = message.command[1]
        if user_input.startswith('@'):
            user = await client.get_users(user_input)
        else:
            user_id = int(user_input)
            user = await client.get_users(user_id)
    
    user_id = user.id
    chat_id = message.chat.id
    member = await client.get_chat_member(chat_id, user_id)

    join_date = member.joined_date.strftime('%Y-%m-%d %H:%M:%S')
    user_mention = f"[{user.first_name}](tg://user?id={user.id})"
    
    fancy_text = (
        "⸺⸺⸺⸺⸺⸺⸺⸺\n"
        f"**{user_mention}** ✔\n"
        f"➝ **Qrupa daxil olma zamanı:**  {join_date} 🗓️\n"
        "⸺⸺⸺⸺⸺⸺⸺⸺"
    )
    
    await message.reply_text(fancy_text, disable_web_page_preview=True)


@app.on_message(filters.command("createqrup", ".") & filters.me)
async def create_group(client, message):
    
    group_name = " ".join(message.command[1:])
    
    if not group_name:
        await message.reply_text("Lütfen bir grup adı yazın.")
        return

    
    new_group = await client.create_group(group_name, [message.from_user.id])
    group_id = new_group.id
    user_mention = f"[{message.from_user.first_name}](tg://user?id={message.from_user.id})"
    
    
    fancy_text = (
        f"📌 **{group_name}** Qrupu quruldu! 📌\n"
        f"🔹 **Qrup ID:** {group_id}\n"
        f"🔹 **Qurucu:** {user_mention}"
    )
    
    await message.reply_text(fancy_text, disable_web_page_preview=True)


async def create_group(self, title: str, user_ids: list):
    chat = await self.send(
        raw.functions.messages.CreateChat(
            users=[await self.resolve_peer(user_id) for user_id in user_ids],
            title=title
        )
    )
    return types.Chat._parse(self, chat.chats[0])

OPENWEATHERMAP_API_KEY = "616ed5ef16d3d2bcadbca8d729fb140d"

@app.on_message(filters.command("hava", prefixes="."))
async def get_weather(client, message):
    try:
        
        text = message.text.split(maxsplit=1)
        if len(text) < 2:
            await message.reply("**İstədiyiniz bölgəni yazın**")
            return
        
        location = text[1]

        
        url = f"https://api.openweathermap.org/data/2.5/weather?q={location}&appid={OPENWEATHERMAP_API_KEY}&units=metric"
        response = requests.get(url)
        weather_data = response.json()

        if weather_data["cod"] != 200:
            await message.reply("Hava məlumatları alınmadı")
            return
        
        # Hava durumu verilerini hazırla
        weather_description = weather_data["weather"][0]["description"].capitalize()
        temperature = weather_data["main"]["temp"]
        humidity = weather_data["main"]["humidity"]
        wind_speed = weather_data["wind"]["speed"]

        # Sonucu kullanıcıya gönder
        await message.edit_text(
            f"**{location}** üçün hava haqqında:\n"
            f"Vəziyyət: {weather_description}\n"
            f"İstilik: {temperature} °C\n"
            f"Nəm: {humidity}%\n"
            f"Hava sürəti: {wind_speed} m/s"
        )

    except Exception as e:
        await message.reply(f"Bir hata oluştu: {e}")

user_activity = defaultdict(int)
word_usage = defaultdict(int)

@app.on_message(filters.group)
def track_activity(client, message):
    if message.text:
       print(f"Processing message from {message.from_user.id}")  
       user_activity[message.from_user.id] += 1
       for word in message.text.split():
           word_usage[word.lower()] += 1
       print(f"Updated user activity and word usage.")
@app.on_message(filters.command("summary"))
def send_summary(client, message):
    top_users = sorted(user_activity.items(), key=lambda x: x[1], reverse=True)[:5]
    top_words = sorted(word_usage.items(), key=lambda x:x[1], reverse=True)[:5]

    user_summary = "\n".join([f"{client.get_users(user_id).first_name}: {count}" for user_id, count in top_users])
    word_summary = "\n".join([f"{word}: {count}" for word, count in top_words])

    message.reply(f"📝 Günlük statistikaI\n\n👥 Ən aktiv Users:\n{user_summary}\n\n📚 Ən çoc istifadə olunan sözlər:\n{word_summary}")



print("Bot aktivdir")
app.run()
