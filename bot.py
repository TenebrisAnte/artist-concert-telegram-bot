import config
import telebot
from googletrans import Translator

bot = telebot.TeleBot(config.token)

trans = Translator()


@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, "Я можу перекласти твій текст. Напиши будь-що англійською")

@bot.message_handler(content_types=["text"])
def repeat_all_messages(message):
    bot.send_message(message.chat.id, trans.translate(message.text, dest='ru').text)

if __name__ == '__main__':
     bot.infinity_polling()