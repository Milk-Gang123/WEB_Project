import os
import ctypes

import flask
from PIL import Image
from flask import Flask, render_template, request
from werkzeug.utils import redirect
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from data import db_session
from data.db_session import global_init, create_session
from data.users import User
from forms.user import RegisterForm, LoginForm
from ASCII import ASCIIConverter

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
login_manager = LoginManager()
login_manager.init_app(app)

current_image_path = ''
processed_image_path = ''
user32 = ctypes.windll.user32
screensize = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
image_size = (int(screensize[0] * 0.6), 620)


def resize_image(image_path, save_path, image_size):
    image = Image.open(image_path)
    new_image = image.resize(image_size)
    new_image.save(save_path)





@login_manager.user_loader
def load_user(user_id):
    global_init('db/blogs.db')
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/')
def show_initial_page():
    return render_template('initial_page.html')


@app.route('/registration', methods=['POST', 'GET'])
def show_registration():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация', form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация', form=form,
                                   message="Такой пользователь уже есть")
        user = User(
            name=form.name.data,
            surname=form.surname.data,
            nickname=form.nickname.data,
            email=form.email.data
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)


@app.route('/login',  methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        global_init('db/blogs.db')
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/main")
        return  render_template('login.html', message="Неправильный логин или пароль", form=form)
    return render_template("login.html", title="Авторизация", form=form)


@app.route('/main', methods=['POST', 'GET'])
@login_required
def base():
    global current_image_path, processed_image_path
    params = {'current_image': current_image_path, 'processed_image': processed_image_path}
    if request.method == 'GET':
        return render_template('main.html', **params)

    elif request.method == 'POST':
        processed_image_path = 'static/img/processed_image_path.jpg'
        current_image_path = 'static/img/current_image.jpg'
        file = request.files['pw']
        file.save(current_image_path)
        resize_image(current_image_path, processed_image_path, image_size)
        return 'gg'


@app.route('/ascii', methods=['POST'])
def make_ascii():
    font_size = int(request.form['font-size'])
    app = ASCIIConverter(image_size[0], image_size[1], font_size)
    image = Image.open(current_image_path)
    resized_image = image.resize(image_size)
    gray_image = app.gray_image(resized_image)
    list_chars = app.pix_to_ascii(gray_image)
    app.draw_image(list_chars, processed_image_path)
    return redirect('/main')



if __name__ == "__main__":
    db_session.global_init("db/blogs.db")
    #app.register_blueprint(user_api.blueprint)
    app.run(port=8080, host='127.0.0.1')