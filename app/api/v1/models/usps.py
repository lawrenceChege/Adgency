"""
    This module handles the models for usps
"""
import time
import psycopg2
from flask import request
from flask_jwt_extended import get_jwt_identity
from migrations import DbModel


class uspsModel(DbModel):
    """
        This clas handles data manipulation for the usps view
    """
    #TODO implement with an object or kwargs

    def __init__(self):
        """
            Initialize the usp class and import 
        """

        super().__init__()
        self.created_on = time.strftime('%a, %d %b %Y, %I:%M:%S %p')
        self.modified_on = time.strftime('%a, %d %b %Y, %I:%M:%S %p')
        self.created_by = get_jwt_identity()
        self.modified_by = get_jwt_identity()

    def find_usp_by_name(self, name):
        """
            Fetch a usp from database using its name
        """
        try:
            self.cur.execute(
                "SELECT * FROM usps WHERE name=%s", (name,)
            )
            return self.findOne()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
            print("An error occured whenretrieving usp using name")
            return None

    def find_usp_by_id(self, usp_id):
        """
            Fetch a usp from database using its id
        """
        try:
            self.cur.execute(
                "SELECT * FROM usps WHERE usp_id=%s", (usp_id,)
            )
            return self.findOne()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
            print("An error occured when retrieving usp using id")
            return None

    def get_all_usps(self):
        """
            This method returns all the saved usps
        """
        try:
            self.cur.execute(
                "SELECT * FROM usps"
            )
            return self.findAll()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
            print("An error occured when retrieving all usps")
            return None

    def find_usps_by_category(self, usp_category):
        """
            Filter incidents by category
        """
        try:
            self.cur.execute(
                """ SELECT * 
                FROM usps
                WHERE 
                category=%s
                """, (usp_category,)
            )
            return self.findAll()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
            print("An error occured when retrieving usps by category")
            return None

    def save_usp_to_database(self, **data):
        """
            Save the usp to the database
        """
        self.name = data["name"]
        self.image = data["image"]
        self.category = data["category"]
        self.overview = data["overview"]
        self.tone = data["tone"]
        self.style = data["style"]
        self.duration= data["duration"] 
        try:
            data = (self.name, self.image, self.category, self.overview, self.tone,
                    self.style, self.duration, self.created_on, self.modified_on,
                    self.created_by, self.modified_by)

            self.cur.execute(
                """
                    INSERT INTO usps (name,image,category,overview,tone,
                    style,duration, created_on, modified_on, created_by,modified_by)
                    VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
                """, data
            )
            self.commit()
            return True
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
            print('An error occured when trying to save the usp to the database')
            return None

#TODO implement without parameters

    def edit_usp(self, usp_id, **data):
        """
            This method can modify one or all the fields of a usp
            
        """
        
        self.name = data["name"]
        self.image = data["image"]
        self.category = data["category"]
        self.overview = data["overview"]
        self.tone = data["tone"]
        self.style = data["style"]
        self.duration= data["duration"] 

        try:
            data = (self.name, self.image, self.category, self.overview, self.tone,
                    self.style, self.duration, self.modified_by, self.modified_on,usp_id,)
            self.cur.execute(
                """
                UPDATE usps
                SET
                name = %s,
                image = %s,
                category = %s,
                overview = %s,
                tone = %s,
                style = %s,
                duration = %s, 
                modified_by= %s,
                modified_on= %s


                WHERE usp_id = %s;
                """,data
            )
            self.commit()
            return True
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
            print('An error occured when trying to edit the usp in the database')
            return None

    def delete_usp(self, usp_id):
        """
            This method removes an usp by id from the database.
        """
        try:
            self.cur.execute(
                "DELETE FROM usps WHERE usp_id=%s", (usp_id,)
            )
            self.commit()
            return True
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
            print('An error occured when trying to delete the usp from the database')
            return None
