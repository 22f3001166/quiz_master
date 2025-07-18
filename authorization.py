from flask import Flask, request, jsonify
from flask_restful import Api, Resource, reqparse
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from datetime import timedelta, datetime, date
from werkzeug.security import generate_password_hash, check_password_hash
from models import User, db, Quiz

class SignupResource(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str, required=True, help='name is required')
        parser.add_argument('email', type=str, required=True, help='email is required')
        parser.add_argument('password', type=str, required=True, help='password is required')
        parser.add_argument('confirm_password', type=str, required=True, help="Confirm password is required")
        parser.add_argument('dob', type=str, required=True, help="Date of Birth")
        parser.add_argument("timezone", type=str, required=True, default="UTC", help="essential for sending timed reminder")
        parser.add_argument('role', type=str, choices=['student', 'teacher'], default='student', help='Role must be either student or teacher')
        
        args = parser.parse_args()
        # Validate Confirm Password
        if args["password"] != args["confirm_password"]:
            return {"message": "Passwords do not match!"}, 400

        # Check if user already exists
        if User.query.filter_by(email=args['email']).first():
            return {"message": "User Email already exists"}, 400

        hashed_password = generate_password_hash(args['password'])
        try:
            dob = datetime.strptime(args['dob'], "%Y-%m-%d").date()
        except ValueError:
            return {"message": "Invalid date format, expected YYYY-MM-DD"}, 400
        
        new_user = User(email=args['email'], name=args['name'], dob=dob, password=hashed_password, role=args['role'],timezone=args["timezone"])
        db.session.add(new_user)
        db.session.commit()
        return {"message": "New user created successfully"}, 201

class LoginResource(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('email', type=str, required=True, help='Email is required')
        parser.add_argument('password', type=str, required=True, help='Password is required')
        args = parser.parse_args()

        # Find user by email
        user = User.query.filter_by(email=args['email']).first()

        if not user or not check_password_hash(user.password, args['password']):
            return {"message": "Invalid email or password"}, 401

        # Generate JWT token with user role
        access_token = create_access_token(identity=user.email, additional_claims={"role": user.role})
        return {
            "message": "Login successful",
            "token": access_token,
            "user": {
                "id": user.id,
                "name": user.name,
                "email": user.email,
                "role": user.role,
                "dob": user.dob.strftime("%Y-%m-%d") if user.dob else None,
                "password": user.password,
                "timzone": user.timezone,
                "qualification": user.qualification
            }
        }, 200
    
