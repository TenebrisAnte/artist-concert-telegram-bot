import config
import telebot
from parser_ import *

bot = telebot.TeleBot(config.token)


@bot.message_handler(commands=['sticker'])
def sticker_id(message):
    print(message)


@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAJfW16v6C36rIoQIwLpLuI8aECQQ74-AAJqAAOFQTIQBK2dCfS3CYQZBA')
    bot.send_message(message.chat.id, 'Я збираю інформацію про артистів та їхні концерти.\n'
                                      'Якщо ти хочеш затусити після душного карантину – то ти по адресу 😎🥳\n\n'
                                      'Список моїх команд:\n'
                                      '/start – початок роботи\n'
                                      '/help – Як я працюю?\n'
                                      '/artist - '
                                      'я допоможу тобі розслабитися) 😏😏😏😏😏😏😏😏😏😏\n')


@bot.message_handler(commands=['artist'])
def start_artist(message):
    bot.send_message(message.chat.id, "Напиши ім'я артиста")


@bot.message_handler(commands=['help'])
def help_for_user(message):
    bot.send_message(message.chat.id, "Напиши ім'я артиста, або дату концерту для пошку доступних концертів, наприклад:\nОлег Винник\n24.07.2020\n24-27.07.2020")


@bot.message_handler(content_types=['text'])
def get_name(message):
    name = search_artist(message.text)
    markup = telebot.types.InlineKeyboardMarkup()
    n=1
    for i in name:
        markup.add(telebot.types.InlineKeyboardButton(text=i, callback_data=i))
        n+=1
    if name == {}:
        bot.send_message(message.chat.id, text="Такого виконавця немає, спробуйте ще раз")
    else:
        bot.send_message(message.chat.id, text="Вибери артиста", reply_markup=markup)
        print(name)


@bot.callback_query_handler(func=lambda call: True)
def query_handler(call):
    bot.answer_callback_query(callback_query_id=call.id, text='Дякую!')
    print(call)
    ans = call.data
    bot.send_message(call.message.chat.id, ans)



if __name__=='__main__':
    bot.infinity_polling()