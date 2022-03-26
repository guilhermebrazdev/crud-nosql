from http import HTTPStatus
from flask import jsonify

from app.exceptions import IdNotFound, IncompatibleKeys
from app.models import Post


def retrieve():
    all_posts = Post.get_all_post()

    for post in all_posts:
        Post.serialize_post(post)
        
    
    return jsonify(all_posts), HTTPStatus.OK

def add_post(data):

    try:
        Post.new_post(data)
    
        data.update({'_id': str(data['_id'])})

        return data, HTTPStatus.CREATED
    
    except IncompatibleKeys:
        return {'error': 'Incompatible Keys'}, HTTPStatus.BAD_REQUEST


def get_post_by_id(id):

    try:
        post_by_id = Post.get_by_id(id)
        return post_by_id, HTTPStatus.OK

    except IdNotFound:
        return {'error': f'id {id} not found'}, HTTPStatus.NOT_FOUND

    
def post_update(id, payload):

    try:
        updated_post = Post.att_post(id, payload)
        Post.serialize_post(updated_post)
        
        return updated_post, HTTPStatus.OK

    except IdNotFound:
        return {'error': f'id {id} not found'}, HTTPStatus.NOT_FOUND
        
    except IncompatibleKeys:
        return {'error': 'Incompatible Keys'}, HTTPStatus.BAD_REQUEST


def post_delete(id):
    try:
        deleted_post = Post.delete(id)
        Post.serialize_post(deleted_post)

        return deleted_post, HTTPStatus.OK

    except IdNotFound:
        return {'error': f'id {id} not found'}, HTTPStatus.NOT_FOUND


