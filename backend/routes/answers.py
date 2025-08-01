from flask import jsonify, request
from flask_restful import Resource, reqparse 
from datetime import datetime
from models import Quiz,db,Subject,Question, Answer,Score,User
from flask_jwt_extended import  jwt_required, get_jwt_identity ,get_jwt

class AnswerResource(Resource):
    @jwt_required()
    def get(self, ans_id=None):
        token = get_jwt_identity()
        user = User.query.filter_by(email=token).first()
        if not user:
            return {"message": "User not found"}, 404
        user_id = user.id
        quiz_id = request.args.get("quiz_id")
        if quiz_id is None:
            return {"message": "quiz_id is required as query parameter"}, 400
        
        if ans_id:
            ans = Answer.query.get(ans_id)
            if not ans:
                return {"message": "Answer not found"}, 404
            if ans.user_id != user_id:
                return {"message": "You are not authorized to see this record."}, 403

            submitted = Score.query.filter_by(user_id=user_id, quiz_id=ans.quiz_id).first()
            return {
                "id": ans.id,
                "quiz_id": ans.quiz_id,
                "question_id": ans.question_id,
                "selected_answer": ans.selected_answer,
                "is_correct": ans.is_correct if submitted else None
            }

        my_answers = Answer.query.filter_by(user_id=user_id, quiz_id=quiz_id).all()
        submitted = Score.query.filter_by(user_id=user_id, quiz_id=quiz_id).first()
        return jsonify([{
            "id": ans.id,
            "quiz_id": ans.quiz_id,
            "question_id": ans.question_id,
            "selected_answer": ans.selected_answer,
            "is_correct": ans.is_correct if submitted else None }
              for ans in my_answers]) 

        

    @jwt_required()
    def post(self):
        data = request.get_json()

        quiz_id = data.get('quiz_id')
        answers = data.get('answers', [])
        time_taken = data.get('time_taken')
        user_email = get_jwt_identity()

        user = User.query.filter_by(email=user_email).first()
        if not user:
            return jsonify({'message': 'User not found'}), 404

        if not quiz_id or not answers or time_taken is None:
            return jsonify({'message': 'Missing required fields'}), 400
            
        try:
            total_attempted = len(answers)
            correct = 0
            total_scored = 0
            quizscore = 0

            all_questions = Question.query.filter_by(quiz_id=quiz_id).all()
            for q in all_questions:
                quizscore += q.marks

            for ans in answers:
                q = Question.query.get(ans['question_id'])
                if q and q.correct_answer == ans['selected_answer']:
                    correct += 1
                    total_scored += q.marks

            incorrect = total_attempted - correct
            percentage = (total_scored / quizscore) * 100 if quizscore > 0 else 0
            accuracy = (correct / total_attempted) * 100 if total_attempted > 0 else 0
            previous_attempts = Score.query.filter_by(user_id=user.id, quiz_id=quiz_id).count()
            user_total_attempts = previous_attempts + 1
            score_record = Score(
                quiz_id=quiz_id,
                user_id=user.id,
                time_stamp_of_attempt=datetime.now(),
                time_taken=int(time_taken),
                total_attempted=total_attempted,
                correct_answers=correct,
                incorrect_answers=incorrect,
                usertotal_attempts=user_total_attempts,
                total_scored=total_scored,
                quiz_score=quizscore,
                percentage_score=percentage,
                accuracy=accuracy
            )
            db.session.add(score_record)
            db.session.flush()  # to get score_record.id

            for ans in answers:
                q = Question.query.get(ans['question_id'])
                isright = q.correct_answer == ans['selected_answer']
                answer = Answer(
                    quiz_id=quiz_id,
                    question_id=int(ans['question_id']),
                    selected_answer=ans['selected_answer'],
                    user_id=user.id,
                    is_correct=isright,
                    score_id=score_record.id
                )
                db.session.add(answer)

            db.session.commit()
            return {
                'message': 'Submission recorded successfully',
                'score_id': score_record.id 
            }, 201
        

        except Exception as e:
            db.session.rollback()
            return {"message": "Submission failed", "error": str(e)}, 500
        
    # @jwt_required()
    # def put(self, ans_id=None):
    #     user_id= get_jwt_identity() 
    #     parser=reqparse.RequestParser()
    #     parser.add_argument("selected_answer", type=str, required=True)
    #     parser.add_argument("quiz_id", type=int, required=True)
    #     parser.add_argument("question_id", type=int, required=True)
    #     data=parser.parse_args()
        
    #     try:
    #         ans=Answer.query.get(ans_id)
    #         if ans.user_id != user_id: # verify user
    #              return {"message":"Only user who attempt can edit this question"}
    #         if "selected_answer" in data:
    #             ans.selected_answer=data["selected_answer"]
    #         db.session.commit()

    #     except Exception as e:
    #                 return {"message": f"Answer updating failed: {str(e)}"}, 500
        
    @jwt_required()
    def delete(self, ans_id):
        user_id = get_jwt_identity()
        answer = Answer.query.get(ans_id)

        if not answer:
            return {"message": "Answer not found"}, 404

        if answer.user_id != user_id:
            return {"message": "You are not authorized to delete this answer."}, 403

        # Prevent deletion if quiz has already been submitted
        submitted = Score.query.filter_by(user_id=user_id, quiz_id=answer.quiz_id).first()
        if submitted:
            return {"message": "Cannot delete answer after quiz submission."}, 403

        # Clear the selected answer and correctness
        answer.selected_answer = None
        answer.is_correct = False

        db.session.commit()
        return {"message": "Selected answer removed successfully."}, 200