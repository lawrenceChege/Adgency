"""
    This module handles the models for votes
"""
import time
import psycopg2
from flask import request
from flask_jwt_extended import get_jwt_identity
from migrations import DbModel


class votesModel(DbModel):
    """
        This clas handles data manipulation for the votes view
    """
    #TODO implement with an object or kwargs

    def __init__(self):
        """
            Initialize the vote class and import 
        """

        super().__init__()
        self.created_on = time.strftime('%a, %d %b %Y, %I:%M:%S %p')
        self.modified_on = time.strftime('%a, %d %b %Y, %I:%M:%S %p')
        self.created_by = get_jwt_identity()
        self.modified_by = get_jwt_identity()

    def find_vote_by_name(self, name):
        """
            Fetch a vote from database using its name
        """
        try:
            self.cur.execute(
                "SELECT * FROM votes WHERE name=%s", (name,)
            )
            return self.findOne()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
            print("An error occured whenretrieving vote using name")
            return None

    def find_vote_by_id(self, vote_id):
        """
            Fetch a vote from database using its id
        """
        try:
            self.cur.execute(
                "SELECT * FROM votes WHERE vote_id=%s", (vote_id,)
            )
            return self.findOne()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
            print("An error occured when retrieving vote using id")
            return None

    def get_all_votes(self):
        """
            This method returns all the saved votes
        """
        try:
            self.cur.execute(
                "SELECT * FROM votes"
            )
            return self.findAll()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
            print("An error occured when retrieving all votes")
            return None

    def find_votes_by_category(self, vote_category):
        """
            Filter incidents by category
        """
        try:
            self.cur.execute(
                """ SELECT * 
                FROM votes
                WHERE 
                category=%s
                """, (vote_category,)
            )
            return self.findAll()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
            print("An error occured when retrieving votes by category")
            return None

    def save_vote_to_database(self, **data):
        """
            Save the vote to the database
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
                    INSERT INTO votes (name,image,category,overview,tone,
                    style,duration, created_on, modified_on, created_by,modified_by)
                    VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
                """, data
            )
            self.commit()
            return True
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
            print('An error occured when trying to save the vote to the database')
            return None

#TODO implement without parameters

    def edit_vote(self, vote_id, **data):
        """
            This method can modify one or all the fields of a vote
            
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
                    self.style, self.duration, self.modified_by, self.modified_on,vote_id,)
            self.cur.execute(
                """
                UPDATE votes
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


                WHERE vote_id = %s;
                """,data
            )
            self.commit()
            return True
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
            print('An error occured when trying to edit the vote in the database')
            return None

    def delete_vote(self, vote_id):
        """
            This method removes an vote by id from the database.
        """
        try:
            self.cur.execute(
                "DELETE FROM votes WHERE vote_id=%s", (vote_id,)
            )
            self.commit()
            return True
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
            print('An error occured when trying to delete the vote from the database')
            return None
