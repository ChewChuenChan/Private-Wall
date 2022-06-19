from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from datetime import datetime
import math
# import re

class Post:
    db = "wall_schema"

    def __init__(self,data):
        self.id = data['id']
        self.message = data['message']
        self.receiver_id = data['receiver_id']
        self.receiver = data['receiver']
        self.sender_id = data['sender_id']
        self.sender = data['sender']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def create_post(cls,data):
        query ="""
        INSERT INTO posts (message, receiver_id, sender_id, created_at, updated_at )
        VALUES 
        (%(message)s, %(receiver_id)s, %(sender_id)s, NOW() , NOW());"""
        result = connectToMySQL(cls.db).query_db(query,data)
        print(result)
        return result
    
    @classmethod
    def get_user_post(cls,data):
        query = """
        SELECT users.first_name as sender, users2.first_name as receiver, posts.*
        FROM users 
        LEFT JOIN posts 
        ON users.id = posts.sender_id
        LEFT JOIN users as users2
        on users2.id = posts.receiver_id
        where users2.id = %(id)s
        ORDER BY sender;
        """
        result = connectToMySQL(cls.db).query_db(query,data)
        print(result)
        all_post = []
        for row in result:
            all_post.append(cls(row))
        return all_post
    
    @classmethod
    def delete_post(cls,data):
        query = "DELETE FROM posts WHERE id = %(id)s;"
        return connectToMySQL(cls.db).query_db(query,data)

    @staticmethod
    def validate_post( post ):
        is_valid = True
        if len(post['message']) < 5:
            flash("Message must be at 5 characters","post")
            is_valid = False
        return is_valid

    def time_spend(self):
        now= datetime.now()
        print(now.strftime("%H:%M:%S"))
        timedelta = now - self.created_at
        print(type(timedelta),timedelta)
        print(timedelta.days)
        print(timedelta.total_seconds())
        if timedelta.days > 0:
            return f"{timedelta.days} days ago"
        elif (math.floor(timedelta.total_seconds()/60)) >=60:
            return f"{math.floor(math.floor(timedelta.total_seconds()/60)/60)} hours ago"
        elif timedelta.total_seconds() >= 60:
            return f"{math.floor(timedelta.total_seconds()/60)} minutes ago"
        else:
            return f"{math.floor(timedelta.total_seconds())} seconds ago"