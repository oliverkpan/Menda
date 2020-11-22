from flask import Flask, Response, render_template, request, session
from camera import VideoCamera
from speech import TextRecorder
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer

import speech
import camera
import settings
import time
import operator

app = Flask(__name__,static_url_path="/static")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/new.html')
def newlog():
    return render_template('new.html')

@app.route('/video_feed')
def video_feed():
    return Response(gen(VideoCamera()), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(host='localhost', debug = True)