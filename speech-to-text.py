# import os
import speech_recognition as sr
import subprocess
# import ffmpeg
# from moviepy.editor import *

import moviepy.editor as mp

clip = mp.VideoFileClip("test.mp4").subclip(0,20)
clip.audio.write_audiofile("test.mp3")


# audioclip = AudioFileClip("test.mp4")
# audioclip.write_audiofile("audio.wav")



# command2mp3 = "ffmpeg -i test.mp4 test.mp3"

# command2wav = "ffmpeg -i test.mp3 test.wav"

# os.system(command2mp3)
# os.system(command2wav)


r = sr.Recognizer()

with sr.AudioFile('test.mp3') as source:
    
    audio_text = r.listen(source)
    
# recoginize_() method will throw a request error if the API is unreachable, hence using exception handling
    try:
        
        # using google speech recognition
        text = r.recognize_google(audio_text)
        print('Converting audio transcripts into text ...')
        print(text)
     
    except:
         print('Sorry.. run again...')