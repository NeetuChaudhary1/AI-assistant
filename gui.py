import tkinter as tk
from tkinter import scrolledtext, simpledialog
import threading
import speech_recognition as sr
import pyttsx3
import webbrowser
import os
import time
import datetime
import smtplib
import requests
from pywikihow import search_wikihow
import PyPDF2
import psutil
import speedtest
import instaloader
import pyautogui
import cv2
from requests import get
import pywhatkit as kit
import pyjokes

def say(text): 
    output_text.insert(tk.END, text + "\n")
    output_text.see(tk.END)
    engine = pyttsx3.init()
    voices=engine.getProperty('voices')
    engine.setProperty('voice',voices[0].id) 
    engine.setProperty('rate', 200)
    engine.say(text)
    engine.runAndWait()
    
def wish():
    hour = int(datetime.datetime.now().hour)
    say("Happy Guru Purnima")
    if hour >= 0 and hour <= 12:
        say("Good Morning")
    elif hour > 12 and hour < 18:
        say("Good Afternoon")
    else:
        say("Good Evening")
    say("I am your assistant sir. please tell me how can i help you") 

def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        output_text.insert(tk.END, "Listening...\n")
        output_text.see(tk.END)
        r.pause_threshold = 1
        audio = r.listen(source)
    try:
        output_text.insert(tk.END, "Recognizing...\n")
        output_text.see(tk.END)
        query = r.recognize_google(audio, language='en-in')
        output_text.insert(tk.END, f"User said: {query}\n")
        output_text.see(tk.END)
        return query
    except Exception as e:
        return "some error occurred"

def send_email(subject, body, to_email):
    gmail = "neetuchaudhary059@gmail.com"
    password = "hxgy kldu qodu vrso"
    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(gmail, password)
            server.sendmail(gmail, to_email, f"Subject: {subject}\n\n{body}")
            return True
    except Exception as e:
        output_text.insert(tk.END, f"An error occurred: {e}\n")
        output_text.see(tk.END)
        return False    

def get_weather(api_key, city):
    base_url = "https://api.openweathermap.org/data/2.5/weather"
    params = {'q': city, 'appid': api_key, 'units': 'metric'}
    response = requests.get(base_url, params=params)
    if response.status_code == 200:
        data = response.json()
        temperature = data['main']['temp']
        description = data['weather'][0]['description']
        output_text.insert(tk.END, f'Temperature: {temperature}°C, Description: {description}\n')
        output_text.see(tk.END)
        say(f"Temperature is {temperature}")
    else:
        output_text.insert(tk.END, f'Error: {response.status_code}\n')
        output_text.see(tk.END)

def pdf_reader():
    try:
        book = open('Notes.pdf', 'rb')
        pdfReader = PyPDF2.PdfReader(book)
        pages = len(pdfReader.pages)
        say(f"Total number of pages in this book: {pages}")

        pg = int(get_input("Please enter the page number: "))
        
        if pg < 0 or pg >= pages:
            output_text.insert(tk.END, "Invalid page number. Please enter a valid page number.\n")
            output_text.see(tk.END)
            return
        
        while True:
            page = pdfReader.pages[pg]
            text = page.extract_text()
            say(text)
            pg += 1
    
    except FileNotFoundError:
        say("The specified PDF file was not found.")
    except PyPDF2.errors.PdfReadError:
        say("The PDF file could not be read.")
    except Exception as e:
        output_text.insert(tk.END, f"An error occurred: {e}\n")
        output_text.see(tk.END)
        say("An error occurred while reading the PDF file.")

def get_input(prompt):
    return simpledialog.askstring("Input", prompt)

