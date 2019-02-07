from telegram.ext import Updater
import logging
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler, Filters
from telegram import InlineQueryResultArticle, InputTextMessageContent
from telegram.ext import InlineQueryHandler
import urllib, json

url = "https://api.uwaterloo.ca/v2/parking/watpark.%7Bformat%7D?key=*********************"

updater = Updater(token='767923332:AAFzLVivCOPf-eId-EtV7_Sg8_o-5mbPxYU')
dispatcher = updater.dispatcher

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)
def start(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text="I'm a bot, please talk to me!")

start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)

updater.start_polling()

def fetch(bot, update):
    response = urllib.urlopen(url)
    data = json.loads(response.read())
    result = 'lot C: ' + str(data['data'][0]['current_count'])+ '\n' \
        'lot N: ' + str(data['data'][1]['current_count'])+ '\n' \
        'lot W: ' + str(data['data'][2]['current_count'])+ '\n' \
        'lot X: ' + str(data['data'][3]['current_count'])+ '\n'
    bot.send_message(chat_id=update.message.chat_id, text= result)

fetch_handler = CommandHandler('fetch', fetch)
dispatcher.add_handler(fetch_handler)

def echo(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text=update.message.text)

echo_handler = MessageHandler(Filters.text, echo)
dispatcher.add_handler(echo_handler)

def caps(bot, update, args):
    text_caps = ' '.join(args).upper()
    bot.send_message(chat_id=update.message.chat_id, text=text_caps)

caps_handler = CommandHandler('caps', caps, pass_args=True)
dispatcher.add_handler(caps_handler)

def inline_caps(bot, update):
    query = update.inline_query.query
    if not query:
        return
    results = list()
    results.append(
        InlineQueryResultArticle(
            id=query.upper(),
            title='Caps',
            input_message_content=InputTextMessageContent(query.upper())
        )
    )
    bot.answer_inline_query(update.inline_query.id, results)

inline_caps_handler = InlineQueryHandler(inline_caps)
dispatcher.add_handler(inline_caps_handler)


def unknown(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text="Sorry, I didn't understand that command.")

unknown_handler = MessageHandler(Filters.command, unknown)
dispatcher.add_handler(unknown_handler)

updater.idle()

# uwapi_key has been masked. to run this script, Please generate your own upapi_key
# at https://uwaterloo.ca/api/register
