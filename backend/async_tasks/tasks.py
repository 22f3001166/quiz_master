from celery import shared_task
from datetime import datetime, timedelta
from models import Score, Answer,Question,Quiz,User
import csv
from jinja2 import Template
from .mail_send import send_email
import requests

# The application should send daily reminders to users on g-chat using Google Chat Webhooks or SMS or mail
# New daily reminder scheduled task
@shared_task(ignore_result=False, name="onetime-reminder")
def onetime_reminder(name,quiz,subject):
    text = f"Hello @{name},\n\nA new quiz titled *{quiz}* has been created today under the *{subject}* subject. \nFeel free to explore it and see if it's relevant to your interests or learning goals."
    res= requests.post("https://chat.googleapis.com/v1/spaces/AAQAyWsWhpU/messages?key=AIzaSyDdI0hCZtE6vySjMm-WEfRq3CPzqKqqsHI&token=Uv3b2p7ltIu-wKkV7E3dJBj1wy__0Ze2awRBQWxKi2o", json={"text": text} )
    print(res.status_code)
    # Simulate reminder sent
    return "Daily reminder sent to users about new quiz pushed."

@shared_task(ignore_result=False, name="daily-reminder")
def daily_reminder():
    quizes= Quiz.query.all()
    users= User.query.all()
    for user in users[1:]:
        scores = Score.query.filter_by(user_id=user.id).all()
        quiz_ids_attempted = [score.quiz_id for score in scores]
        not_attempted_quizzes = [quiz.title for quiz in quizes if quiz.id not in quiz_ids_attempted]

        if not_attempted_quizzes:
            # Create numbered list as plain text
            quiz_list_text = '\n'.join([f"{i+1}. {title}" for i, title in enumerate(not_attempted_quizzes)])

            message = f"""
📘 *Dear @{user.name},*

We noticed you haven’t attempted the following quizzes created in the last 30 days:

{quiz_list_text}

We encourage you to stay consistent and attempt these quizzes to reinforce your learning.

🔔 *Stay focused and curious!*

– Quiz Master Team
"""
            
        res= requests.post("https://chat.googleapis.com/v1/spaces/AAQAyWsWhpU/messages?key=AIzaSyDdI0hCZtE6vySjMm-WEfRq3CPzqKqqsHI&token=Uv3b2p7ltIu-wKkV7E3dJBj1wy__0Ze2awRBQWxKi2o", json={"text": message} )
        print(res.status_code)
    return "Daily reminder sent to users who have not attempt some quizes."


@shared_task(ignore_result=False, name="download_csv_export")
def csv_export(score_id, user_id):
    answers = Answer.query.filter_by(score_id=score_id,user_id=user_id).all()
    csv_file_name=f"answers_{datetime.now().strftime("%f")}.csv"
    with open(f"static/{csv_file_name}" , 'w', newline="") as csvfile:
        ans_csv = csv.writer(csvfile, delimiter=',')
        Serial=1
        ans_csv.writerow([ "S.No ","Statement", "Option A", "Option B", "Option C", "Option D",  "Correct Answer", "Selected Answer", "Question Marks", "Marks Obtained"])
        for ans in answers:
            ques = Question.query.get(ans.question_id)
            ans_csv.writerow([ Serial, ques.statement, ques.option_a, ques.option_b, ques.option_c,ques.option_d, ques.correct_answer, ans.selected_answer, ques.marks, ans.is_correct* ques.marks])
            Serial+=1
    return csv_file_name



@shared_task(ignore_result=False, name="download_quiz_csv")
def quiz_csv_export(quiz_id, user_id):
    scores = Score.query.filter_by(quiz_id=quiz_id,user_id=user_id).all()
    csv_file_name=f"scores_{datetime.now().strftime("%f")}.csv"
    with open(f"static/{csv_file_name}" , 'w', newline="") as csvfile:
        score_csv = csv.writer(csvfile, delimiter=',')
        Serial=1
        score_csv.writerow([ "Attempt Number", "Quiz Title", "Quiz Marks", "User Score","Questions Attempted" , "Accuracy", "Grace"])
        for score in scores:
            score_csv.writerow([ Serial, score.quiz.title, score.quiz_score, score.total_scored,score.total_attempted ,score.accuracy, score.grace ])
            Serial+=1
    return csv_file_name


