# -*- coding: utf-8 -*-

import telebot
from enum import Enum
start_text = '''
Добро пожаловать в бот-список дел!
''' # Приветствие с пользователем




class Waiting(Enum):

    STANDART = '0'              #Состояние покоя
    WAITING_BUSINESS = '1'      #Ожидание ввода дела
    WAITING_LIST = '2'          #Одилание названия списка
    EDIT_BUSINESS = '3'
    EDIT_BUSINESS_WAITING_RESPONSE = '4'

business_0 = '''
На данный момент у вас 0 дел.
Воспользуйтесь кнопкой ниже, чтобы добавить дело
'''



def list_of_business(bussin):
    bussines_not_0 = 'Ваши дела:\n'
    for i in bussin:
        bussines_not_0 = bussines_not_0 + i + '\n'
    return bussines_not_0



def create_markup(events):
    markup = telebot.types.InlineKeyboardMarkup()
    for button in events:
        markup.add(telebot.types.InlineKeyboardButton(button, callback_data=button))
    return markup


