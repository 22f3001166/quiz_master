from flask import jsonify, request
from flask_restful import Resource, reqparse 
from datetime import datetime
from models import Quiz,db,Subject,Question
from flask_jwt_extended import  jwt_required, get_jwt_identity ,get_jwt

class QuestionResource(Resource):
    @jwt_required()
    def get(self, question_id=None):
        if question_id:
            ques = Question.query.filter_by(id= question_id).all() 
            return jsonify({
                "id": ques.id,
                "Statement": ques.Statement,
                "option_a": ques.option_a,
                "option_b": ques.option_b,
                "option_c": ques.option_c,
                "option_d": ques.option_d,
                "answer": ques.correct_answer,
                "marks": ques.marks
            })

        quiz_id = request.args.get("quiz_id")
        if not quiz_id:
            return {"message": "quiz_id is required to fetch quiz questions."}, 400
        questions= Question.query.filter_by(quiz_id=quiz_id).all()
        if not questions:
            return {"questions": []},200
        
        return jsonify({
            "questions": [{
                "id": ques.id,
                "Statement": ques.statement,
                "option_a": ques.option_a,
                "option_b": ques.option_b,
                "option_c": ques.option_c,
                "option_d": ques.option_d,
                "answer": ques.correct_answer,
                "marks": ques.marks
            } for ques in questions]
        })    
    @jwt_required()
    def post(self):
        user_role = get_jwt().get("role")
        if user_role != "admin":
            return {"message": "You do not have permission to create a question"}, 403

        try:
            data = request.get_json()
            questions = data.get("questions", [])
            if not questions:
                parser=reqparse.RequestParser()
                parser.add_argument("Statement", type=str, required=True)
                parser.add_argument("option_a", type=str, required=True)
                parser.add_argument("option_b", type=str, required=True)
                parser.add_argument("option_c", type=str, required=True)
                parser.add_argument("option_d", type=str, required=True)
                parser.add_argument("answer", type=str, required=True)
                parser.add_argument("marks", type=int, required=True, default=1)
                parser.add_argument("quiz_id", type=int, required=True)
                parser.add_argument("subject_id", type=int, required=True)
                data=parser.parse_args()
                newq= Question(statement=data["Statement"],
                            option_a=data["option_a"],
                            option_b=data["option_b"],
                            option_c=data["option_c"],
                            option_d=data["option_d"], 
                            correct_answer=data["answer"],
                            marks=data["marks"],
                            quiz_id=data["quiz_id"],
                            subject_id=data["subject_id"]
                            )
                try:
                    db.session.add(newq)
                    db.session.commit()

                    return {
                        "message":"Question created successfully",
                        "question": {
                            "id": newq.id,
                            "quiz_id" : newq.quiz_id,
                            "subject" : newq.subject_id,
                            "statement" : newq.statement,
                            "option_a" : newq.option_a,
                            "option_b" : newq.option_b,
                            "option_c" : newq.option_c,
                            "option_d" : newq.option_d,
                            "marks": newq.marks,
                            "answer" : newq.correct_answer,
                        }
                    }, 201
                
                except Exception as e:
                    return {"message": f"Question appending failed: {str(e)}"}, 500


            if not isinstance(questions, list):
                return {"message": "Invalid or empty questions list"}, 400
            
            created = []
            for q in questions:
                newq = Question(
                    statement=q["Statement"],
                    option_a=q["option_a"],
                    option_b=q["option_b"],
                    option_c=q["option_c"],
                    option_d=q["option_d"],
                    correct_answer=q["answer"],
                    marks=q.get("marks", 1),
                    quiz_id=q["quiz_id"],
                    subject_id=q["subject_id"]
                )
                db.session.add(newq)
                created.append(newq)

            db.session.commit()

            return {
                "message": f"{len(created)} questions created successfully",
                "created_questions": [
                    {
                        "id": q.id,
                        "statement": q.statement,
                        "quiz_id": q.quiz_id,
                        "subject_id": q.subject_id,
                        "marks": q.marks,
                        "answer": q.correct_answer,
                    } for q in created
                ]
            }, 201

        except Exception as e:
            return {"message": f"Bulk creation failed: {str(e)}"}, 500
            
    # @jwt_required()
    # def post(self):
    #     user_role = get_jwt().get("role")
    #     if user_role != "admin":
    #         return {"message": "You do not have permission to create a question"}, 403
        

        
    @jwt_required()    
    def put(self, question_id=None):
        user_role = get_jwt().get("role")
        if user_role != "admin":
            return {"message": "You do not have permission to update this quiz"}, 403    
        
        parser = reqparse.RequestParser()
        parser.add_argument("Statement", type=str, required=True)
        parser.add_argument("option_a", type=str, required=True)
        parser.add_argument("option_b", type=str, required=True)
        parser.add_argument("option_c", type=str, required=True)
        parser.add_argument("option_d", type=str, required=True)
        parser.add_argument("answer", type=str, required=True)
        parser.add_argument("marks", type=int, required=True)
        data=parser.parse_args()

        try:
            ques=Question.query.get(question_id)

            if "Statement" in data:
                ques.statement = data["Statement"]
            if "option_a" in data:
                ques.option_a = data["option_a"]
            if "option_b" in data:
                ques.option_b = data["option_b"]
            if "option_c" in data:
                ques.option_c = data["option_c"]
            if "option_d" in data:
                ques.option_d = data["option_d"]
            if "answer" in data:
                ques.correct_answer = data["answer"]
            if "marks" in data: # score column marks doesnot support null values 
                ques.marks = data["marks"]
            db.session.commit()

            return {"message" : "question successfully updated"}
        except Exception as e:
            return {"message": f"Question updating failed: {str(e)}"}, 500
        
    @jwt_required()
    def delete(self, question_id=None):
        user_role = get_jwt().get("role")
        if user_role != "admin":
            return {"message": "You do not have permission to delete this question"}, 403 
        
        question=Question.query.filter_by(id=question_id).first()
        if not question:
            return {"message": "Question not found"}, 404
        db.session.delete(question)
        db.session.commit()
        return {"message": f"Question {question_id} deleted from quiz {question.quiz_id}"}, 200