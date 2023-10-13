from functools import wraps

import flask
from flask_socketio import disconnect, emit

from noauth.iam.user.model.user_role import UserRole
from flask import g, request

UNAUTHORIZED = "uhuhuh you didnt say the magic word"


def is_authorized(role: UserRole):
    def is_auth_decorator(f):
        @wraps(f)
        def auth_wrapper(*args, **kwargs):
            if (g.user and g.user.role < role):
                return (UNAUTHORIZED, 401)
            return f(*args, **kwargs)

        return auth_wrapper

    return is_auth_decorator


def is_socket_authorized(role: UserRole):
    def is_auth_decorator(f):
        @wraps(f)
        def auth_wrapper(*args, **kwargs):
            user = flask.session['user']
            if (user and user.role < role):
                emit("UNAUTHORIZED", UNAUTHORIZED, sid=request.sid)
                disconnect()
                return
            return f(*args, **kwargs)

        return auth_wrapper

    return is_auth_decorator

print("a")