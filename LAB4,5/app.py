# Запустить: flask run
# Переходить по этой ссылке http://localhost:5000/
from flask import Flask, render_template, request, redirect
import psycopg2

app = Flask(__name__)

conn = psycopg2.connect(database='service_db',
                        user='postgres',
                        password='mbdd',
                        host='localhost',
                        port='5432')

cursor = conn.cursor()

@app.route('/login/', methods=['POST','GET'])
def login():
    if request.method == 'POST':
        if request.form.get('login'):
            username = request.form.get('username')
            password = request.form.get('password')
            if username == '' or password == '':
                return render_template('empty_label_login.html')
            else:
                cursor.execute('SELECT * FROM service.users WHERE login=%s AND password=%s', (str(username), str(password)))
                info = cursor.fetchall()
                records = list(info)
                if info:
                    return render_template('account.html', full_name=records[0][1], username=username, password=password)
                else:
                    return render_template('no_user.html')
        elif request.form.get('registration'):
            return redirect('/registration/')
    return render_template('login.html')

@app.route('/registration/', methods=['POST', 'GET'])
def registration():
    if request.method == 'POST':
        name = request.form.get('name')
        login = request.form.get('login')
        password = request.form.get('password')
        if name == '' or login == '' or password == '':
            return render_template('empty_label_registration.html')
        else:
            cursor.execute('SELECT login FROM service.users WHERE login=%s', (str(login),))
            info = cursor.fetchall()
            if info:
                return render_template('exist_user.html')
            else:
                cursor.execute('INSERT INTO service.users (full_name, login, password) VALUES (%s, %s, %s);',
                               (str(name), str(login), str(password)))
                conn.commit()
                return redirect('/login/')
    return render_template('registration.html')