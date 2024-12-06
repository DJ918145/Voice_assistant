import speech_recognition as sr  # type: ignore #speech
import pyttsx3                   # type: ignore #for speaking
import whatde                    #for sending whatsapp message
import newsdec as nd             #for news 
import random as rd              #for random number
# for email verification
import smtplib
from email.message import EmailMessage
import ssl
# for translation 
from googletrans import Translator

def trans(text, dest = "hi", src = "en"):
    trans = Translator()
    trans1 = trans.translate(text, src="en", dest="hi")
    return trans1.text
    

user = {
    "admin" : "admin"
}

def ev(er):
    es = 'dj20101004@gmail.com'
    # er = 'dhruvjainmyself@gmail.com'
    epw = 'wqdj xtan coeo dtmx'

    subject = "Jarvis Verification"
    otp = ""
    for i in range(6):
        otp += str(rd.randint(0, 9))
    body = """
        otp is : 
    """
    body = body + otp

    em = EmailMessage()
    em['From'] = es
    em['To'] = er
    em['Subject'] = subject
    em.set_content(body)

    context = ssl.create_default_context()

    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context= context) as smtp:
        smtp.login(es, epw)
        smtp.sendmail(es, er, em.as_string())
    
    return otp


#it was usefull for the creating the new account
def new_entry(): 
    speak("Hello sir can you please fill below things : ")
    name = input("Enter Your name : ")
    pw = input("Enter the Password : ")
    cpw = input("Renter the Password for confirmation : ")
    if pw == cpw:
        email = input("Enter the Email id for confirmation your account : ")
        # email verification 
        code = ev(email)
        speak("Please enter the verification code : ")
        while True:
            vcode = input("Enter the verification code : ")
            if vcode == code:
                user[name] = pw
                speak("Your account is created successfully")
                break
            else:
                speak("Verification code is incorrect")

#it was used for the speaking 
def speak(text):
    engine = pyttsx3.init()
    id =  r'HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-US_DAVID_11.0'
    engine.setProperty('voice',id)
    print("")
    print(f"==> Jarvis AI : {text}")
    print("")
    engine.say(text=text)
    engine.runAndWait()
    
#it was doing work ear of our project
def sinput():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening..........")
        r.pause_threshold = 1
        audio = r.listen(source,0,8)

    try:
        print("Recognizing.................")
        query = r.recognize_google(audio,language="en")
        return query.lower()
    
    except:
        return ""

def main():
    start = 0
    if start == 0:
        speak("hii sir i am jarvis 1 point 0")
        speak("Sir can you please tell me ur good name ")
        uname = sinput()
        users_name = user.keys()
        if uname in users_name:
            speak(f"Welcome {uname} sir")
            while True:
                speak("Enter the password")
                password = input()
                if password != user[uname]:
                    speak("Incorrect password")
                    speak("Sir if you forgot the password then tell yes or retry with old password then tell no ")
                    pchoice = sinput()
                    if pchoice == "yes":
                        speak("Sir please enter the email id :")
                        email = input()
                        # on the entered email send a forget password email.
                        break
                else:
                    break
        else:
            new_entry()
                
    ans = nd.fn()
    for i in ans:
        speak(i)
