import telebot


start_text = 'Добро пожаловать в бот-список дел!\nНа данный момент у вас 0 дел. ' \
             'Воспользуйтесь кнопками ниже, чтобы добавить дело или раздел.'


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


# def check_tasks(user_id):
#     if users[user_id]['tasks'] is None:
#         tasks = mysql.get_task_for_user(user_id)
#         users[user_id]['tasks'] = tasks
#         return tasks
#     return users[user_id]['tasks']


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
