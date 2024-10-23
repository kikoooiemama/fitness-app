# Created by Nikolay Pakhomov 30.07.2024
import os
import json
from main_reports import *
import pprint

# Параметры БД
path_to_conf = os.path.join('../static/conf/prop.json')
with open(path_to_conf, 'r') as f:
    json_data = json.loads(f.read())

path_to_save_reports = os.path.join("H:\\PakhomovProjects\\Python\\fitness-app", 'static', json_data['reports_dir'])

report = create_total_report(path_to_save_reports)
print(report)
