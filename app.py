from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey as survey

app = Flask(__name__)
app.config['SECRET_KEY'] = "never-tell!"
# app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)

RESPONSES = []

@app.get("/")
def start_survey():

    title = survey.title
    instructions = survey.instructions

    return render_template("survey_start.html",title=title, instructions=instructions)

@app.post("/begin")
def redirect_page():
    return redirect("/questions/0")

@app.get("/questions/<int:question_number>")
def questions(question_number):

    question = survey.questions[question_number]
    choices = question.choices

    return render_template("question.html", question = question, choices = choices)

@app.post("/answer")
def store_answer():
    request.form["answer"]
