from flask_app.config.mysqlconnection import connectToMySQL
# from flask_app.models import post
from flask import flash
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class User:
    db = "wall_schema"

    def __init__(self,data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']


    @classmethod
    def create(cls,data):
        query = """
        INSERT INTO users (first_name, last_name, email, password, created_at, updated_at )
        VALUES 
        (%(first_name)s, %(last_name)s, %(email)s, %(password)s , NOW() , NOW());
        """
        result = connectToMySQL(cls.db).query_db(query,data)
        print(result)
        return result
    
    @classmethod
    def get_all(cls):
        query = "SELECT * FROM users;"
        result = connectToMySQL(cls.db).query_db(query)
        all_users = []
        for row in result:
            all_users.append(cls(row))
        print(all_users)
        return all_users
    
    @classmethod
    def get_by_email(cls,data):
        query = "SELECT * FROM users WHERE email =%(email)s;"
        result = connectToMySQL(cls.db).query_db(query,data)
        if len(result) < 1:
            return False
        this_user = cls(result[0])
        return this_user

    @classmethod
    def get_by_id(cls,data):
        query = "SELECT * FROM users WHERE id =%(id)s;"
        result = connectToMySQL(cls.db).query_db(query,data)
        if len(result) < 1:
            return False
        this_user = cls(result[0])
        return this_user

#class method to show individual dojo to the database
#return instance of the dojo object of the row number(ID)
    # @classmethod
    # def get_with_posts(cls,data):
    #     query="""
    #     SELECT * FROM users 
    #     LEFT JOIN posts ON 
    #     users.id = posts.user_id 
    #     WHERE users.id =%(id)s;
    #     """
    #     results = connectToMySQL('wall_schema').query_db(query,data)
    #     print(results)
    #     user_with_posts = cls (results[0])
    #     print(user_with_posts)
    #     for row in results:
    #         post_data ={
    #             "id" : row['posts.id'],
    #             "message" : row['message'],
    #             "created_at" : row['posts.created_at'],
    #             "updated_at" : row['posts.updated_at']
    #         }
    #         user_with_posts.posts.append (Post( post_data))
    #     return user_with_posts

    # @classmethod
    # def delete(cls,data):
    #     query = "DELETE FROM users WHERE id = %(id)s;"
    #     return connectToMySQL(cls.db).query_db(query,data)


    @staticmethod
    def validate_register( user ):
        is_valid = True
        query = "SELECT * FROM users WHERE email = %(email)s;"
        result = connectToMySQL(User.db).query_db(query,user)
        if len(result) >=1:
            flash("Email already taken.","register")
            is_valid = False
        # test whether a field matches the pattern
        if not EMAIL_REGEX.match(user['email']):
            flash("Invalid Email","register") 
            is_valid = False
        if len(user['first_name']) < 2:
            flash("First name must be at least 2 characters.","register")
            is_valid = False
        if len(user['last_name']) < 2:
            flash("Last name must be at least 2 characters.","register")
            is_valid = False
        if len(user['password']) < 8:
            flash("Password must be at least 8 characters.","register")
            is_valid = False
        if not (user['password']) == (user['confirm_pass']):
            flash("Passwords don't match","register")
            is_valid = False
        return is_valid