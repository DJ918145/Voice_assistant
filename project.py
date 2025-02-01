
import speech_recognition as sr  # type: ignore #speech
import pyttsx3                   # type: ignore #for speaking
import whatde as wp              #for sending whatsapp message
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
# for jokes
import pyjokes
# for fact
import randfacts as fact
# for notes
from notes import note
# for weather
import weather
# for nlp 
import spacy

one_time_password = ""
lang = "en"
trans = Translator()
nlp = spacy.load("en_core_web_sm")
engine = pyttsx3.init()  # Initialized once globally

def detect_language(text):
    # Detect the language 
    detection = trans.detect(text) 
    return detection.lang 

def transla(text, dest='en'):
    global lang 
    lang = detect_language(text)
    trans1 = trans.translate(text, lang)
    return trans1.text
    
def song(query):
    query = query.split()
    ans = " ".join(query[query.index('play')+1:])  # Extract query after "play"
    results = YoutubeSearch(ans, max_results=10).to_dict()
    url = results[0]['id']
    url = "https://www.youtube.com/watch?v=" + url
    wb.open(url)

def ev(er):
    global one_time_password
    es = 'dj20101004@gmail.com'
    epw = 'wqdj xtan coeo dtmx'
    subject = "Jarvis Verification"
    otp = ''.join(str(rd.randint(0, 9)) for _ in range(6))
    body = f"otp is : {otp}"
    em = EmailMessage()
    em['From'] = es
    em['To'] = er
    em['Subject'] = subject
    em.set_content(body)

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
        smtp.login(es, epw)
        smtp.sendmail(es, er, em.as_string())
    one_time_password = otp
    return otp

def extract_city(text):
    doc = nlp(text)
    for ent in doc.ents:
        if ent.label_ == "GPE":  # "GPE" refers to a geographic location (city, country)
            return ent.text
    return None

def weather(query):
    city = extract_city(query)
    if city:
        speak(weather.weather(city))
    else:
        speak("Sorry, I couldn't detect the city for weather information.")

def speak(text):
    text = transla(text, lang)
    engine.setProperty('voice', r'HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-US_DAVID_11.0')
    print(f"\n==> Jarvis AI: {text}\n")
    engine.say(text)
    engine.runAndWait()
    
def sinput():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening..........")
        r.pause_threshold = 1
        try:
            audio = r.listen(source, 0, 8)
            print("Recognizing.................")
            query = r.recognize_google(audio, language="auto")
            query = transla(query)
            return query.lower()
        except sr.UnknownValueError:
            return "Sorry, I could not understand that."
        except sr.RequestError:
            return "Sorry, there was an error with the speech service."

def making_notes():
    speak("Do you want to read a previous note or create a new project note?")
    choice = sinput()
    if "new" in choice:
        speak("What is the name of the project?")
        name = sinput()
        note("new", name)
    else:
        speak("Which note do you want to read?")
        name = sinput()
        note("read", name)

def main():
    speak("Hey, Jarvis 1.0 is online. What's your name?")
    uname = sinput()
    if uname == "":
        uname = input("Enter your name: ")

    if database1.check_user(uname):
        speak("Welcome back!")
        for _ in range(3):
            pw = input("Enter password: ")
            if database1.check_password(uname) == pw:
                break
            else:
                speak("Incorrect password. Try again.")
    else:
        new_entry()

    speak(f"Hello {uname}! How can I assist you today?")
    while True:
        query = sinput()
        if 'headlines' in query or 'news' in query:
            ans = nd.fn()
            speak("In which language would you like to hear the news?")
            lang = sinput()
            ans = transla(ans, lang)
            for item in ans:
                speak(item)
        elif 'note' in query or 'notes' in query:
            making_notes()
        elif 'whatsapp' in query or 'message' in query:
            wp.what(query)
        elif 'joke' in query or 'funny' in query:
            speak(pyjokes.get_joke())
        elif 'fact' in query:
            speak(fact.get_fact())
        elif 'weather' in query:
            weather(query)
        elif 'play' in query:
            song(query)
        elif 'bye' in query or 'shutdown' in query:
            speak("Goodbye! Have a great day.")
            break

if __name__ == "__main__":
    main()
