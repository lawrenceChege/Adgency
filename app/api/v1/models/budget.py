"""
    This module handles the models for budgets
"""
import time
import psycopg2
from flask import request
from flask_jwt_extended import get_jwt_identity
from migrations import DbModel


class BudgetModel(DbModel):
    """
        This clas handles data manipulation for the budgets view
    """
    #TODO implement with an object or kwargs

    def __init__(self):
        """
            Initialize the budget class and import 
        """

        super().__init__()
        self.created_on = time.strftime('%a, %d %b %Y, %I:%M:%S %p')
        self.modified_on = time.strftime('%a, %d %b %Y, %I:%M:%S %p')
        self.created_by = get_jwt_identity()
        self.modified_by = get_jwt_identity()

    def find_budget_by_item(self, item):
        """
            Fetch a budget entry from database using an item
        """
        try:
            self.cur.execute(
                "SELECT * FROM budget WHERE item=%s", (item,)
            )
            return self.findOne()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
            print("An error occured when retrieving budget using item")
            return None

    def find_budget_by_id(self, budget_id):
        """
            Fetch a budget from database using its id
        """
        try:
            self.cur.execute(
                "SELECT * FROM budget WHERE budget_id=%s", (budget_id,)
            )
            return self.findOne()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
            print("An error occured when retrieving budget using id")
            return None

    def get_all_budgets(self):
        """
            This method returns all the saved budgets
        """
        try:
            self.cur.execute(
                "SELECT * FROM budget"
            )
            return self.findAll()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
            print("An error occured when retrieving all budgets")
            return None

    def find_budgets_by_status(self, status):
        """
            Filter incidents by status
        """
        try:
            self.cur.execute(
                """ SELECT * 
                FROM budget
                WHERE 
                status=%s
                """, (status,)
            )
            return self.findAll()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
            print("An error occured when retrieving budgets by category")
            return None

    def save_budget_to_database(self, **data):
        """
            Save the budget to the database
        """
        self.item = data["item"]
        self.description = data["description"]
        self.start_date = data["start_date"]
        self.end_date = data["end_date"]
        self.amount = data["amount"]
        self.status = data["status"]

        try:
            data = (self.item, self.description, self.start_date,
                     self.end_date, self.amount, self.status, self.created_on,
                     self.modified_on, self.created_by, self.modified_by)

            self.cur.execute(
                """
                    INSERT INTO budget (item,description,start_date
                                        ,end_date,amount, status,
                                        created_on, modified_on, created_by,modified_by)
                    VALUES(%s, %s, %s, %s, %s, %s,%s, %s, %s, %s);
                """, data
            )
            self.commit()
            return True
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
            print('An error occured when trying to save the budget to the database')
            return None

#TODO implement without parameters

    def edit_budget(self, budget_id, **data):
        """
            This method can modify one or all the fields of a budget
            
        """
        
        self.item = data["item"]
        self.description = data["description"]
        self.start_date = data["start_date"]
        self.end_date = data["end_date"]
        self.amount = data["amount"]
        self.status = data["status"]

        try:
            data = (self.item, self.description, self.start_date,
                     self.end_date, self.amount, self.status, self.created_on,
                     self.modified_on, self.created_by, self.modified_by)
            self.cur.execute(
                """
                UPDATE budget
                SET
                item = %s,
                description = %s,
                start_date = %s,
                end_date = %s,
                amount = %s,
                status = %s,
                modified_by= %s,
                modified_on= %s

                WHERE budget_id = %s;
                """,data
            )
            self.commit()
            return True
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
            print('An error occured when trying to edit the budget in the database')
            return None

    def delete_budget(self, budget_id):
        """
            This method removes an budget by id from the database.
        """
        try:
            self.cur.execute(
                "DELETE FROM budget WHERE budget_id=%s", (budget_id,)
            )
            self.commit()
            return True
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
            print('An error occured when trying to delete the budget from the database')
            return None
