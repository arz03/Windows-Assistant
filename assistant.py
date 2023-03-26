import pyttsx3  # pip install pyttsx3
import speech_recognition as sr  # pip install speechRecognition
import datetime
import wikipedia  # pip install wikipedia
import webbrowser
import os
import openai
from threading import Thread
from dotenv import load_dotenv
from tkinter import *
from tkinter import ttk

browser = 'firefox'
if browser == 'firefox':
    browser_path = "C:\Program Files (x86)\Mozilla Firefox\\firefox.exe %s"
else:
    browser_path = "C:/Program Files (x86)/Google/Chrome/Application/chrome.exe %s"

load_dotenv()
try:
    openai.api_key = os.getenv("keyy")
except:
    openai.api_key = input("input api key:")


def writechat(conv):
    pr = open("chats/chat.txt", "a+")
    pr.writelines(conv)
    pr.close()
    tr = open("chats/trashed.txt", "a+")
    tr.writelines(conv)
    tr.close()


def readchat(file):
    pr = open(file, "r")
    l = pr.readlines()
    str1 = ""
    for ele in l:
        str1 += ele
    pr.close()
    return str1


def reply(reply):
    botmsg(reply)
    print(f"AI: {reply}")
    writechat(f"\nAI: {reply}")
    engine = pyttsx3.init('sapi5')
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[0].id)
    engine.say(reply)
    # engine.runAndWait()



def takeCommand():
    query = input("User:")
    writechat(f"\nUser: {query}")
    return query


def openaii(prompt):
    response = openai.Completion.create(engine="text-davinci-003",
                                         prompt=prompt,
                                         temperature=0.5,
                                         max_tokens=150,
                                         top_p=1,
                                         frequency_penalty=0,
                                         presence_penalty=0.6,
                                         stop=[" User:", " AI:"])
    output1 = response['choices'][0]['text']
    output = output1.strip()
    return output


def openurl(sweb):
    reply(f"looking for{sweb}")
    prompt = readchat("chats/urls.txt")+f"\nUser:open{sweb}\n AI:"
    url = openaii(prompt)
    reply(f"opening {url} with {browser}")
    txt = open("chats/urls.txt", "a")
    txt.writelines(f"\nUser:open{sweb}\nAI:{url}")
    txt.close()
    webbrowser.get(browser_path).open(url)


def processs(query):
    print(f"User:{query}")
    # Logic for executing tasks based on query
    if 'wikipedia' in query:
        reply('Searching Wikipedia...')
        query = query.replace("wikipedia", "")
        results = wikipedia.summary(query, sentences=2)
        reply("According to Wikipedia")
        reply(results)
        return results

    elif 'open paint' in query:
        path = 'C:\Windows\system32\mspaint.exe'
        reply("opening ms paint")
        os.startfile(path)
        return "opening ms paint"

    elif 'open firefox' in query:
        path = "C:\Program Files (x86)\Mozilla Firefox\firefox.exe"
        reply("opening firefox")
        os.startfile(path)
        return "opening firefox"

    elif 'play music' in query:
        reply(f'opening spotify in {browser}')
        webbrowser.get(browser_path).open('open.spotify.com')
        return f'opening spotify in {browser}'

    # elif 'open youtube' in query:
    # webbrowser.open("https://youtube.com")
    # webbrowser.get(browser_path).open("http://youtube.com")
    # openurl("youtube")

    elif query == 'quit':
        reply("please close app manually.")
        return "please close app manually."

    elif 'open' in query:

        query = query.replace("open", "")
        openurl(query)
        return "processing..."

    else:
        gett= openaii("The following is a conversation with an AI assistant. The assistant is helpful, creative, clever, and very friendly.\n\nUser: Hello, who are you?\nAI: I am your Windows Assistant created by Arjun Sarje. How can I help you today?\nHuman: "+query+"\nAI:")
        reply(gett)
        return gett



root = Tk()
root.geometry('800x600')  # set initial window size

root.title('Windows Assistant')

# define the dark theme colors
bg_color = '#222222'
fg_color = '#FFFFFF'
button_color = '#444444'
button_hover_color = '#555555'
button_active_color = '#333333'

# create a resizable frame
frame = Frame(root, bg=bg_color)
frame.pack(fill='both', expand=True)

