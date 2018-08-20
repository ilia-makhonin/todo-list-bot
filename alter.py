import telebot
import utils
import mysql

bot = telebot.TeleBot('553436841:AAE7LE-DzZp3AKi4QLH185UX9ZCMjZ449rY')

users = dict()                  # Состояние пользователей(ожидание ввода и т.д.)


@bot.message_handler(commands=['start'])
def start_handler(message):
    user_id = message.from_user.id
    markup = create_markup([
        {'key': 'Добавить дело', 'call': 'new_task'},
        {'key': 'Новый раздел', 'call': 'new_list'}
    ], 'key', 'call')
    bot.send_message(user_id, utils.start_text, reply_markup=markup)
    mysql.user_db(user_id, message.from_user.first_name)
    users[user_id] = {'action': None, 'tasks': None}


@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    answer = call.data
    user_id = call.from_user.id
    if answer == 'new_task':
        text = 'Введите то, что Вы хотите сделать:'
        bot.send_message(user_id, text)
        users[user_id]['action'] = 'nt'
    elif answer == 'new_list':
        text = 'Введите название нового раздела:'
        bot.send_message(user_id, text)
        users[user_id]['action'] = 'nl'
    elif answer == 'rm_task':
        text = 'Какое дело Вы хотите удалить:'
        bot.send_message(user_id, text)
        users[user_id]['action'] = 'rt'
    elif answer == 'rm_list':
        text = 'Какой раздел Вы хотите удалить:'
        bot.send_message(user_id, text)
        users[user_id]['action'] = 'rl'
    elif answer == 'new_task_in_section':
        sections = mysql.get_task_for_user(user_id)
        print(sections[0])
        if sections[0][0]['section'] is None:
            text = 'У вас нет не одного раздела. Выбирете \"Новый раздел\" что бы создать раздел!'
            new_list = telebot.types.InlineKeyboardMarkup()
            new_list.add(telebot.types.InlineKeyboardButton('Новый раздел', callback_data='new_list'))
            bot.send_message(user_id, text, reply_markup=new_list)
            return True
        markup = create_markup(sections[0], 'section', 'section')
        text = 'Выбирете раздел, в который хотите добавить задачу:'
        bot.send_message(user_id, text, reply_markup=markup)
        users[user_id]['action'] = 'nts'
    else:
        if users[user_id]['action'] == 'nts':
            pass
        if users[user_id]['action'] == 'rt':
            pass
        if users[user_id]['action'] == 'rl':
            pass


@bot.message_handler(func=lambda message: True)
def text_handler(message):
    user_id = message.from_user.id
    text_task = message.text

    try:
        if users[user_id]['action'] == 'nt':
            bot.send_message(user_id, 'Дело добавленно!')
            add_task(user_id, text_task)
        if users[user_id]['action'] == 'nl':
            bot.send_message(user_id, 'Список создан!')
            add_section(user_id, text_task)
    except KeyError:
        users[user_id] = {'action': None, 'tasks': None}
        business_handler(user_id)


def business_handler(user_id):
    text = 'Что Вы хотите сделать?'
    markup = create_markup([
        {'key': 'Добавить дело', 'call': 'new_task'},
        {'key': 'Добавить дело в раздел', 'call': 'new_task_in_section'},
        {'key': 'Новый раздел', 'call': 'new_list'},
        {'key': 'Удалить дело', 'call': 'rm_task'},
        {'key': 'Удалить раздел', 'call': 'rm_list'}
    ], 'key', 'call')
    bot.send_message(user_id, text, reply_markup=markup)


def add_task(user_id, task, section=None):
    mysql.add_task(task, user_id, section=section)
    text = get_tasks(mysql.get_task_for_user(user_id))
    bot.send_message(user_id, text)
    users[user_id]['action'] = None


def add_section(user_id, section_name):
    mysql.add_task_list(user_id, section_name)
    text = get_tasks(mysql.get_task_for_user(user_id))
    bot.send_message(user_id, text)
    users[user_id]['action'] = None


def remove():
    # Удаляет дело из общего списка или из созданного пользователем списка
    pass


# def check_tasks(user_id):
#     if users[user_id]['tasks'] is None:
#         tasks = mysql.get_task_for_user(user_id)
#         users[user_id]['tasks'] = tasks
#         return tasks
#     return users[user_id]['tasks']


def create_markup(events, key, call):
    markup = telebot.types.InlineKeyboardMarkup()
    for button in events:
        markup.add(telebot.types.InlineKeyboardButton(button[key], callback_data=button[call]))
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
                if task['other'] is None:
                    continue
                output += task['other'] + '\n'
    return output


# Пример ответа Базы Данных
# arr = [
#     [
#         {'section': 'bd', 'tasks': None, 's_tk': None},
#         {'section': 'gndx', 'tasks': None, 's_tk': None},
#         {'section': 'gfn', 'tasks': None, 's_tk': None},
#         {'section': 'gsngd', 'tasks': None, 's_tk': None},
#         {'section': 'sfdgbngf', 'tasks': None, 's_tk': None},
#         {'section': 'dnhnh', 'tasks': None, 's_tk': None},
#         {'section': 'gfn', 'tasks': None, 's_tk': None},
#         {'section': 'ndh', 'tasks': None, 's_tk': None},
#         {'section': 'gfndgn', 'tasks': None, 's_tk': None},
#         {'section': 'gnsf', 'tasks': None, 's_tk': None},
#         {'section': 'fgsnsf', 'tasks': None, 's_tk': None},
#         {'section': 'dfnbg', 'tasks': None, 's_tk': None},
#         {'section': 'gfb', 'tasks': None, 's_tk': None},
#         {'section': 'gdngfn', 'tasks': None, 's_tk': None},
#         {'section': 'fbsdbgn', 'tasks': None, 's_tk': None},
#         {'section': 'nhdjhsnd', 'tasks': None, 's_tk': None}
#     ],
#     [
#         {'other': None, 'o_id': None}
#     ]
# ]


if __name__ == "__main__":
    bot.polling(none_stop=True)