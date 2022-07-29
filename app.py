from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import surveys

survey = surveys["satisfaction"]

app = Flask(__name__)
app.config['SECRET_KEY'] = "never-tell!"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)

@app.get("/")
def pick_survey():
    session["responses"] = []
    return render_template("survey_choice.html",surveys=surveys)

# @app.get("/survey")
# def start_survey():
#     """Home page for survey. Sets session cookie."""

#     return render_template("survey_start.html",survey=survey)

@app.post("/begin")
def redirect_page():
    """Redirect to first question."""
    form_value = request.form["pick"]
    survey = surveys[form_value]
    return redirect("/questions/0")

@app.get("/questions/<int:question_number>")
def questions(question_number):
    """Renders survey question and response options. Directs users
    to next sequential question"""

    if question_number != len(session["responses"]):
        question_number = len(session["responses"])
        flash("you have tried to access an invalid question!")
        return redirect(f"/questions/{question_number}")

    if len(session["responses"]) > len(survey.questions):
        return redirect("/thanks")

    question = survey.questions[question_number]
    choices = question.choices

    return render_template("question.html", question = question, choices = choices)

@app.post("/answer")
def store_answer():
    """Stores answer and redirects to next question or thank you page."""

    responses = session["responses"]
    responses.append(request.form["answer"])
    session["responses"] = responses

    responses_length = len(session["responses"])

    if responses_length == len(survey.questions):
        return redirect("/thanks")
    else:
        return redirect(f"/questions/{responses_length}")

@app.get("/thanks")
def say_thanks():
    """Thanks user."""
    return render_template("completion.html")
