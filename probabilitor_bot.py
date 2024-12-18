#!/usr/bin/env python

import logging
import random
import os
import dotenv
import re

from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from telegram import Update

#from telegram.ext import Updater, CommandHandler, CallbackQueryHandler
#from telegram import ParseMode, InlineKeyboardButton, InlineKeyboardMarkup
#from telegram.error import (TelegramError, Unauthorized, BadRequest, TimedOut, ChatMigrated, NetworkError)

__version__ = "0.4"

# enable logging and get logger
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

logger = logging.getLogger(__name__)

dotenv.load_dotenv()

TOKEN = os.getenv("TOKEN")

if TOKEN is None:
    raise EnvironmentError("TOKEN should be provided as environment variable")


async def who_callback(update: Update, context: ContextTypes.DEFAULT_TYPE): 
    """State who you are."""
    chat_id = update.message.chat_id
    text = "I am Probabilitor, the greatest wizard in all mathology - give or take an error of 0.4."
    await context.bot.send_message(chat_id, text)


async def roll_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Roll dice!"""
    chat_id = update.message.chat_id
    msg = "".join(context.args).replace(" ", "")
    roll_pattern = r"^(\d*d\d+|\d)([+-](\d*d\d|\d))*$"
    roll_match = re.match(roll_pattern, msg)
    if roll_match is None:
        text = "This spell works nowise!"
        await context.bot.send_message(chat_id, text)
        return False
    # unfortunately, re does not capture repeated groups
    # need to iterate over rolls and modifiers individually
    pattern = r"([+-]?)(\d*d\d+|[+-]?\d)"
    rolls = []
    for roll_match in re.finditer(pattern, msg):
        print(roll_match.groups())
        sign = -1 if roll_match.group(1) == "-" else 1
        if "d" in roll_match.group(2):
            n, sides = roll_match.group(2).split("d")
            if n == "":
                n = "1"
            for i in range(int(n)):
                roll = sign * random.randint(1, int(sides))
                rolls.append(roll)
        else:
            rolls.append(sign * int(roll_match.group(2)))
    text = "+".join(map(str, rolls)).replace("+-", "-")
    text += f"\n= {sum(rolls)}"
    await context.bot.send_message(chat_id, text)


async def coinflip_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Flip a coin."""
    chat_id = update.message.chat_id
    text = random.choice(['⚪','⚫'])
    await context.bot.send_message(chat_id, text)


async def tableflip_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Flip a table."""
    chat_id = update.message.chat_id
    text = "(╯°□°)╯︵ ┻━┻"
    await context.bot.send_message(chat_id, text)

def error_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)

def main():
    """Start the bot."""
    app = ApplicationBuilder().token(TOKEN).build()

    who_handler = CommandHandler("who", who_callback)
    app.add_handler(who_handler)

    roll_handler = CommandHandler("roll", roll_callback, has_args=True)
    app.add_handler(roll_handler)

    coinflip_handler = CommandHandler("coinflip", coinflip_callback)
    app.add_handler(coinflip_handler)

    tableflip_handler = CommandHandler("tableflip", tableflip_callback)
    app.add_handler(tableflip_handler)

    # roll_handler = CommandHandler("roll", roll, has_args=True)
    # app.add_handler(roll_handler)

    app.add_error_handler(error_callback)

    app.run_polling()

if __name__ == '__main__':
    main()
