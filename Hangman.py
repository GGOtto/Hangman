import random
import turtle
import winsound
from time import sleep

def loading():
    '''loading() -> turtle
    draw Hangman Loading symbol'''
    l = turtle.Turtle()
    p = turtle.Turtle()
    
    l.hideturtle()
    l.left(90)
    p.hideturtle()
    p.up()
    percent = 0
    l.pensize(20)
    l.speed(0)
    l.hideturtle()
    p.right(90)
    p.fd(150)
    p.left(90)
    
    
    while True:
        if percent%9 == 1:
            p.clear()
            if percent == 0:
                p.write('Loading Hangman: 1% Complete', False, 'center',('Arial',20,'normal'))
            else:
                p.write('Loading Hangman: ' + str(percent)+'% Complete', False, 'center',('Arial',20,'normal'))
        l.fd(100)
        l.back(100)
        sleep(0.001)
        l.right(7.2)
        percent += 2
        if percent == 102:
            break


    sleep(1)

    p.clear()
    l.clear()

def animate_lost(le,re,m,la,ra,ll,rl):
    '''animate_lost(head,le,re,la,ra,ll,rl) -> turtle
    animates the fingure if player has losts
    
    h1 = black outline for head
    h2 = white inside for head
    b = body
    le = left eye
    re = right eye
    m = mouth
    la = left arm
    ra = right arm
    ll = left leg
    rl = right leg'''
    
    mSize = .475
    speed = 10
    laHeading = 180
    raHeading = 0
    llHeading = 225
    rlHeading = 315
    
    while speed != 0:
        while True:
            blink = random.random()
            llHeading -= speed
            rlHeading += speed
            raHeading -= speed
            laHeading += speed
            mSize -= speed/200
            
            if 0.1 <= blink <= 0.15:
                le.turtlesize(0.05,0.3)
                re.turtlesize(0.05,0.3)
                le.turtlesize(0.3,0.3)
                re.turtlesize(0.3,0.3)
            
            la.setheading(laHeading)
            rl.setheading(rlHeading)
            m.turtlesize(mSize,.65)
            ra.setheading(raHeading)
            ll.setheading(llHeading)
            if 195<=llHeading<=205:
                break
        while True:
            blink = random.random()
            llHeading += speed
            rlHeading -= speed
            raHeading += speed
            laHeading -= speed
            mSize += speed/200
            
            if 0.1 <= blink <= 0.15:
                le.turtlesize(0.05,0.3)
                re.turtlesize(0.05,0.3)
                le.turtlesize(0.3,0.3)
                re.turtlesize(0.3,0.3)
                
            la.setheading(laHeading)
            rl.setheading(rlHeading)
            m.turtlesize(mSize,.65)
            ra.setheading(raHeading)
            ll.setheading(llHeading)
            if 245<=llHeading<=255:
                break
        speed -= 2
    sleep(0.75)
    while True:
        laHeading += 4
        raHeading -= 4
        la.setheading(laHeading)
        ra.setheading(raHeading)
        if 240 <= laHeading <= 250:
            break
    le.pensize(2.5)
    re.pensize(2.5)
    le.hideturtle()
    re.hideturtle()
    le.pd()
    re.pd()
    le.setheading(135)
    le.fd(2.5)
    le.bk(5)
    le.fd(2.5)
    le.left(90)
    le.fd(2.5)
    le.bk(5)
    le.fd(2.5)
    re.setheading(45)
    re.fd(2.5)
    re.bk(5)
    re.fd(2.5)
    re.left(90)
    re.fd(2.5)
    re.bk(5)
    re.fd(2.5)
    return

def animate_won(wn):
    '''animate_lost(wn) -> turtle
    animates the game if player has won'''
    pass

