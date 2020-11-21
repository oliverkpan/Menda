from flask import Flask, Response
from keras.models import load_model
import tensorflow as tf
from keras.preprocessing.image import img_to_array
from keras.preprocessing import image
import cv2
import numpy as np
import time
import tensorflow.python.keras

app = Flask(__name__)

face_classifier = cv2.CascadeClassifier(r'models\face.xml')
classifier = tensorflow.keras.models.load_model(r'models\emotion2.h5')

class_labels=['Upset','Happy','Anxious','Depressed','Surprise']
video=cv2.VideoCapture(0)
print('Works')

@app.route('/')
def index():
    return "Default Message"

def gen(video):

    capture_duration = 10
    start_time = time.time()

    test = []

    # int(time.time() - start_time) < capture_duration 

    while (1):
        ret,frame=video.read()
        if ret==True:
            labels=[]
            gray=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
            faces=face_classifier.detectMultiScale(gray,1.3,5)



            for (x,y,w,h) in faces:
                cv2.rectangle(frame,(x,y),(x+w,y+h),(255,0,0),2)
                roi_gray=gray[y:y+h,x:x+w]
                roi_gray=cv2.resize(roi_gray,(48,48),interpolation=cv2.INTER_AREA)

                if np.sum([roi_gray])!=0:
                    roi=roi_gray.astype('float')/255.0
                    roi=img_to_array(roi)
                    roi=np.expand_dims(roi,axis=0)

                    preds=classifier.predict(roi)[0]
                    test.append([preds.argmax(axis = 0)])

                    
                    label=class_labels[preds.argmax()]
                    label_position=(x,y)
                    cv2.putText(frame,label,label_position,cv2.FONT_HERSHEY_SIMPLEX,2,(255, 0, 255),20)
                else:
                    cv2.putText(frame,'No Face Found',(20,20),cv2.FONT_HERSHEY_SIMPLEX,2,(0,255,0),3)
            
            cv2.imshow('Emotion Detector',frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                print(preds)
                break
        else:
            break
    print(test)

    d = {}

    for i in test:
        if i[0] not in d:
            d[i[0]] = 1
        else:
            d[i[0]] += 1
    print(d)

    video.release()
    cv2.destroyAllWindows()

@app.route('/video_feed')
def video_feed():
    global video
    return Response(gen(video),
                    mimetype='multipart/x-mixed-replace; boundary=frame')
    return d

if __name__ == '__main__':
    app.debug = True
    app.run(host='127.0.0.1')


