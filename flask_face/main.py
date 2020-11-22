from flask import Flask, Response, render_template, request, redirect
import pyrebase
# from camera import VideoCamera
# from speech import TextRecorder
# import nltk
# from nltk.sentiment.vader import SentimentIntensityAnalyzer

# import speech
# import camera
# import settings
# import time
# import operator

firebaseConfig = {
    "apiKey": "AIzaSyBDPB89itGMDiZgksfiOtOmT0kJ4FMBul4",
    "authDomain": "hack-western-7.firebaseapp.com",
    "databaseURL": "https://hack-western-7.firebaseio.com",
    "projectId": "hack-western-7",
    "storageBucket": "hack-western-7.appspot.com",
    "messagingSenderId": "1061541009957",
    "appId": "1:1061541009957:web:4382341cb8637e3128fdcc"
}

firebase = pyrebase.initialize_app(firebaseConfig)

app = Flask(__name__,static_url_path="/static")
capture_duration = 10
spoken_text = ""

emotions = []

@app.route('/index.html')
def reroute():
    return redirect('/', 302)

@app.route('/')
def index():
    return render_template('index.html')

def gen(camera):

    start_time = time.time()
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
        global spoken_text
        result = text.run()
        spoken_text = result
        final = sentiment_analysis(result)

        return final

@app.route('/login.html')
def login():
    return render_template('login.html')

@app.route('/history.html')
def history():
    return render_template('history.html')

@app.route('/trends.html')
def trends():
    return render_template('trends.html')

@app.route('/music.html')
def music():
    return render_template('music.html')

@app.route('/meditation.html')
def meditation():
    return render_template('meditation.html')

@app.route('/podcast.html')
def podcast():
    return render_template('podcast.html')

@app.route('/new.html')
def newlog():
    return render_template('new.html')

@app.route('/video_feed')
def video_feed():
    return Response(gen(VideoCamera()), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/results')
def results():
    classified_text = TextRecorder()

    final_result = classify(classified_text)

    output = "What you said: "+ spoken_text + "\nSentiment analysis: " + final_result

    return render_template("results.html", results = output)

    # return Response(output)

if __name__ == '__main__':
    app.run(host='localhost', debug = True)