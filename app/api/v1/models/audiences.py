"""
    This module handles the models for audiences
"""
import time
import psycopg2
from flask import request
from flask_jwt_extended import get_jwt_identity
from migrations import DbModel


class audiencesModel(DbModel):
    """
        This clas handles data manipulation for the audiences view
    """
    #TODO implement with an object or kwargs

    def __init__(self):
        """
            Initialize the audience class and import 
        """

        super().__init__()


    def find_audience_by_name(self, name):
        """
            Fetch a audience from database using its name
        """
        try:
            self.cur.execute(
                "SELECT * FROM audiences WHERE name=%s", (name,)
            )
            return self.findOne()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
            print("An error occured whenretrieving audience using name")
            return None

    def find_audience_by_id(self, audience_id):
        """
            Fetch a audience from database using its id
        """
        try:
            self.cur.execute(
                "SELECT * FROM audiences WHERE audience_id=%s", (audience_id,)
            )
            return self.findOne()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
            print("An error occured when retrieving audience using id")
            return None

    def get_all_audiences(self):
        """
            This method returns all the saved audiences
        """
        try:
            self.cur.execute(
                "SELECT * FROM audiences"
            )
            return self.findAll()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
            print("An error occured when retrieving all audiences")
            return None

    def save_audience_to_database(self, **data):
        """
            Save the audience to the database
        """
        self.name = data["name"]
        self.age_group= data["age_group"]
        self.gender = data["gender"]
        self.location = data["location"]
        try:
            data = (self.name, self.age_group, self.gender, self.location)

            self.cur.execute(
                """
                    INSERT INTO audiences (name,age_group, gender, location)
                    VALUES(%s, %s, %s, %s);
                """, data
            )
            self.commit()
            return True
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
            print('An error occured when trying to save the audience to the database')
            return None

#TODO implement without parameters

    def edit_audience(self, audience_id, **data):
        """
            This method can modify one or all the fields of a audience
            
        """
        
       self.name = data["name"]
        self.age_group= data["age_group"]
        self.gender = data["gender"]
        self.location = data["location"]
        try:
            data = (self.name, self.age_group, self.gender, self.location)
            self.cur.execute(
                """
                UPDATE audiences
                SET
                name = %s,
                age_group = %s,
                gender = %s,
                location = %s

                WHERE audience_id = %s;
                """,data
            )
            self.commit()
            return True
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
            print('An error occured when trying to edit the audience in the database')
            return None

    def delete_audience(self, audience_id):
        """
            This method removes an audience by id from the database.
        """
        try:
            self.cur.execute(
                "DELETE FROM audiences WHERE audience_id=%s", (audience_id,)
            )
            self.commit()
            return True
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
            print('An error occured when trying to delete the audience from the database')
            return None
