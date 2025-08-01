from flask import jsonify,request
from flask_restful import Resource, reqparse 
from datetime import datetime
from models import Quiz,db,Subject,Question, Answer,Score, User
from flask_jwt_extended import  jwt_required, get_jwt_identity ,get_jwt

class ScoreResource(Resource):
    @jwt_required()
    def get(self, score_id=None):
        # identity= get_jwt_identity()
        if score_id:
            score = Score.query.filter_by(id=score_id).first()
            if not score:
                return {"message": "Score not found"}, 404
            return jsonify({
                "id": score.id,
                "user_id": score.user_id,
                "quiz_id": score.quiz_id,
                "timestamp": score.time_stamp_of_attempt,
                "time_taken": score.time_taken,
                "user_attempts": score.usertotal_attempts,
                "total_attempted": score.total_attempted,
                "correct_answers": score.correct_answers,
                "incorrect_answers": score.incorrect_answers,
                "total_scored": score.total_scored,
                "quiz_score": score.quiz_score,
                "percentage_score": score.percentage_score,
                "accuracy": score.accuracy,
                "grace": score.grace
            })
        user_id = request.args.get("user_id")
        if user_id:
            scores = Score.query.filter_by(user_id=user_id).all()
        else:
            scores = Score.query.all()
        return jsonify({  "scores": [{"id": score.id,
                    "user_id": score.user_id,
                    "quiz_id": score.quiz_id,
                    "timestamp": score.time_stamp_of_attempt,
                    "time_taken": score.time_taken,
                    "user_attempts": score.usertotal_attempts,
                    "total_attempted": score.total_attempted,
                    "correct_answers": score.correct_answers,
                    "incorrect_answers": score.incorrect_answers,
                    "total_scored": score.total_scored,
                    "quiz_score": score.quiz_score,
                    "percentage_score": score.percentage_score,
                    "accuracy": score.accuracy,
                    "grace": score.grace
            } 
            for score in scores]})



 
    # PUT /score/<score_id> — admin-only — to update total_scored, percentage, etc.
	# •	Admin wants to correct a wrongly calculated score
	# •	A quiz had an error and marks were adjusted
	# •	Admin gave grace marks to some students
    @jwt_required()
    def put(self,score_id=None):
        role = get_jwt().get("role")
        if role != "admin":
            return {"message": "Forbidden"}, 403
        score = Score.query.get(score_id)
        if not score:
            return {"message": "Score not found"}, 404

        parser = reqparse.RequestParser()
        parser.add_argument("grace", type=int, required=True)
        data = parser.parse_args()
        grace = data["grace"]

        total_quiz_marks = sum(q.marks for q in score.quiz.questions)
        updated_total = min(score.total_scored + grace, total_quiz_marks)
        updated_percentage = min((updated_total / total_quiz_marks) * 100, 100)
        updated_accuracy = (score.correct_answers / score.total_attempted) * 100 if score.total_attempted > 0 else 0

        score.grace = grace
        score.total_scored = updated_total
        score.percentage_score = round(updated_percentage, 2)
        score.accuracy = round(updated_accuracy, 2)

        db.session.commit()

        return {
            "message": "Grace marks applied.",
            "score_id": score.id,
            "updated_score": updated_total,
            "percentage_score": score.percentage_score,
            "accuracy": score.accuracy
        }
    # 	•	Admin needs to remove an invalid quiz attempt.
	# •	A quiz was submitted accidentally or has to be reset.
	# •	You’re testing and want to clean up test submissions.

    @jwt_required()
    def delete(self, score_id=None):
        role = get_jwt().get("role")
        if role != "admin":
            return {"message": "Forbidden: Admin access required."}, 403

        if not score_id:
            return {"message": "Score ID must be provided."}, 400

        score = Score.query.get(score_id)
        if not score:
            return {"message": "Score not found."}, 404

        try:
            db.session.delete(score)
            db.session.commit()
            return {"message": f"Score with ID {score_id} deleted successfully."}, 200
        except Exception as e:
            db.session.rollback()
            return {"message": "An error occurred while deleting the score.", "error": str(e)}, 500