def draw_board(word,t):
    '''draw_board(word) -> turtle
    draw a hangman board for word'''
    t.pensize(5)

    # draw bottom line
    if len(word)*40 + len(word) * 10 + 10 > 300:
        t.fd(len(word)*20 + len(word) * 5 + 5)
        t.back((len(word)*40 + len(word)*10 + 10))
    else:
        t.fd(150)
        t.back(300)

    # position turtle
    t.up()
    t.goto(0,-50)
    t.back((len(word)*20 + len(word)*5 + 5))

    # set up dicts
    positionDic = {}
    countDic = {}
    
    # create countDic
    for letter in word:
        countDic[letter] = 0

    # draw letter slots and create positionDic
    for letter in word:
        countDic[letter] += 1
        t.up()
        t.fd(10)
        positionDic[letter + str(countDic[letter])] = t.position()   
        t.down()
        t.fd(40)

    # draw scaffold
    t.up()
    t.goto(-140,0)
    t.down()
    t.goto(-90,50)
    t.goto(-40,0)
    t.goto(-90,50)
    t.goto(-90,250)
    t.goto(90,250)
    t.goto(-40,250)
    t.goto(-90,200)
    t.up()
    t.goto(90,250)
    t.down()
    t.goto(90,220)
    
    return positionDic

def write_text(t,text):
    '''write_text(t,lastTextLength) -> turtle
    writes text at the bottom of the hangman board'''

    # clear previous text
    t.clear()

    # write text
    t.color('black')
    t.write(text,False,'center',('Arial', 20, 'normal'))

def draw_man(numIncorrect,h1,h2,b,le,re,m,la,ra,ll,rl):
    '''draw_man(numInccorect) -> turtle
    draws the correct body part for an incorrect guess'''

    # draw head
    if numIncorrect == 1:
        h1.showturtle()
        h2.showturtle()
        m.showturtle()
        le.showturtle()
        re.showturtle()
        
    # draw body
    elif numIncorrect == 2:
        b.showturtle()

    # draw arms
    elif numIncorrect == 3:
        la.showturtle()
    elif numIncorrect == 4:
        ra.showturtle()

    # draw legs
    elif numIncorrect == 5:
        ll.showturtle()
    elif numIncorrect == 6:
        rl.showturtle()
    
