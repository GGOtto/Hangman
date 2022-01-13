# Name: Hangman
# Author: G.G.Otto
# Date: 1/1/2021
# Version 1.0

from tkinter import *
import random

class HangmanButton(Canvas):
    '''represents a button for the game'''

    def __init__(self, master, game, letter):
        '''HangmanButton(master, game, letter) -> HangmanButton
        constructs the button'''
        width, height = 45,45
        Canvas.__init__(self, master, bg="blue", width=width, height=height, highlightthickness=0)
        
        self.master = game
        self.letter = letter

        # draw button
        self.create_oval(3,3,width-3,height-3,fill="#aaaaff",outline="blue",tag=("button","circle"))
        self.create_text(width/2,height/2+0.5,text=letter,font=("Arial",width//3),tag=("button","letter"))

        # command and button binding
        self.tag_bind("button", "<Button-1>", self.button_down)
        self.tag_bind("button", "<ButtonRelease-1>", self.button_up)

    def disable(self):
        '''HangmanButton.disable() -> None
        disables the hangman button'''
        self.tag_unbind("button", "<Button-1>")
        self.tag_unbind("button", "<ButtonRelease-1>")
        
    def button_down(self, event):
        '''HangmanButton.button_down() -> None
        performs the button down event'''
        self.itemconfigure("circle", fill="white")

    def button_up(self, event):
        '''HangmanButton.button_up() -> None
        performs the button up event'''
        self.itemconfigure("circle", fill="#ccccdd")
        self.disable()
        self.master.guess_letter(self.letter.lower())

class HangmanFigure(Canvas):
    '''represents the canvas for the figure'''

    def __init__(self, master, word):
        '''HangmanFigure(master, word) -> HangmanFigure
        constructs the canvas for the hangman figure'''
        Canvas.__init__(self, master, width=45*12, height=300, bg="#ddddff", highlightthickness=0)
        self.grid(row=0, column=0)

        # placeholders
        self.word = word
        self.letters = {}
        start = int(self["width"])/2-len(word)*15
        for letter in word:
            self.create_line(start+2.5,int(self["height"])-25,start+25,int(self["height"])-25,width=3)
            start += 30

            # add letters to dict
            if letter in self.letters:
                self.letters[letter].append(start-15)
            else:
                self.letters[letter] = [start-15]

        # body parts
        width, height = int(self["width"]), int(self["height"])
        self.bodyParts = [(width/2-25,50,width/2+25,100,"circle"), (width/2, 100, int(self["width"])/2, 180),
            (width/2, 120, width/2-35, 120), (width/2, 120, width/2+35, 120), (width/2, 179, width/2-35, 214),
            (width/2, 179, width/2+35, 214)]

        # number of guesses
        self.guesses = self.create_text(width-15, 18, text=6, font=("Arial", 15))
                          
    def get_letters(self):
        '''HangmanFigure.get_letters() -> dict
        returns all the letters left'''
        return self.letters

    def fill_letter(self, letter, color="black"):
        '''HangmanFigure.fill_letter(letter, color="black") -> None
        fills in the letter specified'''
        for pos in self.letters[letter]:
            self.create_text(pos,int(self["height"])-40,text=letter.upper(),font=("Arial",20),fill=color)
        self.letters.pop(letter)

    def draw_figure(self, guesses):
        '''HangmanFigure.draw_figure(guesses) -> None
        draws a part of the figure for guesses'''
        if guesses > len(self.bodyParts):
            return

        # draw head
        if self.bodyParts[guesses-1][-1] == "circle":
            self.create_oval(*self.bodyParts[guesses-1][:-1], width=2)
        # other parts
        elif guesses-1 < len(self.bodyParts):
            self.create_line(*self.bodyParts[guesses-1], width=2)
        # guesses
        self.itemconfigure(self.guesses, text=6-guesses)
                
class HangmanFrame(Frame):
    '''manipulates the hangman game'''

    def __init__(self, master, wordFile="wordlist.txt"):
        '''HangmanFrame(master, wordFile) -> HangmanFrame
        constructs the game frame'''
        Frame.__init__(self, master, bg="blue")
        self.grid()
        self.master = master
        self.wordFile = wordFile
        self.popup = None

        # buttons
        self.buttons = {}
        buttonSeqs = ("qwertyuiop", "asdfghjkl", "zxcvbnm")
        for i in range(len(buttonSeqs)):
            buttonFrame = Frame(self, bg="blue")
            buttonFrame.grid(row=i+2, column=0)
            for j in range(len(buttonSeqs[i])):
                new = HangmanButton(buttonFrame, self, buttonSeqs[i][j].upper())
                new.grid(row=0, column=j+1, sticky=W)
                self.buttons[buttonSeqs[i][j]]  = new

        # word setup
        file = open(wordFile)
        words = file.read().split()
        file.close()
        self.word = random.choice(words)
        self.guesses = []
        self.wrong = 0
        self.figure = HangmanFigure(self, self.word)

        # spacers
        Canvas(self, bg="blue", width=10, height=10, highlightthickness=0).grid(row=1, column=0, columnspan=12)
        Canvas(self, bg="blue", width=10, height=10, highlightthickness=0).grid(row=5, column=0, columnspan=12)
        Canvas(self, bg="blue", width=10, height=10, highlightthickness=0).grid(row=7, column=0, columnspan=12)

        # entry field
        entryField = Frame(self, bg="#ddddff")
        entryField.grid(row=6, column=0, columnspan=13)

        self.text = StringVar()
        self.enter = Entry(entryField, font=("Arial", 12), bg="#ddddff", textvariable=self.text)
        self.enter.grid(row=0, column=0)
        self.enter.focus_set()
        self.guess = Button(entryField, command=self.guess_with_entry, text="Guess", bg="#ddddff", relief=RIDGE)
        self.guess.grid(row=0, column=1)
        self.enter.bind_all("<Return>", self.guess_with_entry)

    def guess_with_entry(self, event=''):
        '''HangmanFrame.guess_with_entry(event) -> None
        guesses with the entry box'''
        if (event != '' and self.focus_get() != self.enter):
            return
        if not self.text.get().isalpha():
            self.show_info("Invalid")
            return

        guess = self.text.get().lower()
        self.text.set("")

        # disable button
        if len(guess) == 1:
            self.buttons[guess].disable()
            self.buttons[guess].itemconfigure("circle", fill="#ccccdd")
            
        self.guess_letter(guess)

    def guess_letter(self, guess):
        '''HangmanFrame.guess_letter(guess) -> None
        checks the player's guess'''
        if len(guess) == 0:
            return

        # already guessed
        self.text.set("")
        if guess in self.guesses:
            self.show_info("Already guessed")
            return
        # single letter guess
        elif len(guess) == 1 and guess in self.word:
            self.figure.fill_letter(guess)
        # word guess
        elif guess == self.word:
            for letter in self.figure.get_letters().copy():
                self.figure.fill_letter(letter)
            
        # incorrect guess
        else:
            self.wrong += 1
            self.figure.draw_figure(self.wrong)
            
        # word guess
        
        self.guesses.append(guess)
        if self.wrong == 6:
            # show letters
            self.disable_all()
            for letter in self.figure.get_letters().copy():
                self.figure.fill_letter(letter, "red")
            self.show_info("Sorry, you lost", True)
            
        elif len(self.figure.get_letters()) == 0:
            self.disable_all()
            self.show_info("Congrats! You won", True)

    def disable_all(self):
        '''HangmanFrame.disable_all() -> None
        disables everything about the game'''
        self.text.set("")
        self.focus_set()
        
        # disable buttons
        for button in self.buttons:
            self.buttons[button].disable()
        # disable text field
        self.enter["state"] = DISABLED
        self.guess["state"] = DISABLED

    def show_info(self, message, restart=False):
        '''HangmanFrame.show_info(message, False) -> None
        shows info with custom popup
        'o' for ok and 'r' for restart'''
        if self.popup != None:
            self.popup.destroy()
            
        self.popup = Toplevel(self, bg="white")
        self.popup.geometry(f"200x70+{self.winfo_rootx()+self.winfo_width()//2-110}+{self.winfo_rooty()+self.winfo_height()//2+80}")

        # popup display
        end = StringVar()
        Label(self.popup, text=message, font=("Arial", 13), width=21, bg="white").grid(row=0, column=0)
        Canvas(self.popup, bg="white", highlightthickness=0, width=10, height=8).grid(row=1, column=0)

        # buttons        
        if restart:
            restart = Button(self.popup, text="Restart", bg="white", command=self.restart)
            restart.grid(row=2, column=0)
            restart.focus_set()
        else:
            ok = Button(self.popup, text="Ok", width=5, bg="white", command=lambda: end.set("go"))
            ok.grid(row=2, column=0)
            ok.focus_set()
        
        self.wait_variable(end)
        self.popup.destroy()
        self.popup = None

    def restart(self):
        '''HangmanFrame.restart() -> None
        restarts the game'''
        self.destroy()
        self.__init__(self.master, self.wordFile)            

root = Tk()
root.title("Hangman")
HangmanFrame(root, "wordlist.txt")
