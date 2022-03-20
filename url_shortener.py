import logging
import urllib
import requests
import redis

from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update, ParseMode, InlineKeyboardMarkup, \
    InlineKeyboardButton
from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters,
    ConversationHandler,
    CallbackContext,
)

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
re = redis.Redis(
    host='redis-11024.c8.us-east-1-3.ec2.cloud.redislabs.com',
    port=11024,
    password='6GxkgPwOWUUlm1cSINg8XnWGgPBfS4te')

logger = logging.getLogger(__name__)

GENDER, PHOTO, LOCATION, BIO = range(4)
URL = range(600)
key = '3e8274e7feaf9eaaf909be641a1ca15691b7b'


def start(update: Update, context: CallbackContext) -> int:
    """Starts the conversation and asks the user about their gender."""
    # reply_keyboard = [['Boy', 'Girl', 'Other']]

    update.message.reply_text(
        'Hey! Please mention the url you want to shorten'
        # reply_markup=ReplyKeyboardMarkup(
        #     reply_keyboard, one_time_keyboard=True, input_field_placeholder='Boy or Girl?'
        # ),

    )

    return URL


def shorten_url(update: Update, context: CallbackContext) -> int:
    user = update.message.from_user
    send_suggestion = False
    logger.info("URL of %s: %s", user.first_name, update.message.text)
    url = urllib.parse.quote(update.message.text)
    chat_id = update.message.chat_id
    r = requests.get('http://cutt.ly/api/api.php?key={}&short={}'.format(key, url))
    if r.json()['url']['status'] is not 7:
        update.message.reply_text("Please enter a valid URL")
    else:
        shortened_link = r.json()['url']['shortLink']
        count = int(re.get(chat_id))
        if count is not None:
            count = count + 1
            if count % 10 == 0:
                send_suggestion = True
            re.set(chat_id, count)
            print(count)
        else:
            re.set(chat_id, 1)

        update.message.reply_text(shortened_link)
        if send_suggestion:
            update.message.reply_text(
                'Hope you are enjoying the tool!!!\n Consider buying me a coffee if you wish!!!',
                reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton(text='BuyMeACoffee', url='https://www.buymeacoffee.com/dk17')],
                ])
            )


def cancel(update: Update, context: CallbackContext) -> int:
    """Cancels and ends the conversation."""
    user = update.message.from_user
    logger.info("User %s canceled the conversation.", user.first_name)
    update.message.reply_text(
        'Bye! I hope we can talk again some day.', reply_markup=ReplyKeyboardRemove()
    )

    return ConversationHandler.END


def main() -> None:
    """Run the bot."""
    # Create the Updater and pass it your bot's token.
    updater = Updater("5194362531:AAE62SA72SWXyE6Dqb29_JooTjdJ_VJiafE")

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # Add conversation handler with the states GENDER, PHOTO, LOCATION and BIO
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            URL: [MessageHandler(Filters.text & ~Filters.command, shorten_url)],
        },
        fallbacks=[CommandHandler('cancel', cancel)],
    )

    dispatcher.add_handler(conv_handler)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
