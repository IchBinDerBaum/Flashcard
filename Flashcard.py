from tkinter import *
from tkinter import ttk, Frame
import os
import random
route = Tk()
Width = 990
Height = 620
X = route.winfo_screenwidth() // 2 - Width // 2
Y = route.winfo_screenheight() // 2 - Height // 2

route.geometry(f"{Width}x{Height}+{X}+{Y}")
route.title("Flashcard")
route.resizable(False, False)
route["bg"] = "Sky blue"

correctanswers = 0

def getLesson():
    files = os.listdir(path="sections")
    n = len(files)
    lessonlist = list(range(1, n +1))
    return lessonlist


def preparedlesson():
    global totalpoints
    try:
        numberlesson = number.get()
        Words = {}
        with open(f"sections/section{numberlesson}.txt", "r", encoding ="UTF-8") as f:
            for i in f:
                i = i.strip("\n")
                i = i.split(",")
                Words[i[0]] = i[1:]
        totalpoints = len(Words)
        return Words
    except:
        questionword.config(text = "Sorry, this section is empty")
        correctanswerlabel.config(text="")
        resultlabel.config(text="")
        return Words


def resetSession():
    preparedlesson()
    getMode()
    resultlabel.config(text = "")
    correctanswerlabel.config(text = "")
    newWord()
    resetbutton.config(text = "reset session")


def getMode():
    try:
        if mode.get == 1:
            newWord()
        elif mode.get == 2:
            preparedlesson()
            newExamWord()
    except:
        questionword.config(text="Sorry, this section is empty")
        correctanswerlabel.config(text="")
        resultlabel.config(text="")


def newExamWord():
    global Words, word
    word = random.choice(list(Words.keys()))
    questionword.config(text=word)


def examMode():
    global totalpoints, word, correctanswers
    if insertanswer.get() == ", ".join(Words[word]) or insertanswer.get() == ",".join(Words[word]) or insertanswer.get() == " ".join(Words[word]):
        correctanswers += 1
    elif insertanswer.get() in (Words[word]):
        correctanswers += 0.5
    del Words[word]
    print(Words)
    print(correctanswers)
    try:
        newExamWord()
    except:
        questionword.config(text = "Congratulations!")
        resultlabel.config(text = f"You have {round(correctanswers)}/{totalpoints} points!")
        resultlabel.place(x = 425, y = 290)
        correctanswerlabel.config(text = f"That is {round((correctanswers/totalpoints * 100),1)}%")
        correctanswerlabel.place(x = 445, y = 310)
        return


def checkAnswer():

    try:
        global Words, word
        if insertanswer.get() == ", ".join(Words[word]) or insertanswer.get() == ",".join(Words[word]) or insertanswer.get() == " ".join(Words[word]):
            resultlabel.config(text = "That's correct!")
            correctanswerlabel.config(text = "")
            resultlabel.place(x=455, y=290)
        elif insertanswer.get() in (Words[word]):
            resultlabel.config(text = f"You're right, but ")
            correctanswerlabel.config(text = ", ".join(Words[word]))
            resultlabel.place(x=450, y=290)
            b = len(", ".join(Words[word]))
            correctanswerlabel.place(x = 495 - b * 2.7, y = 310)
        else:
            resultlabel.config(text = f"Wrong! The correct answer is")
            correctanswerlabel.config(text = ", ".join(Words[word]))
            resultlabel.place(x = 425, y = 290)
            a = len(", ".join(Words[word]))
            correctanswerlabel.place(x = (495 - a * 2.7), y = 310)
    except:
        questionword.config(text = "Sorry, this section is empty")
        correctanswerlabel.config(text = "")
        resultlabel.config(text = "")


def enter(event = None):
    global word
    if mode.get() == 1:
        checkAnswer()
        newWord()
        insertanswer.delete(0, END)
    else:
        examMode()
        insertanswer.delete(0, END)
route.bind("<Return>", enter)


def newWord():
    try:
        global Words,word
        Words = preparedlesson()
        word = random.choice(list(Words.keys()))
        questionword.config(text = word)
    except:
        questionword.config(text="Sorry, this section is empty")
        correctanswerlabel.config(text="")
        resultlabel.config(text="")


frame = Frame(route, width = 330, height = 200, bd = 10, bg = "beige", relief = RIDGE)
frame.place(x = 330, y = 180)
insertanswer = Entry(route, bg = "Lavender Blush", width = 22)
insertanswer.place(x = 425, y = 410)
questionword = Label(route, bg = "beige", text = "Latin word", width = 20)
questionword.place(x = 425, y = 260)
resultlabel = Label(route, text = "", bg = "beige" , justify = LEFT, anchor = N)
resultlabel.place(x = 495, y = 290)
correctanswerlabel = Label(route, bg = "beige", text = "")
correctanswerlabel.place(x = 495, y = 310)
mode = IntVar()
mode.set(1)

LearnButton = Radiobutton(text = "Learn Mode",bg = "light blue", variable = mode, value = 1, command = getMode)
LearnButton.place(x = 200, y = 200)
ExamButton = Radiobutton(text = "Exam Mode", bg = "light blue", variable = mode, value = 2, command = getMode)
ExamButton.place(x = 200, y = 230)
SectionNumber = Label(route, text = "Choose the number of the section", bg = "light blue")
SectionNumber.place(x = 400, y = 100)

number = IntVar()
number.set(1)

section = ttk.Combobox(route, textvariable = number, value = getLesson())
section.place(x = 420, y = 130)
resetbutton = Button(route, text = "Start Session", bg = "light blue", command = resetSession)
resetbutton.place(x = 680, y = 190)
enterButton = Button(route, text = "Enter", bg = "light blue", command = enter)
enterButton.place(x = 585, y = 408)
getMode()
route.mainloop()
