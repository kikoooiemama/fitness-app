# Created by Nikolay Pakhomov 26.07.2024

from main_helper import *
import os, json

path_to_conf = os.path.join('../static/conf/prop.json')
with open(path_to_conf, 'r') as f:
    json_data = json.loads(f.read())

# Создание или подключение к базе данных
db_path = f"../static/conf/{json_data['db_name']}"

a = username_in_db(db_path, "admin1")
print(a)
