# Created by Nikolay Pakhomov 26.07.2024
import sqlite3
import datetime

'''
    Файл с функциями работы АПИ с БД.
'''


def get_db_connection(db_path):
    db_conn = sqlite3.connect(db_path)
    db_conn.row_factory = sqlite3.Row
    return db_conn


def get_time_now():
    return datetime.datetime.now().strftime("%d-%m-%Y %X")


# def get_new_index_db(db_path, table_name):
#     conn = get_db_connection(db_path)
#     c = conn.cursor()
#     d = conn.execute(f"SELECT COUNT(*) FROM {table_name}").fetchall()
#     conn.close()
#     i = d[0][0]
#     return i
#
#
# def get_new_index_c(cursor, table_name):
#     d = cursor.execute(f"SELECT COUNT(*) FROM {table_name}").fetchall()
#     i = d[0][0]
#     return i


def get_all_data_db(db_path, table_name):
    conn = get_db_connection(db_path)
    c = conn.cursor()
    data = c.execute(f"SELECT * FROM {table_name}").fetchall()
    conn.close()
    data = [dict(ix) for ix in data]
    return data


def get_user_db(db_path, username):
    conn = get_db_connection(db_path)
    user = conn.execute('SELECT * FROM accounts WHERE username = ?', (username,)).fetchone()
    conn.close()
    return user


def get_role_db(db_path, role_id):
    conn = get_db_connection(db_path)
    c = conn.cursor()
    role = c.execute(f"SELECT * FROM role_types WHERE id = ?", (role_id,)).fetchone()
    conn.close()
    return role['name']


def insert_user_db(db_path, user_info):
    conn = get_db_connection(db_path)
    c = conn.cursor()
    c.execute(
        "INSERT INTO accounts "
        "(username, password, role, auth, name, date_of_birth, email, phone, created_at) "
        "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
        (user_info['username'], user_info['password'], user_info['role'],
         user_info['auth'], user_info['name'], user_info['date_of_birth'], user_info['email'],
         user_info['phone'], user_info['created_at']))
    conn.commit()
    conn.close()


def username_in_db(db_path, username):
    conn = get_db_connection(db_path)
    c = conn.cursor()
    unique = c.execute(f"SELECT COUNT(*) FROM accounts WHERE username = '{username}'").fetchall()
    conn.close()
    i = unique[0][0]
    if i > 0:
        return True
    else:
        return False


# получить список заявок
def get_bids_from_db(db_path):
    conn = get_db_connection(db_path)
    c = conn.cursor()
    data = c.execute(f"SELECT user_id, role, name, date_of_birth, email, phone, created_at"
                     f" FROM accounts WHERE (auth = 0 AND role = 1)").fetchall()
    conn.close()
    bids = [dict(ix) for ix in data]
    return bids


def del_user_from_db(db_path, user_id):
    conn = get_db_connection(db_path)
    c = conn.cursor()
    c.execute("DELETE FROM accounts WHERE user_id = ?", (user_id,))
    conn.commit()
    conn.close()


def ver_user_from_db(db_path, user_id):
    conn = get_db_connection(db_path)
    c = conn.cursor()
    c.execute("UPDATE accounts SET auth = ? WHERE user_id = ?", (1, user_id))
    conn.commit()
    conn.close()


def get_employees_from_db(db_path):
    conn = get_db_connection(db_path)
    c = conn.cursor()
    data = c.execute(f"SELECT user_id, role, name, date_of_birth, email, phone, created_at"
                     f" FROM accounts WHERE (role = 0 OR role = 1) AND (auth = 1)").fetchall()
    conn.close()
    employees = [dict(ix) for ix in data]
    for d in employees:
        r = d['role']
        if r == 0:
            d['position'] = 'Администратор'
        elif r == 1:
            d['position'] = 'Тренер'
        else:
            d['position'] = 'Сотрудник'
    return employees


def get_clients_from_db(db_path):
    conn = get_db_connection(db_path)
    c = conn.cursor()
    data = c.execute(f"SELECT user_id, role, name, date_of_birth, email, phone, created_at"
                     f" FROM accounts WHERE role = 2").fetchall()
    conn.close()
    clients = [dict(ix) for ix in data]
    return clients


def get_trainers_from_db(db_path):
    conn = get_db_connection(db_path)
    c = conn.cursor()
    data = c.execute(f"SELECT user_id, role, name, date_of_birth, email, phone, created_at"
                     f" FROM accounts WHERE (role = 1 AND auth = 1)").fetchall()
    conn.close()
    trainers = [dict(ix) for ix in data]
    return trainers


def get_trainers_from_db_rebuild(db_path):
    conn = get_db_connection(db_path)
    c = conn.cursor()
    trainers = c.execute(f"SELECT user_id, role, name, date_of_birth, email, phone, created_at"
                         f" FROM accounts WHERE (role = 1 AND auth = 1)").fetchall()
    services = c.execute("SELECT * FROM services").fetchall()
    conn.close()
    result_json = {}
    trainers = [dict(ix) for ix in trainers]
    for tr in trainers:
        tr_id = tr['user_id']
        tr['services'] = []
        tr.pop('user_id')
        result_json[tr_id] = tr
    # нужно учесть, что в таблице не появятся никогда записи с id тренера, которого не существует
    services = [dict(ix) for ix in services]
    for row in services:
        tr_id = row['trainer_id']
        row.pop('trainer_id')
        category = row['category_id']
        if category == 0:
            row['category'] = "Зал"
        elif category == 1:
            row['category'] = "Групповые тренировки"
        else:
            row['category'] = "Бассейн"
        result_json[tr_id]['services'].append(row)
    return result_json


def insert_service_in_db(db_path, service_info):
    conn = get_db_connection(db_path)
    c = conn.cursor()
    c.execute(
        "INSERT INTO services (trainer_id, category_id, service, price, comment) VALUES (?, ?, ?, ?, ?)",
        (service_info['trainer_id'], service_info['category'], service_info['service'], service_info['price'], service_info['comment']))
    conn.commit()
    conn.close()


def del_service_from_db(db_path, service_id):
    conn = get_db_connection(db_path)
    c = conn.cursor()
    c.execute("DELETE FROM services WHERE service_id = ?", (service_id,))
    conn.commit()
    conn.close()
