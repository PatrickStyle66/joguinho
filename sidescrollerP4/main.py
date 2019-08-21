import pygame

from pygame.locals import *

import os

import random

import mysql.connector

import random

from itertools import chain

pygame.init()

W, H = 928, 591

win = pygame.display.set_mode((W, H))

pygame.display.set_caption('Dummy Runner!')

bg = pygame.image.load(os.path.join('images', 'bg.png')).convert()

bgX = 0

bgX2 = bg.get_width()

clock = pygame.time.Clock()

chayenne = pygame.image.load(os.path.join('images','chayenne.jpg'))

music = pygame.mixer.music.load('Jumper.mp3')
pygame.mixer.music.play(-1)

class player(object):
    run = [pygame.image.load(os.path.join('images', str(x) + '.png')) for x in range(8, 16)]

    jump = [pygame.image.load(os.path.join('images', str(x) + '.png')) for x in range(1, 8)]
    fall = pygame.image.load(os.path.join('images','0.png'))
    slide = [pygame.image.load(os.path.join('images', 'S1.png')), pygame.image.load(os.path.join('images', 'S2.png')),
             pygame.image.load(os.path.join('images', 'S2.png')), pygame.image.load(os.path.join('images', 'S2.png')),
             pygame.image.load(os.path.join('images', 'S2.png')), pygame.image.load(os.path.join('images', 'S2.png')),
             pygame.image.load(os.path.join('images', 'S2.png')), pygame.image.load(os.path.join('images', 'S2.png')),
             pygame.image.load(os.path.join('images', 'S3.png')), pygame.image.load(os.path.join('images', 'S4.png')),
             pygame.image.load(os.path.join('images', 'S5.png'))]

    jumpList = [1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 4, 4, 4, 4, 4,
                4, 4, 4, 4, 4, 4, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -1, -1,
                -1, -1, -1, -1, -2, -2, -2, -2, -2, -2, -2, -2, -2, -2, -2, -2, -3, -3, -3, -3, -3, -3, -3, -3, -3, -3,
                -3, -3, -4, -4, -4, -4, -4, -4, -4, -4, -4, -4, -4, -4]

    def __init__(self, x, y, width, height):

        self.x = x

        self.y = y

        self.width = width

        self.height = height

        self.jumping = False

        self.sliding = False

        self.slideCount = 0

        self.jumpCount = 0

        self.runCount = 0

        self.slideUp = False

        self.falling = False

    def draw(self, win):
        if self.falling:
            win.blit(self.fall, (self.x,self.y+30))
        elif self.jumping:

            self.y -= self.jumpList[self.jumpCount] * 1.2

            win.blit(self.jump[self.jumpCount // 18], (self.x, self.y))

            self.jumpCount += 1

            if self.jumpCount > 108:
                self.jumpCount = 0

                self.jumping = False

                self.runCount = 0
            self.hitbox = (self.x + 6,self.y,self.width -26,self.height - 10)
        elif self.sliding or self.slideUp:

            if self.slideCount < 20:

                self.y += 1

            elif self.slideCount == 80:

                self.y -= 19

                self.sliding = False

                self.slideUp = True
            elif self.slideCount > 20 and self.slideCount < 80:
                self.hitbox = (self.x,self.y+3,self.width-8,self.height-35)

            if self.slideCount >= 110:
                self.slideCount = 0

                self.slideUp = False

                self.runCount = 0
                self.hitbox = (self.x + 4, self.y, self.width - 26, self.height - 10)
            win.blit(self.slide[self.slideCount // 10], (self.x, self.y))

            self.slideCount += 1



        else:

            if self.runCount > 42:
                self.runCount = 0

            win.blit(self.run[self.runCount // 6], (self.x, self.y))

            self.runCount += 1
            self.hitbox = (self.x + 4, self.y, self.width - 24, self.height - 13)
        #pygame.draw.rect(win,(255,0,0),self.hitbox,2)

class saw(object):

    img = [pygame.image.load(os.path.join('images','SAW0.png')),pygame.image.load(os.path.join('images','SAW1.png')),pygame.image.load(os.path.join('images','SAW2.png')),pygame.image.load(os.path.join('images','SAW3.png'))]

    def __init__(self,x,y,width,height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.hitbox = (x,y,width,height)
        self.count = 0

    def collide(self,rect):
        if rect[0] + rect[2] > self.hitbox[0] and rect[0] < self.hitbox[0] + self.hitbox[2]:
            if rect[1] + rect[3] > self.hitbox[1]:
                return True
        return False
    def draw(self,win):
        self.hitbox = (self.x + 7, self.y+5,self.width - 13,self.height)
        if self.count >= 8:
            self.count = 0
        win.blit(pygame.transform.scale(self.img[self.count//2],(64,64)),(self.x,self.y))
        self.count += 1
        #pygame.draw.rect(win,(255,0,0),self.hitbox,2)


class spike(saw):
    img = pygame.image.load(os.path.join('images','spike.png'))
    def draw(self,win):
        self.hitbox = (self.x + 13, self.y,22,470)
        self.hitbox2 =(self.x,self.y,47,420)
        win.blit(self.img,(self.x,self.y))
        #pygame.draw.rect(win,(255,0,0),self.hitbox,2)
        #pygame.draw.rect(win, (255, 0, 0), self.hitbox2, 2)

    def collide(self, rect):
        if rect[0] + rect[2] > self.hitbox[0] and rect[0] < self.hitbox[0] + self.hitbox[2]:
            if rect[1] < self.hitbox[3]:
                return True
        if rect[0] + rect[2] > self.hitbox2[0] and rect[0] < self.hitbox2[0] + self.hitbox2[2]:
            if rect[1] < self.hitbox2[3]:
                return True
        return False


class button():
    def __init__(self, color, x, y, width, height, text=''):
        self.color = color
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text

    def draw(self, win, outline=None):

        if outline:
            pygame.draw.rect(win, outline, (self.x - 2, self.y - 2, self.width + 4, self.height + 4), 0)

        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.height), 0)

        if self.text != '':
            font = pygame.font.SysFont('comicsans', 50)
            text = font.render(self.text, 1, (0, 0, 0))
            win.blit(text, (
            self.x + (self.width / 2 - text.get_width() / 2), self.y + (self.height / 2 - text.get_height() / 2)))

    def isOver(self, pos):

        if pos[0] > self.x and pos[0] < self.x + self.width:
            if pos[1] > self.y and pos[1] < self.y + self.height:
                return True

        return False


class database(object):

    def __init__(self,user,password,host,db):
        self.user = user
        self.password = password
        self.host = host
        self.db = db

    def connect(self):
        return mysql.connector.connect(user=self.user, password=self.password,host=self.host,database=self.db)



def truncline(text, font, maxwidth):
    real = len(text)
    stext = text
    l = font.size(text)[0]
    cut = 0
    a = 0
    done = 1
    old = None
    while l > maxwidth:
        a = a + 1
        n = text.rsplit(None, a)[0]
        if stext == n:
            cut += 1
            stext = n[:-cut]
        else:
            stext = n
        l = font.size(stext)[0]
        real = len(stext)
        done = 0
    return real, done, stext


def wrapline(text, font, maxwidth):
    done = 0
    wrapped = []

    while not done:
        nl, done, stext = truncline(text, font, maxwidth)
        wrapped.append(stext.strip())
        text = text[nl:]
    return wrapped


def wrap_multi_line(text, font, maxwidth):
    lines = chain(*(wrapline(line, font, maxwidth) for line in text.splitlines()))
    return list(lines)


def redrawWindow():
    global imunity,undead
    win.blit(bg,(bgX,0))
    win.blit(bg,(bgX2,0))
    runner.draw(win)
    for x in objects:
        x.draw(win)
    font = pygame.font.SysFont('comicsans', 30)
    text = font.render('Pontuação: ' + str(score),1,(255,255,255))
    imunFont = pygame.font.SysFont('comicsans',19)
    imun = font.render('',1,(255,255,255))
    if imunity > 0 and undead > 0:
        if imunity >=250 and imunity <= 500:
            imun = imunFont.render("imunidade!",1,(158, 255, 158))
        elif imunity >=100 :
            imun = imunFont.render("imunidade!", 1,(255,165,0))
        else:
            imun = imunFont.render("Imunidade!",1,(139,0,0))
    win.blit(text,(700,10))
    win.blit(imun,(runner.x - 5, runner.y - 15))
    pygame.display.update()

def updateFile():
    f = open('scores.txt','r')
    file = f.readlines()
    last = int(file[0])

    if last < int(score):
        f.close()
        file = open('scores.txt','w')
        file.write(str(score))
        file.close()
        return score
    return last

def endScreen():
    global pause, objects,speed, score,imunity
    pause = 0
    objects = []
    speed = 60
    imunity = 0
    tryagain = button((0,255,0), 200,420,250,100,'Reiniciar')
    back = button((0,255,0),500,420,250,100,'Menu')
    run = True
    while run:
        pygame.time.delay(100)
        tryagain.draw(win,(0,0,0))
        back.draw(win,(0,0,0))
        pygame.display.update()
        for event in pygame.event.get():
            pos = pygame.mouse.get_pos()
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if tryagain.isOver(pos):
                    run = False
                if back.isOver(pos):
                    menu()
                    run = False
        win.blit(bg,(0,0))
        largeFont = pygame.font.SysFont('comicsans',80)
        deathmsg = largeFont.render('Morreu :(',1,(255,255,255))
        win.blit(deathmsg,(W/2 - deathmsg.get_width()/2, 100))
        previousScore = largeFont.render('Melhor Pontuação: ' +str(updateFile()),1,(255,255,255))
        win.blit(previousScore,(W/2 - previousScore.get_width()/2,200))
        newScore = largeFont.render('Pontuação Final: ' + str(score),1,(255,255,255))
        win.blit(newScore, (W / 2 - newScore.get_width() / 2, 320))
    score = 0
    runner.falling = False

def questionScreen():
    global score, pause, imunity
    imunity  = 500
    pause = 0
    run = True
    ButtonA = button((0,255,0),220,350,250,100,'Alternativa A')
    ButtonB = button((0, 255, 0), 220, 470, 250, 100, 'Alternativa B')
    ButtonC = button((0,255,0),520,350,250,100,'Alternativa C')
    ButtonD = button((0, 255, 0), 520, 470, 250, 100, 'Alternativa D')
    font = pygame.font.SysFont('comicsans',30)
    y = font.get_height()
    index = str(random.randrange(1, 11))
    query = ("SELECT * FROM questions WHERE indice = {}".format(index))
    cursor.execute(query)
    result = cursor.fetchall()
    for sentence in result:
        text = wrapline(sentence[1],font,928)
        questA = font.render('a)' + sentence[2], 1, (255, 255, 255))
        questB = font.render('b)' + sentence[3], 1, (255, 255, 255))
        questC = font.render('c)' + sentence[4], 1, (255, 255, 255))
        questD = font.render('d)' + sentence[5], 1, (255, 255, 255))
        right = sentence[6]
    blits = []
    buttons = [ButtonA,ButtonB,ButtonC,ButtonD]
    correct = buttons.pop(int(right))
    while run:
        pygame.time.delay(100)
        ButtonA.draw(win,(0,0,0))
        ButtonB.draw(win, (0, 0, 0))
        ButtonC.draw(win,(0,0,0))
        ButtonD.draw(win,(0,0,0))
        pygame.display.update()
        for event in pygame.event.get():
            pos = pygame.mouse.get_pos()
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if correct.isOver(pos):
                    run = False
                for wrong in buttons:
                    if wrong.isOver(pos):
                        endScreen()
                        run = False
        win.blit(bg, (0, 0))
        for line in text:
            quest = font.render(line, 1, (255, 255, 255))
            blits.append(win.blit(quest,(0,y)))
            y += font.get_height()
        win.blit(questA,(0,y + font.get_height()))
        win.blit(questB, (0, y + (2 * font.get_height())) )
        win.blit(questC, (0, y + (3 * font.get_height())))
        win.blit(questD, (0, y + (4 * font.get_height())))
        y = font.get_height()
    runner.falling =False


def creditScreen():
    run = True
    back = button((0,255,0),600,25,250 ,100,'Voltar')
    font = pygame.font.SysFont('comicsans', 30)
    patrick = font.render('-Jonathas Patrick H. de Azevedo | jpha@ic.ufal.br',1,(255,255,255))
    thalyssa = font.render('-Thalyssa de Almeida Monteiro | tam@ic.ufal.br',1,(255,255,255))
    cat = font.render('...e chayenne ^ ^',1,(255,255,255))
    copyright = font.render('©2019 Thalick games',1,(255,255,255))
    music = font.render('Música: Waterflame - Jumper',1,(255,255,255))
    while run:
        pygame.time.delay(100)
        back.draw(win,(0,0,0))
        pygame.display.update()
        for event in pygame.event.get():
            pos = pygame.mouse.get_pos()
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if back.isOver(pos):
                    run = False
        win.blit(bg, (0, 0))
        win.blit(patrick, (0, 100))
        win.blit(thalyssa, (0, 250))
        win.blit(cat, (0, 350))
        win.blit(chayenne,(10,380))
        win.blit(copyright,(650,550))
        win.blit(music,(50,550))

def menu():
    run = True
    start = button((0,255,0),350,250,250,100,'Jogar')
    credit = button((0,255,0),350,400,250,100,'Créditos')
    font = pygame.font.SysFont('minecrafteralt',100)
    soundfont = pygame.font.SysFont('comicsans',30)
    sound1 = soundfont.render('Som(M):On',1,(255,255,255))
    sound2 = soundfont.render('Som(M):Off',1,(255,255,255))
    title = font.render('Dummy Runner',1,(255,255,255))
    state = 1
    while run:
        pygame.time.delay(100)
        start.draw(win,(0,0,0))
        credit.draw(win,(0,0,0))
        pygame.display.update()
        for event in pygame.event.get():
            pos = pygame.mouse.get_pos()
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if start.isOver(pos):
                    run = False
                if credit.isOver(pos):
                    creditScreen()
        keys = pygame.key.get_pressed()
        if keys[pygame.K_m]:
            state *= -1
            if state == -1:
                pygame.mixer.music.stop()
            else:
                pygame.mixer.music.play(-1)
        if state < 0:
            win.blit(sound2,(25,550))
            pygame.display.update()
        else:
            win.blit(sound1,(25,550))
            pygame.display.update()
        win.blit(bg, (0, 0))
        win.blit(title,(W / 2 - title.get_width() / 2, 50))

server = database('root','123456','localhost','p4')

cnx = server.connect()
cursor = cnx.cursor()

runner = player(200,468,64,64)
pygame.time.set_timer(USEREVENT+1,1000)
pygame.time.set_timer(USEREVENT+2,random.randrange(3000,5000))
speed = 60
run = True

pause = 0
fallSpeed = 0
imunity = 0
undead = 0
objects = []

menu()

while run:
    score = speed//5 - 12
    if imunity > 0:
        imunity -= 1

    if pause > 0:
        pause += 1
        if pause > fallSpeed * 2:
            questionScreen()
            undead = 1

    for objectt in objects:
        if objectt.collide(runner.hitbox) and imunity == 0:
            runner.falling = True
            if pause == 0:
                fallSpeed = speed
                pause = 1
                imunity = 500
                undead = 0

        objectt.x -= 1.4
        if objectt.x < objectt.width * -1:
            objects.pop(objects.index(objectt))

    bgX -= 1.4
    bgX2 -= 1.4
    if bgX < bg.get_width() * -1:
        bgX = bg.get_width()
    if bgX2 < bg.get_width() * -1:
        bgX2 = bg.get_width()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            pygame.quit()
            quit()
        if event.type == USEREVENT+1:
            speed += 1
        if event.type == USEREVENT + 2:
            r = random.randrange(0,2)
            if r == 0:
                objects.append(saw(910,468,64,64))
            else:
                objects.append(spike(910, 0, 48, 472))


    keys = pygame.key.get_pressed()

    if keys[pygame.K_UP]:
        if not (runner.jumping):
            runner.jumping = True
    if keys[pygame.K_DOWN]:
        if not(runner.sliding):
            runner.sliding = True
    clock.tick(speed)
    redrawWindow()
cursor.close()
cnx.close()

