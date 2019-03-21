import urllib.request
import urllib.parse
import re
import pafy
import vlc
import speech_recognition as sr
from time import ctime
import time
import os
from gtts import gTTS
 
def speak(audioString):
    print(audioString)
    tts = gTTS(text=audioString, lang='en')
    tts.save("audio.mp3")
    os.system("mpg321 audio.mp3")
 
def recordAudio():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Say something!")
        audio = r.listen(source)
        
    data = ""
    try:
        data = r.recognize_google(audio)
        
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))
 
    return data
    
listener(command):
    if "pause" in command:
        player.pause()
        speak("music paused...")
    
    if "resume" in command:
        print("resuming...") 
        player.resume()
    
    if "help" in command:
        speak("say 'pause' to pause the music.")
        speak("say 'resume' to resume music.")
        speak("say 'stop' to stop music player. You can search for another music after saying 'stop'.")
        
    if "stop" in command:
        player.stop()
        speak("exiting music player")
        speak("do you want to listen more ?")
        restart = recordAudio() 
        if "yes" in restart:
            speak("restarting music player")
            os.system("rm -f stream_music.link")
            os.system("python music_online_restart.py")
            break
        if "ok" in restart:
            speak("restarting music player")
            os.system("rm -f stream_music.link")
            os.system("python music_online_restart.py")
            break
        if "sure" in restart:
            speak("restarting music player")
            os.system("rm -f stream_music.link")
            os.system("python  music_online_restart.py")
            break
        if "no" in restart:
            os.system("rm -f stream_music.link")
            break
        if "not now" in restart:
            os.system("rm -f stream_music.link")
            break

speak("what do you want to listen ?") input = recordAudio()
query_string = urllib.parse.urlencode({"search for" : input })
html_content = urllib.request.urlopen("http://www.youtube.com/results?" + query_string)
search_results = re.findall(r'href=\"\/watch\?v=(.{11})', html_content.read().decode())
print("Playing : http://www.youtube.com/watch?v=" + search_results[0])

file = open("stream_music.link", "w")
file.write("http://www.youtube.com/watch?v=" + search_results[0])
file.close()

file = open("stream_music.link", "r")
link = file.read() 

Instance = vlc.Instance()
player = Instance.media_player_new()
Media = Instance.media_new(link)
Media.get_mrl()
player.set_media(Media)
player.play()


while 1:
    command = recordAudio()
    listener(command) 
    
    

