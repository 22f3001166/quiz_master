from flask import  jsonify
from flask_restful import Resource
from flask_jwt_extended import jwt_required,get_jwt
from models import User, Score



