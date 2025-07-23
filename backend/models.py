from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from datetime import datetime
from sqlalchemy.sql import func
from sqlalchemy import Enum

app= Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///quizmaster.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']= False
db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(200), nullable=False)  # 'student' or admin
    dob = db.Column(db.Date, nullable=True)
    timezone = db.Column(db.String(100), default="UTC", nullable=False)  # e.g. "Asia/Kolkata"
    qualification = db.Column(db.String(100), nullable=True)
    active= db.Column(db.Boolean,default=True)  
    def set_password(self, password):
        self.password = generate_password_hash(password)
    def check_password(self, password):
        return check_password_hash(self.password, password)
    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "role": self.role,
            "dob": self.dob.isoformat() if self.dob else None,
            "timezone": self.timezone,
            "qualification": self.qualification,
            "active": self.active
        }
    def __repr__(self):
        return f"<User {self.email}({self.role})>"

class Subject(db.Model):
    id = db.Column(db.Integer, primary_key=True) 
    name = db.Column(db.String, nullable=False, unique=True)
    description = db.Column(db.Text, nullable=True)
    chapters = db.relationship("Chapter", backref="subject", cascade="all, delete", lazy=True)
    quizzes = db.relationship("Quiz", backref="subject", cascade="all, delete", lazy=True)     # Relationship to all quizes
    # quizzes= db.relationship("Quiz", secondary="chapter",primaryjoin="Subject.id==Chapter.subject_id",secondaryjoin="Chapter.id==Quiz.chapter_id", viewonly=True, lazy="dynamic")
    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "chapters": [chapter.to_dict() for chapter in self.chapters],
            "quizzes": [quiz.to_dict() for quiz in self.quizzes]
        }
    def __repr__(self):
        return f"<Subject {self.name}>"

class Chapter(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    description = db.Column(db.Text, nullable=True)
    subject_id = db.Column(db.Integer, db.ForeignKey("subject.id"), nullable=False)
    quizzes = db.relationship("Quiz", backref="chapter", cascade="all, delete", lazy=True) # ONE TO MANY RELATIONSHIP BETWEEN Parent and child components

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "subject_id": self.subject_id,
            "quizzes": [quiz.to_dict() for quiz in self.quizzes]
        }

class Quiz(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # Add this line
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=True)
    created_on = db.Column(db.DateTime(timezone=True), server_default=func.now(), nullable=False)
    time_duration = db.Column(db.Integer)  # Format HH:MM
    remarks = db.Column(db.Text, nullable=True)

    chapter_id = db.Column(db.Integer, db.ForeignKey("chapter.id"), nullable=False)
    subject_id = db.Column(db.Integer, db.ForeignKey("subject.id"), nullable=False)
    questions = db.relationship("Question", backref="quiz", cascade="all, delete", lazy=True)

    def __repr__(self):
        return f"<Quiz {self.title} - Subject ID: {self.subject_id}, Chapter ID: {self.chapter_id}, Created at {self.created_on}>"
    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "duration": self.time_duration,
            "remarks": self.remarks,
            "chapter_id": self.chapter_id,
            "subject_id": self.subject_id,
            "created_on": self.created_on.isoformat() if self.created_on else None
        }

class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # Add primary key for consistency
    quiz_id = db.Column(db.Integer, db.ForeignKey("quiz.id"), nullable=False)
    subject_id = db.Column(db.Integer, db.ForeignKey("subject.id"), nullable=False)  # Link to subject
    statement = db.Column(db.Text, nullable=False)
    option_a = db.Column(db.String(255), nullable=False)
    option_b = db.Column(db.String(255), nullable=False)
    option_c = db.Column(db.String(255), nullable=False)
    option_d = db.Column(db.String(255), nullable=False)
    correct_answer = db.Column(Enum("A", "B", "C", "D", name="answer_option"), nullable=False)
    marks = db.Column(db.Integer, default=1, nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "quiz_id": self.quiz_id,
            "subject_id": self.subject_id,
            "statement": self.statement,
            "option_a": self.option_a,
            "option_b": self.option_b,
            "option_c": self.option_c,
            "option_d": self.option_d,
            "correct_answer": self.correct_answer,
            "marks": self.marks
        }

    def __repr__(self):
        return f"<Question {self.Statement[:20]}...>"

class Answer(db.Model):
    __tablename__ = "answer"
    id = db.Column(db.Integer, primary_key=True)  # Add primary key
    selected_answer = db.Column(db.String(1), nullable=False)  # A, B, C, or D
    is_correct = db.Column(db.Boolean, default=False)
    #Foreign Keys
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    quiz_id = db.Column(db.Integer, db.ForeignKey("quiz.id"), nullable=False)        #Helps group answers under a quiz for scoring, reports, summaries
    question_id = db.Column(db.Integer, db.ForeignKey("question.id"), nullable=False)
    score_id = db.Column(db.Integer, db.ForeignKey('score.id'), nullable=False)
    
    # Relationships
    user = db.relationship("User", backref="answers", lazy=True)
    quiz = db.relationship("Quiz", backref="answers", lazy='select')
    question = db.relationship("Question", backref="answers", lazy='select')
    

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "quiz_id": self.quiz_id,
            "question_id": self.question_id,
            "selected_answer": self.selected_answer,
            "is_correct": self.is_correct
        }
    def __repr__(self):
        return f"<Answer by User {self.user_id} for Question {self.question_id}>"

