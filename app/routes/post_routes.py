from flask import request
from app.controllers import post_controller


def post_route(app):
    @app.post("/posts")
    def create_post():

        data = request.get_json()
        

        return post_controller.add_post(data)
    
    @app.delete('/posts/<int:id>')
    def delete_post(id):
        return post_controller.post_delete(id)

    
    @app.get("/post/<int:id>")
    def read_post_by_id(id):

        return post_controller.get_post_by_id(id) 
    
    @app.get("/posts")
    def read_posts():
        return post_controller.retrieve()

    @app.patch("/posts/<int:id>")
    def update_post(id):

        payload = request.get_json()

        return post_controller.post_update(id, payload)
         