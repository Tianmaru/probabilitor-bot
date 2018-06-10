#!/usr/bin/env python
# -*- coding: utf-8 -*-


import logging, random
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler
from telegram import ParseMode, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.error import (TelegramError, Unauthorized, BadRequest, TimedOut, ChatMigrated, NetworkError)

TOKEN = '522163911:AAE2to2TTuXANv3dLkfJZlyyktFDI7FjI-8'
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)


def add(bot, update, args):
    """Add numbers together."""
    arg_sum = 0
    for arg in args:
        arg_sum += float(arg)
    bot.sendMessage(chat_id=update.message.chat_id, text='%s=%.2f' % ('+'.join(args), arg_sum))


def roll(bot, update, args):
    """Roll a dice."""
    try:
        number, faces = (int(x) for x in args[0].split('d'))
    except (IndexError, ValueError):
        number = 1
        faces = 20
    finally:
        results = []
        for i in range(number):
            results.append(random.randint(1, faces))
        if not number > 1:
            result = str(sum(results))
        else:
            results_sum = sum(results)
            result = '+'.join(map(str,results))+'='+str(results_sum)
        bot.sendMessage(chat_id=update.message.chat_id, text='*%dd%d:* %s' % (number, faces, result), parse_mode=ParseMode.MARKDOWN)


def flip(bot,update):
    """Flip a coin"""
    bot.sendMessage(chat_id=update.message.chat_id, text=random.choice(['⚪','⚫']))


ATTRIBUTES = ['lonely','obese','confused','friendly','wild','suspicious','hysterical','exhausted','fluffy','pink', 'beautiful','enraged','grabby','boozed','ancient','bloodthirsty','smelly','cuddly','lovely','greedy','spooky','wobbly','sleepy','tiny','giant', 'hungry']
ACTORS = ['troll', 'vampire', 'goblin', 'orc', 'zombie', 'elf','dwarf','cyborg','centaurtaur', 'sphinx','minotaur','mermaid','dragon','skeleton','unicorn','ghost','medusa','beholder', 'wolf', 'demon','man','woman','pirate','merchant','bandit','priest','witch']
VOWELS = ['a', 'e', 'i', 'o', 'u']


def encounter(bot,update):
    """Random encounter."""
    actor = random.choice(ACTORS)
    attribute = random.choice(ATTRIBUTES)
    article = 'A'
    for vowel in VOWELS:
        if attribute.startswith(vowel):
            article = 'An'
    bot.sendMessage(chat_id=update.message.chat_id, text='*%s %s %s appears!*' % (article,attribute, actor), parse_mode=ParseMode.MARKDOWN)


def build_menu(buttons,n_cols,header_buttons=None,footer_buttons=None):
    menu = [buttons[i:i + n_cols] for i in range(0, len(buttons), n_cols)]
    if header_buttons:
        menu.insert(0, header_buttons)
    if footer_buttons:
        menu.append(footer_buttons)
    return menu


CALLBACK_SUMMON_POSITIVE = 'summon_positive'
CALLBACK_SUMMON_NEGATIVE = 'summon_negative'


def summon_reply_markup():
    summon_button_list = [
        InlineKeyboardButton("Yay!", callback_data=CALLBACK_SUMMON_POSITIVE),
        InlineKeyboardButton("Nay!", callback_data=CALLBACK_SUMMON_NEGATIVE)
    ]
    return InlineKeyboardMarkup(build_menu(summon_button_list, n_cols=2))


def summon(bot,update):
    """Summon your companions!"""
    reply_markup = summon_reply_markup()
    summoner = update.message.from_user.first_name
    bot.sendMessage(chat_id=update.message.chat_id,
                    text='*%s summons you!*\n*Are you ready for a new adventure?*' % (summoner),
                    parse_mode=ParseMode.MARKDOWN,
                    reply_markup=reply_markup)


def summon_callback(bot, update):
    query = update.callback_query
    data = query.data
    user = query.from_user.first_name
    if data == CALLBACK_SUMMON_POSITIVE:
        text = '\"Yay!\"'
    elif data == CALLBACK_SUMMON_NEGATIVE:
        text = '\"Nay!\"'
    reply_markup = summon_reply_markup()
    query.edit_message_text(text=query.message.text_markdown + "\n{}: {}".format(user, text),
                            parse_mode=ParseMode.MARKDOWN,
                            reply_markup=reply_markup)
    # For Telegram notification:
    # query.answer(text="{}: {}".format(user, text))


def query_callback(bot, update):
    """CallbackQueryHandler"""
    data = update.callback_query.data
    if data.startswith('summon'):
        summon_callback(bot, update)
    else:
        pass


def error_callback(bot, update, error):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, error)


def main():
    """Start the bot."""
    updater = Updater(token=TOKEN)
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler('add', add, pass_args=True))
    dispatcher.add_handler(CommandHandler('roll', roll, pass_args=True))
    dispatcher.add_handler(CommandHandler('flip', flip))
    dispatcher.add_handler(CommandHandler('encounter', encounter))
    dispatcher.add_handler(CommandHandler('summon', summon))
    dispatcher.add_handler(CallbackQueryHandler(query_callback))
    dispatcher.add_error_handler(error_callback)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