def play_hangman():
    '''play_hangman -> string
    plays the game Hangman'''
    # set up screen
    wordFile = open('mywordlist.txt','r')
    wordString = wordFile.read()
    wordList = wordString.split()
    highest = 6
    for e in  wordList:
        if len(e) > highest:
            highest = len(e)

    wn = turtle.Screen()
    wn.setup(highest*50+60,600,1500-(highest*50+60),100)
    
    while True:
        print('\tHANGMAN\n')
        wn.clear()
        loading()
        
        # set up regular turtle
        t = turtle.Turtle()
        t.speed(0)
        t.hideturtle()
    
        # set up notifier
        notif = turtle.Turtle()
        notif.speed(0)
        notif.up()
        notif.hideturtle()
        notif.goto(0,-200)

        # set up the turtles that draw the man
        h1 = turtle.Turtle()
        h1.hideturtle()
        h1.speed(0)
        h1.shape('circle')
        h1.pu()
        h1.goto(90,195)
        h1.turtlesize(2.5,2.5)

        h2 = turtle.Turtle()
        h2.hideturtle()
        h2.speed(0)
        h2.shape('circle')
        h2.color('white')
        h2.pu()
        h2.goto(90,195)
        h2.turtlesize(2.2,2.2)

        le = turtle.Turtle()
        le.hideturtle()
        le.speed(0)
        le.shape('circle')
        le.pu()
        le.goto(80,200)
        le.turtlesize(0.3,0.3)

        re = turtle.Turtle()
        re.hideturtle()
        re.speed(0)
        re.shape('circle')
        re.pu()
        re.goto(100,200)
        re.turtlesize(0.3,0.3)

        m = turtle.Turtle()
        m.hideturtle()
        m.speed(0)
        m.shape('circle')
        m.pu()
        m.goto(90,182.5)
        m.turtlesize(.475,.65)

        b = turtle.Turtle()
        b.hideturtle()
        b.speed(0)
        b.shape('square')
        b.pu()
        b.goto(90,130)
        b.turtlesize(4,.25)

        la = turtle.Turtle()
        la.hideturtle()
        la.speed(0)
        la.shape('arrow')
        la.pu()
        la.goto(90,150)
        la.turtlesize(.15,4.25)
        la.setheading(180)

        ra = turtle.Turtle()
        ra.hideturtle()
        ra.speed(0)
        ra.shape('arrow')
        ra.pu()
        ra.goto(90,150)
        ra.turtlesize(.15,4.25)

        ll = turtle.Turtle()
        ll.hideturtle()
        ll.speed(0)
        ll.shape('arrow')
        ll.pu()
        ll.goto(90,90)
        ll.turtlesize(.15,5.25)
        llHeading = 225
        ll.setheading(llHeading)

        rl = turtle.Turtle()
        rl.hideturtle()
        rl.speed(0)
        rl.shape('arrow')
        rl.pu()
        rl.goto(90,90)
        rl.turtlesize(.15,5.25)
        rlHeading = 315
        rl.setheading(rlHeading)
        #
        
        word = random.choice(wordList) # get word
        word = word.upper()
        positionDic = draw_board(word,t) # draw board and get positionDic
        
        # last minute things
        t.up()
        guessList = []
        lastTextLength = 0
        numIncorrect = 0

        # loop through turns
        while True:
            # get player guess
            guess = ''
            while True:
                guess = input('What letter do you guess? ')
                if not guess.isalpha() or len(guess) > 1:
                    print('\nYou may only guess a single letter.\n')
                    continue
                guess = guess.upper()
                if guess in guessList:
                    print('\nYou already guessed that.\n')
                    continue
                break

            # guessList plus new guess
            guessList.append(guess)

            # if correct
            if guess in word:
                winsound.Beep(1000,120)
                for letter in positionDic:
                    if guess == letter[0]:
                        t.goto(positionDic[letter]) # goto position
                        t.fd(35)
                        if guess.lower() == 'i':
                            t.bk(10)
                        elif guess.lower() == 'w':
                            t.fd(5)
                        t.write(guess,False,'right',('Arial',30,'normal'))
                # remove guess from positionDic      
                for i in range(word.count(guess)):
                    positionDic.pop(guess + str(i+1))
                # write text
                if len(positionDic) != 0:
                    write_text(notif,guess + ' is correct!')   
                # if player won end game
                elif len(positionDic) == 0:
                    write_text(notif,'Congrats! You won!')
                    print('Congrats! You won!')
                    break
            
            # if incorrect
            else:
                winsound.MessageBeep(10)
                numIncorrect += 1 
                draw_man(numIncorrect,h1,h2,b,le,re,m,la,ra,ll,rl) # draw body part
                # write text
                if numIncorrect != 6:
                    write_text(notif,guess + ' is incorrect!')
                # if player lost end game    
                else:
                    # show word
                    t.color('red')
                    for letter in positionDic:
                        t.goto(positionDic[letter])
                        #if letter.lower() == 'i':
                        #    t.fd(20)
                        #else:
                        #    t.fd(35)
                        t.fd(35)
                        t.write(letter[0],False,'right',('Arial',30,'normal'))
        
                    write_text(notif,'Sorry! You lost!')
                    print('Sorry! You lost!')
                    animate_lost(le,re,m,la,ra,ll,rl)
                    break
                
        print()
        sleep(1)
        
        playAgain = ''
        while playAgain != 'y' and playAgain != 'n':
            playAgain = input('Do you want to play again? (y/n) ')
        if playAgain == 'y':
            continue
        else:
            break

        wordFile.close()
        
play_hangman() # play game

        
        
                
    

