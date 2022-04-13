from flask_wtf import FlaskForm
from sqlalchemy import orm
from werkzeug.security import generate_password_hash, check_password_hash
from wtforms import PasswordField, StringField, TextAreaField, SubmitField, BooleanField, FileField
from wtforms.fields import EmailField
from wtforms.validators import DataRequired


class CreateForm(FlaskForm):
    name = StringField('Название фильтра', validators=[DataRequired()])
    user = orm.relation("User", back_populates='user')
    description = StringField('Описание', validators=[DataRequired()])
    image = FileField('Изображение', validators=[DataRequired()])
    file = FileField('Код фильтра', validators=[DataRequired()])
    submit = SubmitField('Создать')