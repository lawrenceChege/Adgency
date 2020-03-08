"""
    This module handles the models for clients
"""
import time
import psycopg2
from flask import request
from flask_jwt_extended import get_jwt_identity
from migrations import DbModel


class clientsModel(DbModel):
    """
        This clas handles data manipulation for the clients view
    """
    #TODO implement with an object or kwargs

    def __init__(self):
        """
            Initialize the client class and import 
        """

        super().__init__()
        self.created_on = time.strftime('%a, %d %b %Y, %I:%M:%S %p')
        self.modified_on = time.strftime('%a, %d %b %Y, %I:%M:%S %p')
        self.created_by = get_jwt_identity()
        self.modified_by = get_jwt_identity()

    def find_client_by_name(self, name):
        """
            Fetch a client from database using its name
        """
        try:
            self.cur.execute(
                "SELECT * FROM clients WHERE name=%s", (name,)
            )
            return self.findOne()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
            print("An error occured whenretrieving client using name")
            return None

    def find_client_by_id(self, client_id):
        """
            Fetch a client from database using its id
        """
        try:
            self.cur.execute(
                "SELECT * FROM clients WHERE client_id=%s", (client_id,)
            )
            return self.findOne()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
            print("An error occured when retrieving client using id")
            return None

    def get_all_clients(self):
        """
            This method returns all the saved clients
        """
        try:
            self.cur.execute(
                "SELECT * FROM clients"
            )
            return self.findAll()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
            print("An error occured when retrieving all clients")
            return None

    def find_clients_by_category(self, client_category):
        """
            Filter incidents by category
        """
        try:
            self.cur.execute(
                """ SELECT * 
                FROM clients
                WHERE 
                category=%s
                """, (client_category,)
            )
            return self.findAll()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
            print("An error occured when retrieving clients by category")
            return None

    def save_client_to_database(self, **data):
        """
            Save the client to the database
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
                    INSERT INTO clients (name,image,category,overview,tone,
                    style,duration, created_on, modified_on, created_by,modified_by)
                    VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
                """, data
            )
            self.commit()
            return True
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
            print('An error occured when trying to save the client to the database')
            return None

#TODO implement without parameters

    def edit_client(self, client_id, **data):
        """
            This method can modify one or all the fields of a client
            
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
                    self.style, self.duration, self.modified_by, self.modified_on,client_id,)
            self.cur.execute(
                """
                UPDATE clients
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


                WHERE client_id = %s;
                """,data
            )
            self.commit()
            return True
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
            print('An error occured when trying to edit the client in the database')
            return None

    def delete_client(self, client_id):
        """
            This method removes an client by id from the database.
        """
        try:
            self.cur.execute(
                "DELETE FROM clients WHERE client_id=%s", (client_id,)
            )
            self.commit()
            return True
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
            print('An error occured when trying to delete the client from the database')
            return None
