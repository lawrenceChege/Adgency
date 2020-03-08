"""
    This module handles the models for objectives
"""
import time
import psycopg2
from flask import request
from flask_jwt_extended import get_jwt_identity
from migrations import DbModel


class objectivesModel(DbModel):
    """
        This clas handles data manipulation for the objectives view
    """
    #TODO implement with an object or kwargs

    def __init__(self):
        """
            Initialize the objective class and import 
        """

        super().__init__()
        self.created_on = time.strftime('%a, %d %b %Y, %I:%M:%S %p')
        self.modified_on = time.strftime('%a, %d %b %Y, %I:%M:%S %p')
        self.created_by = get_jwt_identity()
        self.modified_by = get_jwt_identity()

    def find_objective_by_name(self, name):
        """
            Fetch a objective from database using its name
        """
        try:
            self.cur.execute(
                "SELECT * FROM objectives WHERE name=%s", (name,)
            )
            return self.findOne()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
            print("An error occured whenretrieving objective using name")
            return None

    def find_objective_by_id(self, objective_id):
        """
            Fetch a objective from database using its id
        """
        try:
            self.cur.execute(
                "SELECT * FROM objectives WHERE objective_id=%s", (objective_id,)
            )
            return self.findOne()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
            print("An error occured when retrieving objective using id")
            return None

    def get_all_objectives(self):
        """
            This method returns all the saved objectives
        """
        try:
            self.cur.execute(
                "SELECT * FROM objectives"
            )
            return self.findAll()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
            print("An error occured when retrieving all objectives")
            return None

    def find_objectives_by_category(self, objective_category):
        """
            Filter incidents by category
        """
        try:
            self.cur.execute(
                """ SELECT * 
                FROM objectives
                WHERE 
                category=%s
                """, (objective_category,)
            )
            return self.findAll()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
            print("An error occured when retrieving objectives by category")
            return None

    def save_objective_to_database(self, **data):
        """
            Save the objective to the database
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
                    INSERT INTO objectives (name,image,category,overview,tone,
                    style,duration, created_on, modified_on, created_by,modified_by)
                    VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
                """, data
            )
            self.commit()
            return True
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
            print('An error occured when trying to save the objective to the database')
            return None

#TODO implement without parameters

    def edit_objective(self, objective_id, **data):
        """
            This method can modify one or all the fields of a objective
            
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
                    self.style, self.duration, self.modified_by, self.modified_on,objective_id,)
            self.cur.execute(
                """
                UPDATE objectives
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


                WHERE objective_id = %s;
                """,data
            )
            self.commit()
            return True
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
            print('An error occured when trying to edit the objective in the database')
            return None

    def delete_objective(self, objective_id):
        """
            This method removes an objective by id from the database.
        """
        try:
            self.cur.execute(
                "DELETE FROM objectives WHERE objective_id=%s", (objective_id,)
            )
            self.commit()
            return True
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
            print('An error occured when trying to delete the objective from the database')
            return None
