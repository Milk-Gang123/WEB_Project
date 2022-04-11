import flask
import requests
from flask import request, jsonify
from data import db_session
from data.users import User
from data.filters import Filter


blueprint = flask.Blueprint(
    "users_api",
    __name__,
    template_folder="templates"
)


@blueprint.route("/api/users")
def get_users():
    db_sess = db_session.create_session()
    users = db_sess.query(User).all()
    return jsonify(
        {
            "users": [item.to_dict() for item in users]
        }
    )


@blueprint.route("/api/users/<int:user_id>", methods=['GET'])
def get_users_1(user_id):
    db_sess = db_session.create_session()
    news = db_sess.query(User).get(user_id)
    if not news:
        return jsonify({"error": "Not found"})
    return jsonify(
        {
            "user": news.to_dict()
        }
    )

@blueprint.route("/api/filters")
def get_filters():
    db_sess = db_session.create_session()
    filters = db_sess.query(Filter).all()
    for filter in filters:
        filter.file = str(filter.file)
        filter.image = str(filter.image)
    return jsonify(
        {
            "users": [item.to_dict() for item in filters]
        }
    )


@blueprint.route("/api/filters/<int:filter_id>", methods=['GET'])
def get_filters_1(filter_id):
    db_sess = db_session.create_session()
    filter = db_sess.query(Filter).get(filter_id)
    filter.file = str(filter.file)
    filter.image = str(filter.image)
    if not filter:
        return jsonify({"error": "Not found"})
    return jsonify(
        {
            "user": filter.to_dict()
        })