import os
import ctypes
from PIL import Image
from flask import Flask, render_template, request
from flask_login import LoginManager, login_user
from werkzeug.utils import redirect

from data import db_session
from data.db_session import global_init, create_session
from data.users import User
from forms.user import RegisterForm, LoginForm


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


@app.route('/', methods=['POST', 'GET'])
@app.route('/index', methods=['POST', 'GET'])
def base():
    global current_image_path, processed_image_path
    params = {'current_image': current_image_path, 'processed_image': processed_image_path}
    if request.method == 'GET':
        return render_template('main.html', **params)

    elif request.method == 'POST':
        processed_image_path = 'static/img/carousel_1.png'
        current_image_path = 'static/img/current_image.jpg'
        filename = request.form['file']
        pth = 'C:\\'
        for root, dirnames, filenames in os.walk(pth):
            for file in filenames:
                if file == filename:
                    path = os.path.join(root, file)
        current_image = Image.open(path)
        current_image.save(current_image_path)
        resize_image(current_image_path, processed_image_path, image_size)
        return 'gg'


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



if __name__ == "__main__":
    app.run(port=8000, host="127.0.0.1")