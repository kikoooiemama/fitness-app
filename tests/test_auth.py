# Created by Nikolay Pakhomov 30.07.2024
import os
import json
from main_helper import *
import pprint

# Параметры БД
path_to_conf = os.path.join('../static/conf/prop.json')
with open(path_to_conf, 'r') as f:
    json_data = json.loads(f.read())

# Создание или подключение к базе данных
db_path = f"../static/conf/{json_data['db_name']}"

ver_user_from_db(db_path, 3)

accs = get_all_data_db(db_path, 'accounts')
print("Аккаунты:")
pprint.pp(accs)
