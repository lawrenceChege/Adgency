""" This is the base class for all the tests"""

import unittest
from unittest import TestCase
from flask import current_app
from app import create_app
from migrations import DbModel


class BaseTestCase(TestCase):
    """
        This class allows for dynamic creation of the database and
        provides a blank database after every scenario
    """
    
    def setUp(self):
        """
            Setup the flask app for testing.
            It initializes the app and app context.
        """
        APP = create_app("testing")
        self.app = APP.test_client()
        self.app_context = APP.app_context()
        self.app_context.push()
        with APP.app_context():
            db = DbModel()
            db.init_db(APP)
            db.drop_tables('users')
            db.create_tables()
        self.token = 0
        self.person = {
            "username": "carol",
            "isAdmin": False,
            "email": "carolmumbi@gmail.com",
            "phoneNumber": "708123123",
            "active": False,
            "password": "mae12#embiliA"
        }
        self.person1 = {
            "username": "Larry",
            "isAdmin": False,
            "email": "larrymumbi@gmail.com",
            "phoneNumber": "708193123",
            "active": False,
            "password": "mae12#embiliA"
        }
        self.person_no_username = {
            "email": "bluish@gmail.com",
            "password": "mae12#embili"
        }
        self.person_no_phone = {
            "username": "lawrence",
            "email": "bluish@gmail.com",
            "password": "mae12#embili"
        }
        self.person_no_email = {
            "username": "lawrence",
            "password": "mae12#embili"
        }
        self.person_no_password = {
            "username": "lawrence",
            "email": "mbuchez8@gmail.com",
        }
        self.person_invalid_phone = {
            "username": "lawrence",
            "email": "mbuchez@gnail.com",
            "phoneNumber": "08123123",
            "password": "mae12#embili"
        }
        self.person_invalid_email = {
            "username": "lawrence",
            "email": "mbuchez.com",
            "phoneNumber": "708123123",
            "password": "mae12#embili"
        }
        self.person_invalid_username = {
            "username": "",
            "email": "mbuchez@gmail.com",
            "phoneNumber": "708123123",
            "password": "mae12#embili"
        }
        self.person_invalid_password = {
            "username": "mama yao",
            "email": "mbuchez@gmail.com",
            "phoneNumber": "708123123",
            "password": "maembe"
        }
        self.person_existing_user = {
            "firstname": "carolol",
            "lastname": "mumbi",
            "email": "carolmumbi@gmail.com",
            "phoneNumber": "708123123",
            "username": "carolmobic",
            "password": "aswdeAWSE$WE"
        }

        self.correct_login = {
            "username": "carolmobic",
            "password": "mae12#embiliA"
            }
        self.correct_login1 = {
            "username": "carolmobic",
            "password": "aswdeAWSE$WE"
            }

        self.wrong_login = {"username": "carolmoboc",
                            "password": "mistubishi"}
        self.no_username = {"username": "",
                            "password": "maembembili"}
        self.no_password = {"username": "lawrence",
                            "password": ""}
        self.admin = {
            "id": 1,
            "firstname": "carol",
            "lastname": "mumbi",
            "email": "carolmumbi@gmail.com",
            "phoneNumber": "0708123123",
            "username": "carolmobic",
            "registered": "26/11/2018"
        }

        self.admin_correct = {"username": "admin",
                              "password": "admn1234"}
        self.admin_wrong = {"username": "lawrence",
                            "password": "mimi"}

    def tearDown(self):
        """
            This method is called if setUp() succeeds.
            It destroys the app context.
        """
        pass

if __name__ == '__main__':
    unittest.main()