"""
    This module handles the models for companies
"""
import time
import psycopg2
from flask import request
from flask_jwt_extended import get_jwt_identity
from migrations import DbModel


class companiesModel(DbModel):
    """
        This clas handles data manipulation for the companies view
    """
    #TODO implement with an object or kwargs

    def __init__(self):
        """
            Initialize the company class and import 
        """

        super().__init__()
        self.created_at = time.strftime('%a, %d %b %Y, %I:%M:%S %p')
        self.modified_on = time.strftime('%a, %d %b %Y, %I:%M:%S %p')

    def find_company_by_name(self, name):
        """
            Fetch a company from database using its name
        """
        try:
            self.cur.execute(
                "SELECT * FROM companies WHERE company_name=%s", (name,)
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
                "SELECT * FROM companies WHERE company_id=%s", (company_id,)
            )
            return self.findOne()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
            print("An error occured when retrieving company using id")
            return None

    def get_all_companies(self):
        """
            This method returns all the saved companies
        """
        try:
            self.cur.execute(
                "SELECT * FROM companies"
            )
            return self.findAll()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
            print("An error occured when retrieving all companies")
            return None

    def find_clients(self):
        """
            Filter incidents by role
        """
        try:
            self.cur.execute(
                """ SELECT * 
                FROM companies
                WHERE 
                is_client=%s
                """, ("true",)
            )
            return self.findAll()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
            print("An error occured when retrieving companies by category")
            return None

    def save_company_to_database(self, **data):
        """
            Save the company to the database
        """
        self.company_name = data["company_name"]
        self.email = data["email"]
        self.is_client = data["is_client"]
        
        try:
            sdata = (self.company_name, self.email, self.is_client,
                     self.created_at, self.modified_on)
            print(sdata)

            self.cur.execute(
                """
                    INSERT INTO companies (company_name, email, is_client,created_at, modified_on,)
                    VALUES(%s, %s, %s, %s, %s);
                """, sdata
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
        
        self.company_name = data["company_name"]
        self.email = data["email"]
        self.is_client = data["is_client"]

        try:
            data = (self.company_name, self.email, self.is_client, company_id,)
            self.cur.execute(
                """
                UPDATE companies
                SET
                company_name = %s,
                email = %s,
                is_client = %s,
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
                "DELETE FROM companies WHERE company_id=%s", (company_id,)
            )
            self.commit()
            return True
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
            print('An error occured when trying to delete the company from the database')
            return None