class Score(db.Model):
    __tablename__ = "score"

    id = db.Column(db.Integer, primary_key=True)
    quiz_id = db.Column(db.Integer, db.ForeignKey("quiz.id"), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)

    time_stamp_of_attempt = db.Column(db.DateTime, nullable=False)
    time_taken = db.Column(db.Integer, nullable=False)  # in seconds
    usertotal_attempts = db.Column(db.Integer, nullable=False) # to dynamically store the no. of attempts for a particular quiz by particular user_id
    # total_attemptes= db.Column(db.Integer, nullable=False) # to dynamically store the number of attempts for a particular quiz by all user 

    total_attempted = db.Column(db.Integer, nullable=False) # questions attempts in a particular quiz
    correct_answers = db.Column(db.Integer, nullable=False)
    incorrect_answers = db.Column(db.Integer, nullable=False)

    total_scored = db.Column(db.Float, nullable=False)       # score earned
    quiz_score = db.Column(db.Float, nullable=False)         # max possible
    percentage_score = db.Column(db.Float, nullable=False)   # total_scored / quiz_score * 100
    accuracy = db.Column(db.Float, nullable=False)           # correct_answers / total_attempted * 100

    grace = db.Column(db.Float, nullable=False, default=0)

    quiz = db.relationship("Quiz", backref="scores")
    user = db.relationship("User", backref="scores")

    def __repr__(self):
        return f"<Score User {self.user_id} - Quiz {self.quiz_id} - {self.total_scored}/{self.quiz_score}>"

    def to_dict(self):
        return {
            "id": self.id,
            "quiz_id": self.quiz_id,
            "user_id": self.user_id,
            "time_stamp_of_attempt": self.time_stamp_of_attempt.isoformat(),
            "time_taken": self.time_taken,
            "total_attempted": self.total_attempted,
            "correct_answers": self.correct_answers,
            "incorrect_answers": self.incorrect_answers,
            "total_scored": self.total_scored,
            "quiz_score": self.quiz_score,
            "percentage_score": self.percentage_score,
            "accuracy": self.accuracy,
            "grace": self.grace
        }


with app.app_context():
    db.create_all()
    if User.query.filter_by(email='singhadmin@gmail.com').first() is None:
        admin_password= generate_password_hash('penduwarrior')
        admin_dob = datetime.strptime('2002-08-17', '%Y-%m-%d').date()  # Convert to date
        admin = User(email='singhadmin@gmail.com',name='yodhsingh',password=admin_password,role='admin',dob=admin_dob)
        db.session.add(admin)
        db.session.commit()
        print("Admin user created.")
    else:
        print('admin already exits')

    if User.query.filter_by(email='dalyodhsingh1@gmail.com').first() is None:
        user_password= generate_password_hash('penduwarrior')
        user_dob = datetime.strptime('2002-08-17', '%Y-%m-%d').date()  # Convert to date
        user = User(email='dalyodhsingh1@gmail.com',name='Dalyodh Singh',password=user_password,role='student',dob=user_dob)
        db.session.add(user)
        db.session.commit()
        print("Student Role created successfully.")
    else:
        print('student already exits')

    if Subject.query.first() is None:
        print("Seeding subjects and chapters...")

        subjects_data = [
            {"name": "Gurmukhi Language", "description": "Learn Gurmukhi"},
            {"name": "Sikh Itihass", "description": "History of Sikhism"}
        ]
        chapters_data = [
            {"name": "35 Akhars", "description": "Intro to Gurmukhi letters", "subject_name": "Gurmukhi Language"},
            {"name": "Vowels and Symbols", "description": "Matras in Gurmukhi", "subject_name": "Gurmukhi Language"},
            {"name": "Guru Nanak Dev Ji", "description": "Life of Guru Nanak", "subject_name": "Sikh Itihass"},
            {"name": "Formation of Khalsa", "description": "Creation of Khalsa by Guru Gobind Singh", "subject_name": "Sikh Itihass"}
        ]

        for subj in subjects_data:
            if not Subject.query.filter_by(name=subj["name"]).first():
                db.session.add(Subject(name=subj["name"], description=subj["description"]))
        db.session.commit()
        for chap in chapters_data:
            if not Chapter.query.filter_by(name=chap["name"]).first():
                subject = Subject.query.filter_by(name=chap["subject_name"]).first()
                if subject:
                    db.session.add(Chapter(name=chap["name"], description=chap["description"], subject_id=subject.id))
        db.session.commit()
        print("Subjects and Chapters seeded.")
        
    else:
        print("Subjects and Chapters already exist. Skipping.")


