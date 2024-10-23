# Created by Nikolay Pakhomov 22.07.2024
import flask
from flask import Flask, render_template, redirect, url_for, request, session, send_file
from main_helper import *
import hashlib
import os
import json
from main_reports import *

app = Flask(__name__)

# Загрузка данных для web.
path_to_conf = os.path.join(app.root_path, 'static', 'conf', 'prop.json')
with open(path_to_conf, 'r') as f:
    json_data = json.loads(f.read())

# Сеттинг параметров
app.secret_key = json_data['secret_key']
path_to_db = os.path.join(app.root_path, 'static', 'conf', json_data['db_name'])
path_to_save_images = os.path.join(app.root_path, 'static', json_data['imgs_dir'])
path_to_save_reports = os.path.join(app.root_path, 'static', json_data['reports_dir'])
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/', methods=['GET', 'POST'])
def home():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        hashed_password = hashlib.sha256(password.encode('utf-8')).hexdigest()
        user = get_user_db(path_to_db, username)
        # conn = get_db_connection(path_to_db)
        # user = conn.execute('SELECT * FROM accounts WHERE username = ?', (username,)).fetchone()
        # conn.close()

        if user and user['password'] == hashed_password:
            # admin
            user_role = get_role_db(path_to_db, user['role'])
            if user_role == json_data['db_roles']['admin']:
                session['user_id'] = user['user_id']
                return redirect(url_for('admin_panel'))
            # manager
            elif user_role == json_data['db_roles']['trainer']:
                if user['auth'] == 0:
                    error = "Аккаунт не верифицирован Администратором. Ожидайте."
                    return render_template('login.html', error=error)
                else:
                    session['user_id'] = user['user_id']
                    return redirect(url_for('trainer_panel'))
            # trainer
            elif user_role == json_data['db_roles']['client']:
                session['user_id'] = user['user_id']
                return redirect(url_for('client_panel'))
            # others
            else:
                error = "Недостаточно прав"
                render_template('login.html', error=error)

        else:
            error = 'Неправильное имя пользователя или пароль'

    return render_template('login.html', error=error)


@app.route('/admin_panel')
def admin_panel():
    if 'user_id' not in session:
        return redirect(url_for('home'))
    json_ap_data = get_bids_from_db(path_to_db)
    return render_template('admin_panel_01_bids.html', json_ap_data=json_ap_data)


@app.route('/admin_panel_bids')
def ap_bids():
    if 'user_id' not in session:
        return redirect(url_for('home'))

    json_ap_data = get_bids_from_db(path_to_db)
    return render_template('admin_panel_01_bids.html', json_ap_data=json_ap_data)


@app.route('/ap_bids_verify', methods=['POST'])
def ap_bids_verify():
    ver_id = request.form['ver_user_id']
    ver_user_from_db(path_to_db, ver_id)
    return redirect(url_for('ap_bids'))


@app.route('/ap_bids_del/', methods=['POST'])
def ap_bids_remove():
    del_id = request.form['del_user_id']
    del_user_from_db(path_to_db, del_id)
    return redirect(url_for('ap_bids'))


@app.route('/admin_panel_employees')
def ap_employees():
    if 'user_id' not in session:
        return redirect(url_for('home'))

    json_ap_data = get_employees_from_db(path_to_db)
    return render_template('admin_panel_02_employees.html', json_ap_data=json_ap_data)


@app.route('/ap_employees_update', methods=['POST'])
def ap_employees_update():
    return redirect(url_for('ap_employees'))


@app.route('/ap_employees_del/', methods=['POST'])
def ap_employees_remove():
    del_id = request.form['del_employee_id']
    del_user_from_db(path_to_db, del_id)
    return redirect(url_for('ap_employees'))


@app.route('/admin_panel_clients')
def ap_clients():
    if 'user_id' not in session:
        return redirect(url_for('home'))

    json_ap_data = get_clients_from_db(path_to_db)
    return render_template('admin_panel_05_clients.html', json_ap_data=json_ap_data)


