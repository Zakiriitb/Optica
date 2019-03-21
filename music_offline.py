import pygame
import speech_recognition as sr
from gtts import gTTS

def speak(audioString):
    print(audioString)
    tts = gTTS(text=audioString, lang='en')
    tts.save("speak_optika.mp3")
    os.system("omxplayer optika_speak.mp3")

def recordAudio():
    # Record Audio
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Say something!")
        audio = r.listen(source)

    # Speech recognition using Google Speech Recognition
    case = ""
    try:
        # Uses the default API key
        # To use another API key: `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
        case = r.recognize_google(audio)
        print("You said: " + case)
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
        #speak("sorry i didn't understand that")
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))

    file = open("music_offline_speech_output", "w")
    file.write(case + '\n')
    file.close()

    file = open("music_offline_speech_output", "rb")
    data = file.read()

    dict_file = open("dict.dictionary")
    dict = set(dict_file.read().split())
    words = dict.intersection(data)

    return case

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
            os.system("python music_offline_restart.py")
            break
        if "ok" in restart:
            speak("restarting music player") 
            os.system("python music_offline_restart.py")
            break
        if "sure" in restart:
            speak("restarting music player")
            os.system("python  music_offline_restart.py")
            break
        if "no" in restart:
            break
        if "not now" in restart:
            break

while 1:
    music = recordAudio()
    pygame.mixer.init()
    pygame.mixer.music.load(music)
    pygame.mixer.music.play()
    command = recordAudio()
    listener(command) 
    

