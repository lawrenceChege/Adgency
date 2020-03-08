"""
    This module handles the models for platforms
"""
import time
import psycopg2
from flask import request
from flask_jwt_extended import get_jwt_identity
from migrations import DbModel


class platformsModel(DbModel):
    """
        This clas handles data manipulation for the platforms view
    """
    #TODO implement with an object or kwargs

    def __init__(self):
        """
            Initialize the platform class and import 
        """

        super().__init__()
        self.created_on = time.strftime('%a, %d %b %Y, %I:%M:%S %p')
        self.modified_on = time.strftime('%a, %d %b %Y, %I:%M:%S %p')
        self.created_by = get_jwt_identity()
        self.modified_by = get_jwt_identity()

    def find_platform_by_name(self, name):
        """
            Fetch a platform from database using its name
        """
        try:
            self.cur.execute(
                "SELECT * FROM platforms WHERE name=%s", (name,)
            )
            return self.findOne()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
            print("An error occured whenretrieving platform using name")
            return None

    def find_platform_by_id(self, platform_id):
        """
            Fetch a platform from database using its id
        """
        try:
            self.cur.execute(
                "SELECT * FROM platforms WHERE platform_id=%s", (platform_id,)
            )
            return self.findOne()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
            print("An error occured when retrieving platform using id")
            return None

    def get_all_platforms(self):
        """
            This method returns all the saved platforms
        """
        try:
            self.cur.execute(
                "SELECT * FROM platforms"
            )
            return self.findAll()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
            print("An error occured when retrieving all platforms")
            return None

    def find_platforms_by_category(self, platform_category):
        """
            Filter incidents by category
        """
        try:
            self.cur.execute(
                """ SELECT * 
                FROM platforms
                WHERE 
                category=%s
                """, (platform_category,)
            )
            return self.findAll()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
            print("An error occured when retrieving platforms by category")
            return None

    def save_platform_to_database(self, **data):
        """
            Save the platform to the database
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
                    INSERT INTO platforms (name,image,category,overview,tone,
                    style,duration, created_on, modified_on, created_by,modified_by)
                    VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
                """, data
            )
            self.commit()
            return True
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
            print('An error occured when trying to save the platform to the database')
            return None

#TODO implement without parameters

    def edit_platform(self, platform_id, **data):
        """
            This method can modify one or all the fields of a platform
            
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
                    self.style, self.duration, self.modified_by, self.modified_on,platform_id,)
            self.cur.execute(
                """
                UPDATE platforms
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


                WHERE platform_id = %s;
                """,data
            )
            self.commit()
            return True
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
            print('An error occured when trying to edit the platform in the database')
            return None

    def delete_platform(self, platform_id):
        """
            This method removes an platform by id from the database.
        """
        try:
            self.cur.execute(
                "DELETE FROM platforms WHERE platform_id=%s", (platform_id,)
            )
            self.commit()
            return True
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
            print('An error occured when trying to delete the platform from the database')
            return None
