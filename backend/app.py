from flask import Flask, send_from_directory, request
from flask_restful import Api
from flask_cors import CORS
from flask_jwt_extended import JWTManager,jwt_required, get_jwt_identity
from flask_caching import Cache 
from async_tasks.celery_factory import celery_init_app
from celery.result import AsyncResult
from async_tasks.tasks import daily_reminder,csv_export,monthly_report, quiz_csv_export
from celery.schedules import crontab

from datetime import timedelta,datetime
from models import db,User
from routes.authorization import LoginResource,SignupResource
from routes.Profile import UserProfile
from routes.subject import SubjectResource
from routes.chapter import ChapterResource
from routes.quiz import QuizResource
from routes.questions import QuestionResource
from routes.answers import AnswerResource
from routes.scores import ScoreResource
from routes.user_details import UserDetails
from async_tasks.cache_config import cache

app = Flask(__name__)
CORS(app, origins='*')

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///quizmaster.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'yodhsingh'
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(minutes=90)
app.config["CACHE_TYPE"] = "RedisCache"
app.config["CACHE_DEFAULT_TIMEOUT"] = 30
app.config["CACHE_REDIS_PORT"] = 6379

db.init_app(app)
cache.init_app(app)



jwt = JWTManager(app)

api = Api(app)
api.add_resource(SignupResource, '/api/signup') # Add Signup API endpoint
api.add_resource(LoginResource, '/api/login') # Add login API endpoint
api.add_resource(UserProfile, "/api/user","/api/user/<int:user_id>")
api.add_resource(UserDetails, "/api/users")
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
        monthly_report.s(),
        name='Send Monthly Report'
    )
    # Daily Reminder Task (every minute)
    sender.add_periodic_task(
        crontab(minute="*/2"),
        daily_reminder.s(),
        name='Send Daily Reminder'
    )

@app.route('/api/export_csv/<int:score_id>')
@jwt_required()
def export(score_id):
    try:
        token= get_jwt_identity()
        user= User.query.filter_by(email=token).first()
        res = csv_export.delay(score_id, user.id)
        return {
            "id": res.id,
            "result": res.result
        }
    
    except Exception as e:
        print("Error in export_csv:", str(e))
        return {"error": str(e)}, 500

@app.route('/api/export_quiz_csv/<int:quiz_id>')
@jwt_required()
def quiz_export(quiz_id):
    token= get_jwt_identity()
    try:
        user= User.query.filter_by(email=token).first()
        res = quiz_csv_export.delay(quiz_id, user.id)
        return {
            "id": res.id,
            "result": res.result
        }
    
    except Exception as e:
        print("Error in export_csv:", str(e))
        return {"error": str(e)}, 500


@app.route('/api/csv_result/<id>')
def csv_result(id):
    res= AsyncResult(id)
    # return res.result
    return send_from_directory('static',res.result)

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)

__all__ = ["app", "cache"]