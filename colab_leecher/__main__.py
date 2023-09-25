# copyright 2023 © Xron Trix | https://github.com/Xrontrix10


import logging, os
from pyrogram import filters
from datetime import datetime
from pyrogram.errors import BadRequest
from asyncio import sleep, get_event_loop
from colab_leecher import colab_bot, OWNER
from .utility.task_manager import taskScheduler
from colab_leecher.utility.handler import cancelTask
from .utility.variables import BOT, MSG, BotTimes, Paths
from .utility.helper import isLink, setThumbnail, message_deleter
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

src_request_msg = None


@colab_bot.on_message(filters.command("start") & filters.private)
async def start(client, message):
    await message.delete()
    text = "**Hey There, 👋🏼 It's Colab Leecher**\n\n◲ I am a Powerful File Transloading Bot 🚀\n◲ I can Transfer Files To Telegram or Your Google Drive From Various Sources 🦐"
    keyboard = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    "Repository 🦄", url="https://github.com/XronTrix10/Telegram-Leecher"
                ),
                InlineKeyboardButton("Support 💝", url="https://t.me/Colab_Leecher"),
            ],
        ]
    )
    await message.reply_text(text, reply_markup=keyboard)


@colab_bot.on_message(filters.command("colabxr") & filters.private)
async def colabxr(client, message):
    global BOT, src_request_msg
    text = "<b>◲ Send Me DOWNLOAD LINK(s) 🔗»\n◲</b> <i>You can enter multiple links in new lines and I will download each of them 😉 </i>"
    await message.delete()
    BOT.State.started = True
    if BOT.State.task_going == False:
        src_request_msg = await message.reply_text(text)
    else:
        msg = await message.reply_text(
            "I am Already Working ! Please Wait Until I finish !!"
        )
        await sleep(15)
        await msg.delete()


async def send_settings(client, message, msg_id, command: bool):
    up_mode = "document" if BOT.Options.stream_upload else "media"
    keyboard = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    f"Set {up_mode.capitalize()}", callback_data=up_mode
                ),
                InlineKeyboardButton("Video Convert", callback_data="video"),
            ],
            [
                InlineKeyboardButton("Caption Font", callback_data="caption"),
                InlineKeyboardButton("Thumbnail", callback_data="thumb"),
            ],
            [
                InlineKeyboardButton("Set Suffix", callback_data="set-suffix"),
                InlineKeyboardButton("Set Prefix", callback_data="set-prefix"),
            ],
            [InlineKeyboardButton("Close ✘", callback_data="close")],
        ]
    )
    text = "**CURRENT BOT SETTINGS ⚙️ »**"
    text += f"\n\n╭⌬ UPLOAD » <i>{BOT.Setting.stream_upload}</i>"
    text += f"\n├⌬ CONVERT » <i>{BOT.Setting.convert_video}</i>"
    text += f"\n├⌬ CAPTION » <i>{BOT.Setting.caption}</i>"
    pr = "None" if BOT.Setting.prefix == "" else "Exists"
    su = "None" if BOT.Setting.suffix == "" else "Exists"
    thmb = "None" if not BOT.Setting.thumbnail else "Exists"
    text += f"\n├⌬ PREFIX » <i>{pr}</i>\n├⌬ SUFFIX » <i>{su}</i>"
    text += f"\n╰⌬ THUMBNAIL » <i>{thmb}</i>"
    try:
        if command:
            await message.reply_text(text=text, reply_markup=keyboard)
        else:
            await colab_bot.edit_message_text(
                chat_id=message.chat.id, message_id=msg_id, text=text, reply_markup=keyboard
            )
    except BadRequest as error:
        logging.error(f"Same text not modified | {error}")
    except Exception as error:
        logging.error(f"Error Modifying message | {error}")


@colab_bot.on_message(filters.command("settings") & filters.private)
async def settings(client, message):
    if message.chat.id == OWNER:
        await message.delete()
        await send_settings(client, message, message.id, True)