# create a chat area
chat_area = Text(frame, state='disabled', bg=bg_color, fg=fg_color)
chat_area.pack(fill='both', expand=True)

# create a message bar
style = ttk.Style()
style.configure('TEntry', background='white', foreground='black', bordercolor='blue',
                borderwidth=2, relief='ridge', padding=5, focuscolor='light blue')
message_bar = ttk.Entry(frame, style='TEntry')
message_bar.pack(side='left', fill='x', expand=True)

def audi():
    #It takes microphone input from the user and returns string output
    r = sr.Recognizer()
    with sr.Microphone() as source:
        reply("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source)
    try:
        reply("Recognizing...")    
        query = r.recognize_google(audio, language='en-in')
        engine = pyttsx3.init('sapi5')
        voices = engine.getProperty('voices')
        engine.setProperty('voice', voices[0].id)
        engine.say(f"User said: {query}\n")
        engine.runAndWait()
        processs(query)
    except Exception as e:
        print(e)    
        reply("Try again...")  
        return "None"

def usermsg():
    message = message_bar.get()
    message_bar.delete(0, 'end')
    chat_area.config(state='normal')
    chat_area.insert('end', '\n')
    message_widget = Label(frame, text="You: "+message, font=('Helvetica', 12), bg='blue', fg=fg_color,
                           anchor='e', justify='right', wraplength=250)
    message_widget.pack(side='top', pady=5, padx=10, fill='x', anchor='e')
    chat_area.window_create('end', window=message_widget)
    chat_area.config(state='disabled')
    processs(message)
    
def botmsg(reply):
    chat_area.config(state='normal')
    chat_area.insert('end', '\n')
    response_widget = Label(frame, text="AI: "+reply, font=('Helvetica', 12), bg='blue', fg=fg_color,
                             anchor='w', justify='left', wraplength=250)
    response_widget.pack(side='top', pady=5, padx=10, fill='x', anchor='w')
    chat_area.window_create('end-1c linestart + 1line', window=response_widget)
    chat_area.config(state='disabled')


# create a 'Send' button
send_button = Button(frame, text='Send', command=usermsg, bg=button_color, fg=fg_color,
                     activebackground=button_active_color, activeforeground=fg_color,
                     highlightbackground=bg_color, highlightcolor=button_hover_color,
                     highlightthickness=1, relief='flat')
send_button.pack(side='left', padx=5)

# bind the 'Return' key to send a message
message_bar.bind('<Return>', lambda event: usermsg())

# function to toggle the dark theme
def toggle_theme():
    bg = bg_color if frame['bg'] == fg_color else fg_color
    fg = fg_color if frame['bg'] == bg_color else bg_color
    frame.config(bg=bg)
    chat_area.config(bg=bg, fg=fg)
    message_bar.config(foreground='black', focuscolor='light blue')
    send_button.config(bg=button_color if bg == bg_color else fg_color,
                       fg=fg_color if bg == bg_color else bg_color,
                       activebackground=button_active_color if bg == bg_color else button_color,
                       activeforeground=fg_color if bg == bg_color else bg_color,
                       highlightbackground=bg, highlightcolor=button_hover_color,
                       highlightthickness=1)

# create a button to toggle the theme
theme_button = Button(frame, text='Toggle Theme', command=toggle_theme, bg=button_color, fg=fg_color,
                      activebackground=button_active_color, activeforeground=fg_color,
                      highlightbackground=bg_color, highlightcolor=button_hover_color,
                      highlightthickness=1, relief='flat')
theme_button.pack(side='top', anchor='ne', padx=5, pady=5)
# audio button
audio_button = Button(frame, text='Audio Input', command=audi, bg=button_color, fg=fg_color,
                      activebackground=button_active_color, activeforeground=fg_color,
                      highlightbackground=bg_color, highlightcolor=button_hover_color,
                      highlightthickness=1, relief='flat')
audio_button.pack(side='left', padx=5)
def wishMe():
    hour = int(datetime.datetime.now().hour)
    if hour>=0 and hour<12:
        reply("Good Morning!")

    elif hour>=12 and hour<18:
        reply("Good Afternoon!")   

    else:
        reply("Good Evening!")  

    reply("I am your Windows Assistant. Please let me know how may I help you")

wishMe()
root.mainloop()
