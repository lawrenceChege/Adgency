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

    def __init__(self):
        """
            Initialize the concept class and import 
        """

        super().__init__()
        self.created_on = time.strftime('%a, %d %b %Y, %I:%M:%S %p')
        self.modified_on = time.strftime('%a, %d %b %Y, %I:%M:%S %p')
        self.created_by = get_jwt_identity()
        self.modified_by = get_jwt_identity()

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

    def find_concept_by_id(self, concept_id):
        """
            Fetch a concept from database using its id
        """
        try:
            self.cur.execute(
                "SELECT * FROM concepts WHERE concept_id=%s", (concept_id,)
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
                category=%s
                """, (concept_category,)
            )
            return self.findAll()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
            print("An error occured when retrieving concepts by category")
            return None

    def save_concept_to_database(self, **data):
        """
            Save the concept to the database
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
                    INSERT INTO concepts (name,image,category,overview,tone,
                    style,duration, created_on, modified_on, created_by,modified_by)
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

    def edit_concept(self, concept_id, **data):
        """
            This method can modify one or all the fields of a concept
            
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
                    self.style, self.duration, self.modified_by, self.modified_on,concept_id)
            self.cur.execute(
                """
                UPDATE concepts
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


                WHERE concept_id = %s;
                """, data
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