@colab_bot.on_message(filters.reply)
async def setPrefix(client, message):
    global BOT, SETTING
    if BOT.State.prefix:
        BOT.Setting.prefix = message.text
        BOT.State.prefix = False

        await send_settings(client, message, message.reply_to_message_id, False)
        await message.delete()
    elif BOT.State.suffix:
        BOT.Setting.suffix = message.text
        BOT.State.suffix = False

        await send_settings(client, message, message.reply_to_message_id, False)
        await message.delete()


@colab_bot.on_message(filters.create(isLink) & ~filters.photo)
async def handle_url(client, message):
    success = await Do_Mirror(source, is_ytdl, is_zip, is_unzip, is_dualzip)
    if success:
        msg = await message.reply_text("**Link Successfully Added ✅**")
        await message.delete()
    else:
        msg = await message.reply_text(
            "🥲 **Could not add link, Please Try Again !**", quote=True
        )

@colab_bot.on_message(filters.photo & filters.private)
async def handle_image(client, message):
    success = await setThumbnail(message)
    if success:
        msg = await message.reply_text("**Thumbnail Successfully Changed ✅**")
        await message.delete()
    else:
        msg = await message.reply_text(
            "🥲 **Couldn't Set Thumbnail, Please Try Again !**", quote=True
        )
    await sleep(15)
    await message_deleter(message, msg)


@colab_bot.on_message(filters.command("setname") & filters.private)
async def custom_name(client, message):
    global BOT
    if len(message.command) != 2:
        msg = await message.reply_text(
            "Send\n/setname <code>custom_fileame.extension</code>\nTo Set Custom File Name 📛",
            quote=True,
        )
    else:
        BOT.Options.custom_name = message.command[1]
        msg = await message.reply_text(
            "Custom Name Has Been Successfully Set !", quote=True
        )

    await sleep(15)
    await message_deleter(message, msg)


@colab_bot.on_message(filters.command("zipaswd") & filters.private)
async def zip_pswd(client, message):
    global BOT
    if len(message.command) != 2:
        msg = await message.reply_text(
            "Send\n/zipaswd <code>password</code>\nTo Set Password for Output Zip File. 🔐",
            quote=True,
        )
    else:
        BOT.Options.zip_pswd = message.command[1]
        msg = await message.reply_text(
            "Zip Password Has Been Successfully Set !", quote=True
        )

    await sleep(15)
    await message_deleter(message, msg)


@colab_bot.on_message(filters.command("unzipaswd") & filters.private)
async def unzip_pswd(client, message):
    global BOT
    if len(message.command) != 2:
        msg = await message.reply_text(
            "Send\n/unzipaswd <code>password</code>\nTo Set Password for Extracting Archives. 🔓",
            quote=True,
        )
    else:
        BOT.Options.unzip_pswd = message.command[1]
        msg = await message.reply_text(
            "Unzip Password Has Been Successfully Set !", quote=True
        )

    await sleep(15)
    await message_deleter(message, msg)


@colab_bot.on_message(filters.command("help") & filters.private)
async def help_command(client, message):
    msg = await message.reply_text(
        "Send /start To Check If I am alive 🤨\n\nSend /colabxr and follow prompts to start transloading 🚀\n\nSend /settings to edit bot settings ⚙️\n\nSend /setname To Set Custom File Name 📛\n\nSend /zipaswd To Set Password For Zip File 🔐\n\nSend /unzipaswd To Set Password to Extract Archives 🔓\n\n⚠️ **You can ALWAYS SEND an image To Set it as THUMBNAIL for your files 🌄**",
        quote=True,
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "Instructions 📖",
                        url="https://github.com/XronTrix10/Telegram-Leecher/wiki/INSTRUCTIONS",
                    ),
                ],
                [
                    InlineKeyboardButton(  # Opens a web URL
                        "Channel 📣",
                        url="https://t.me/Colab_Leecher",
                    ),
                    InlineKeyboardButton(  # Opens a web URL
                        "Group 💬",
                        url="https://t.me/Colab_Leecher_Discuss",
                    ),
                ],
            ]
        ),
    )
    await sleep(15)
    await message_deleter(message, msg)


logging.info("Colab Leecher Started !")
colab_bot.run()
