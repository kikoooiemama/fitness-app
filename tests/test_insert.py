# Created by Nikolay Pakhomov 29.07.2024

from main_helper import *
import os, json

path_to_conf = os.path.join('../static/conf/prop.json')
with open(path_to_conf, 'r') as f:
    json_data = json.loads(f.read())

# Создание или подключение к базе данных
db_path = f"../static/conf/{json_data['db_name']}"

inf = {'user_id': 1459, 'username': '234523256', 'password': '9546bf227f665aa8388c6cf2ba17e51566e375c327b06caac440d84485e383ef', 'created_at': '29-07-2024 07:53:13', 'name': '2345235', 'date_of_birth': None, 'email': '213@askd.ru', 'phone': '262626', 'role': 2, 'auth': 1}

insert_user_db(db_path, inf)
