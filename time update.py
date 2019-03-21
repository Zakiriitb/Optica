import os

os.system("sudo apt-get install rdate")
os.system("rdate -n -4 -p time-a.nist.gov")

#os.system("sudo rdate -n -4 time-a.nist.gov") 