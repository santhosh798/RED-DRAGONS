# ==============================
# LearnSphere - AI Personalized Tutor
# Single File Python System
# ==============================

import json
import os
import random
import pyttsx3
from colorama import Fore, Back, Style, init
from googletrans import Translator

init(autoreset=True)

translator = Translator()
engine = pyttsx3.init()

DATA_FILE = "student_memory.json"

# -------------------------------
# Memory System (Remembers User)
# -------------------------------

def load_memory():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return {}

def save_memory(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

memory = load_memory()

# -------------------------------
# Speech System
# -------------------------------

def speak(text):
    engine.say(text)
    engine.runAndWait()

def speak_line_by_line(lines):
    for line in lines:
        print(Fore.CYAN + line)
        speak(line)

# -------------------------------
# Language Translation
# -------------------------------

current_lang = "en"

def translate(text):
    if current_lang == "en":
        return text
    try:
        return translator.translate(text, dest=current_lang).text
    except:
        return text

# -------------------------------
# Themes
# -------------------------------

def set_theme():
    print("\nChoose Theme:")
    print("1. Blue (Technology)")
    print("2. Green (Learning)")
    print("3. Yellow (Energy)")
    ch = input("> ")

    if ch == "1":
        print(Back.BLUE + "Theme Applied!")
    elif ch == "2":
        print(Back.GREEN + "Theme Applied!")
    else:
        print(Back.YELLOW + "Theme Applied!")

# -------------------------------
# Lessons Database
# -------------------------------

lessons = {
"Python":{
"Variables":{
"content":[
"A variable stores data in a program.",
"In Python you do not need to declare type.",
"Example: x = 5"
],
"example":"x = 10\nname = 'John'\nprint(x,name)",
"quiz":[
("Which symbol assigns value?","="),
("Is Python typed strictly?","no")
]
},

"Loops":{
"content":[
"Loops repeat code multiple times.",
"For loop is used when count is known.",
"While loop runs until condition fails."
],
"example":"for i in range(5):\n    print(i)",
"quiz":[
("Which loop repeats fixed times?","for"),
("Which loop checks condition?","while")
]
}
},

"Java":{
"Variables":{
"content":[
"Java variables must declare type.",
"int stores integers.",
"String stores text."
],
"example":"int x=5;\nString name=\"Sam\";",
"quiz":[
("Which type stores text?","string"),
("Java is typed?","yes")
]
}
}
}

# -------------------------------
# Student Setup
# -------------------------------

def register():
    print(Fore.GREEN + "Welcome to LearnSphere AI Tutor")
    name = input("Enter your name: ")

    if name in memory:
        print(Fore.YELLOW + f"Welcome back {name}!")
        return name

    memory[name] = {
        "language":"Python",
        "progress":{},
        "score":0
    }
    save_memory(memory)
    return name

# -------------------------------
# Choose Programming Language
# -------------------------------

def choose_language(user):
    print("\nChoose Programming Language:")
    for i,lang in enumerate(lessons.keys()):
        print(i+1,lang)

    ch=int(input("> "))
    lang=list(lessons.keys())[ch-1]
    memory[user]["language"]=lang
    save_memory(memory)

# -------------------------------
# Teach Topic
# -------------------------------

def teach(user):
    lang=memory[user]["language"]
    topics=lessons[lang]

    for topic in topics:
        print(Fore.MAGENTA + f"\n--- {topic} ---")

        lines=[translate(line) for line in topics[topic]["content"]]

        # Ask audio
        aud=input("Do you want audio explanation? (y/n): ")
        if aud=="y":
            speak_line_by_line(lines)
        else:
            for line in lines:
                print(Fore.CYAN+line)

        print(Fore.GREEN+"\nExample:")
        print(topics[topic]["example"])

        quiz(user,topic,topics[topic]["quiz"])

# -------------------------------
# Quiz System
# -------------------------------

def quiz(user,topic,questions):
    print(Fore.YELLOW+"\nQuiz Time!")

    correct=0
    for q,a in questions:
        ans=input(q+" : ").lower()
        if ans==a:
            print("Correct!")
            correct+=1
        else:
            print("Wrong! Correct:",a)

    score=int((correct/len(questions))*100)
    memory[user]["progress"][topic]=score
    memory[user]["score"]+=score
    save_memory(memory)

    if score<50:
        print(Fore.RED+"You are weak in this topic. AI will repeat later.")
    else:
        print(Fore.GREEN+"Good! Moving ahead.")

# -------------------------------
# Study Plan Generator
# -------------------------------

def study_plan(user):
    weak=[]
    for t,s in memory[user]["progress"].items():
        if s<50:
            weak.append(t)

    print(Fore.CYAN+"\nYour Study Plan:")
    if weak:
        print("Revise:",",".join(weak))
    else:
        print("You are doing great!")

# -------------------------------
# Main
# -------------------------------

def main():
    set_theme()
    user=register()

    print("\nSelect Language (UI):")
    print("1 English")
    print("2 Tamil")
    global current_lang
    ch=input("> ")
    if ch=="2":
        current_lang="ta"

    choose_language(user)
    teach(user)
    study_plan(user)

    print(Fore.GREEN+"\nAI Motivation:")
    print("Keep learning! Small progress daily = Big success!")

if __name__=="__main__":
    main()