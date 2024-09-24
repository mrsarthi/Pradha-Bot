import time
from typing import Final
import botScript
from telegram import Update
from telegram.ext import Updater, Application, CommandHandler, MessageHandler, filters, ContextTypes


TOKEN: Final = '7058434566:AAE21MjZaHMEf2xhmg8Dt63LtQKhVL5wJK0'
BOT_USERNAME: Final = '@harshPBot'


def get_greeting():
    current_time = time.localtime().tm_hour
    if 6 <= current_time < 12:
        return "Good morning!"
    elif 12 <= current_time < 18:
        return "Good afternoon!"
    elif 18 <= current_time < 22:
        return "Good evening!"
    else:
        return "Hello!"


# COMMANDS
async def startCommand(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(get_greeting() + '. How can I help you today:')


async def helpCommand(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('What can I help you with?')


async def askCommand(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # await update.message.reply_text('Ask away: ')
    user_query = update.message.text
    response = botScript.search_response(user_query)
    await update.message.reply_text(response)


async def stopCommand(update: Update, context: ContextTypes.DEFAULT_TYPE, updater: Updater):
    await update.message.reply_text('Stopping the bot.')
    updater.stop()


async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f'Update {update} caused error {context.error}')


def main():
    print('Starting Bot....')
    app = Application.builder().token(TOKEN).build()

    # COMMANDS & MESSAGES
    app.add_handler(CommandHandler('start', startCommand))
    app.add_handler(CommandHandler('help', helpCommand))
    app.add_handler(CommandHandler('stop', stopCommand))
    app.add_handler(MessageHandler(
        filters.TEXT, askCommand))

    # ERRORS
    app.add_error_handler(error)

    print('Polling....')
    app.run_polling(poll_interval=3)


if __name__ == "__main__":
    main()
