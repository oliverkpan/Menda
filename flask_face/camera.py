from keras.models import load_model
import tensorflow as tf
from keras.preprocessing.image import img_to_array
from keras.preprocessing import image
import cv2
import numpy as np  
import tensorflow.python.keras
import settings

face_classifier = cv2.CascadeClassifier(r'face.xml')
classifier = tensorflow.keras.models.load_model(r'emotion2.h5')
class_labels=['Angry','Happy','Nervous','Sad','Fearful']
ds_factor = 0.6
print('Works')



class VideoCamera(object):
    def __init__(self):
       #capturing video
       self.cap = cv2.VideoCapture(0)
    
    def __del__(self):
        #releasing camera
        self.cap.release()

    def get_frame(self):
        global test
        test = []      
        ret,frame=self.cap.read()
        frame = cv2.resize(frame,None,fx=ds_factor,fy=ds_factor,interpolation=cv2.INTER_AREA)
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
                settings.myList.append([preds.argmax(axis = 0)])
                
                label=class_labels[preds.argmax()]
                label_position=(x,y)
                cv2.putText(frame,label,label_position,cv2.FONT_HERSHEY_SIMPLEX,2,(255, 0, 255),10)
            else:
                cv2.putText(frame,'No Face Found',(20,20),cv2.FONT_HERSHEY_SIMPLEX,2,(0,255,0),3)
            break
        success, jpeg = cv2.imencode('.jpg', frame)
        return jpeg.tobytes()

    def get_array():
        return test


