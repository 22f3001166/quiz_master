from flask import Flask, request, jsonify
from flask_restful import Api, Resource, reqparse
from flask_cors import CORS
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from datetime import timedelta, datetime
from werkzeug.security import generate_password_hash, check_password_hash
from models import User, db, Quiz
from quiz import QuizResource
from questions import QuestionResource
from Profile import UserProfile
from subject import SubjectResource
from chapter import ChapterResource
# from flask_caching import Cache
from authorization import LoginResource,SignupResource

app = Flask(__name__)
CORS(app, origins='*')

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///quizmaster.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'yodhsingh'

db.init_app(app)
jwt = JWTManager(app)
api = Api(app)
# cache= Cache(app) # cache init
# app.cache = cache


api.add_resource(SignupResource, '/api/signup') # Add Signup API endpoint
api.add_resource(LoginResource, '/api/login') # Add login API endpoint
api.add_resource(UserProfile, "/api/users","/api/user/<int:user_id>")
api.add_resource(SubjectResource, "/api/subjects", "/api/subject/<int:subject_id>")
api.add_resource(ChapterResource, "/api/chapters", "/api/chapter/<int:chapter_id>")
api.add_resource(QuizResource, "/api/quizzes","/api/quiz/<int:quiz_id>")
api.add_resource(QuestionResource, "/api/questions", "/api/question/<int:quiz_id>", "/api/question/<int:quiz_id>/<int:ques_id>")

class ApproveQuizResource(Resource):
    @jwt_required()
    def put(self, quiz_id):
        identity = get_jwt_identity()
        admin = User.query.filter_by(email=identity["email"]).first()

        if admin.role != "admin":
            return {"message": "Only admins can approve quizzes"}, 403

        quiz = Quiz.query.get(quiz_id)
        if not quiz:
            return {"message": "Quiz not found"}, 404

        quiz.status = "approved"
        db.session.commit()
        return {"message": f"Quiz '{quiz.title}' approved"}, 200


api.add_resource(ApproveQuizResource, "/api/admin/approve-quiz/<int:quiz_id>")

class AvailableQuizzesResource(Resource):
    @jwt_required()
    def get(self):
        identity = get_jwt_identity()
        student = User.query.filter_by(email=identity["email"]).first()

        if student.role != "student":
            return {"message": "Only students can access this resource"}, 403

        approved_quizzes = Quiz.query.filter_by(status="approved").all()
        quizzes_list = [{"id": q.id, "title": q.title, "description": q.description} for q in approved_quizzes]

        return {"quizzes": quizzes_list}, 200


api.add_resource(AvailableQuizzesResource, "/api/student/quizzes")

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)