import pyttsx3  # pip install pyttsx3
import speech_recognition as sr  # pip install speechRecognition
import datetime
import time
import wikipedia  # pip install wikipedia
import webbrowser
import os
#import openai #pip install openai
from threading import Thread
from dotenv import load_dotenv # pip install python-dotenv
from tkinter import *
from tkinter import ttk
import threading
import google.generativeai as genai #pip install google-generativeai 

learning = False
browser = 'browser'
if browser == 'firefox':
    browser_path = "C:\Program Files (x86)\Mozilla Firefox\\firefox.exe %s"
else:
    browser_path = "C:/Program Files (x86)/Google/Chrome/Application/chrome.exe %s"

# load_dotenv()
# try:
#     openai.api_key = os.getenv("keyy")
# except:
#     openai.api_key = input("input api key:")
load_dotenv()
try:
    genai.configure(api_key=os.getenv("gemini_api"))
except:
    genai.configure(api_key=input("Input API key:"))
gemini_generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

def writechat(*args):
    if type(args) is tuple:
        if learning:
            pr = open("chats/chat.txt", "a+")
            pr.writelines("".join(args))
            pr.close()
        tr = open("chats/trashed.txt", "a+")
        tr.writelines("".join(args))
        tr.close()
        cr = open("chats/current.txt", "a+")
        cr.writelines("".join(args))
        cr.close()

def readchat(file):
    pr = open(file, "r")
    l = pr.readlines()
    str1 = ""
    for ele in l:
        str1 += ele
    pr.close()
    return str1

# speak and append bot replies
def reply(reply):
    botmsg(reply)
    print(f"AI: {reply}")
    try:
        t1= threading.Thread(target=writechat,args=(f"\nAI: {reply}"))
        engine = pyttsx3.init('sapi5')
        voices = engine.getProperty('voices')
        engine.setProperty('voice', voices[0].id)
        engine.say(reply)
        t2= threading.Thread(target=engine.runAndWait)
        t1.start()
        t2.start()
    except:
        pass
    #t1.join()
    #t2.join()

# take inputs from console (unused now)
def takeCommand():
    query = input("User:")
    writechat(f"\nUser: {query}")
    return query

# extract responses from openai api
def openaii(prompt, chat = 'yes'):
    print("-------------Generative AI FUNCTION----------------")
    print("Generative AI prompt: "+prompt, "\nchat mode?:", chat)
    # if chat == 'yes':
    #     response = openai.Completion.create(engine="text-davinci-003",
    #                                      prompt=prompt,
    #                                      temperature=0.5,
    #                                      max_tokens=256,
    #                                      top_p=1,
    #                                      frequency_penalty=0,
    #                                      presence_penalty=0,
    #                                      stop=[" User:", " AI:"])
    # else:
    #     response = openai.Completion.create(engine="text-davinci-003",
    #                                      prompt=prompt,
    #                                      temperature=0.5,
    #                                      max_tokens=256,
    #                                      top_p=1,
    #                                      frequency_penalty=0,
    #                                      presence_penalty=0)
    # output1 = response['choices'][0]['text']
    # output = output1.strip()
    model = genai.GenerativeModel(model_name="gemini-1.5-flash", generation_config=gemini_generation_config)
    chat_session = model.start_chat(history=[])
    response = chat_session.send_message(prompt)
    output = response.text.strip()
    if output.startswith("AI:"):
        output = output.replace("AI: ","")
    print ("Generative AI api output: "+output)
    print("-------------Generative AI FUNCTION END----------------")
    return output

# function to phrase urls and open in browser
def openurl(sweb):
    print("-------------URL OPENER FUNCTION----------------")
    reply(f"looking for {sweb}")
    prompt = readchat("chats/urls.txt")+f"\nUser:open{sweb}\n AI:"
    url = openaii(prompt, 'no')
    reply(f"opening {url} with {browser}")
    if learning:
        txt = open("chats/urls.txt", "a")
        txt.writelines(f"\nUser:open{sweb}\nAI:{url}")
        txt.close()
    webbrowser.open(url)
    print("-------------URL OPENER FUNCTION END----------------")

# main function to process user inputs
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
        webbrowser.open('https://open.spotify.com')
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

    elif 'the time' in query:
            strTime = datetime.datetime.now().strftime("%I:%M:%S %p")  
            reply(f"the time is {strTime}")
            return f"the time is {strTime}"
    
    elif "set alarm" in query or "remindme" in query or ('set' in query and 'alarm' in query):
        promptcmd="Act as function that takes a string as input and returns a list in the format `['for', 'HH:MM', reason]`, where 'HH:MM' is in 24-hour format. The input string will contain a time in the format 'HH:MM' or 'HH:MM am or pm' ( may not be 24-hour format) and a reason for a task, separated by a space. The function should extract the time and reason from the input string and return them as a list with the format mentioned above. Here's an example input and output:\n\nExample Input: \"13:45 Meeting with the team\"\nExample Output: ['for', '13:45', 'Meeting with the team']\n\nNote that the output should always start with the string 'for', followed by the extracted time and reason.\n\nInput: \"set alarm for 7:55pm eat\"\nOutput:  ['for', '19:55', 'eat']"
        apicmd = openaii(promptcmd+"\n\nInput: "+query+"\"\nOutput: ", 'no')
        words = apicmd.strip('[]').replace("'", "").split(', ')
        time_idx = words.index("for") + 1
        alarm_time_str = words[time_idx]
        alarm_time = time.strptime(alarm_time_str, "%H:%M")
        current_time = time.localtime()
        alarm_seconds = (alarm_time.tm_hour - current_time.tm_hour) * 3600 + \
                        (alarm_time.tm_min - current_time.tm_min) * 60 - \
                        current_time.tm_sec
        reason = " ".join(words[words.index("for")+2:])
        def alarm_callback():
            reply("ALARM GOES OFF!!! Reason: {} ".format(reason))
        timer = threading.Timer(alarm_seconds, alarm_callback)
        timer.start()
        reply("Alarm set for {}".format(alarm_time_str))

    else:
        chattxt = readchat("chats/chat.txt")
        currenttxtinp = readchat("chats/current.txt")
        # add a method to clean up the current.txt file if it gets too large
        if len(currenttxtinp) > 1000:
            currfile = open("chats/current.txt", "w")
            currfile.write("")
            currfile.close()
            currenttxt = ""
        else:
            currenttxt = currenttxtinp

        fpormpt=chattxt+currenttxt+f"\nUser: {query}\nAI:"
        gett= openaii(fpormpt, 'yes')
        reply(gett)
        return gett

# creating gui
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
    writechat(f"\nUser: {message}")
    
    
def botmsg(reply):
    chat_area.config(state='normal')
    chat_area.insert('end', '\n')
    response_widget = Label(frame, text="AI: "+reply, font=('Helvetica', 12), bg='blue', fg=fg_color,
                             anchor='w', justify='left', wraplength=250)
    response_widget.pack(side='top', pady=5, padx=10, fill='x', anchor='w')
    chat_area.window_create('end-1c linestart + 1line', window=response_widget)
    chat_area.config(state='disabled')
    chat_area.see('end')

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
    try:
        if hour>=3 and hour<12:
            reply("Good Morning!")

        elif hour>=12 and hour<18:
            reply("Good Afternoon!")   

        else:
            reply("Good Evening!")  

        reply("I am your Windows Assistant. Please let me know how may I help you")
    except:
        pass

wishMe()

while True:
    try:
        root.mainloop()
    except:
        continue