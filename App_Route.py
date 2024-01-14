from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/IdeaValidator')
def ideavalidator():
    return render_template('IdeaValidator.html')

@app.route('/MoonShotFinder')
def moonshotfinder():
    return render_template('MoonShotFinder.html')

@app.route('/IdeaFilterAI')
def ideafilter():
    return render_template('IdeaFilterAI.html')