from flask import Flask, Response, render_template
from camera import VideoCamera
from speech import TextRecorder
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer

import speech
import camera
import settings
import time
import operator

app = Flask(__name__)

capture_duration = 20
start_time = time.time()

emotions = []

@app.route('/')
def index():
    return render_template('index.html')

def gen(camera):
    while (int(time.time() - start_time) < capture_duration):
        settings.init()
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
        if len(settings.myList) != 0:
            emotions.append(settings.myList[0][0])
            print(settings.myList[0][0])

def sentiment_analysis(sentiment_text):

    score = SentimentIntensityAnalyzer().polarity_scores(sentiment_text)

    neg = score['neg']

    pos = score['pos']

    if neg > pos:
        return("Negative :(")
    elif pos > neg:
        return("Positive :)")
    else:
        return("Neutral")

def classify(text):
    while True:
        result = text.run()

        final = sentiment_analysis(result)

        return final

# def text_feed():
#     # if request.method == "POST"
#     text = TextRecorder()
#     return Response(classify(text))
# def text_feed():
#     # if request.method == "POST"
#     text = TextRecorder()

#     return Response(classify(text))

@app.route('/video_feed')
def video_feed():
    return Response(gen(VideoCamera()), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/text_feed')
def text_feed():
    # if request.method == "POST"
    text = TextRecorder()

    return Response(classify(text))

# def store_result():


@app.route('/test2')
def index2():
    d = {}
    emotion_count = 0
    for i in emotions:
        if i not in d:
            d[i] = 1
        else:
            d[i] += 1
        emotion_count += 1


    # score = (d["0"] + d["1"] + d["2"] + d["3"] + d["4"])/emotion_count
    # print(score)
    # return render_template('index2.html', variable = str(max(d, key=d.get)))
    return render_template('index2.html', variable = d["1"])

if __name__ == '__main__':
    app.run(host='127.0.0.1', debug = True)

