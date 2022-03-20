import logging

from telegram import Update
from telegram.ext import Updater, Filters, CommandHandler, MessageHandler, CallbackContext

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',     #take time,level,name
                    level=logging.INFO)
logger = logging.getLogger(__name__)

TOKEN = "5173482597:AAGq28BsTbHO6XG-iuJjCkDk9l7Dqv_sC9I"


def start(update: Update, context: CallbackContext) -> None:
    print("hello")
    name  = update.message.from_user.first_name  #first name of the user messaging
    reply = "Hi!! {}".format(name)
    update.send_message(chat_id=update.message.chat_id, text=reply)      #sending message

def help(bot,update):
    reply = "How can I help You"
    bot.send_message(chat_id = update.message.chat_id, text = reply)  #sending message

def echo_text(bot,update):
    reply = update.message.text
    bot.send_message(chat_id = update.message.chat_id, text = reply)

def sticker(bot,update):
    reply = update.message.sticker.file_id
    bot.send_sticker(chat_id = update.message.chat_id, sticker = reply)

def error(bot,update):
    logger.error("Shit!! Update {} caused error {}".format(update,update.error))

def main():
    updater = Updater(token=TOKEN, use_context=True)  #take the updates
    dp = updater.dispatcher   #handle the updates

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(MessageHandler(Filters.text, echo_text))   #if the user sends text
    dp.add_handler(MessageHandler(Filters.sticker, sticker))  #if the user sends sticker
    dp.add_error_handler(error)
    updater.start_polling()
    logger.info("Started...")
    updater.idle()

if __name__=="__main__":
    main()