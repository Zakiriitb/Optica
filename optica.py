import imaplib
import smtplib
from pathlib import Path
import speech_recognition as sr
from time import ctime
import time
import datetime
import os
from gtts import gTTS

def speak(audioString):
    print(audioString)
    tts = gTTS(text=audioString, lang='en')
    tts.save("optica_speak.mp3")
    os.system("omxplayer optica_speak.mp3")
 
def recordAudio():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Say something!")
        audio = r.listen(source)
 
    case = ""
    try:
        case = r.recognize_google(audio)
        print("You said: " + case)
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))
    
    file = open("optica_speech_output", "w")
    file.write(case + '\n')
    file.close()
    
    file = open("optica_speech_output", "r")
    data = file.read()
    
    dict_file = open("dict.dictionary")
    dict = set(dict_file.read().split())
    words = dict.intersection(data)

    return case

def recordNumbers():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Say something!")
        audio = r.listen(source)
 
    case = ""
    try:
        case = r.recognize_google(audio)
        print("You said: " + case)
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))
    
    file = open("optica_speech_output", "w")
    file.write(case + '\n')
    file.close()
    
    file = open("optica_speech_output", "r")
    data = file.read()
    
    dict_file = open("dict_alarm.dictionary")
    dict = set(dict_file.read().split())
    words = dict.intersection(data)

    return case



def alarm():
    speak("Hi, I am your alarm assistant")
    speak("so , when do you want me ringing for you ?")
    not_executed = 1

    while(not_executed):
	dt = list(time.localtime())
	hour = dt[3]
	minute = dt[4]
        speak("say hours...")
	hours_input = recordNumbers()
        file = open("alarm_hours.alarm")
        file.write(hours_input)
        file.close()
        speak("say minutes...")
	minutes_input = recordNumbers()
        file = open("alarm_minutes.alarm")
        file.write(minutes_input)
        file.close()

        speak("alarm is been set")
        speak("i will ring for you at specified time")
        file1 = open("alarm_hours.alarm", "r")
        a = file1.read()
        b = int(a)
        
        file2 = open("alarm_minutes.alarm", "r")
        c = file2.read()
        d = int(c)
        
	if hour == b and minute == d: #this is the time for which you want the alarm
		os.system("omxplayer alarm_ringtone.mp3")
                file1.close()
                file2.close()
		not_executed = 0


                  
def notification():
        check_email()
        check_alarm()
        check_music()
        check_error()

def check_alarm():

    check1 = Path("alarm_hour.alarm")
    check2 = Path("alarm_minute.alarm")
    hour = open("alarm_hour.alarm" , "r")
    minute = open("alarm_minute.alarm", "r")
    if check1.is_file():
        if check2.is_file():
            speak("There is an alarm set for time, " + hour + " hours " + minute + " minutes ")

    else:
        speak("no alarm is been set")
    
def check_email():
    mail = imaplib.IMAP4_SSL('imap.gmail.com',993)
    unm = username
    pwd = password
    mail.login(unm,pwd)
    mail.list()
    
    mail.select('Inbox')

    result, data = mail.search(None, "ALL")

    ids = data[0]
    id_list = ids.split()
    latest_email_id = id_list[-1]

    result, data = mail.fetch(latest_email_id, "(RFC822)")

    raw_email = data[0][1]

    if raw_email != None:
        print(raw_email)
        speak(raw_email)

    else:
        speak("There are no unread emails yet. Better luck next time")

    mail.logout()
    mail.close()

def email_send():

    server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    try:
        server.login(username, password)
    except Exception:
        print(Exception)
        speak("can't connect to the server")
    
    speak("to whom ?")
    send_to = recordAudio()
    file = open("contacts.contact" , "r")
    contacts = set(file.read().split)
    reciever = contacts.intersection(send_to)
    get_reciever_id = str(object = "contact_" + reciever + ".contact")
    file = open(get_reciever_id, "r")
    reciever_id = file.read()
    msg = recordAudio()
    server.sendmail(username, reciever_id, msg)
    server.quit()

def paper_read():
    os.system("raspistill -sh 50 -co 100 -br 60 -o paper_read.jpg")
    speak("reading information")
    os.system("tesseract paper_read.jpg paper_read.tts")
    file = open("paper_read.tts", "r")
    data = file.read()
    if data != None:
        speak("following text is written")
        speak(data)

    else:
        speak("i don't understand what is written")

def optica(case):
    
    if "how" in case:
        if "are" in case:
            if "you" in case:
                speak("I am fine")
 
    if "time" in case:
        speak(ctime())
        
    if "what" in case:
        if "name" in case:
            if "your" in case:
                speak("my  name is optica")
            if  "my" in case:
                speak("your name is tejas")
        if "notifications" in case:
            notification()
        if "updates" in case:
            notification()
        if "written" in case:
            paper_read()

    if "are" in case:
        if "updates"in case:
            notification()

    if "check" in case:
        if "alarm" in case:
            check_alarm()
        if "emails" or "mails" in case:
            check_email()
    
    if "repeat" in case:
        speak("i can repeat your speech of 10 seconds")
        os.system("start repeat_after_me.py")
    
    if "goodbye" in case:
        speak("i will be leaving in a minute. if you want me to stay, then, just say cancel shutdown")
        os.system("sudo shutdown")
    
    if "cancel" in case:
        if "shutdown" in case:
            os.system("sudo shutdown -c")
            speak("i am back. what can i do for you")

    if "read" in case:
        paper_read()

    if "send" in case:
        if "email" in case:
            os.system("python contacts.py");
            file = ("contacts.contact_operator", "r")
            contacts = set(file.read().split())
            reciever = contacts.intersection(case)
            if reciever != None:
                reciever_id = "contact_" + reciever
                file = open(reciever_id, "r")
                server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
                server.login(my_id, my_pass)
                speak("say your message for " + reciever)
                msg = recordAudio()
                server.sendmail(my_id, my_pass, msg)
                server.logout()
                server.quit()
                os.system("rm -f contacts.contact_operator")
                os.system("rm -f contact_*")
                
            else:
                break

    if "image" in case:
        if "audio" in case:
            os.system("sh ita.sh")

    if "help" in case:
        #if "list" in case:
        speak("Now listing out all the features accessible in optica.")
        time.sleep(1)
        speak("Say image to audio for convert ")
        time.sleep(1)
        speak("Say S O S in case of emergency")
        time.sleep(1)
        speak("Say compose email to send Email")
        time.sleep(1)
        speak("Say Set Alarm to Use Alarm")
        time.sleep(1)
        speak("Say Audio Book to play some nice sample AudioBook")
        time.sleep(1)
        speak("Say music player to listen some trending Music")
        time.sleep(1)
        speak("Say goodbye to poweroff optica")
        
    #else:
         #speak("sorry i didn't understand that")
        
# initialization
time.sleep(1)
speak("Introduction Blah Blah")
print("[Introduction]")
while 1:
    init = recordAudio()

    if "optica" in init:
        say("yes sir")
        case = recordAudio()
        optica(case)

    else:
        speak("say, optica, to activate voice command")
