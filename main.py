import io
import ctypes
import os

from PIL import Image
from flask import Flask, render_template, request
from werkzeug.utils import redirect
from flask_login import LoginManager, login_user, login_required
from data import db_session
from data.db_session import global_init
from data.users import User
from forms.filter import CreateForm
from data.filters import Filter
from data import user_api
from forms.user import RegisterForm, LoginForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
login_manager = LoginManager()
login_manager.init_app(app)
current_user_id = -1
current_image_path = ''
processed_image_path = ''
user32 = ctypes.windll.user32
screensize = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
image_size = (int(screensize[0] * 0.6), 620)

page_number = 1
filter_id = 1
current_fields = []


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
            email=form.email.data,
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)


@app.route('/create_filter',  methods=['GET', 'POST'])
@login_required
def create_filter_page():
    form = CreateForm()
    if form.validate_on_submit():
        global_init('db/blogs.db')
        db_sess = db_session.create_session()
        user_nickname = db_sess.query(User.nickname).filter(User.name == 'Alex').first()
        user_nickname = user_nickname[0]
        image = form.image.data.read()
        file = form.file.data.read()
        new_filter = Filter(
            name=form.name.data,
            description=form.description.data,
            image=image,
            file=file,
            user_nickname=user_nickname
        )
        db_sess.add(new_filter)
        db_sess.commit()
        return redirect("/filter_log")
    return render_template("adding_filter_page.html", form=form)


@app.route('/login',  methods=['GET', 'POST'])
def login():
    global current_user_id
    form = LoginForm()
    if form.validate_on_submit():
        global_init('db/blogs.db')
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        current_user_id = user.id
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/filter_log")
        return render_template('login.html', message="Неправильный логин или пароль", form=form)
    return render_template("login.html", title="Авторизация", form=form)


@app.route('/filter_log', methods=['GET'])
def show_log():
    global page_number
    if page_number < 1:
        page_number = 1
    if request.method == 'GET':
        db_sess = db_session.create_session()
        filters = []
        for i in range(1, 3):
            filt = db_sess.query(Filter).filter(Filter.id == (i + (page_number - 1) * 2)).first()
            if not filt:
                continue
            image = Image.open(io.BytesIO(filt.image))
            image = image.resize((int(0.25 * screensize[0]), int(0.25 * screensize[1])))
            filt.image = i
            image.save(f'static/img/filter_image_{i}.png')
            filters.append(filt)
        if not filters:
            page_number -= 1
            return render_template('filter_page.html')
        db_sess.close()
        params = {'filters': filters}
        return render_template('filter_page.html', **params)


@app.route('/main', methods=['POST', 'GET'])
@login_required
def base():
    global current_image_path, processed_image_path, current_fields
    db_sess = db_session.create_session()
    filt = db_sess.query(Filter).filter(Filter.id == filter_id).first()
    with open('filter.py', 'w', encoding='utf-8') as file:
        file.write(filt.file.decode('utf-8'))
    from filter import ImageFilter
    app_ = ImageFilter()
    if current_fields != [] and filter_id == filt.id:
        fields = current_fields
    else:
        current_fields = app_.fields
        fields = current_fields
    params = {'current_image': current_image_path, 'processed_image': processed_image_path,
              'fields': fields}
    if request.method == 'GET':
        return render_template('main.html', **params)

    elif request.method == 'POST':
        processed_image_path = 'static/img/processed_image.png'
        current_image_path = 'static/img/current_image.png'
        file = request.files['pw']
        image = Image.open(file)
        image = image.resize(image_size)
        image.save(current_image_path)
        resize_image(current_image_path, processed_image_path, image_size)
        return redirect('/main')


@app.route('/go_main/<int:id>', methods=['GET', 'POST'])
def go_main(id):
    global filter_id, current_fields, current_image_path, processed_image_path
    filter_id = id
    current_fields = []
    os.remove('static/img/current_image.png')
    os.remove('static/img/processed_image.png')
    current_image_path = ''
    processed_image_path = ''
    return redirect('/main')


@app.route('/draw_image', methods=['POST'])
def draw_image():
    global current_fields
    from filter_examples.Pixelart import ImageFilter
    app_ = ImageFilter()
    current_fields = app_.fields
    try:
        a = request.form['field1']
        app_.field_1(a)
        current_fields[0][1] = a
    except Exception as e:
        print(e)
    try:
        b = request.form['field2']
        app_.field_2(b)
        current_fields[1][1] = b
    except Exception as e:
        pass
    try:
        c = request.form['field3']
        app_.field_3(c)
        current_fields[2][1] = c
    except Exception as e:
        pass
    app_.make_image(current_image_path)
    return redirect('/main')


@app.route('/next_page')
def go_next():
    global page_number
    page_number += 1
    return redirect('/filter_log')


@app.route('/prev_page')
def go_prev():
    global page_number
    page_number -= 1
    return redirect('/filter_log')


if __name__ == "__main__":
    db_session.global_init("db/blogs.db")
    app.register_blueprint(user_api.blueprint)
    app.run(port=8080, host='127.0.0.1')