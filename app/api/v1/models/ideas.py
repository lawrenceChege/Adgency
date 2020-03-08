"""
    This module handles the models for ideas
"""
import time
import psycopg2
from flask import request
from flask_jwt_extended import get_jwt_identity
from migrations import DbModel


class ideasModel(DbModel):
    """
        This clas handles data manipulation for the ideas view
    """
    #TODO implement with an object or kwargs

    def __init__(self):
        """
            Initialize the idea class and import 
        """

        super().__init__()
        self.created_on = time.strftime('%a, %d %b %Y, %I:%M:%S %p')
        self.modified_on = time.strftime('%a, %d %b %Y, %I:%M:%S %p')
        self.created_by = get_jwt_identity()
        self.modified_by = get_jwt_identity()

    def find_idea_by_name(self, name):
        """
            Fetch a idea from database using its name
        """
        try:
            self.cur.execute(
                "SELECT * FROM ideas WHERE name=%s", (name,)
            )
            return self.findOne()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
            print("An error occured whenretrieving idea using name")
            return None

    def find_idea_by_id(self, idea_id):
        """
            Fetch a idea from database using its id
        """
        try:
            self.cur.execute(
                "SELECT * FROM ideas WHERE idea_id=%s", (idea_id,)
            )
            return self.findOne()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
            print("An error occured when retrieving idea using id")
            return None

    def get_all_ideas(self):
        """
            This method returns all the saved ideas
        """
        try:
            self.cur.execute(
                "SELECT * FROM ideas"
            )
            return self.findAll()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
            print("An error occured when retrieving all ideas")
            return None

    def find_ideas_by_category(self, idea_category):
        """
            Filter incidents by category
        """
        try:
            self.cur.execute(
                """ SELECT * 
                FROM ideas
                WHERE 
                category=%s
                """, (idea_category,)
            )
            return self.findAll()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
            print("An error occured when retrieving ideas by category")
            return None

    def save_idea_to_database(self, **data):
        """
            Save the idea to the database
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
                    INSERT INTO ideas (name,image,category,overview,tone,
                    style,duration, created_on, modified_on, created_by,modified_by)
                    VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
                """, data
            )
            self.commit()
            return True
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
            print('An error occured when trying to save the idea to the database')
            return None

#TODO implement without parameters

    def edit_idea(self, idea_id, **data):
        """
            This method can modify one or all the fields of a idea
            
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
                    self.style, self.duration, self.modified_by, self.modified_on,idea_id,)
            self.cur.execute(
                """
                UPDATE ideas
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


                WHERE idea_id = %s;
                """,data
            )
            self.commit()
            return True
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
            print('An error occured when trying to edit the idea in the database')
            return None

    def delete_idea(self, idea_id):
        """
            This method removes an idea by id from the database.
        """
        try:
            self.cur.execute(
                "DELETE FROM ideas WHERE idea_id=%s", (idea_id,)
            )
            self.commit()
            return True
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
            print('An error occured when trying to delete the idea from the database')
            return None
