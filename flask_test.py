from flask import Flask, Response
from keras.models import load_model
import tensorflow as tf
from keras.preprocessing.image import img_to_array
from keras.preprocessing import image
import cv2
import numpy as np
import time
import tensorflow.python.keras

# sentiment analysis
import speech_recognition as sr 
import pyttsx3  

import nltk
nltk.download('vader_lexicon')
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import pyaudio

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



# Function to convert text to 
# speech 
def SpeakText(command): 
    
    # Initialize the engine 
    engine = pyttsx3.init() 
    engine.say(command)  
    engine.runAndWait() 
    
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

def analyze_feed:()
    while(1):     
        
        # Exception handling to handle 
        # exceptions at the runtime 
        try: 
            
            # use the microphone as source for input. 
            with sr.Microphone() as source2: 
                
                # wait for a second to let the recognizer 
                # adjust the energy threshold based on 
                # the surrounding noise level  
                r.adjust_for_ambient_noise(source2, duration=0.2) 
                
                print("Please speak")  
                #listens for the user's input  
                audio2 = r.listen(source2) 
                
                # Using ggogle to recognize audio 
                MyText = r.recognize_google(audio2) 
                MyText = MyText.lower() 
    
                print(MyText)
                sentiment_analysis(MyText) 
                SpeakText(MyText)
                break 

        except sr.RequestError as e: 
            print("Could not request results; {0}".format(e))
            break 
            
        except sr.UnknownValueError: 
            print("unknown error occured") 
            break

@app.route('/video_feed')
def video_feed():
    global video
    return Response(gen(video),
                    mimetype='multipart/x-mixed-replace; boundary=frame')
    return d

@app.route('/text_feed')
def text_feed():
    r = sr.Recognizer()

    while(1):     
        
        # Exception handling to handle 
        # exceptions at the runtime 
        try: 
            
            # use the microphone as source for input. 
            with sr.Microphone() as source2: 
                
                # wait for a second to let the recognizer 
                # adjust the energy threshold based on 
                # the surrounding noise level  
                r.adjust_for_ambient_noise(source2, duration=0.2) 
                
                print("Please speak")  
                #listens for the user's input  
                audio2 = r.listen(source2) 
                
                # Using ggogle to recognize audio 
                MyText = r.recognize_google(audio2) 
                MyText = MyText.lower() 
    
                print(MyText)
                return sentiment_analysis(MyText) 
                SpeakText(MyText)
                break 

        except sr.RequestError as e: 
            print("Could not request results; {0}".format(e))
            break 
            
        except sr.UnknownValueError: 
            print("unknown error occured") 
            break


if __name__ == '__main__':
    app.debug = True
    app.run(host='127.0.0.1')


