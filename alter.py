import telebot
import utils
import bot_token
import mysql

bot = telebot.TeleBot('553436841:AAF2SSE5eVnLq_rV231OuGJDD3hqr_cf9eU')

users = dict()                  # Состояние пользователей(ожидание ввода и т.д.)


@bot.message_handler(commands=['start'])
def start_handler(message):
    user_id = message.from_user.id
    markup = create_markup([
        ['Новое дело', 'new_task'],
        ['Новый список', 'new_list']
    ])
    bot.send_message(user_id, utils.start_text, reply_markup=markup)
    mysql.user_db(user_id, message.from_user.first_name)
    users[user_id] = None


@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    answer = call.data
    user_id = call.from_user.id
    if answer == 'new_task':
        text = 'Введите то, что Вы хотите сделать:'
        bot.send_message(user_id, text)
        users[user_id] = 'nt'
    elif answer == 'new_list':
        text = 'Введите название нового раздела:'
        bot.send_message(user_id, text)
        users[user_id] = 'nl'
    elif answer == 'rm_task':
        text = 'Какое дело Вы хотите удалить:'
        bot.send_message(user_id, text)
        users[user_id] = 'rt'
    elif answer == 'rm_list':
        text = 'Какой раздел Вы хотите удалить:'
        bot.send_message(user_id, text)
        users[user_id] = 'rl'
    elif answer == 'new_task_in_section':
        text = 'Введите название раздела и то, что Вы хотите сделать:'
        bot.send_message(user_id, text)
        users[user_id] = 'nts'


@bot.message_handler(func=lambda message: True)
def text_handler(message):
    print('func "text_handler" -', message.text)
    business_handler(message.from_user.id)
    # Логика работы с текстовыми сообщениями


def business_handler(user_id):
    text = 'Что Вы хотите сделать?'
    markup = create_markup([
        ['Добавить дело', 'new_task'],
        ['Добавить дело в раздел', 'new_task_in_section'],
        ['Новый раздел', 'new_list'],
        ['Удалить дело', 'rm_task'],
        ['Удалить раздел', 'rm_list']
    ])
    bot.send_message(user_id, text, reply_markup=markup)
    print('users[{}] = {}'.format(user_id, users[user_id]))


def add_task(user_id, task):
    mysql.add_task(task, user_id)
    text = mysql.get_task_for_user(user_id)
    bot.send_message(user_id, text)


def add_section(user_id, section_name):
    mysql.add_task_list(user_id, section_name)
    text = mysql.get_task_for_user(user_id)
    bot.send_message(user_id, text)

def rm_task(user_id):
    # Удаляет дело из общего списка или из созданного пользователем списка
    pass

def rm_section(user_id):
    # Удаляет раздел
    pass


def create_markup(events):
    markup = telebot.types.InlineKeyboardMarkup()
    for button in events:
        markup.add(telebot.types.InlineKeyboardButton(button[0], callback_data=button[1]))
    return markup


def get_tasks(tasks_arr):
    output = 'Ваш список дел:\n'
    for type_task in tasks_arr:
        for task in type_task:
            if 'section' in task:
                if task['tasks'] is None:
                    output += task['section'] + ': Empty section' + '\n'
                    continue
                output += task['section'] + ': ' + task['tasks'] + '\n'
            if 'other' in task:
                output += task['other'] + '\n'
    return output




if __name__ == "__main__":
    bot.polling(none_stop=True)