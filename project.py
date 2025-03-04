import requests
import re
import psutil
import os
import sympy as sp
import tweepy
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from datetime import datetime
import pyttsx3
import pyjokes
import random as rd
import smtplib
from email.message import EmailMessage
import ssl
import webbrowser as wb
from googletrans import Translator
# import spacy
import whatde as wp
import newsdec as nd
import randfacts as fact
from notes import note
import weather
import database1
import speech_recognition as sr
from youtube_search import YoutubeSearch
import webbrowser as wb
import song_recommandation as songr
import read_text as rt


# features..........
'''
1. weather forcasting 
2. notes using voice controll
3. system monitering
4. searching files and application
5. math solver
6. word translaiton
7. News Updating 
8. Whatsapp messaging via voice command 
9. Telling Jokes and Facts 

'''




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
    
def sinput():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening..........")
        r.pause_threshold = 1
        audio = r.listen(source,0,8)

    try:
        print("Recognizing.................")
        query = r.recognize_google(audio,language="auto")
        # query = transla(query)
        return query.lower()
    
    except:
        return ""
    
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

    

one_time_password = ""
lang = "en"
trans = Translator()
# nlp = spacy.load("en_core_web_sm")
engine = pyttsx3.init()  # Initialized once globally

# Weather Forecasting with More Details
def get_weather_details(city):
    api_key = "your_api_key"
    base_url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}"
    response = requests.get(base_url)
    data = response.json()
    if data["cod"] != "404":
        main_data = data["main"]
        weather_data = data["weather"][0]
        temperature = main_data["temp"]
        description = weather_data["description"]
        return f"The temperature in {city} is {temperature}°C with {description}."
    else:
        return "City not found."

# Voice-Controlled Notes App
def making_notes():
    speak("Do you want to read a previous note or create a new project note?")
    choice = sinput()
    if "new" in choice:
        speak("What is the name of the project?")
        name = sinput()
        speak("Tell me what to write in the note.")
        content = sinput()  # User dictates the content
        note("new", name, content)
    else:
        speak("Which note do you want to read?")
        name = sinput()
        note("read", name)

# System Monitoring
def system_monitor(query):
    if "cpu" in query:
        cpu_usage = psutil.cpu_percent()
        speak(f"CPU usage is {cpu_usage} percent.")
    elif "memory" in query:
        memory = psutil.virtual_memory()
        speak(f"Memory usage is {memory.percent} percent.")
    elif "disk" in query:
        disk = psutil.disk_usage('/')
        speak(f"Disk usage is {disk.percent} percent.")

# Search for Files/Applications
def search_files(query):
    if "search" in query or "find" in query:
        filename = query.split("find")[-1].strip()  # Extract the file name to search for
        files = [f for f in os.listdir() if filename.lower() in f.lower()]
        if files:
            speak(f"Found the following files: {', '.join(files)}")
        else:
            speak("No files found.")

# Music and Podcast Integration (Spotify)
def play_music(query):
    if "play" in query and "music" in query:
        song_name = query.split("play")[-1].strip()
        sp = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials(client_id="your_client_id", client_secret="your_client_secret"))
        results = sp.search(q=song_name, limit=1)
        song_url = results['tracks']['items'][0]['external_urls']['spotify']
        wb.open(song_url)
        speak(f"Playing {song_name} from Spotify.")

# Math and Unit Conversions
def solve_math(query):
    if "solve" in query or "calculate" in query:
        expression = query.split("calculate")[-1].strip()
        try:
            result = sp.sympify(expression)
            speak(f"The result is {result}.")
        except:
            speak("Sorry, I could not solve that.")

# Translate Voice Commands
def translate_command(query):
    if "translate" in query:
        lang_to_translate = query.split("to")[-1].strip()  # Get language
        text_to_translate = query.split("translate")[-1].strip()
        translated = trans.translate(text_to_translate, dest=lang_to_translate)
        speak(f"Translation: {translated.text}")

# Voice Recognition for Security
def voice_recognition_security(query):
    if "verify voice" in query:
        speak("Please say your secret passphrase.")
        secret_passphrase = "your_secret_passphrase"
        audio = sinput()  # Use the sinput method to capture the voice command
        if secret_passphrase.lower() in audio.lower():
            speak("Voice verified successfully!")
        else:
            speak("Voice verification failed.")

# Personalized Assistant
user_preferences = {}

def set_preference(query):
    if "favorite" in query:
        preference = query.split("favorite")[-1].strip()
        user_preferences['favorite'] = preference
        speak(f"Your favorite preference has been set to {preference}.")

def get_preference(query):
    if "favorite" in query:
        if 'favorite' in user_preferences:
            speak(f"Your favorite is {user_preferences['favorite']}.")
        else:
            speak("You haven't set any favorites yet.")

# AI-Based Task Recommendations
def recommend_task():
    current_hour = datetime.now().hour
    if 9 <= current_hour < 12:
        speak("I recommend you focus on your work today.")
    elif 12 <= current_hour < 18:
        speak("You can take a break now, or perhaps do some light work.")
    else:
        speak("It's evening. Relax and enjoy your time.")

def extract_city(query):
    city_patterns = [
        r'weather in ([a-zA-Z\s]+)',
        r'weather for ([a-zA-Z\s]+)',
        r'weather like in ([a-zA-Z\s]+)',
        r'how hot in ([a-zA-Z\s]+)',
        r'need an umbrella in ([a-zA-Z\s]+)',
        r'good weather for a picnic in ([a-zA-Z\s]+)',
        r'forecast for ([a-zA-Z\s]+)',
    ]

    for pattern in city_patterns:
        match = re.search(pattern, query)
        if match:
            city_name = match.group(1)
            return city_name.strip()

    # Default case if no patterns match
    print("City name not found in query.")
    return 

# Main Logic to Handle Queries
def weather(query):
    city = extract_city(query)
    if city:
        speak(get_weather_details(city))
    else:
        speak("Sorry, I couldn't detect the city for weather information.")
        
def song(query):
    songr.recommandation(query)
    
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
            speak(ans)
        elif 'note' in query or 'notes' in query:
            making_notes()
        elif 'read' in query:
            speak(rt.read_txt())
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
        elif "cpu" in query or "memory" in query or "disk" in query:
            system_monitor(query)
        elif "search" in query or "find" in query:
            search_files(query)
        elif "play music" in query:
            play_music(query)
        elif "calculate" in query or "solve" in query:
            solve_math(query)
        elif "translate" in query:
            translate_command(query)
        elif "verify voice" in query:
            voice_recognition_security(query)
        elif "favorite" in query:
            set_preference(query)
        elif "recommend" in query:
            recommend_task()

if __name__ == "__main__":
    main()
