# -*- coding: utf-8 -*-

import telebot
import utils
import bot_token
import mysql

bot = telebot.TeleBot('553436841:AAF2SSE5eVnLq_rV231OuGJDD3hqr_cf9eU')

condition = dict()                  #Состояние пользователей(ожидание ввода и т.д.)
business = dict()                   #Список общих дел пользователей
list_business = dict()              #Списки дел
edit_business = None


@bot.message_handler(commands=['start'])
def start_handler(message):
    chat_id = message.chat.id
    bot.send_message(chat_id, utils.start_text)
    condition[chat_id] = utils.Waiting.STANDART.value          #Пользователь добавляется в БД
    mysql.user_db(message.from_user.id, message.from_user.first_name)
    business[chat_id] = []
    list_business[chat_id] = []
    business_handler(message)


@bot.callback_query_handler(func=lambda call: True)  #Ответ на кнопки
def callback_handler(call):
    global edit_business
    if call.data == "Новое дело":
        bot.send_message(call.from_user.id, 'Введите название дела')
        condition[call.from_user.id] = utils.Waiting.WAITING_BUSINESS.value
    elif call.data == "Удалить дело":
        markup = utils.create_markup(business[call.from_user.id])
        bot.send_message(call.from_user.id, 'Выберите, какое дело вы хотите удалить:', reply_markup=markup)
        condition[call.from_user.id] = utils.Waiting.EDIT_BUSINESS.value
    elif condition[call.from_user.id] == utils.Waiting.EDIT_BUSINESS.value:
        markup = utils.create_markup(('Удалить',))
        edit_business = call.data
        bot.send_message(call.from_user.id, 'Вы выбрали дело "{}"'.format(call.data), reply_markup=markup)
        condition[call.from_user.id] = utils.Waiting.EDIT_BUSINESS_WAITING_RESPONSE
    elif condition[call.from_user.id] == utils.Waiting.EDIT_BUSINESS_WAITING_RESPONSE:
        business[call.from_user.id].remove(edit_business)
        business_handler(call)


def business_handler(call):
    try:
        chat_id = call.chat.id
    except AttributeError:
        chat_id = call.message.chat.id

    condition[chat_id] = utils.Waiting.STANDART.value
    markup = utils.create_markup([
        "Новое дело", "Удалить дело", "Мои списки дел", "Новый список дел"
    ])
    if len(business[chat_id]) == 0:
        bot.send_message(chat_id, utils.business_0, reply_markup=markup)
    else:
        bot.send_message(chat_id, utils.list_of_business(business[chat_id]), reply_markup=markup)


@bot.message_handler(func=lambda message: True)
def new_business(message):
    try:
        if condition[message.chat.id] == utils.Waiting.WAITING_BUSINESS.value:
            business[message.chat.id].append(message.text)
            bot.send_message(message.chat.id, 'Отлично, дело добавлено')
            business_handler(message)
        else:
            business_handler(message)
    except KeyError:
        business[message.chat.id] = []
        business_handler(message)


if __name__ == "__main__":
    bot.polling(none_stop=True)