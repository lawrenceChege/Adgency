"""
    This module handles the models for companys
"""
import time
import psycopg2
from flask import request
from flask_jwt_extended import get_jwt_identity
from migrations import DbModel


class companysModel(DbModel):
    """
        This clas handles data manipulation for the companys view
    """
    #TODO implement with an object or kwargs

    def __init__(self):
        """
            Initialize the company class and import 
        """

        super().__init__()
        self.created_on = time.strftime('%a, %d %b %Y, %I:%M:%S %p')
        self.modified_on = time.strftime('%a, %d %b %Y, %I:%M:%S %p')
        self.created_by = get_jwt_identity()
        self.modified_by = get_jwt_identity()

    def find_company_by_name(self, name):
        """
            Fetch a company from database using its name
        """
        try:
            self.cur.execute(
                "SELECT * FROM companys WHERE name=%s", (name,)
            )
            return self.findOne()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
            print("An error occured whenretrieving company using name")
            return None

    def find_company_by_id(self, company_id):
        """
            Fetch a company from database using its id
        """
        try:
            self.cur.execute(
                "SELECT * FROM companys WHERE company_id=%s", (company_id,)
            )
            return self.findOne()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
            print("An error occured when retrieving company using id")
            return None

    def get_all_companys(self):
        """
            This method returns all the saved companys
        """
        try:
            self.cur.execute(
                "SELECT * FROM companys"
            )
            return self.findAll()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
            print("An error occured when retrieving all companys")
            return None

    def find_companys_by_category(self, company_category):
        """
            Filter incidents by category
        """
        try:
            self.cur.execute(
                """ SELECT * 
                FROM companys
                WHERE 
                category=%s
                """, (company_category,)
            )
            return self.findAll()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
            print("An error occured when retrieving companys by category")
            return None

    def save_company_to_database(self, **data):
        """
            Save the company to the database
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
                    INSERT INTO companys (name,image,category,overview,tone,
                    style,duration, created_on, modified_on, created_by,modified_by)
                    VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
                """, data
            )
            self.commit()
            return True
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
            print('An error occured when trying to save the company to the database')
            return None

#TODO implement without parameters

    def edit_company(self, company_id, **data):
        """
            This method can modify one or all the fields of a company
            
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
                    self.style, self.duration, self.modified_by, self.modified_on,company_id,)
            self.cur.execute(
                """
                UPDATE companys
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


                WHERE company_id = %s;
                """,data
            )
            self.commit()
            return True
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
            print('An error occured when trying to edit the company in the database')
            return None

    def delete_company(self, company_id):
        """
            This method removes an company by id from the database.
        """
        try:
            self.cur.execute(
                "DELETE FROM companys WHERE company_id=%s", (company_id,)
            )
            self.commit()
            return True
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
            print('An error occured when trying to delete the company from the database')
            return None
