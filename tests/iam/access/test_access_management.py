import unittest
from unittest.mock import patch

import flask

from flask import Flask, g

from noauth.iam.access.access_management import is_authorized, is_socket_authorized, UNAUTHORIZED
from noauth.iam.user.model.user import User
from noauth.iam.user.model.user_role import UserRole


class TestAccessManagement(unittest.TestCase):

    def setUp(self):
        # I tried mocking g and it was major fucked, it wouldn't let me as it kept saying
        # I wasn't in the app context? Hey bozo(python), what do you think a MOCK is
        self.app = Flask(__name__)
        self.app.secret_key = "lol"

    def test_user_request_is_unauthorized(self):
        with self.app.app_context():
            g.user = User(id="whatever", role=UserRole.PLAYER)

            @is_authorized(UserRole.ADMIN)
            def my_test_function():
                raise AssertionError("This function should not have been called")

            actual = my_test_function()

            self.assertEqual(type(actual), tuple)

            self.assertEqual(actual[0], UNAUTHORIZED)

    def test_user_request_is_authorized(self):
        with self.app.app_context():
            expected = "foo"
            g.user = User(id="whatever", role=UserRole.ADMIN)

            @is_authorized(UserRole.ADMIN)
            def my_test_function():
                return expected

            actual = my_test_function()

            self.assertEqual(actual, expected)

    @patch("noauth.iam.access.access_management.disconnect", new=lambda: None)
    @patch("noauth.iam.access.access_management.emit")
    def test_user_socket_request_is_unauthorized(self, mock_emit):
        with self.app.test_request_context():
            flask.request.sid = "does_not_matter"
            flask.session['user'] = User(id="whatever", role=UserRole.PLAYER)

            @is_socket_authorized(UserRole.ADMIN)
            def my_test_function():
                raise AssertionError("This function should not have been called")

            self.assertIsNone(my_test_function())

            mock_emit.assert_called_with("UNAUTHORIZED", UNAUTHORIZED, sid=flask.request.sid)

    @patch("noauth.iam.access.access_management.disconnect", new=lambda: None)
    @patch("noauth.iam.access.access_management.emit", )
    def test_user_socket_request_is_authorized(self, mock_emit):
        expected = "foo"

        with self.app.test_request_context():
            flask.request.sid = "does_not_matter"
            flask.session['user'] = User(id="whatever", role=UserRole.ADMIN)

            @is_socket_authorized(UserRole.ADMIN)
            def my_test_function():
                return expected

            actual = my_test_function()

            self.assertEqual(actual, expected)

    def tearDown(self):
        pass
