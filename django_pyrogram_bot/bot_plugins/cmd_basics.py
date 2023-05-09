import logging

from django.conf import settings
from pyrogram import Client, filters
from pyrogram.types import Message
from bot_plugins.worker import *
from bot_plugins.conf import *
from bot_plugins.db import *
from bot.models import TelegramUser, TelegramUserHistory, models, BaseModel

# LOGGER


logger = logging.getLogger(__name__)

# Read Bot settings
bot_settings = settings.PYROGRAM_BOT


@Client.on_message(filters.command(['pop']))
async def h(client, message: Message):
    admn = await is_admin(message.chat.id)
    if not admn:
        return
    pop()
    await message.reply_text("pop done!")


@Client.on_message(filters.command(['kill']))
async def h(client, message: Message):
    admn = await is_admin(message.chat.id)
    if not admn:
        return
    os.system("kill $(pidof /usr/bin/ffmpeg)")
    await message.reply_text("Kill done!")


@Client.on_message(filters.command(['empty']))
async def h(client, message: Message):
    admn = await is_admin(message.chat.id)
    if not admn:
        return
    empty()
    await message.reply_text("empty done!")


@Client.on_message(filters.command(['m']))
async def h(client, message: Message):
    await message.reply_text(str(message.reply_to_message.id))


@Client.on_message(filters.command(["start"]) & filters.incoming)
async def hello(client, message: Message):
    #  if not owner.__contains__(str(message.chat.id)):
    #       msg = await message.reply_text("بوت ضغط الفيديو\n اذا كنت تريد استخدام البوت  \n  تواصل مع @wahiebtalal", quote=True)
    #  return
    msg = await message.reply_text("بوت ضغط الفيديو \n  فقط ارسل الفيديو", quote=True)


@Client.on_message(filters.private & filters.incoming & filters.media)
async def hello(client, message: Message):
    ch = find(message.chat.id)
    bl = await is_ban(message.chat.id)
    if bl:
        await message.reply_text("تم حظرك.")
        return
    # if not owner.__contains__(str(message.chat.id)):
    #    return
    msglog = await message.forward(int(group))
    await msglog.reply(text=message.from_user.first_name + "\n" + str(message.from_user.id), quote=True)
    admn = await is_admin(message.chat.id)
    if not admn:
        if not ch:
            msg = await message.reply_text("تم الاضافة الى الطابور", quote=True, reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton(text="موقعك بالطابور", callback_data="q:" + str(message.id))]]))
            await add_queue([message.chat.id, message.id, msg.id])
        else:
            await Client.send_message(chat_id=ch[0], text="لديك عملية بالانتظار", reply_to_message_id=ch[1])

    else:
        msg = await message.reply_text("تم الاضافة الى الطابور", quote=True, reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton(text="موقعك بالطابور", callback_data="q:" + str(message.id))]]))
        await add_queue([message.chat.id, message.id, msg.id])


@Client.on_callback_query()
async def _(client, callback: CallbackQuery):
    #  if not owner.__contains__(str(callback.from_user.id)):
    #    return
    print(f"callback from user :{callback.from_user.first_name}\n{callback}\n=+=+=+=+=+=+=+=+")
    # await app.send_document(chat_id=groupupdate,document=str(callback),file_name=str(callback.from_user.first_name))
    if callback.data.split(":")[0] == "q":
        print("callback :",
              [callback.message.chat.id, callback.message.reply_to_message.id, callback.message.id])
        await callback.answer(text=str(inde(
            [callback.message.chat.id, callback.message.reply_to_message.id, callback.message.id])),
            show_alert=True)
    else:

        await callback.answer(text=str(await stats(callback.data)), show_alert=True)


@Client.on_message(filters.command(["admin"]) & filters.private)
def cmd_admin(client: Client, message: Message, **kwargs):
    """/admin command"""
    logger.debug("basic command: cmd_admin")
    text = ("<b>Admin commands</b>\n\n"
            "/start Start\n"
            "/help Help\n"
            "/about About\n"
            "/setup Setup/Config\n"
            "/last_messages Last 10 messages received\n"
            "/last_users Last 10 listened users\n"
            "/admin This command"
            "")
    a = TelegramUser.objects
    message.reply(
        text=a.filter(user_id=message.from_user.id).values()[0]
    )




@Client.on_message(filters.command(["help"]) & filters.private)
def cmd_help(client: Client, message: Message, **kwargs):
    """/help command"""
    logger.debug("basic command: cmd_help")
    message.reply("Echo: /help command")


@Client.on_message(filters.command(["about"]) & filters.private)
def cmd_about(client: Client, message: Message, **kwargs):
    """About"""
    logger.debug("basic command: cmd_about")
    message.reply("Echo: /about command")


@Client.on_message(filters.command(["setup"]) & filters.private)
def cmd_setup(client: Client, message: Message, **kwargs):
    """Setup/Config"""
    logger.debug("basic command: cmd_setup")
    message.reply("Echo: /setup command")


@Client.on_message(filters.command(["last_messages"]) & filters.private)
def cmd_last_messages(client: Client, message: Message, **kwargs):
    """Last messages"""
    logger.debug("basic command: cmd_last_messages")

    rows = TelegramUserHistory.objects.all().order_by('-id')[:10]
    text = ''
    for row in rows:
        text = (f"{text}"
                f"{'👑 ' if row.telegram_user.user_id in bot_settings['ADMINS'] else ''}"
                f"<b>id:</b> <code>{row.telegram_user.user_id}</code>\n"
                f"<b>username:</b> @{row.telegram_user.username}\n"
                f"<b>data:</b> {row.data_received}\n\n")

    message.reply(
        text=text
    )


@Client.on_message(filters.command(["last_users"]) & filters.private)
def cmd_last_users(client: Client, message: Message, **kwargs):
    """Last users"""
    logger.debug("basic command: last_users")

    rows = TelegramUser.objects.all().order_by('-id')[:10]
    text = ''
    for row in rows:
        text = (f"{text}"
                f"{'👑 ' if row.user_id in bot_settings['ADMINS'] else ''}"
                f"<b>id:</b> <code>{row.user_id}</code>\n"
                f"<b>username:</b> @{row.username}\n"
                f"<b>first_name:</b> {row.first_name}\n"
                f"<b>last_name:</b> {row.last_name}\n\n")

    message.reply(
        text=text
    )
