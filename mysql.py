import pymysql.cursors
from config_mysql import HOST, USER, PASS, DB, CHARSET

def user_db(user_id, name):
    connection = pymysql.connect(
            host=HOST, user=USER, password=PASS, db=DB,
            charset=CHARSET, cursorclass=pymysql.cursors.DictCursor
    )
    try:
        with connection.cursor() as cursor:
            sql = "SELECT * FROM users WHERE user_id=%s"
            cursor.execute(sql, (user_id,))
            result = cursor.fetchone()
            if not result:
                sql = "INSERT INTO users (`user_id`, `name`) VALUES (%s, %s)"
                cursor.execute(sql, (user_id, name))
        connection.commit()
    finally:
        connection.close()
    return True


def add_task_list(user_id, section_name):
    connection = pymysql.connect(
        host=HOST, user=USER, password=PASS, db=DB,
        charset=CHARSET, cursorclass=pymysql.cursors.DictCursor
    )
    try:
        with connection.cursor() as cursor:
            sql = "SELECT `id` FROM users WHERE user_id=%s"
            cursor.execute(sql, (user_id,))
            result = cursor.fetchone()
            if not result:
                return False
            sql = "INSERT INTO sections (section_name, `user`) VALUES (%s, %s)"
            cursor.execute(sql, (section_name, result['id']))
        connection.commit()
    finally:
        connection.close()
    return True


def add_task(task_text, user_id, section=None):
    connection = pymysql.connect(
        host=HOST, user=USER, password=PASS, db=DB,
        charset=CHARSET, cursorclass=pymysql.cursors.DictCursor
    )
    try:
        with connection.cursor() as cursor:
            sql = "SELECT `id` FROM users WHERE user_id=%s"
            cursor.execute(sql, (user_id,))
            user = cursor.fetchone()
            if section and user:
                sql = "SELECT `id` FROM sections WHERE `section_name`=%s AND `user`=%s"
                cursor.execute(sql, (section, user['id']))
                result = cursor.fetchone()
                if not result:
                    return False
                sql = "INSERT INTO section_tasks (`task`, `section`) VALUES (%s, %s)"
                cursor.execute(sql, (task_text, result['id']))
            elif user:
                sql = "INSERT INTO other_tasks (`task`, `user`) VALUES (%s, %s)"
                cursor.execute(sql, (task_text, user['id']))
            else:
                return False
        connection.commit()
    finally:
        connection.close()
    return True


def remove(type_rm, filter):
    connection = pymysql.connect(
        host=HOST, user=USER, password=PASS, db=DB,
        charset=CHARSET, cursorclass=pymysql.cursors.DictCursor
    )
    try:
        with connection.cursor() as cursor:
            sql = "SELECT * FROM users WHERE user_id=1234567"
            cursor.execute(sql)
            result = cursor.fetchone()
        connection.commit()
    finally:
        connection.close()
    return result


def get_task_for_user(user_id):
    connection = pymysql.connect(
        host=HOST, user=USER, password=PASS, db=DB,
        charset=CHARSET, cursorclass=pymysql.cursors.DictCursor
    )
    try:
        with connection.cursor() as cursor:
            sql = "SELECT section, tasks FROM `sec_tasks_users` WHERE `user`=%s"
            cursor.execute(sql, (user_id,))
            sections = cursor.fetchall()
            sql = "SELECT other FROM `oth_tasks_users` WHERE `user`=%s"
            cursor.execute(sql, (user_id,))
            other = cursor.fetchall()
            return [sections, other]
    finally:
        connection.close()

if __name__ == '__main__':
    print(get_task_for_user(123456789))