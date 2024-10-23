# Created by Nikolay Pakhomov 25.07.2024
import sqlite3
import os
import json
import hashlib
from main_helper import *

# Параметры БД.
path_to_conf = os.path.join('static/conf/prop.json')
with open(path_to_conf, 'r') as f:
    json_data = json.loads(f.read())

# Создание или подключение к базе данных.
conn = sqlite3.connect(f"static/conf/{json_data['db_name']}")

# Создание курсора.
c = conn.cursor()

# Создание таблицы с аккаунтами, accounts.
# auth - верификация.
c.execute('''CREATE TABLE IF NOT EXISTS accounts (
                user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL,
                password TEXT NOT NULL,
                role INT UNSIGNED NOT NULL,
                auth INTEGER NOT NULL DEFAULT 0,
                name VARCHAR(255) NOT NULL,
                date_of_birth DATE,
                email VARCHAR(255),
                phone VARCHAR(31),
                created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
                CONSTRAINT fk_role_type FOREIGN KEY (role) REFERENCES role_types(id)
                )''')

# Создание таблицы с типами ролей для Users, role_types.
c.execute('''CREATE TABLE IF NOT EXISTS role_types(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name VARCHAR(127) NOT NULL UNIQUE 
                )''')

# Создание таблицы с занятиями (запланированными и прошедшими), classes.
c.execute('''CREATE TABLE IF NOT EXISTS classes(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                client_id INTEGER,
                trainer_id INTEGER,
                service_id INTEGER,
                start_time DATETIME,
                end_time DATETIME,
                verification INTEGER NOT NULL DEFAULT 0, 
                comment TEXT, 
                CONSTRAINT fk_client_id FOREIGN KEY (client_id) REFERENCES accounts (user_id) ON UPDATE CASCADE, 
                CONSTRAINT fk_trainer_id FOREIGN KEY (trainer_id) REFERENCES accounts (user_id) ON UPDATE CASCADE, 
                CONSTRAINT fk_service_id FOREIGN KEY (service_id) REFERENCES services (id) ON UPDATE CASCADE
                )''')

# Создание таблицы услуг, которые могут выполнять тренера (ее должен заполнять администратор).
c.execute('''CREATE TABLE IF NOT EXISTS services (
                service_id INTEGER PRIMARY KEY AUTOINCREMENT,
                trainer_id INTEGER,
                category_id INTEGER,
                service VARCHAR(255) NOT NULL,
                price INTEGER UNSIGNED NOT NULL,
                comment TEXT,
                CONSTRAINT fk_trainer_id FOREIGN KEY (trainer_id) 
                    REFERENCES accounts(user_id) ON DELETE CASCADE ON UPDATE CASCADE
                CONSTRAINT fk_category_id FOREIGN KEY (category_id) 
                    REFERENCES category_types(id) ON DELETE CASCADE ON UPDATE CASCADE    
                )''')

c.execute('''CREATE TABLE IF NOT EXISTS category_types (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name VARCHAR(127) NOT NULL UNIQUE 
                )''')

# Заполнение таблицы с типами ролями.
for k, role in enumerate(json_data['db_roles']):
    c.execute('INSERT INTO role_types (id, name) VALUES (?, ?)', (k, role,))

# Заполнение таблицы с категориями
for value, v_id in json_data['db_categories'].items():
    c.execute('INSERT INTO category_types (id, name) VALUES (?, ?)', (v_id, value))

# Добавление нулевого пользователя с правами.
admin_id = json_data['db_auth'][0]
username = json_data['db_auth'][1]
password = json_data['db_auth'][2]
role = json_data['db_auth'][3]
auth = json_data['db_auth'][4]
created_at = get_time_now()
# Хеширование пароля
hashed_password = hashlib.sha256(password.encode('utf-8')).hexdigest()

# Добавление нового пользователя
c.execute('INSERT INTO accounts (username, password, role, auth, name, created_at) VALUES (?, ?, ?, ?, ?, ?)',
          (username, hashed_password, role, auth, username, created_at))

# Сохранение изменений и закрытие соединения.
conn.commit()
conn.close()
