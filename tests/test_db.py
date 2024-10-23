# Created by Nikolay Pakhomov 26.07.2024
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

# Смотрим что в аккаунтах и профилях
accs = get_all_data_db(db_path, 'accounts')

cats = get_all_data_db(db_path, 'category_types')
roles = get_all_data_db(db_path, 'role_types')
services = get_all_data_db(db_path, 'services')
print("Роли:")
pprint.pp(roles)
print()
print("Аккаунты:")
pprint.pp(accs)
print()
print("Категории:")
pprint.pp(cats)
print()
print("Услуги:")
pprint.pp(services)
print()
