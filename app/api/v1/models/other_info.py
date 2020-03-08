"""
    This module handles the models for other_infos
"""
import time
import psycopg2
from flask import request
from flask_jwt_extended import get_jwt_identity
from migrations import DbModel


class other_infosModel(DbModel):
    """
        This clas handles data manipulation for the other_infos view
    """
    #TODO implement with an object or kwargs

    def __init__(self):
        """
            Initialize the other_info class and import 
        """

        super().__init__()
        self.created_on = time.strftime('%a, %d %b %Y, %I:%M:%S %p')
        self.modified_on = time.strftime('%a, %d %b %Y, %I:%M:%S %p')
        self.created_by = get_jwt_identity()
        self.modified_by = get_jwt_identity()

    def find_other_info_by_name(self, name):
        """
            Fetch a other_info from database using its name
        """
        try:
            self.cur.execute(
                "SELECT * FROM other_infos WHERE name=%s", (name,)
            )
            return self.findOne()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
            print("An error occured whenretrieving other_info using name")
            return None

    def find_other_info_by_id(self, other_info_id):
        """
            Fetch a other_info from database using its id
        """
        try:
            self.cur.execute(
                "SELECT * FROM other_infos WHERE other_info_id=%s", (other_info_id,)
            )
            return self.findOne()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
            print("An error occured when retrieving other_info using id")
            return None

    def get_all_other_infos(self):
        """
            This method returns all the saved other_infos
        """
        try:
            self.cur.execute(
                "SELECT * FROM other_infos"
            )
            return self.findAll()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
            print("An error occured when retrieving all other_infos")
            return None

    def find_other_infos_by_category(self, other_info_category):
        """
            Filter incidents by category
        """
        try:
            self.cur.execute(
                """ SELECT * 
                FROM other_infos
                WHERE 
                category=%s
                """, (other_info_category,)
            )
            return self.findAll()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
            print("An error occured when retrieving other_infos by category")
            return None

    def save_other_info_to_database(self, **data):
        """
            Save the other_info to the database
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
                    INSERT INTO other_infos (name,image,category,overview,tone,
                    style,duration, created_on, modified_on, created_by,modified_by)
                    VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
                """, data
            )
            self.commit()
            return True
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
            print('An error occured when trying to save the other_info to the database')
            return None

#TODO implement without parameters

    def edit_other_info(self, other_info_id, **data):
        """
            This method can modify one or all the fields of a other_info
            
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
                    self.style, self.duration, self.modified_by, self.modified_on,other_info_id,)
            self.cur.execute(
                """
                UPDATE other_infos
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


                WHERE other_info_id = %s;
                """,data
            )
            self.commit()
            return True
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
            print('An error occured when trying to edit the other_info in the database')
            return None

    def delete_other_info(self, other_info_id):
        """
            This method removes an other_info by id from the database.
        """
        try:
            self.cur.execute(
                "DELETE FROM other_infos WHERE other_info_id=%s", (other_info_id,)
            )
            self.commit()
            return True
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
            print('An error occured when trying to delete the other_info from the database')
            return None