def main(query):
    if "open youtube".lower() in query.lower():
        say("Opening YouTube sir...")
        webbrowser.open("https://www.youtube.com")
    elif "open wikipedia".lower() in query.lower():
        say("Opening Wikipedia sir...")
        webbrowser.open("https://www.wikipedia.com")
    elif "open google".lower() in query.lower():
        say("Opening Google sir...")
        webbrowser.open("https://www.google.com")
    elif "the time".lower() in query.lower():
        strfTime = datetime.datetime.now().strftime("%H:%M:%S")
        say(f"Sir the time is {strfTime}")
    elif "send an email".lower() in query.lower():
        say("Please say the email subject.")
        subject = takeCommand()
        say("Please say the email body.")
        body = takeCommand()
        to_email = "kinguniyal1311@gmail.com"
        success = send_email(subject, body, to_email)
        if success:
            say("Email sent successfully!")
        else:
            say("There was an error sending the email. Please check your credentials.")
    elif "give me weather update".lower() in query.lower():
        api_key = "0ff352134f91d97a673f1e44270286be"
        city = simpledialog.askstring("City", "Enter the city:")
        root.after(0, get_weather, api_key, city)
    elif "no thanks".lower() in query.lower():
        say("thanks for using me sir, have a good day")
        exit()
    elif "activate how to do mod".lower() in query.lower():
        say("How to do mod is activated")
        while True:
            say("Please tell me what you want to know")
            how = takeCommand()
            try:
                if "exit".lower() in how or "close".lower() in how.lower():
                    say("Ok sir, how to do mode is closed")
                    break
                else:
                    max_results = 1
                    how_to = search_wikihow(how, max_results)
                    assert len(how_to) == 1
                    how_to[0].print()
                    say(how_to[0].summary)
            except Exception as e:
                say("Sorry sir, I am not able to find this")
    elif "read pdf".lower() in query.lower():
        pdf_reader()
    elif "how much power left".lower() in query or "how much power we have".lower() in query.lower() or "battery".lower() in query.lower():
        battery = psutil.sensors_battery()
        percentage = battery.percent
        say(f"Sir our system has {percentage} percent battery")
        if percentage >= 75:
            say("We have enough power to continue our work")
        elif percentage >= 40 and percentage <= 75:
            say("We should connect our system to a charging point to charge our battery")
        elif percentage <= 15 and percentage <= 30:
            say("We don't have enough power to work, please connect to charging")
        elif percentage <= 15:
            say("We have very low power, please connect to charging, the system will shutdown very soon")
    elif "internet speed".lower() in query.lower():
        st = speedtest.Speedtest()
        dl = st.download()
        up = st.upload()
        say(f"Sir we have {dl} bits per second downloading speed and {up} bits per second uploading speed")
    
    elif "instagram profile".lower() in query.lower() or "profile on instagram".lower() in query.lower():
        say("Sir please enter the username correctly")
        name = get_input("Enter username here:")
        webbrowser.open(f"www.instagram.com/{name}")
        say(f"Sir here is the profile of user {name}")
        time.sleep(5)
        say("Sir would you like to download the profile picture of this account")
        condition = get_input("Enter yes/no:")
        if "yes".lower() in condition.lower():
            mod = instaloader.Instaloader()
            mod.download_profile(name, profile_pic_only=True)
            say("I am done sir, profile picture is saved in our main folder")
    elif "take screenshot".lower() in query.lower() or "take a screenshot" in query.lower():
        say("Sir, please tell me the name for this screenshot file")
        name = takeCommand().lower()
        say("Please sir hold the screen for few seconds, I am taking screenshot")
        time.sleep(3)
        img = pyautogui.screenshot()
        img.save(f"{name}.png")
        say("I am done sir, the screenshot is saved in our main folder")
    elif "open onenote".lower() in query.lower():
        npath="C:\\ProgramData\\Microsoft\\Windows\\Start Menu\\Programs\\OneNote"  
        os.startfile(npath)
    elif "open command prompt".lower() in query.lower():
        os.system("start cmd") 
    elif "open camera".lower() in query.lower():
        cap=cv2.VideoCapture(0)
        while True:
            ret, img=cap.read()
            cv2.imshow('webcam',img)
            k=cv2.waitKey(50)
            if k==27:
                break
        cap.release()
        cv2.destroyAllWindows() 
    elif "ip address".lower() in query.lower():
        ip=get('https://api.ipify.org').text
        say(f"your ip address is {ip}")
    elif "send message".lower() in query.lower():
        try:
            say("tell the phone number (including country code):")
            num = takeCommand()
            time.sleep(5)
            say("tell your message:")
            mssg = takeCommand()
            say("tell hour (in 24-hour format):")
            h = int(takeCommand())
            say("tell  minute:")
            m = int(takeCommand())
            kit.sendwhatmsg(num, mssg, h, m)
            say("Message scheduled successfully!")
        except ValueError:
            print("Error: Please enter valid numeric values for hour and minute.")
        except Exception as e:
            print(f"An error occurred: {e}")
            print("Failed to send the message.")
    elif "play songs on youtube".lower() in query.lower():
        say("tell your song name")
        song=takeCommand()
        say("wait for sometime...")
        kit.playonyt(song) 
        say("song played sucessfully")
    elif "tell me a joke".lower() in query.lower():
        joke=pyjokes.get_joke()
        say(joke)
    elif "volume up".lower() in query.lower():
        pyautogui.press("volumeup")
    elif "volume down".lower() in query.lower():
        pyautogui.press("volumedown")
    elif "volume mute".lower() in query.lower():
        pyautogui.press("volumemute")        

    else:
        say("Sorry something went wrong")

def start_listening():
    wish()
    while True:
        query = takeCommand()
        if query:
            root.after(0, main, query)

def on_run():
    listening_thread = threading.Thread(target=start_listening)
    listening_thread.start()

def on_exit():
    root.destroy()

root = tk.Tk()
root.title("Voice Assistant")

command_label = tk.Label(root, text="Enter Command:",bg="black",fg="white",font="white")
command_label.pack()

run_button = tk.Button(root, text="Run", command=on_run)
run_button.pack()

exit_button = tk.Button(root, text="Exit", command=on_exit)
exit_button.pack()

output_text = scrolledtext.ScrolledText(root, height=20, width=100)
output_text.pack()

root.mainloop()
