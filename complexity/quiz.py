from flask import Blueprint, render_template

quiz = Blueprint('quiz', __name__, template_folder='templates/quiz')

@quiz.route("/")
def new():
    return render_template('new.html')

