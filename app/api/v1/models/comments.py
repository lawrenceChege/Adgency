"""
    This module handles the models for comments
"""
import time
import psycopg2
from flask import request
from flask_jwt_extended import get_jwt_identity
from migrations import DbModel


class CommentsModel(DbModel):
    """
        This class handles data manipulation for the comments view
    """
    #TODO implement with an object or kwargs

    def __init__(self):
        """
            Initialize the comment class and import 
        """

        super().__init__()
        self.created_on = time.strftime('%a, %d %b %Y, %I:%M:%S %p')
        self.modified_on = time.strftime('%a, %d %b %Y, %I:%M:%S %p')
        self.created_by = get_jwt_identity()
        self.modified_by = get_jwt_identity()

    def find_comment_by_name(self, name):
        """
            Fetch a comment from database using its name
        """
        try:
            self.cur.execute(
                "SELECT * FROM comments WHERE description=%s", (name,)
            )
            return self.findOne()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
            print("An error occured whenretrieving comment using name")
            return None

    def find_comment_by_id(self, comment_id):
        """
            Fetch a comment from database using its id
        """
        try:
            self.cur.execute(
                "SELECT * FROM comments WHERE comment_id=%s", (comment_id,)
            )
            return self.findOne()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
            print("An error occured when retrieving comment using id")
            return None

    def get_all_comments(self):
        """
            This method returns all the saved comments
        """
        try:
            self.cur.execute(
                "SELECT * FROM comments"
            )
            return self.findAll()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
            print("An error occured when retrieving all comments")
            return None


    def save_comment_to_database(self, **data):
        """
            Save the comment to the database
        """
        self.description = data["description"] 
        try:
            data = (self.description, self.created_on, self.modified_on,
                    self.created_by, self.modified_by)

            self.cur.execute(
                """
                    INSERT INTO comments (description,created_on, modified_on, created_by,modified_by)
                    VALUES(%s, %s, %s, %s, %s);
                """, data
            )
            self.commit()
            return True
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
            print('An error occured when trying to save the comment to the database')
            return None

#TODO implement without parameters

    def edit_comment(self, comment_id, **data):
        """
            This method can modify one or all the fields of a comment
            
        """
        
        self.description = data["description"]

        try:
            data = (self.description,self.modified_by, self.modified_on,comment_id,)
            self.cur.execute(
                """
                UPDATE comments
                SET
                description = %s
                WHERE comment_id = %s;
                """,data
            )
            self.commit()
            return True
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
            print('An error occured when trying to edit the comment in the database')
            return None

    def delete_comment(self, comment_id):
        """
            This method removes an comment by id from the database.
        """
        try:
            self.cur.execute(
                "DELETE FROM comments WHERE comment_id=%s", (comment_id,)
            )
            self.commit()
            return True
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
            print('An error occured when trying to delete the comment from the database')
            return None
