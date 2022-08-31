from boggle import Boggle 
from flask import Flask, request, render_template, session, jsonify
from flask_debugtoolbar import DebugToolbarExtension
import os

app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", 'asjdhashdj')
app.config["DEBUG_TB_INTERCEPT_REDIRECTS"] = False
debug = DebugToolbarExtension(app)

boggle_game = Boggle()

@app.route('/')
def main_page(): 
    """Return the game board""" 
    board = boggle_game.make_board() 
    session['board'] = board
    highscore = session.get("highscore", 0)
    number_of_plays = session.get("number_of_plays", 0)

    return render_template('index.html', board=board, highscore=highscore, number_of_plays=number_of_plays)

@app.route('/check-word') 
def check_word(): 
    """Check if word is found in dictionary"""
    word = request.args["word"]
    board = session["board"]
    response = boggle_game.check_valid_word(board, word) 

    return jsonify({'result': response}) 

@app.route("/post-score", methods=["POST"])
def post_score():
    """Receive score, update number_of_plays, update high score if appropriate."""

    score = request.json["score"]
    highscore = session.get("highscore", 0)
    number_of_plays = session.get("number_of_plays", 0)

    session['number_of_plays'] = number_of_plays + 1
    session['highscore'] = max(score, highscore)

    return jsonify(brokeRecord=score > highscore)
