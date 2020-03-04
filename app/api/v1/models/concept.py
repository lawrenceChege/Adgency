"""
    This module handles the models for concepts
"""
import time
import psycopg2
from flask import request
from flask_jwt_extended import get_jwt_identity
from migrations import DbModel


class ConceptsModel(DbModel):
    """
        This clas handles data manipulation for the concepts view
    """
    def __init__(self, concept_name=None, concept_item=None, concept_category=None,
        concept_mood=None, concept_audience=None, concept_platform=None,project_id=None):
        """
            Initialize the concept class and import 
        """


        super().__init__()
        self.concept_name = concept_name
        self.concept_item = concept_item
        self.concept_category = concept_category
        self.concept_mood = concept_mood
        self.concept_audience = concept_audience
        self.concept_platform = concept_platform
        self.project_id = project_id
        self.created_on = time.strftime('%a, %d %b %Y, %I:%M:%S %p')
        self.modified_on = time.strftime('%a, %d %b %Y, %I:%M:%S %p')
        self.created_by = get_jwt_identity()

    def find_concept_by_name(self, name):
        """
            Fetch a concept from database using its name
        """
        try:
            self.cur.execute(
                "SELECT * FROM concepts WHERE name=%s", (name,)
            )
            return self.findOne()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
            print("An error occured whenretrieving concept using name")
            return None

    def find_concept_by_id(self,concept_id):
        """
            Fetch a concept from database using its id
        """
        try:
            self.cur.execute(
                "SELECT * FROM conceptss WHERE concept_id=%s", (concept_id,)
                )
            return self.findOne()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
            print("An error occured when retrieving concept using id")
            return None

    def save_concept_to_database(self):
        """
            Save the concept to the database
        """
        try:
            data =( self.concept_name, self.concept_category, self.concept_mood ,
                    self.concept_audience, self.concept_platform,self.project_id,
                    self.created_by,self.created_on,self.modified_on )

            self.cur.execute(
                """
                    INSERT INTO incidents (
                       concept_name, concept_category, concept_mood,
                       concept_audience, concept_platform, project_id,
                       created_by,created_on,modified_on)
                    VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s);
                """, data
            )
            self.commit()
            return True
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
            print('An error occured when trying to save the concept to the database')
            return None