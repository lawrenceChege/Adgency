"""
    This module handles the models for mandatory_infos
"""
import time
import psycopg2
from flask import request
from flask_jwt_extended import get_jwt_identity
from migrations import DbModel


class mandatory_infosModel(DbModel):
    """
        This clas handles data manipulation for the mandatory_infos view
    """
    #TODO implement with an object or kwargs

    def __init__(self):
        """
            Initialize the mandatory_info class and import 
        """

        super().__init__()
        self.created_on = time.strftime('%a, %d %b %Y, %I:%M:%S %p')
        self.modified_on = time.strftime('%a, %d %b %Y, %I:%M:%S %p')
        self.created_by = get_jwt_identity()
        self.modified_by = get_jwt_identity()

    def find_mandatory_info_by_name(self, name):
        """
            Fetch a mandatory_info from database using its name
        """
        try:
            self.cur.execute(
                "SELECT * FROM mandatory_infos WHERE name=%s", (name,)
            )
            return self.findOne()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
            print("An error occured whenretrieving mandatory_info using name")
            return None

    def find_mandatory_info_by_id(self, mandatory_info_id):
        """
            Fetch a mandatory_info from database using its id
        """
        try:
            self.cur.execute(
                "SELECT * FROM mandatory_infos WHERE mandatory_info_id=%s", (mandatory_info_id,)
            )
            return self.findOne()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
            print("An error occured when retrieving mandatory_info using id")
            return None

    def get_all_mandatory_infos(self):
        """
            This method returns all the saved mandatory_infos
        """
        try:
            self.cur.execute(
                "SELECT * FROM mandatory_infos"
            )
            return self.findAll()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
            print("An error occured when retrieving all mandatory_infos")
            return None

    def find_mandatory_infos_by_category(self, mandatory_info_category):
        """
            Filter incidents by category
        """
        try:
            self.cur.execute(
                """ SELECT * 
                FROM mandatory_infos
                WHERE 
                category=%s
                """, (mandatory_info_category,)
            )
            return self.findAll()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
            print("An error occured when retrieving mandatory_infos by category")
            return None

    def save_mandatory_info_to_database(self, **data):
        """
            Save the mandatory_info to the database
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
                    INSERT INTO mandatory_infos (name,image,category,overview,tone,
                    style,duration, created_on, modified_on, created_by,modified_by)
                    VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
                """, data
            )
            self.commit()
            return True
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
            print('An error occured when trying to save the mandatory_info to the database')
            return None

#TODO implement without parameters

    def edit_mandatory_info(self, mandatory_info_id, **data):
        """
            This method can modify one or all the fields of a mandatory_info
            
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
                    self.style, self.duration, self.modified_by, self.modified_on,mandatory_info_id,)
            self.cur.execute(
                """
                UPDATE mandatory_infos
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


                WHERE mandatory_info_id = %s;
                """,data
            )
            self.commit()
            return True
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
            print('An error occured when trying to edit the mandatory_info in the database')
            return None

    def delete_mandatory_info(self, mandatory_info_id):
        """
            This method removes an mandatory_info by id from the database.
        """
        try:
            self.cur.execute(
                "DELETE FROM mandatory_infos WHERE mandatory_info_id=%s", (mandatory_info_id,)
            )
            self.commit()
            return True
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
            print('An error occured when trying to delete the mandatory_info from the database')
            return None