@app.route('/ap_clients_del/', methods=['POST'])
def ap_clients_remove():
    del_id = request.form['del_client_id']
    del_user_from_db(path_to_db, del_id)
    return redirect(url_for('ap_clients'))


@app.route('/admin_panel_reports')
def ap_reports():
    if 'user_id' not in session:
        return redirect(url_for('home'))
    json_ap_data = get_trainers_from_db(path_to_db)
    return render_template('admin_panel_03_reports.html', json_ap_data=json_ap_data)


@app.route('/ap_reports_total/', methods=['POST'])
def ap_reports_total():
    if 'user_id' not in session:
        return redirect(url_for('home'))
    report_after = request.form['after']
    report_after = datetime.datetime.strptime(report_after, '%Y-%m-%d').date() if report_after else '2020-01-01'
    report_before = request.form['before']
    report_before = datetime.datetime.strptime(report_before,
                                               '%Y-%m-%d').date() if report_before else datetime.datetime.now().date()
    print(report_after, report_before)
    report_path, file_name = create_total_report(path_to_save_reports, report_after, report_before)
    return send_file(report_path, as_attachment=True, download_name=file_name)


@app.route('/ap_reports_trainer/', methods=['POST'])
def ap_reports_trainer():
    if 'user_id' not in session:
        return redirect(url_for('home'))
    report_trainer_id = request.form['report_trainer_id']
    report_after = request.form['rep_after']
    report_after = datetime.datetime.strptime(report_after, '%Y-%m-%d').date() if report_after else '2020-01-01'
    report_before = request.form['rep_before']
    report_before = datetime.datetime.strptime(report_before,
                                               '%Y-%m-%d').date() if report_before else datetime.datetime.now().date()
    report_path, file_name = create_trainer_report(path_to_save_reports, report_trainer_id, report_after, report_before)
    return send_file(report_path, as_attachment=True, download_name=file_name)


@app.route('/admin_panel_pl')
def ap_price_list():
    if 'user_id' not in session:
        return redirect(url_for('home'))
    json_ap_data = get_trainers_from_db_rebuild(path_to_db)
    return render_template('admin_panel_04_pricelist.html', json_ap_data=json_ap_data)


@app.route('/ap_pl_del/', methods=['POST'])
def ap_pl_remove():
    del_id = request.form['del_service_id']
    del_service_from_db(path_to_db, del_id)
    return redirect(url_for('ap_price_list'))


@app.route('/trainer_panel')
def trainer_panel():
    if 'user_id' not in session:
        return redirect(url_for('home'))
    json_tp_data = get_employees_from_db(path_to_db)
    return render_template('trainer_panel_01_schedule.html', json_tp_data=json_tp_data)


@app.route('/tp_schedule')
def tp_schedule():
    if 'user_id' not in session:
        return redirect(url_for('home'))

    json_tp_data = get_employees_from_db(path_to_db)
    return render_template('trainer_panel_01_schedule.html', json_tp_data=json_tp_data)


@app.route('/tp_reports')
def tp_reports():
    if 'user_id' not in session:
        return redirect(url_for('home'))

    json_tp_data = get_employees_from_db(path_to_db)
    return render_template('trainer_panel_02_reports.html', json_tp_data=json_tp_data)


@app.route('/client_panel')
def client_panel():
    if 'user_id' not in session:
        return redirect(url_for('home'))
    json_cp_data = get_employees_from_db(path_to_db)
    return render_template('client_panel_01_classes.html', json_cp_data=json_cp_data)


@app.route('/cp_classes')
def cp_classes():
    if 'user_id' not in session:
        return redirect(url_for('home'))

    json_cp_data = get_employees_from_db(path_to_db)
    return render_template('client_panel_01_classes.html', json_cp_data=json_cp_data)


@app.route('/cp_recording')
def cp_recording():
    if 'user_id' not in session:
        return redirect(url_for('home'))

    json_cp_data = get_employees_from_db(path_to_db)
    return render_template('client_panel_02_recording.html', json_cp_data=json_cp_data)


