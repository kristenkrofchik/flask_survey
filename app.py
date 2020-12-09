from flask import Flask, render_template, request, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import Question, Survey, satisfaction_survey, personality_quiz, surveys

app = Flask(__name__)
app.config['SECRET_KEY'] = "secret-key"

debug = DebugToolbarExtension(app)

responses = []


@app.route('/')
def show_home():
    title = satisfaction_survey.title
    instructions = satisfaction_survey.instructions
    return render_template('base.html', title=title, instructions=instructions)

@app.route('/start', methods=['POST'])
def set_sessions():
    session["responses"] = []
    return redirect('/questions/0')


@app.route('/questions/<int:qid>')
def show_question(qid):

    responses = session.get('responses')
    
    if (responses is None):
        flash('You do not have access to the questions yet.')
        return redirect('/')

    if (qid != len(responses)):
        flash('You cannot access the questions out of order.')
        return redirect(f'/questions/{len(responses)}')

    if (len(responses) == len(satisfaction_survey.questions)):
        flash('You have completed this survey.')
        return redirect('/thank_you')
    
    question = satisfaction_survey.questions[qid]
    return render_template('question.html', qid=qid, question=question)


@app.route('/answer', methods=['POST'])
def handle_answer():
    answer = request.form['answer']
    
    responses = session["responses"]
    responses.append(answer)
    session["responses"] = responses
    
    if (len(responses) == len(satisfaction_survey.questions)):
        return redirect('/thank_you')
    else:
        return redirect(f"/questions/{len(responses)}")

@app.route('/thank_you')
def thank_you():
    return render_template('thankyou.html')


