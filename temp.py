from data import db_session
from data.filters import Filter

db_session.global_init("db/blogs.db")
db_sess = db_session.create_session()
user = Filter()
db_sess.add(user)
db_sess.commit()