@app.route('/cp_reports')
def cp_reports():
    if 'user_id' not in session:
        return redirect(url_for('home'))

    json_cp_data = get_employees_from_db(path_to_db)
    return render_template('client_panel_03_reports.html', json_cp_data=json_cp_data)


@app.route('/register')
def register():
    return render_template('register.html')


@app.route('/register_handler', methods=['POST'])
def register_handler():
    info = {}
    info['username'] = request.form['username']
    if username_in_db(path_to_db, info['username']):
        error = "Пользователь с таким логином уже существует!"
        return render_template('register.html', error=error)
    password = request.form['password']
    info['password'] = hashlib.sha256(password.encode('utf-8')).hexdigest()
    info['created_at'] = get_time_now()
    info['name'] = request.form['name']
    brd = request.form['birthday']
    info['date_of_birth'] = datetime.datetime.strptime(brd, '%Y-%m-%d').date() if brd else None
    info['email'] = request.form['email']
    info['phone'] = request.form['phone']
    role = request.form['role']
    if role == "client":
        info['role'] = 2
        info['auth'] = 1
        insert_user_db(path_to_db, info)
        return redirect(url_for('home'))
    elif role == "trainer":
        info['role'] = 1
        info['auth'] = 0
        insert_user_db(path_to_db, info)
        return redirect(url_for('home'))
    else:
        error = "Неправильная роль!"
        return render_template('register.html', error=error)


@app.route('/register_handler_admin', methods=['POST'])
def register_handler_admin():
    info = {}
    info['username'] = request.form['username']
    if username_in_db(path_to_db, info['username']):
        error = "Пользователь с таким логином уже существует!"
        if 'user_id' not in session:
            return redirect(url_for('home'))

        json_ap_data = get_employees_from_db(path_to_db)
        return render_template('admin_panel_02_employees.html', json_ap_data=json_ap_data, error=error)
    password = request.form['password']
    info['password'] = hashlib.sha256(password.encode('utf-8')).hexdigest()
    info['created_at'] = get_time_now()
    info['name'] = request.form['name']
    brd = request.form['birthday']
    info['date_of_birth'] = datetime.datetime.strptime(brd, '%Y-%m-%d').date() if brd else None
    info['email'] = request.form['email']
    info['phone'] = request.form['phone']
    info['role'] = 0
    info['auth'] = 1
    insert_user_db(path_to_db, info)
    return redirect(url_for('ap_employees'))


@app.route('/register_handler_trainer', methods=['POST'])
def register_handler_trainer():
    info = {}
    info['username'] = request.form['username']
    if username_in_db(path_to_db, info['username']):
        error = "Пользователь с таким логином уже существует!"
        if 'user_id' not in session:
            return redirect(url_for('home'))

        json_ap_data = get_employees_from_db(path_to_db)
        return render_template('admin_panel_02_employees.html', json_ap_data=json_ap_data, error=error)
    password = request.form['password']
    info['password'] = hashlib.sha256(password.encode('utf-8')).hexdigest()
    info['created_at'] = get_time_now()
    info['name'] = request.form['name']
    brd = request.form['birthday']
    info['date_of_birth'] = datetime.datetime.strptime(brd, '%Y-%m-%d').date() if brd else None
    info['email'] = request.form['email']
    info['phone'] = request.form['phone']
    info['role'] = 1
    info['auth'] = 1
    insert_user_db(path_to_db, info)
    return redirect(url_for('ap_employees'))


@app.route('/price_trainer_handler', methods=['POST'])
def price_trainer_handler():
    info = {}
    info['service'] = request.form['task']
    info['price'] = request.form['price']
    info['category'] = request.form['category']
    info['comment'] = request.form['comment']
    info['trainer_id'] = request.form['trainer_id']
    insert_service_in_db(path_to_db, info)
    return redirect(url_for('ap_price_list'))


@app.route('/logout')
def logout():
    # Удаление данных пользователя из сессии
    session.clear()
    # Перенаправление на главную страницу или страницу входа
    return redirect(url_for('home'))


if __name__ == '__main__':
    app.run(debug=True)
