import telebot
import utils
import mysql

bot = telebot.TeleBot('553436841:AAE7LE-DzZp3AKi4QLH185UX9ZCMjZ449rY')

users = dict()                  # Состояние пользователей(ожидание ввода и т.д.)


@bot.message_handler(commands=['start'])
def start_handler(message):
    user_id = message.from_user.id
    markup = utils.create_markup([
        {'key': 'Добавить дело', 'call': 'new_task'},
        {'key': 'Новый раздел', 'call': 'new_list'}
    ], 'key', 'call')
    bot.send_message(user_id, utils.start_text, reply_markup=markup)
    mysql.user_db(user_id, message.from_user.first_name)  # Сохранение пользователя в БД
    users[user_id] = {'action': None, 'tasks': None}      # Объект с действием пользователя и актуальным списком дел


@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    answer = call.data                                # Обработка действий из основного списка
    user_id = call.from_user.id                       # 1) Добавить дело
    if answer == 'new_task':                          # 2) Создать раздел
        text = 'Введите то, что Вы хотите сделать:'   # 3) Добавить дело в раздел
        bot.send_message(user_id, text)               # 4) Удалить дело
        users[user_id]['action'] = 'nt'               # 5) Удалить раздел
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
        if sections[0][0]['section'] is None:              # Проверка - есть ли у пользователя разделы
            text = 'У вас нет не одного раздела. Выбирете \"Новый раздел\" что бы создать раздел!'
            new_list = telebot.types.InlineKeyboardMarkup()
            new_list.add(telebot.types.InlineKeyboardButton('Новый раздел', callback_data='new_list'))
            bot.send_message(user_id, text, reply_markup=new_list)
            return True                          # Отобразить кнопку создания раздела, если у пользователя их нет
        markup = utils.create_markup(sections[0], 'section', 'section')
        text = 'Выбирете раздел, в который хотите добавить задачу:'
        bot.send_message(user_id, text, reply_markup=markup)
        users[user_id]['action'] = 'nts'
    else:                       # Второй уровень обработки действий
        if users[user_id]['action'] == 'nts':
            pass                # Добавление дела в выбранный раздел, удаление дела, удаление раздела
        if users[user_id]['action'] == 'rt':
            pass
        if users[user_id]['action'] == 'rl':
            pass


@bot.message_handler(func=lambda message: True)
def text_handler(message):              # Обработка текстовых сообщений
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
    markup = utils.create_markup([
        {'key': 'Добавить дело', 'call': 'new_task'},
        {'key': 'Добавить дело в раздел', 'call': 'new_task_in_section'},
        {'key': 'Новый раздел', 'call': 'new_list'},
        {'key': 'Удалить дело', 'call': 'rm_task'},
        {'key': 'Удалить раздел', 'call': 'rm_list'}
    ], 'key', 'call')
    bot.send_message(user_id, text, reply_markup=markup)


def add_task(user_id, task, section=None):
    mysql.add_task(task, user_id, section=section)               # Добавление дела в БД
    text = utils.get_tasks(mysql.get_task_for_user(user_id))     # Актуальный список дел пользователя
    bot.send_message(user_id, text)
    users[user_id]['action'] = None


def add_section(user_id, section_name):
    mysql.add_task_list(user_id, section_name)                   # Добавление раздела в БД
    text = utils.get_tasks(mysql.get_task_for_user(user_id))     # Актуальный список дел пользователя
    bot.send_message(user_id, text)
    users[user_id]['action'] = None


def remove():
    # Удаляет дело из общего списка или из созданного пользователем списка
    pass


if __name__ == "__main__":
    bot.polling(none_stop=True)