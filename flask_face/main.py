from flask import Flask, Response, render_template
from camera import VideoCamera
from speech import TextRecorder
import speech
import camera
import settings
import time
import operator

app = Flask(__name__)

capture_duration = 10
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

def classify(text):
    while True:
        result = text.run()
        return result


@app.route('/video_feed')
def video_feed():
    return Response(gen(VideoCamera()), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/text_feed')


def text_feed():
    # if request.method == "POST"
    text = TextRecorder()
    return Response(classify(text))

@app.route('/test2')
def index2():
    d = {}
    for i in emotions:
        if i[0] not in d:
            d[i[0]] = 1
        else:
            d[i[0]] += 1
    return render_template('index2.html', variable = max(d.iteritems(), key=operator.itemgetter(1))[0])

if __name__ == '__main__':
    app.run(host='127.0.0.1', debug = True)

