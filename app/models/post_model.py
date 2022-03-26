from os import getenv
import pymongo
from pymongo import ReturnDocument
from datetime import datetime as dt

from app.exceptions import IdNotFound, IncompatibleKeys

HOST_DOOR = getenv("HOST_DOOR")
DB_NAME = getenv("DB_NAME")

client = pymongo.MongoClient(HOST_DOOR)
db = client[DB_NAME]

class Post:
    def __init__(self, **post):
        self.title = post['title']
        self.author = post['author']
        self.tags = post['tags']
        self.content = post['content']
        self.created_at = dt.utcnow()
        self.updated_at = dt.utcnow()

    @staticmethod
    def serialize_post(post):
        
        post.update({'_id': str(post['_id'])})

    @staticmethod
    def get_all_post():
        db_posts = db.posts.find() 
        db_posts= list(db_posts)
        


        return db_posts

    @staticmethod
    def get_by_id(id):
        all_posts = Post.get_all_post()

        for post in all_posts:
            Post.serialize_post(post)
    
        for post in all_posts:
            if post['id'] == id:
                return post
        
        raise IdNotFound

    
    def id_creator(data):
        all_posts = Post.get_all_post()

        if len(all_posts) == 0 :

            data['id'] = 1
        else:
            last_post = all_posts[len(all_posts) - 1]
            last_id = last_post['id']

            data['id'] = last_id + 1

    @staticmethod
    def new_post(data):
        data_keys = data.keys()
        default_keys = [ 'author', 'tags', 'title', 'content']

        if set(data_keys) != set(default_keys):
            raise IncompatibleKeys

        Post.id_creator(data)
        
        db.posts.insert_one(data)
    
    @staticmethod
    def att_post(id, payload):
        default_keys = [ 'author', 'tags', 'title', 'content']
        data_keys = payload.keys()

        for key in list(data_keys):
            if key not in default_keys:
                raise IncompatibleKeys
        

        updated_post = db.posts.find_one_and_update({"id": id}, {"$set": payload}, return_document=ReturnDocument.AFTER)

        if not updated_post:
            raise IdNotFound

        updated_post['updated_at'] = dt.utcnow()

        return updated_post

    @staticmethod
    def delete(id):
        deleted_post = db.posts.find_one_and_delete({'id': id})

        if not deleted_post:
            raise IdNotFound
        
        return deleted_post
    
  