def format_time(sec):
    minutes= sec //60
    secs = sec %60
    return f"{minutes}min {secs}seconds"

@shared_task(ignore_result=False, name="monthly report")
def monthly_report():
    today = datetime.today()
    start_month = datetime(today.year, today.month, 1)
    next_month = datetime(today.year + today.month // 12, today.month % 12 + 1, 1)
    end_of_month = next_month - timedelta(days=1)

    users = User.query.all()
    for user in users[1:]:
        user_id = user.id
        scores = Score.query.filter(
            Score.user_id == user_id,
            Score.time_stamp_of_attempt >= start_month,
            Score.time_stamp_of_attempt <= end_of_month
        ).all()
        if not scores:
            # User didn’t attempt any quiz — send friendly academic reminder
            message_html = f"""
            <html>
            <body style="font-family: Arial, sans-serif; padding: 20px;">
                <h3>Dear {user.name},</h3>
                <p>We noticed that you haven't attempted any quizzes this month ({start_month.strftime('%B %Y')}).</p>
                <p>To stay informed and not miss upcoming quizzes, we invite you to join our discussion space:</p>

                <p>
                    👉 <a href="https://chat.google.com/room/AAQAyWsWhpU?cls=7" target="_blank" style="color: #1a73e8; font-weight: bold;">
                    Join Gurmukhi GSpace</a>
                </p>

                <p>You can also visit our app regularly to track your progress and improve.</p>
                <p>Let’s keep learning! 🎓</p>
                <p><strong>Quiz Master Team</strong></p>
            </body>
            </html>
            """
            send_email(user.email, "Urgently Join Gspace", message=message_html)
            continue

        total_score = 0
        total_quizzes = len(scores)
        quiz_score = 0

        table_html = f'''
        <html>
        <head>
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    background-color: #f9f9f9;
                    padding: 20px;
                }}
                h3 {{
                    color: #2c3e50;
                }}
                table {{
                    width: 100%;
                    border-collapse: collapse;
                    margin-top: 20px;
                }}
                th, td {{
                    border: 1px solid #ddd;
                    padding: 8px;
                    text-align: center;
                }}
                th {{
                    background-color: #4169E1;
                    color: white;
                }}
                tr:nth-child(even) {{ background-color: #f2f2f2; }}
                tr:hover {{ background-color: #ddd; }}
                .summary {{
                    margin-top: 20px;
                    font-size: 16px;
                }}
            </style>
        </head>
        <body>
            <h3>Dear {user.name},</h3>
            <p>Here is your quiz performance summary for the month of {start_month.strftime('%B %Y')}:</p>

            <table>
                <tr>
                    <th>Quiz Title</th>
                    <th>Date of Attempt</th>
                    <th>Time Taken</th>
                    <th>User Score</th>
                    <th>Quiz Marks</th>
                    <th>Total Attempted</th>
                    <th>Correct Answers</th>
                    <th>Incorrect Answers</th>
                    <th>Percentage</th>
                    <th>Grace Marks</th>
                </tr>
        '''

        for s in scores:
            total_score += s.total_scored
            quiz_score += s.quiz_score
            format_time_taken = format_time(s.time_taken)
            table_html += f'''
                <tr>
                    <td>{s.quiz.title}</td>
                    <td>{s.time_stamp_of_attempt.strftime('%Y-%m-%d %H:%M')}</td>
                    <td>{format_time_taken}</td>
                    <td>{s.total_scored}</td>
                    <td>{s.quiz_score}</td>
                    <td>{s.total_attempted}</td>
                    <td>{s.correct_answers}</td>
                    <td>{s.incorrect_answers}</td>
                    <td>{round(s.percentage_score, 2)}%</td>
                    <td>{s.grace}</td>
                </tr>
            '''

        avgscore = round(total_score / quiz_score, 2) if quiz_score > 0 else 0
        table_html += f'''
            </table>
            <div class="summary">
                <p><strong>Monthly Average Score:</strong> {avgscore}</p>
                <p><strong>Total Quizzes Attempted:</strong> {total_quizzes}</p>
            </div>
            <p>Keep up the great work!<br><br>Regards,<br><strong>Quiz Master Team</strong></p>
        </body>
        </html>
        '''

        format = Template(table_html).render(user=user)
        send_email(user.email, "Monthly Quiz Performance Summary", message=format)

    return "Score email sent to all users"

