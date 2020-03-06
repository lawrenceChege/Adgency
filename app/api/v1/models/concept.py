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
    #TODO implement with an object or kwargs
    def __init__(self, concept_name=None, concept_item=None, concept_image=None, concept_category=None,
        concept_mood=None, concept_audience=None, concept_platform=None,project_id=None):
        """
            Initialize the concept class and import 
        """


        super().__init__()
        self.concept_name = concept_name
        self.concept_item = concept_item
        self.concept_image = concept_image
        self.concept_category = concept_category
        self.concept_mood = concept_mood
        self.concept_audience = concept_audience
        self.concept_platform = concept_platform
        self.project_id = project_id
        self.created_on = time.strftime('%a, %d %b %Y, %I:%M:%S %p')
        self.modified_on = time.strftime('%a, %d %b %Y, %I:%M:%S %p')
        self.created_by = get_jwt_identity()
        self.modified_by = get_jwt_identity()

    def find_concept_by_name(self, concept_name):
        """
            Fetch a concept from database using its name
        """
        try:
            self.cur.execute(
                "SELECT * FROM concepts WHERE concept_name=%s", (concept_name,)
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


    def get_all_concepts(self):
        """
            This method returns all the saved concepts
        """
        try:
            self.cur.execute(
                "SELECT * FROM concepts"
            )
            return self.findAll()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
            print("An error occured when retrieving all concepts")
            return None

    def find_concepts_by_category(self, concept_category):
        """
            Filter incidents by category
        """
        try:
            self.cur.execute(
                """ SELECT * 
                FROM concepts
                WHERE 
                concept_category=%s
                """,(concept_category,)
            )
            return self.findAll()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
            print("An error occured when retrieving concepts by category")
            return None

    def save_concept_to_database(self):
        """
            Save the concept to the database
        """
        try:
            data =( self.concept_name,self.concept_item, self.concept_image, self.concept_category, self.concept_mood ,
                    self.concept_audience, self.concept_platform,
                    self.created_by,self.created_on,self.modified_on, self.modified_by, )

            self.cur.execute(
                """
                    INSERT INTO concepts (concept_name,concept_item,concept_image, 
                                            concept_category, concept_mood,concept_audience,concept_platform,
                                            created_by,created_on,modified_on, modified_by)
                    VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
                """, data
            )
            self.commit()
            return True
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
            print('An error occured when trying to save the concept to the database')
            return None

#TODO implement without parameters
 
    def edit_concept(self,concept_name,concept_item, concept_image, concept_category, concept_mood,
                       concept_audience, concept_platform, concept_id):
        """
            This method can modify one or all the fields of a concept
            
        """
        try:
            self.cur.execute(
                """
                UPDATE concepts
                SET
                concept_name= %s,
                concept_item=%s,
                concept_image=%s,
                concept_category= %s,
                concept_mood= %s,
                concept_audience= %s,
                concept_platform= %s,
                modified_by= %s,
                modified_on= %s,
                WHERE concept_id = %s;
                """,(concept_name, concept_item,concept_image, concept_category, concept_mood,
                       concept_audience, concept_platform,
                       self.modified_by,self.modified_on, concept_id,
                )
                )
            self.commit()
            return True
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
            print('An error occured when trying to edit the concept in the database')
            return None

    def delete_concept(self, concept_id):
        """
            This method removes an concept by id from the database.
        """
        try:
            self.cur.execute(
                "DELETE FROM concepts WHERE concept_id=%s", (concept_id,)
                )
            self.commit()
            return True
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
            print('An error occured when trying to delete the concept from the database')
            return None

    