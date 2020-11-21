import speech_recognition as sr 
import pyttsx3  

import nltk
nltk.download('vader_lexicon')
from nltk.sentiment.vader import SentimentIntensityAnalyzer
  
# Initialize the recognizer  
r = sr.Recognizer()  
  

class TextRecorder(object):
    # Function to convert text to 
    # speech 

    def __init__(self):
        self.r = sr.Recognizer()  

    def SpeakText(self,command): 
        
        # Initialize the engine 
        engine = pyttsx3.init() 
        engine.say(command)  
        engine.runAndWait() 
        
    def sentiment_analysis(self,sentiment_text):

        score = SentimentIntensityAnalyzer().polarity_scores(sentiment_text)

        neg = score['neg']

        pos = score['pos']

        if neg > pos:
            return("Negative :(")
        elif pos > neg:
            return("Positive :)")
        else:
            return("Neutral")
        

    def run(self):
        # Loop infinitely for user to 
        # speak 
        
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
                    return self.sentiment_analysis(MyText) 
                    # self.SpeakText(MyText)
                    break 

            except sr.RequestError as e: 
                return("Could not request results; {0}".format(e))
                break 
                
            except sr.UnknownValueError: 
                return("unknown error occured") 
                break