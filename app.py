import os
import sqlite3

from flask import Flask, render_template, request, g, flash, abort, redirect, url_for, make_response

from FDataBase import FDataBase

DATABASE = '/tmp/my_newDB_2.db'
DEBUG = True
SECRET_KEY = 'fdgfh78@#5?>gfhf89dx,v06k'
MAX_CONTENT_LENGTH = 1024 * 1024

app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://anohin_r_b:NewPass21@localhost'
app.config.from_object(__name__)
app.config.update(dict(DATABASE=os.path.join(app.root_path, 'my_newDB_2.db')))


# manager = Manager(app)
# db = SQLAlchemy(app)

def connect_db():
    conn = sqlite3.connect(app.config['DATABASE'])
    conn.row_factory = sqlite3.Row
    return conn


def get_db():
    '''Соединение с БД, если оно еще не установлено'''
    if not hasattr(g, 'link_db'):
        g.link_db = connect_db()
    return g.link_db


def connect_db():
    conn = sqlite3.connect(app.config['DATABASE'])
    conn.row_factory = sqlite3.Row
    return conn


def create_db():
    """Вспомогательная функция для создания таблиц БД"""
    db = connect_db()
    with app.open_resource('cr_newDB.style', mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()
    db.close()


# create_db()


def get_db():
    '''Соединение с БД, если оно еще не установлено'''
    if not hasattr(g, 'link_db'):
        g.link_db = connect_db()
    return g.link_db


#
dbase = None


# @app.before_request
def before_request():
    """Установление соединения с БД перед выполнением запроса"""
    global dbase
    db = get_db()
    dbase = FDataBase(db)


@app.teardown_appcontext
def close_db(error):
    '''Закрываем соединение с БД, если оно было установлено'''
    if hasattr(g, 'link_db'):
        g.link_db.close()


@app.route("/", methods=["POST", "GET"])
def index():
    return render_template('menu.html')


@app.route("/employee", methods=["POST", "GET"])
def show_employees():
    db = get_db()
    dbase = FDataBase(db)
    empl = dbase.get_all_emplyee()
    for e in empl:
        print(e[1], e[2])
    return render_template('employee.html', empl=empl)

@app.route("/show_employee/<empl_id>", methods=["POST", "GET"])
def show_employee(empl_id):
    db = get_db()
    dbase = FDataBase(db)
    empl = dbase.get_emplyee(empl_id)
    posts = dbase.get_all_posts()
    offices = dbase.get_all_offices()
    if request.method == "POST":
        res1 = dbase.update_employee(empl_id, request.form['name'], request.form['surname'], request.form['email'],
                                  request.form['home_address'])
        empl = dbase.get_all_emplyee()
        if not (res1):
            flash('Ошибка добавления статьи', category='error')
        else:
            flash('Информация добавлена успешно', category='success')
            return render_template('employee.html', empl=empl)
    return render_template('change-employee.html', empl=empl, posts=posts, offices=offices,)


@app.route("/offices", methods=["POST", "GET"])
def show_offices():
    db = get_db()
    dbase = FDataBase(db)
    offices = dbase.get_all_offices()
    for e in offices:
        print(e[1], e[2])
    return render_template('offices.html', offices=offices)


@app.route("/posts", methods=["POST", "GET"])
def show_posts():
    db = get_db()
    dbase = FDataBase(db)
    posts = dbase.get_all_posts()
    for p in posts:
        print(p[1], p[2])
    return render_template('posts.html', posts=posts)


@app.route("/add_employee", methods=["POST", "GET"])
def add_employee():
    db = get_db()
    dbase = FDataBase(db)
    posts = dbase.get_all_posts()
    offices = dbase.get_all_offices()
    if request.method == "POST":
        res1 = dbase.add_employee(request.form['name'], request.form['surname'], request.form['email'],
                                 request.form['home_address'], request.form['selectPosts'], request.form['selectOffices'])
        employee = dbase.get_all_emplyee()
        if not (res1):
            flash('Ошибка добавления статьи', category='error')
        else:
            flash('Информация добавлена успешно', category='success')
            return render_template('employee.html', empl=employee)
    return render_template('add-employee.html', posts=posts, offices=offices, title="Добавление информации о сотруднике")


@app.route("/add_post", methods=["POST", "GET"])
def add_post():
    db = get_db()
    dbase = FDataBase(db)
    if request.method == "POST":
        res = dbase.add_post(request.form['title'], request.form['duties'])


        posts = dbase.get_all_posts()
        if not res:
            flash('Ошибка добавления статьи', category='error')
        else:
            flash('Информация добавлена успешно', category='success')
            return render_template('posts.html', posts=posts)

    return render_template('add-post.html', title="Добавление информации о сотруднике")

@app.route("/add_post_test", methods=["POST", "GET"])
def add_post_test():
    db = get_db()
    dbase = FDataBase(db)
    posts = dbase.get_all_posts()
    if request.method == "POST":
        print("hgfvh")
        print(request.form['nubexSelect'])
        # res = dbase.add_post(request.form['title'], request.form['duties'])
        # posts = dbase.get_all_posts()
        # if not res:
        #     flash('Ошибка добавления статьи', category='error')
        # else:
        #     flash('Информация добавлена успешно', category='success')
        #     return render_template('posts.html', posts=posts)

    return render_template('menu.html', posts = posts, title="Добавление информации о сотруднике")


@app.route("/add_office", methods=["POST", "GET"])
def add_office():
    db = get_db()
    dbase = FDataBase(db)
    if request.method == "POST":
        res = dbase.add_office(request.form['address'], request.form['phone_number'])
        offices = dbase.get_all_offices()
        if not res:
            flash('Ошибка добавления статьи', category='error')
        else:
            flash('Информация добавлена успешно', category='success')
            return render_template('offices.html', offices=offices)
    return render_template('add-office.html', title="Добавление информации о сотруднике")


@app.route("/delete_employee", methods=["POST", "GET"])
def delete_employee():
    db = get_db()
    dbase = FDataBase(db)
    print(request.form['id'])
    dbase.delete_employee(request.form['id'])
    empl = dbase.get_all_emplyee()
    return render_template('employee.html', empl=empl)


@app.route("/delete_office", methods=["POST", "GET"])
def delete_office():
    db = get_db()
    dbase = FDataBase(db)
    dbase.delete_office(request.form['code'])
    offices = dbase.get_all_offices()
    for e in offices:
        print(e[1], e[2])
    return render_template('offices.html', offices=offices)

@app.route("/delete_post", methods=["POST", "GET"])
def delete_post():
    db = get_db()
    dbase = FDataBase(db)
    dbase.delete_post(request.form['code'])
    posts = dbase.get_all_posts()
    for e in posts:
        print(e[1], e[2])
    return render_template('posts.html', posts=posts)


@app.route("/employee_del", methods=["POST", "GET"])
def employee_del():
    db = get_db()
    dbase = FDataBase(db)
    empl = dbase.get_all_emplyee()
    for e in empl:
        print(e[1], e[2])
    return render_template('del-employee.html', empl=empl)

@app.route("/office_del", methods=["POST", "GET"])
def office_del():
    db = get_db()
    dbase = FDataBase(db)
    offices = dbase.get_all_offices()
    for e in offices:
        print(e[1], e[2])
    return render_template('del-office.html', offices=offices)

@app.route("/post_del", methods=["POST", "GET"])
def post_del():
    db = get_db()
    dbase = FDataBase(db)
    posts = dbase.get_all_offices()
    for e in posts:
        print(e[1], e[2])
    return render_template('del-post.html', posts=posts)

# @app.teardown_appcontext
# def close_db(error):
#     '''Закрываем соединение с БД, если оно было установлено'''
#     if hasattr(g, 'link_db'):
#         g.link_db.close()
#
#
# # @app.route("/", methods=["POST", "GET"])
# # def index():
#     # dbase.get_all_emplyees()
# empl = dbase.get_all_emplyees()
# list_empl = []
# for s in empl:
#     print(s[0])
#         # user = dbase.getUser(s[4])
#         # list_empl.append(user)
#     # return render_template('employee.html')
#
#
if __name__ == "__main__":
    app.run(debug=True)
