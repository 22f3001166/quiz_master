from flask import Flask, request, jsonify
from flask_restful import Api, Resource, reqparse
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity,get_jwt
from datetime import timedelta, datetime, date
from werkzeug.security import generate_password_hash, check_password_hash
from models import User, db, Quiz


class UserProfile(Resource):
    @jwt_required()
    def get(self):
        identity = get_jwt_identity()
        user=User.query.filter_by(email=identity).first()
        return jsonify({
                    "id": user.id,
                    "name": user.name,
                    "email": user.email,
                    "role": user.role,
                    "dob": user.dob.strftime("%Y-%m-%d") if user.dob else None,
                    "timezone": user.timezone,
                    "active": user.active,
                    "qualification": user.qualification,
                    "scores": [score.to_dict() for score in user.scores]
            })       
         
        
    @jwt_required()
    def put(self):
        identity = get_jwt_identity()
        user=User.query.filter_by(email=identity).first()
        parser=reqparse.RequestParser()
        parser.add_argument("name",type=str,required=False)
        parser.add_argument("dob",type=str,required=False)
        parser.add_argument("qualification",type=str,required=False)
        parser.add_argument("timezone",type=str,required=False)
        args=parser.parse_args()

        if not args:
            return {"message": "Invalid request, no args provided"}, 400

        try:
            if args["name"]:
                user.name = args["name"]
            if args["dob"]:
                user.dob = datetime.strptime(args["dob"], "%Y-%m-%d").date()
            if args["qualification"]:
                user.qualification = args["qualification"]
            if args["timezone"]:
                user.timezone = args["timezone"] 
          
            db.session.commit()
            db.session.refresh(user)  # Ensure session reflects changes

            return {
                "message": "Profile updated successfully"
            }, 200

        except Exception as e:
            db.session.rollback()  # Rollback on failure
            return {"message": f"Database update failed: {str(e)}"}, 500


    @jwt_required()
    def delete(self, user_id):
        token_user = get_jwt_identity()  # Check if JWT is valid
        user_role = get_jwt().get("role")

        # Get user from database
        user = User.query.filter_by(id=user_id).first()
        if not user:
            return {"message": "User not found"}, 404
        else:
            user = User.query.filter_by(id=user_id).first()
            

        try:
            db.session.delete(user)
            db.session.commit()
            return {
                "message": "Profile deleted successfully"
            }, 204

        except Exception as e:
            db.session.rollback()  # Rollback on failure
            return {"message": f"Database update failed: {str(e)}"}, 500