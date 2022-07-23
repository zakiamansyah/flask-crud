from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/inputData')
def inputData():
    return render_template('inputData.html')