"""
    This module handles the models for insights
"""
import time
import psycopg2
from flask import request
from flask_jwt_extended import get_jwt_identity
from migrations import DbModel


class InsightsModel(DbModel):
    """
        This clas handles data manipulation for the insights for the insights view
    """
    
    def __init__(self, insight=None):
        """
            Initialize the insight class and import 
        """

        super().__init__()
        self.insight = insight

    def find_insight(self, insight):
        """
            Fetch a insight from database using its name
        """
        try:
            self.cur.execute(
                "SELECT * FROM insights WHERE insight=%s", (insight,)
            )
            return self.findOne()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
            print("An error occured whenretrieving concept using name")
            return None

    def find_insight_by_id(self, insight_id):
        """
            Fetch a insight from database using its id
        """
        try:
            self.cur.execute(
                "SELECT * FROM insights WHERE insight_id=%s", (insight_id,)
            )
            return self.findOne()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
            print("An error occured when retrieving insight using id")
            return None

    def get_all_insights(self):
        """
            This method returns all the saved insights
        """
        try:
            self.cur.execute(
                "SELECT * FROM insights"
            )
            return self.findAll()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
            print("An error occured when retrieving all insights")
            return None


    def save_insight_to_database(self):
        """
            Save the insight to the database
        """
        try:

            self.cur.execute(
                """
                    INSERT INTO insights (insight)
                    VALUES(%s);
                """, (self.insight,)
            )
            self.commit()
            return True
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
            print('An error occured when trying to save the insight to the database')
            return None

#TODO implement without parameters

    def edit_insight(self, insight_id):
        """
            This method can modify one or all the fields of a insight
            
        """ 

        try:
            
            self.cur.execute(
                """
                UPDATE insights
                SET
                insight = %s
                WHERE insight_id = %s;
                """,(self.insight,)
            )
            self.commit()
            return True
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
            print('An error occured when trying to edit the insight in the database')
            return None

    def delete_insight(self, insight_id):
        """
            This method removes an insight by id from the database.
        """
        try:
            self.cur.execute(
                "DELETE FROM insights WHERE insight_id=%s", (insight_id,)
            )
            self.commit()
            return True
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
            print('An error occured when trying to delete the insight from the database')
            return None

    def update_insight(self, insight_id):
        """
            This method updates the foreing key relationship on concepts table
            
        """ 

        try:
            
            self.cur.execute(
                """
                UPDATE concepts
                SET
                insight = %s
                """,(insight_id,)
            )
            self.commit()
            return True
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
            print('An error occured when trying to edit the insight in the database')
            return None