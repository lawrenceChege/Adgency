"""
    This module holds the Model for the Users
"""
import datetime
from flask_restplus import reqparse
from flask import request
from flask_jwt_extended import create_access_token
from werkzeug.security import generate_password_hash, check_password_hash

USERS = []

class UserModel():
    """
        This class manages the data for the users
    """
    id = 1

    def __init__(self, email=None, phoneNumber=None, is_admin=True,
                 username=None, password=None, active=None):
        self.id = UserModel.id
        self.email = email
        self.password = self.generate_pass_hash()
        self.phoneNumber = phoneNumber
        self.username = username
        self.active = active
        self.is_admin = is_admin
        self.created_on = datetime.datetime.now()
        self.db = USERS

        UserModel.id += 1

    @staticmethod
    def generate_pass_hash():
        """
        encrypt password
        """

        private_key = generate_password_hash(request.json["password"])
        return private_key

    def check_password_match(self):
        """
        Check if pass match
        :param :password: password
        return: Boolean
        """
        match = check_password_hash(self.password, request.json["password"])
        return match

    def generate_jwt_token(self):
        token = create_access_token(identity=self.username)
        return token

    def find_by_id(self, incident_id):
        """
        Find user by id
        """
        for user in self.db:
            if user["id"] == incident_id:
                return user
            return None

    def find_by_username(self):
        """
        Find user by username
        """
        user = [u.username for u in self.db if u.username ==
                request.json["username"]]
        if user:
            return user
        return None

    def save_to_db(self):
        """
            This method saves the user to the database.
        """
        self.db.append(self)

    def login_user(self):
        """
            This method logs in the user.
            It takes username and password as parameters and
            It returns jwt token
        """
        if self.check_password_match():
            token = self.generate_jwt_token()
            return token
        return None