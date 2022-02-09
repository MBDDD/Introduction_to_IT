# Запустить: flask run
# Переходить по этой ссылке http://localhost:5000/login/

from flask import Flask, render_template, request
import psycopg2
app = Flask(__name__)

conn = psycopg2.connect(database='service_db',
                        user='postgres',
                        password='mbdd',
                        host='localhost',
                        port='5432')

cursor = conn.cursor()

@app.route('/login/', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')
    if username == '' or password == '':
        return render_template('empty_label.html')
    else:
        cursor.execute('SELECT * FROM service.users WHERE login=%s AND password=%s', (str(username), str(password)))
        info = cursor.fetchall()
        records = list(info)
        if info:
            return render_template('account.html', full_name=records[0][1], username=username, password=password)
        else:
            return render_template('no_user.html')

@app.route('/login/', methods=['GET'])
def index():
    return render_template('login.html')