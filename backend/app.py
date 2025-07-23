from flask import Flask, send_from_directory, request
from flask_restful import Api
from flask_cors import CORS
from flask_jwt_extended import JWTManager,jwt_required, get_jwt_identity
from flask_caching import Cache 
from async_tasks.celery_factory import celery_init_app
from celery.result import AsyncResult
from async_tasks.tasks import daily_reminder,csv_export,monthly_report
from celery.schedules import crontab

from datetime import timedelta
from models import db,User
from resources.authorization import LoginResource,SignupResource
from resources.Profile import UserProfile
from resources.subject import SubjectResource
from resources.chapter import ChapterResource
from resources.quiz import QuizResource
from resources.questions import QuestionResource
from resources.answers import AnswerResource
from resources.scores import ScoreResource


app = Flask(__name__)
CORS(app, origins='*')

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///quizmaster.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'yodhsingh'
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(minutes=90)

app.config["CACHE_TYPE"] = "RedisCache"
app.config["CACHE_DEFAULT_TIMEOUT"] = 90
app.config["CACHE_REDIS_PORT"] = 6379

db.init_app(app)
# cache= Cache(app) # cache init
# app.cache = cache


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


celery=celery_init_app(app)
celery.autodiscover_tasks() 

@celery.on_after_finalize.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(
        crontab(minute="*/2"),
        monthly_report.s()
    )

@app.route('/api/export_csv/<int:quiz_id>')
@jwt_required()
def export(quiz_id):
    try:
        token= get_jwt_identity()
        user= User.query.filter_by(email=token).first()
        res = csv_export.delay(quiz_id, user.id)
        return {
            "id": res.id,
            "result": res.result
        }
    
    except Exception as e:
        print("Error in export_csv:", str(e))
        return {"error": str(e)}, 500

@app.route('/api/csv_result/<id>')
# @jwt_required()
def csv_result(id):
    res= AsyncResult(id)
    return send_from_directory('static',res.result)


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
     
    app.run(debug=True)
    
