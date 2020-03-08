"""
    This module handles the models for projects
"""
import time
import psycopg2
from flask import request
from flask_jwt_extended import get_jwt_identity
from migrations import DbModel


class projectsModel(DbModel):
    """
        This clas handles data manipulation for the projects view
    """
    #TODO implement with an object or kwargs

    def __init__(self):
        """
            Initialize the project class and import 
        """

        super().__init__()
        self.created_on = time.strftime('%a, %d %b %Y, %I:%M:%S %p')
        self.modified_on = time.strftime('%a, %d %b %Y, %I:%M:%S %p')
        self.created_by = get_jwt_identity()
        self.modified_by = get_jwt_identity()

    def find_project_by_name(self, name):
        """
            Fetch a project from database using its name
        """
        try:
            self.cur.execute(
                "SELECT * FROM projects WHERE name=%s", (name,)
            )
            return self.findOne()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
            print("An error occured whenretrieving project using name")
            return None

    def find_project_by_id(self, project_id):
        """
            Fetch a project from database using its id
        """
        try:
            self.cur.execute(
                "SELECT * FROM projects WHERE project_id=%s", (project_id,)
            )
            return self.findOne()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
            print("An error occured when retrieving project using id")
            return None

    def get_all_projects(self):
        """
            This method returns all the saved projects
        """
        try:
            self.cur.execute(
                "SELECT * FROM projects"
            )
            return self.findAll()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
            print("An error occured when retrieving all projects")
            return None

    def find_projects_by_category(self, project_category):
        """
            Filter incidents by category
        """
        try:
            self.cur.execute(
                """ SELECT * 
                FROM projects
                WHERE 
                category=%s
                """, (project_category,)
            )
            return self.findAll()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
            print("An error occured when retrieving projects by category")
            return None

    def save_project_to_database(self, **data):
        """
            Save the project to the database
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
                    INSERT INTO projects (name,image,category,overview,tone,
                    style,duration, created_on, modified_on, created_by,modified_by)
                    VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
                """, data
            )
            self.commit()
            return True
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
            print('An error occured when trying to save the project to the database')
            return None

#TODO implement without parameters

    def edit_project(self, project_id, **data):
        """
            This method can modify one or all the fields of a project
            
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
                    self.style, self.duration, self.modified_by, self.modified_on,project_id,)
            self.cur.execute(
                """
                UPDATE projects
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


                WHERE project_id = %s;
                """,data
            )
            self.commit()
            return True
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
            print('An error occured when trying to edit the project in the database')
            return None

    def delete_project(self, project_id):
        """
            This method removes an project by id from the database.
        """
        try:
            self.cur.execute(
                "DELETE FROM projects WHERE project_id=%s", (project_id,)
            )
            self.commit()
            return True
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
            print('An error occured when trying to delete the project from the database')
            return None
