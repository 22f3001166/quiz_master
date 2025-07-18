from flask import Flask, request, jsonify
from flask_restful import Api, Resource, reqparse
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity,get_jwt
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, Quiz, Subject




class SubjectResource(Resource):
    @jwt_required()
    def get(self, subject_id=None):
        if not subject_id:
            subjects = Subject.query.all()
            return jsonify({
                "subjects": [{"id":sub.id , "name": sub.name, "description": sub.description, "quizzes": [q.to_dict() for q in sub.quizzes] } for sub in subjects]
            })
        else:
            sub=Subject.query.get(subject_id)
            return jsonify({"id":sub.id , "name": sub.name, "description": sub.description, "quizzes": [q.to_dict() for q in sub.quizzes]})


    @jwt_required()
    def post(self):
        user_role = get_jwt().get("role")
        if user_role != "admin":
            return {"message": "Only admin can add subjects"}, 404
        
        api = reqparse.RequestParser()
        api.add_argument("name", type=str, required=True, help="subject name is required")
        api.add_argument("description", type=str, required=False, help="subject name is not required")
        data= api.parse_args()
        if not data["name"]:
            return jsonify({"error": "Subject name is required"}), 400

        existing = Subject.query.filter_by(name=data["name"]).first()
        if existing:
            return jsonify({"error": "Subject with same name already existing"}), 400

        new_subject = Subject(name=data["name"], description=data["description"])

        db.session.add(new_subject)
        db.session.commit()
        return { "message": "New Subject created successfully" }, 201

    @jwt_required()
    def put(self, subject_id=None):
        user_role = get_jwt().get("role") # Only allow the admin who created the quiz to edit it
        if user_role != "admin":
            return {"message": "Only admin can edit subjects"}, 404
        
        subject= Subject.query.filter_by(id=subject_id).first()
        if not subject:
            return {"message": "No subject Found"}, 404
        
        api = reqparse.RequestParser()
        api.add_argument("name", type=str, required=True, help="subject name is required")
        api.add_argument("description", type=str, required=False, help="subject name is not required")
        data= api.parse_args()

        if "name" in data:
            subject.name = data["name"]
        if "description" in data:
            subject.description = data["description"]

        db.session.commit()
        return { "message": "Subject updated successfully" }, 200
    
    @jwt_required()
    def delete(self, subject_id=None):
        user_role = get_jwt().get("role") # Only allow the admin who created the quiz to edit it
        if user_role != "admin":
            return {"message": "Only admin can delete subject"}, 404

        subject= Subject.query.filter_by(id=subject_id).first()
        if not subject:
            return {"message": "No subjet Found"}, 404
        
        db.session.delete(subject)
        db.session.commit()

        return { "message": "Subject deleted successfully" }, 200 
        

