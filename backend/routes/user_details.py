from flask import  jsonify
from flask_restful import Resource
from flask_jwt_extended import jwt_required,get_jwt
from models import User
from async_tasks.cache_config import cache


class UserDetails(Resource):
    @jwt_required()
    @cache.memoize(timeout=100)
    def get(self):
        user_role = get_jwt().get('role')
        if user_role != "admin":
            return {"message": "Only admin can fetch all user details"}
        users=User.query.all()
        return jsonify({
            "users": [ user.to_dict() for user in users] 
            })       
