import speech_recognition as sr  # type: ignore #speech
import pyttsx3                   # type: ignore #for speaking
import whatde as wp                    #for sending whatsapp message
import newsdec as nd             #for news 
import random as rd              #for random number
# for email verification
import smtplib
from email.message import EmailMessage
import ssl
# for translation 
from googletrans import Translator
# for youtube song 
from youtube_search import YoutubeSearch
import webbrowser as wb
# for database 
import database1

one_time_password = ""
lang = "en"

trans = Translator()

def detect_language(text):
    # Detect the language 
    detection = trans.detect(text) 
    return detection.lang 



def transla(text, dest='en'):
    global lang 
    lang = detect_language(text)
    trans1 = trans.translate(text,lang)
    return trans1.text
    
def song(query):
    query.split()
    ans = ""
    for i in range(len(query)):
        if query[i]=='play':
            query = query[i:]
    for i in query:
        ans = ans + query
            
    results = YoutubeSearch(ans, max_results=10).to_dict()
    url = results[0]['id']
    url = "https://www.youtube.com/watch?v="+url
    wb.open(url)


def ev(er):
    global one_time_password
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
    one_time_password = otp
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
                database1.user_info_database(uname = name, email=email, pw=pw)
                speak("Your account is created successfully")
                break
            else:
                speak("Verification code is incorrect")

#it was used for the speaking 
def speak(text):
    text = trans(text, lang)
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
        query = r.recognize_google(audio,language="auto")
        query = transla(query)
        return query.lower()
    
    except:
        return ""

def main():
    start = 0
    choice = 0
    count = 0
    if start == 0:
        speak("hii sir i am jarvis 1 point 0")
        speak("Sir can you please tell me ur good name ")
        uname = sinput()
        if uname == "":
            uname = input("ENter teh name : ")
        if database1.check_user(uname):
            speak("Welcome back sir")
            while choice == 0 and count < 3:
            # speak("Enter the password")
                count = count + 1
                pw = input("PASSWORD : ")
                if database1.check_password(uname) == pw:
                    pass
                else:
                    speak("Incorrect password")
                    speak("If you want to update ur password then enter 1 else enter 0")
                    choice = sinput()
                    if choice == 1:
                        ev(database1.getemail(uname))
                        speak("Enter the otp : ")
                        if input("OTP : ") == one_time_password:
                            speak("Enter new Password")
                            pw = input("New PassWord")
                            con_pw = input("Confirm PassWord")
                            if pw == con_pw:
                                database1.update_password(uname, pw)
                if count == 2:
                    choice = 1
                
    else:
        new_entry()
    wish = "welcome mister" + uname
    speak(wish )
    speak("How can i help you today ?")
    query = sinput()
    if 'headlines' in query or 'news' in query:             
        ans = nd.fn()
        speak("Sir in which language you want to listen the news : ")
        lang = sinput()
        ans = trans(ans, lang)
        for i in ans:
            speak(i)
    elif 'whatsapp' in query or 'message' in query:
        wp.what(query)
    elif 'play' in query:
        song(query)
    elif 'bye' in query or 'shutdown' in query:
        exit()


if __name__ == "__main__":
    main()
