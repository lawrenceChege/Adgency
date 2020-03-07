"""
    This module holds the database schema used in migrations
"""
import psycopg2
from psycopg2.extras import RealDictCursor
from flask import current_app

class DbModel():
    """
        Conncets methods to connect and perfom instructions to the database
    """

    def __init__(self):
        self.db_url = current_app.config['DATABASE_URL']

        try:
            self.conn = psycopg2.connect(self.db_url)
            self.cur = self.conn.cursor(cursor_factory=RealDictCursor)
        except (Exception, psycopg2.OperationalError) as err:
            print (err)
            print('oops! Could not connect using Url\n')
            

    def init_db(self, app):
        try:
            url =app.config['DATABASE_URL']
            self.conn = psycopg2.connect(url)
            print('connected to db using url...\n')
            self.cur = self.conn.cursor(cursor_factory=RealDictCursor)
        except (Exception, psycopg2.OperationalError) as err:
            print (err)
            print('oops! Could not connect using Url\n')
            

    def create_tables(self):
        """
            Create tables in the database
        """
        commands = (

            """
                CREATE TABLE IF NOT EXISTS companies(
                    company_id SERIAL PRIMARY KEY NOT NULL,
                    email VARCHAR(100) unique,
                    name VARCHAR(100) NOT NULL,
                    is_client BOOLEAN NOT NULL DEFAULT FALSE
                )
            """,
            """
                CREATE TABLE IF NOT EXISTS users(
                    user_id SERIAL PRIMARY KEY NOT NULL,
                    user_name CHAR(100) NOT NULL,
                    user_phone INT,
                    user_email VARCHAR(100) NOT NULL unique,
                    password VARCHAR(100),
                    created_at DATE NOT NULL,
                    active BOOLEAN NOT NULL DEFAULT FALSE,
                    is_admin BOOLEAN NOT NULL DEFAULT FALSE,
                    company_id INT REFERENCES companies (company_id)
                )
            """,
            """
                CREATE TABLE IF NOT EXISTS projects(
                    project_id SERIAL PRIMARY KEY NOT NULL,
                    name VARCHAR(100) NOT NULL,
                    company INT REFERENCES companies (company_id),
                    client INT REFERENCES companies (company_id),
                    status CHAR(10),
                    created_at DATE NOT NULL
                    
                )
            """,
            """
                CREATE TABLE IF NOT EXISTS workspaces(
                    workspace_id SERIAL PRIMARY KEY NOT NULL,
                    name VARCHAR(100) NOT NULL
                )
            """,
            """
                CREATE TABLE IF NOT EXISTS audiences(
                    audience_id SERIAL PRIMARY KEY NOT NULL,
                    age_group VARCHAR(100) NOT NULL,
                    gender VARCHAR(255),                    
                    location VARCHAR(100)
                )
            """,
            """
                CREATE TABLE IF NOT EXISTS objectives(
                    objective_id SERIAL PRIMARY KEY NOT NULL,
                    objective VARCHAR(255)
                )
            """,
            """
                CREATE TABLE IF NOT EXISTS insights(
                    insight_id SERIAL PRIMARY KEY NOT NULL,
                    insight VARCHAR(255)
                )
            """,
            """
                CREATE TABLE IF NOT EXISTS usps (
                    usp_id SERIAL PRIMARY KEY NOT NULL,
                    usp VARCHAR(255)
                )
            """,
            """
                CREATE TABLE IF NOT EXISTS platforms(
                    platform_id SERIAL PRIMARY KEY NOT NULL,
                    name VARCHAR(100), 
                    requirement VARCHAR(255)
                )
            """,
            """
                CREATE TABLE IF NOT EXISTS other_info(
                    other_info_id SERIAL PRIMARY KEY NOT NULL,
                    info VARCHAR(255)
                )
            """,
            """
                CREATE TABLE IF NOT EXISTS mandatory_info(
                    mandatory_info_id SERIAL PRIMARY KEY NOT NULL,
                    info VARCHAR(255)
                )
            """,
            """
                CREATE TABLE IF NOT EXISTS concepts(
                    concept_id SERIAL PRIMARY KEY NOT NULL,
                    name VARCHAR(100) NOT NULL unique,
                    image VARCHAR(200),
                    category VARCHAR(100),
                    overview VARCHAR(200),
                    tone VARCHAR(100),
                    style VARCHAR(100),
                    duration VARCHAR(100),
                    usp INT REFERENCES usps (usp_id),
                    insight INT REFERENCES insights (insight_id),
                    audience INT REFERENCES audiences (audience_id),
                    platform INT REFERENCES platforms (platform_id),
                    objective INT REFERENCES objectives (objective_id),
                    other_info INT REFERENCES other_info (other_info_id),
                    mandatory_info INT REFERENCES mandatory_info (mandatory_info_id),
                    project_id INT REFERENCES projects (project_id),
                    created_by INT REFERENCES users (user_id),
                    created_on VARCHAR(50) NOT NULL ,
                    modified_by INT REFERENCES users (user_id),
                    modified_on VARCHAR(50) NOT NULL
                )
            """,
            """
                CREATE TABLE IF NOT EXISTS budget(
                    budget_id SERIAL PRIMARY KEY NOT NULL,
                    budget_item VARCHAR(100) NOT NULL,
                    item_description VARCHAR(255),                    
                    start_date DATE NOT NULL,
                    end_date DATE NOT NULL,
                    item_amount numeric(15,6),
                    item_status BOOLEAN NOT NULL DEFAULT FALSE,
                    project_id INT REFERENCES projects (project_id)
                )
            """,
            """
                CREATE TABLE IF NOT EXISTS ideas(
                    idea_id SERIAL PRIMARY KEY NOT NULL,
                    idea_name VARCHAR(100) NOT NULL,
                    idea_description VARCHAR(255), 
                    image_link VARCHAR(100),                   
                    project_id INT REFERENCES projects (project_id),
                    workspace_id INT REFERENCES workspaces (workspace_id),
                    user_id INT REFERENCES users (user_id)
                )
            """,
            """
                CREATE TABLE IF NOT EXISTS comments(
                    comment_id SERIAL PRIMARY KEY NOT NULL,
                    comment_description VARCHAR(255) NOT NULL,
                    user_id INT REFERENCES users (user_id),
                    idea_id INT REFERENCES ideas (idea_id)
                )
            """,
            """
                CREATE TABLE IF NOT EXISTS votes(
                    vote_id SERIAL PRIMARY KEY NOT NULL,
                    vote_value INT NOT NULL,                 
                    user_id INT REFERENCES users (user_id),
                    idea_id INT REFERENCES ideas (idea_id)
                )
            """,
            """
                CREATE TABLE IF NOT EXISTS workspace_projects(               
                    project_id INT REFERENCES projects (project_id) ON UPDATE CASCADE,
                    workspace_id INT REFERENCES workspaces (workspace_id) ON UPDATE CASCADE ON DELETE CASCADE,
                    user_id INT REFERENCES users (user_id),
                    CONSTRAINT workspace_projects_pkey PRIMARY KEY (project_id, workspace_id)
                )
            """,
            """
                CREATE TABLE IF NOT EXISTS workspace_users(               
                    project_id INT REFERENCES projects (project_id),
                    workspace_id INT REFERENCES workspaces (workspace_id) ON UPDATE CASCADE ON DELETE CASCADE,
                    user_id INT REFERENCES users (user_id) ON UPDATE CASCADE,
                    CONSTRAINT workspace_users_pkey PRIMARY KEY (user_id, workspace_id)
                )
            """,
            """
                CREATE TABLE IF NOT EXISTS revoked_tokens(               
                    token_id SERIAL PRIMARY KEY NOT NULL,
                    token VARCHAR(120) NOT NULL
                )
            """

        )

        try:
            for command in commands:
                self.cur.execute(command)
                print('creating table ... :-)\n')
            self.commit()
            self.close()

        except (Exception, psycopg2.DatabaseError) as error:
            print (error)
            print('could not create tables :-(\n')
        finally:
            if self.conn is not None:
                self.conn.close()



    def drop_tables(self, table):
        """ drop existing tables """
        try:
            self.cur.execute("DROP TABLE IF EXISTS" + ' '+ table)
            self.commit()
        except (Exception, psycopg2.DatabaseError) as error:
            print (error)
            print('could not drop tables\n')

    def commit(self):
        """
        commit changes to the db
        """
        self.conn.commit()

    def close(self):
        """
            close the cursor and the connection
        """
        self.cur.close()
        self.conn.close()

    def findOne(self):
        """ return one item from query"""
        return self.cur.fetchone()

    def findAll(self):
        """ return all items from query"""
        return self.cur.fetchall()
        