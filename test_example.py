import logging
import string
from typing import List, Tuple, cast

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (
    Updater,
    CommandHandler,
    CallbackQueryHandler,
    CallbackContext,
    InvalidCallbackData,
    PicklePersistence,
)

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)


def start(update: Update, context: CallbackContext) -> None:
    """Sends a message with 5 inline buttons attached."""
    print("called start")
    number_list: List[int] = []
    update.message.reply_text('Please choose:', reply_markup=build_keyboard(number_list))


def help_command(update: Update, context: CallbackContext) -> None:
    """Displays info on how to use the bot."""
    update.message.reply_text(
        "Use /start to test this bot. Use /clear to clear the stored data so that you can see "
        "what happens, if the button data is not available. "
    )


def clear(update: Update, context: CallbackContext) -> None:
    """Clears the callback data cache"""
    context.bot.callback_data_cache.clear_callback_data()  # type: ignore[attr-defined]
    context.bot.callback_data_cache.clear_callback_queries()  # type: ignore[attr-defined]
    update.effective_message.reply_text('All clear!')


def build_keyboard(current_list: List[int]) -> InlineKeyboardMarkup:
    """Helper function to build the next inline keyboard."""
    return InlineKeyboardMarkup.from_column(
        [InlineKeyboardButton(str(i), callback_data=(i, current_list)) for i in range(1, 6)]
    )


def url_short(update: Update, context: CallbackContext) -> None:
    """Helper function to build the next inline keyboard."""
    update.message.reply_text("please give url")
    user_input = update.message.text
    update.message.reply_text("you have typed: "+user_input)


def list_button(update: Update, context: CallbackContext) -> None:
    """Parses the CallbackQuery and updates the message text."""
    query = update.callback_query
    query.answer()
    # Get the data from the callback_data.
    # If you're using a type checker like MyPy, you'll have to use typing.cast
    # to make the checker get the expected type of the callback_data
    number, number_list = cast(Tuple[int, List[int]], query.data)
    # append the number to the list
    number_list.append(number)

    query.edit_message_text(
        text=f"So far you've selected {number_list}. Choose the next item:",
        reply_markup=build_keyboard(number_list),
    )

    # we can delete the data stored for the query, because we've replaced the buttons
    context.drop_callback_data(query)


def handle_invalid_button(update: Update, context: CallbackContext) -> None:
    """Informs the user that the button is no longer available."""
    update.callback_query.answer()
    update.effective_message.edit_text(
        'Sorry, I could not process this button click 😕 Please send /start to get a new keyboard.'
    )


def main() -> None:
    """Run the bot."""
    # We use persistence to demonstrate how buttons can still work after the bot was restarted
    persistence = PicklePersistence(
        filename='arbitrarycallbackdatabot.pickle', store_callback_data=True
    )
    # Create the Updater and pass it your bot's token.
    updater = Updater("5173482597:AAGq28BsTbHO6XG-iuJjCkDk9l7Dqv_sC9I", persistence=persistence,
                      arbitrary_callback_data=True)

    updater.dispatcher.add_handler(CommandHandler('start', start))
    updater.dispatcher.add_handler(CommandHandler('help', help_command))
    updater.dispatcher.add_handler(CommandHandler('clear', clear))
    updater.dispatcher.add_handler(CommandHandler('url_short', url_short))
    updater.dispatcher.add_handler(
        CallbackQueryHandler(handle_invalid_button, pattern=InvalidCallbackData)
    )
    updater.dispatcher.add_handler(CallbackQueryHandler(list_button))

    # Start the Bot
    updater.start_polling()

    # Run the bot until the user presses Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT
    updater.idle()


if __name__ == '__main__':
    main()
