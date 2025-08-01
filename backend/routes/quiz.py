from flask import jsonify , request 
from flask_restful import Resource, reqparse 
from datetime import datetime
from models import Quiz,User,db,Subject
from flask_jwt_extended import  jwt_required, get_jwt_identity ,get_jwt
from celery.result import AsyncResult
from async_tasks.tasks import onetime_reminder
from async_tasks.cache_config import cache

class QuizResource(Resource):
    @jwt_required()
    @cache.memoize(timeout=180)
    def get(self,quiz_id=None):
        if quiz_id:
            quiz = Quiz.query.filter_by(id=quiz_id).first()
            return jsonify({"id": quiz_id, "title": quiz.title, "description": quiz.description, 
                            "subject": quiz.subject_id, "chapter": quiz.chapter_id, "created_on": quiz.created_on, "duration":quiz.time_duration,
                              "remarks":quiz.remarks, "questions":  [q.to_dict() for q in quiz.questions],  "subjects":[quiz.subject.to_dict()]})
        
        chapter_id = request.args.get("chapter_id")
        subject_id = request.args.get("subject_id")
        if chapter_id:
            quizes = Quiz.query.filter_by(chapter_id=chapter_id).all()
        elif subject_id:
            quizes = Quiz.query.filter_by(subject_id=subject_id).all()
        else:
            quizes = Quiz.query.all()
        if not quizes:
            return {"quizzes": []}, 200
        return jsonify({ "quizzes": [{"id": quiz.id,"title": quiz.title,"description": quiz.description,
                            "subject_id": quiz.subject_id, "chapter_id": quiz.chapter_id, "created_on": quiz.created_on,
                            "duration":quiz.time_duration, "remarks":quiz.remarks, "subject":[quiz.subject.to_dict()],
                            "questions":  [q.to_dict() for q in quiz.questions] }
                            for quiz in quizes]}) 
            
             

    @jwt_required()
    def post(self):
        token=get_jwt_identity()
        user=User.query.filter_by(email=token).first()
        user_role = get_jwt().get("role")
        if user_role != "admin":
            return {"message": "Only admin can create quizzes"}, 403
        
        parser = reqparse.RequestParser()
        parser.add_argument("title",type=str,required=True,help="Title of the quiz is required.")
        parser.add_argument("description",type=str,required=False,help="Optional description for the quiz.")
        parser.add_argument("duration",type=int,required=True,help="Time duration is required.")
        parser.add_argument("remarks",type=str,required=True,help="Time duration is required.")
        parser.add_argument("chapter_id", type=int, required=True, help="Chapter ID is required.")
        parser.add_argument("subject_id", type=int, required=True, help="Subject ID is required.")
        data = parser.parse_args()         # Parse request data

        new_quiz = Quiz(title=data["title"],description=data["description"],time_duration=data["duration"],
                        remarks=data["remarks"],chapter_id=data["chapter_id"],subject_id=data["subject_id"])
        
        db.session.add(new_quiz)
        db.session.commit()
        cache.clear()  # Clear cache to reflect newly added quiz
        subject=Subject.query.get(new_quiz.subject_id)
        res= onetime_reminder.delay("All",new_quiz.title,subject.name)
        return {
            "message": "Quiz created successfully",
            "quiz": {
                "id": new_quiz.id,
                "title": new_quiz.title,
                "description": new_quiz.description,
                "created_on": new_quiz.created_on.strftime("%Y-%m-%d %H:%M:%S"),
                "duration": new_quiz.time_duration
            }
        }, 201

    @jwt_required()    
    def put(self, quiz_id=None):
        user_role = get_jwt().get("role")
        if user_role != "admin":
            return {"message": "You do not have permission to update this quiz"}, 403
        
        quiz = Quiz.query.filter_by(id=quiz_id).first()
        if not quiz:
            return {"message": "Quiz not found"}, 404        
        
        parser = reqparse.RequestParser()
        parser.add_argument("title",type=str,required=True,help="Title of the quiz is required.")
        parser.add_argument("description",type=str,required=True,help="description for the quiz.")
        parser.add_argument("duration",type=int,required=True,help="Time duration is required.")
        parser.add_argument("remarks",type=str,required=True,help="Remarks is required.")
        data = parser.parse_args()

        if "title" in data:
            quiz.title = data["title"]
        if "description" in data:
            quiz.description = data["description"]
        if "duration" in data:
            quiz.time_duration = data["duration"]
        if "remarks" in data:
            quiz.remarks = data ["remarks"]

        db.session.commit()
        cache.clear()

        return {"message": "Quiz updated successfully", "quiz": {
            "id": quiz.id,
            "title": quiz.title,
            "description": quiz.description,
            "created_on": quiz.created_on.strftime("%Y-%m-%d %H:%M:%S"),
            "duration": quiz.time_duration
        }}, 203
     
    @jwt_required()    
    def delete(self, quiz_id):
        user_role = get_jwt().get("role")
        if user_role != "admin":
            return {"message": "Only admin can delete quizzes"}, 403

        quiz = Quiz.query.get(quiz_id)
        if not quiz:
            return {"message": "Quiz not found"}, 404 
        db.session.delete(quiz)
        db.session.commit()
        cache.clear()  # Clear cache to remove deleted quiz
        return {"message": "Quiz Deleted Succcesfully"}