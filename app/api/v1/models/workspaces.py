"""
    This module handles the models for workspaces
"""
import time
import psycopg2
from flask import request
from flask_jwt_extended import get_jwt_identity
from migrations import DbModel


class workspacesModel(DbModel):
    """
        This clas handles data manipulation for the workspaces view
    """
    #TODO implement with an object or kwargs

    def __init__(self):
        """
            Initialize the workspace class and import 
        """

        super().__init__()
        self.created_on = time.strftime('%a, %d %b %Y, %I:%M:%S %p')
        self.modified_on = time.strftime('%a, %d %b %Y, %I:%M:%S %p')
        self.created_by = get_jwt_identity()
        self.modified_by = get_jwt_identity()

    def find_workspace_by_name(self, name):
        """
            Fetch a workspace from database using its name
        """
        try:
            self.cur.execute(
                "SELECT * FROM workspaces WHERE name=%s", (name,)
            )
            return self.findOne()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
            print("An error occured whenretrieving workspace using name")
            return None

    def find_workspace_by_id(self, workspace_id):
        """
            Fetch a workspace from database using its id
        """
        try:
            self.cur.execute(
                "SELECT * FROM workspaces WHERE workspace_id=%s", (workspace_id,)
            )
            return self.findOne()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
            print("An error occured when retrieving workspace using id")
            return None

    def get_all_workspaces(self):
        """
            This method returns all the saved workspaces
        """
        try:
            self.cur.execute(
                "SELECT * FROM workspaces"
            )
            return self.findAll()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
            print("An error occured when retrieving all workspaces")
            return None

    def find_workspaces_by_category(self, workspace_category):
        """
            Filter incidents by category
        """
        try:
            self.cur.execute(
                """ SELECT * 
                FROM workspaces
                WHERE 
                category=%s
                """, (workspace_category,)
            )
            return self.findAll()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
            print("An error occured when retrieving workspaces by category")
            return None

    def save_workspace_to_database(self, **data):
        """
            Save the workspace to the database
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
                    INSERT INTO workspaces (name,image,category,overview,tone,
                    style,duration, created_on, modified_on, created_by,modified_by)
                    VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
                """, data
            )
            self.commit()
            return True
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
            print('An error occured when trying to save the workspace to the database')
            return None

#TODO implement without parameters

    def edit_workspace(self, workspace_id, **data):
        """
            This method can modify one or all the fields of a workspace
            
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
                    self.style, self.duration, self.modified_by, self.modified_on,workspace_id,)
            self.cur.execute(
                """
                UPDATE workspaces
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


                WHERE workspace_id = %s;
                """,data
            )
            self.commit()
            return True
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
            print('An error occured when trying to edit the workspace in the database')
            return None

    def delete_workspace(self, workspace_id):
        """
            This method removes an workspace by id from the database.
        """
        try:
            self.cur.execute(
                "DELETE FROM workspaces WHERE workspace_id=%s", (workspace_id,)
            )
            self.commit()
            return True
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
            print('An error occured when trying to delete the workspace from the database')
            return None
