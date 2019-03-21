import os
from gtts import gTTS

os.system("arecord -D plughw:1,0 -f dat --duration=10 repeat_after_me_in.wav")
os.system("ffmpeg -i in.wav -ar 16000 -ac 1 repeat_after_me_in_converted.wav");
os.system("pocketsphinx_continuous -infile out.wav > repeat_after_me.temp");

filename = "/home/pi/Desktop/Tejas/New/repeat_after_me.temp"
file_read = open(filename, "r")
lines = file_read.read()
print(lines)
tts = gTTS("You said , " + lines, 'hi')
tts.save("output.mp3")

os.system("omxplayer output.mp3")

os.system("rm -f repeat_after_me_in.wav")
os.system("rm -f repeat_after_me_in_converted.wav")
os.system("rm -f repeat_after_me.temp")
os.system("rm -f repeat_after_me_result.mp3")
