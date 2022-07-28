from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey as survey

app = Flask(__name__)
app.config['SECRET_KEY'] = "never-tell!"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)

RESPONSES = []

@app.get("/")
def start_survey():
    """Home page for survey."""

    return render_template("survey_start.html",survey=survey)

@app.post("/begin")
def redirect_page():
    """Redirect to first question."""
    return redirect("/questions/0")

@app.get("/questions/<int:question_number>")
def questions(question_number):
    """Renders survey question and response options."""

    question = survey.questions[question_number]
    choices = question.choices

    return render_template("question.html", question = question, choices = choices)

@app.post("/answer")
def store_answer():
    """Stores answer and redirects to next question or thank you page."""

    RESPONSES.append(request.form["answer"])
    #cleaner way to do this?
    responses_length = len(RESPONSES)
    
    if responses_length == len(survey.questions):
        return redirect("/thanks")
    else:
        return redirect(f"/questions/{responses_length}")

@app.get("/thanks") 
def say_thanks():
    """Thanks user."""
    return render_template("completion.html")
