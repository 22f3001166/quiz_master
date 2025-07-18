from flask import Flask
from flask_restful import Api
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_caching import Cache 
# from .celery_config import celery_init_app
from flask_caching import Cache

from models import db
from authorization import LoginResource,SignupResource
from Profile import UserProfile
from subject import SubjectResource
from chapter import ChapterResource
from quiz import QuizResource
from questions import QuestionResource
from answers import AnswerResource
from scores import ScoreResource
from datetime import timedelta




app = Flask(__name__)
CORS(app, origins='*')

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///quizmaster.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'yodhsingh'
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(minutes=30)

app.config["CACHE_TYPE"] = "RedisCache"
app.config["CACHE_DEFAULT_TIMEOUT"] = 90
app.config["CACHE_REDIS_PORT"] = 6379

db.init_app(app)
cache= Cache(app) # cache init
app.cache = cache

# celery=celery_init_app(app)

jwt = JWTManager(app)
api = Api(app)
api.add_resource(SignupResource, '/api/signup') # Add Signup API endpoint
api.add_resource(LoginResource, '/api/login') # Add login API endpoint
api.add_resource(UserProfile, "/api/user","/api/user/<int:user_id>")
api.add_resource(SubjectResource, "/api/subject", "/api/subject/<int:subject_id>")
api.add_resource(ChapterResource, "/api/chapter", "/api/chapter/<int:chapter_id>")
api.add_resource(QuizResource, "/api/quiz","/api/quiz/<int:quiz_id>")
api.add_resource(QuestionResource, "/api/question", "/api/question/<int:question_id>")
api.add_resource(AnswerResource, "/api/answer", "/api/answer/<int:ans_id>")
api.add_resource(ScoreResource, "/api/score", "/api/score/<int:score_id>")



if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)