from flask import Flask, request, jsonify
from flask_restful import Api, Resource, reqparse
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity,get_jwt
from datetime import timedelta, datetime, date
from werkzeug.security import generate_password_hash, check_password_hash
from models import User, db, Quiz ,Chapter, Subject
# from app import cache


class ChapterResource(Resource):
    @jwt_required()
    def get(self, chapter_id=None):
        if chapter_id:
            chapter = Chapter.query.filter_by(id=chapter_id).first()
            if not chapter:
                return {"message": "Chapter not found"}, 404
            
            return jsonify({
                "id": chapter.id,
                "name": chapter.name,
                "description": chapter.description,
                "quizes": [quiz.to_dict() for quiz in chapter.quizzes],
                "subject_id": chapter.subject_id
            })

        subject_id = request.args.get("subject_id")
        if subject_id:
            chapters = Chapter.query.filter_by(subject_id=subject_id).all()
            if not chapters:
                return {"message": "No chapters found for this subject."}, 404
            return jsonify({
                "chapters": [
                    {
                        "id": chapter.id,
                        "name": chapter.name,
                        "description": chapter.description,
                        "Quizes": [quiz.to_dict() for quiz in chapter.quizzes],
                        "subject_id": chapter.subject_id
                    }
                    for chapter in chapters
                ]
            })
        chapters = Chapter.query.all()
        if not chapters:
                return {"chaptes": []}, 200
        return jsonify({
                "chapters": [
                    {
                        "id": chapter.id,
                        "name": chapter.name,
                        "description": chapter.description,
                        "Quizes": [quiz.to_dict() for quiz in chapter.quizzes],
                        "subject_id": chapter.subject_id
                    }
                    for chapter in chapters
                ]
            })        


    @jwt_required()
    def post(self):
        user_role = get_jwt().get("role")
        if user_role != "admin":
            return {"message": "Only admin can create chapters"} ,403
        
        parser = reqparse.RequestParser()
        parser.add_argument("name",type=str,required=True,help="Title of the chapter is required.")
        parser.add_argument("description",type=str, required=False, help="description for the chapter.")
        parser.add_argument("subject_id", type=str, required=False, help="description for the chapter." )
        data = parser.parse_args() # Parse request data

        new_chapter=Chapter(name= data["name"], description=data["description"], subject_id=data["subject_id"]) # add new chapter
        db.session.add(new_chapter)
        db.session.commit()
        return { "message": "chapter created successfully.!!!!!!"},201
    
    @jwt_required()
    def put(self, chapter_id=None):
        user_role = get_jwt().get("role")
        if user_role != "admin":
            return {"message": "Only admin can update chapters"} ,403
        
        chapter= Chapter.query.filter_by(id=chapter_id).first()
        if not chapter:
            return {"message": "Chapter not found"}, 404
        
        parser = reqparse.RequestParser()
        parser.add_argument("name",type=str,required=True,help="Title of the chapter is required.")
        parser.add_argument("description",type=str,required=False,help=" description for the chapter.")
        data = parser.parse_args() # Parse request data

        if "name" in data:
            chapter.name=data["name"]

        if "description" in data:
            chapter.description = data["description"]

        db.session.commit()
        return { "message": "chapter updated successfully.!!!!!!"},201
    
    @jwt_required()
    def delete(self, chapter_id = None):
        user_role = get_jwt().get("role")
        if user_role != "admin":
            return {"message": "Only admin can delete chapters"} ,403
        chapter = Chapter.query.get(chapter_id)
        if not chapter:
            return {"message": "Chapter not found"}, 404

        db.session.delete(chapter)
        db.session.commit()
        return {"message": f"Chapter '{chapter.name}' and all its related quizzes/questions deleted."}, 200
        

