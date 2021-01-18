import pygame
from pygame.locals import *
import sys
import random





class Player(pygame.sprite.Sprite):

    def __init__(self):
        super().__init__()
        self.__leftRight=252
        self.__upDown=252
        self.__points=1
        self.__longMove=12
        self.__sizeBlock=10
        self.__ifPlay=True
        self.__ifPoint=False
        self.__rand = 1
        self.__rand2 = 1
        self.__text=""
        self.__buttonPress=0
        self.listPlace=[]
        self.sizeWindowX=502
        self.sizeWindowY=552

        pygame.init()
        self.surface = pygame.display.set_mode([self.sizeWindowX, self.sizeWindowY])
        pygame.display.set_caption("Snake")

        self.__colorREd = (255, 0, 0)
        self.__colorWhite = (255, 255, 255)
        self.__colorblack = (0, 0, 0)
        self.__colorBlue = (0, 0, 255)
        self.__colorGreen = (0, 255, 0)

    #lista gdzie moze powstac enemy
        self.__listXY = []
        for x in range(0, self.sizeWindowX-10, self.__longMove):
            for y in range(48, self.sizeWindowY-2, self.__longMove):
                self.__listXY.append([x, y])


    #Buttony
    def __update(self):
        pressed_key=pygame.key.get_pressed()
        lenList = len(self.listPlace)

        #right
        if(pressed_key[K_RIGHT] and self.__ifPlay):
            if(self.__buttonPress!=2 or lenList<=1):
                self.__buttonPress = 1
        # left
        elif(pressed_key[K_LEFT] and self.__ifPlay):
            if(self.__buttonPress!=1 or lenList<=1):
                self.__buttonPress = 2
        # up
        elif(pressed_key[K_UP] and self.__ifPlay):
            if(self.__buttonPress!=4 or lenList<=1):
                self.__buttonPress = 3
        # down
        elif(pressed_key[K_DOWN] and self.__ifPlay):
            if(self.__buttonPress!=3 or lenList<=1):
                self.__buttonPress = 4

    def changeDirect(self):
        if(self.__buttonPress==4):
            self.__drawMoreDown()
        elif(self.__buttonPress==3):
            self.__drawMoreUP()
        elif(self.__buttonPress==2):
            self.__drawMoreLeft()
        else:
            self.__drawMoreRight()

    #rysowanie w gore
    def __drawMoreUP(self):
        self.__upDown -= self.__longMove
        self.__draw(self.__leftRight,self.__upDown)


    def __drawMoreDown(self):
        self.__upDown += self.__longMove
        self.__draw(self.__leftRight, self.__upDown)


    #rysowanie w lewo
    def __drawMoreLeft(self):
        self.__leftRight -= self.__longMove
        self.__draw(self.__leftRight,self.__upDown)


    #rysowanie w prawo
    def __drawMoreRight(self):
        self.__leftRight += self.__longMove
        self.__draw(self.__leftRight, self.__upDown)

    #Rysowanie snaka
    def __draw(self,leftright=252,updown=252):

        if(self.__ifPlay):
            self.__outOfBorder()
            self.__cutSnake()
            self.__firstDraw(leftright, updown)
            self.__firstGreen()
            self.__randList()
            self.__longerSnake()



    #rysowanie pojedynczej kostki
    def __firstDraw(self,leftright=252,updown=252):
        circle = pygame.draw.rect(self.surface, self.__colorGreen, (leftright, updown, self.__sizeBlock, self.__sizeBlock))
        self.listPlace.append([leftright, updown])

    #pokolorowanie ostatniej kostki jako czarnej
    def __deleteLast(self):
        leftright=self.listPlace[0][0]
        updown=self.listPlace[0][1]
        self.listPlace.pop(0)
        circle = pygame.draw.rect(self.surface, self.__colorblack, (leftright, updown, self.__sizeBlock, self.__sizeBlock))
        self.__listXY.append([leftright,updown])


        # tablica gdzie moze zosatc narysowany przeszkoda
    def __randList(self):
        listTemp = []
        for x in self.__listXY:
            for y in self.listPlace:
                if (x == y):
                    listTemp.append(y)

        for x in listTemp:
            self.__listXY.remove(x)

    #sprawdzanie kiedy kostka wyjdzie poza plansze
    def __outOfBorder(self):
        if(self.__leftRight<0 or self.__leftRight>self.sizeWindowX-10 or self.__upDown<48 or self.__upDown>self.sizeWindowY-10):
            self.__lostGame()

    #Wypisywanie napisu przegrana
    def __lostGame(self):
            self.__ifPlay = False
            self.__textPlace()
            myfont = pygame.font.SysFont("monospace", 30)
            label = myfont.render("{} pkt. Przegrałeś!!!!".format(self.__points), 0, (0, 255, 0))
            self.surface.blit(label, (120,15))

    #losowanie z listy możliwych pozycji enemy oraz rysowanie na niebiesko enemy
    def __drawEnemy(self):
        randXY=random.choice(self.__listXY)
        self.rand=randXY[0]
        self.rand2=randXY[1]

        circle = pygame.draw.rect(self.surface, self.__colorBlue, (self.rand, self.rand2, self.__sizeBlock, self.__sizeBlock))



    #zdobycie punktu Jeśli pierwszy klocek będzie w tymm samym miejscu co przeszkoda
    def __getPoint(self):
        lenList= len(self.listPlace)
        if(self.__leftRight==self.rand and self.__upDown==self.rand2):
            self.__winPoint()

    #metoda zdobycia punktu
    def __winPoint(self):
        self.__drawEnemy()
        self.__ifPoint = True
        self.__points+=1
        self.__textInfo()

    #Wyswietlanie napisu o ilosci punktow
    def __textInfo(self):
        self.__textPlace()
        myfont = pygame.font.SysFont("monospace", 30)
        self.text = "{} pkt.".format(self.__points)
        label = myfont.render(self.text, 1, (0, 250, 0))
        self.surface.blit(label, (120, 15))

    #tworzeni bialej przestrzeni dla tekstu
    def __textPlace(self):
        textPlace = pygame.draw.rect(self.surface, self.__colorWhite, (0, 0, self.sizeWindowX, 48))


    def __longerSnake(self):
        self.__getPoint()
        if (self.__ifPoint == False):
            self.__deleteLast()
        else:
            self.__ifPoint = False

    #Jesli snake dotknie sam sibie
    def __cutSnake(self):
        a=[self.__leftRight,self.__upDown]
        lenList= len(self.listPlace)
        for x in range(lenList-1):
            if self.listPlace[x]==a:
                #print(self.__leftRight,"  ",self.__upDown," ",a)
                self.__lostGame()

    #Pierwsza kropka jest zielona a nastepne czerwone
    def __firstGreen(self):
        listLen= len(self.listPlace)

        if(listLen>=2):
            leftRight= self.listPlace[listLen-1][0]
            upDown = self.listPlace[listLen - 1][1]

            leftRight2= self.listPlace[listLen-2][0]
            upDown2= self.listPlace[listLen-2][1]

            circle = pygame.draw.rect(self.surface, self.__colorGreen,(leftRight, upDown, self.__sizeBlock, self.__sizeBlock))
            circle = pygame.draw.rect(self.surface, self.__colorREd,(leftRight2, upDown2, self.__sizeBlock, self.__sizeBlock))

    #metdoa glowna
    def mainGame(self):

        self.__drawEnemy()
        self.__firstDraw()
        self.__textInfo()

        frameperSec = pygame.time.Clock()

        while True:
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()


            self.__update()
            self.changeDirect()
            #self.__drawMoreLeft()

            frameperSec.tick(10)




p1 = Player()
p1.mainGame()