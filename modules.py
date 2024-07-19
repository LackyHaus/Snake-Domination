from os import environ
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
import pygame as pg
from random import randint
from time import sleep, time
from datetime import timedelta

VERSION = "Snake Domination 0.2"

#==============================================================================================================

class Player_class():
    def __init__(self, screen, x, y, Hungry=0, GodMode=0, LenghtLimit=16):
        global Map
        self.sc = screen
        self.lastMove = (0,1)
        self.dMove = ["Right"]
        self.Hungry = Hungry
        self.Moves = 0
        self.GodMode = GodMode
        self.LenghtLimit = LenghtLimit
        self.head = pg.Rect(x, y, RectSize, RectSize)
        self.body = [(x, y), (x, y+1), (x, y+2), (x, y+3)]
        Colors = []
        for i in range(len(self.body)):
            Colors.append([max(Color-(80//self.LenghtLimit)*i, 0) for Color in Player_Color2])
        [pg.draw.rect(self.sc, pg.Color(Colors[k]), ((Convert(i),Convert(j)),(RectSize+2,RectSize+2))) for k, (i, j) in enumerate(self.body)]
        pg.draw.rect(self.sc, pg.Color(Player_Color1), ((Convert(self.head.x),Convert(self.head.y)),(RectSize+2,RectSize+2)))
        for x, y in self.body:
            Map[x][y] = 1

    def Move(self, direct=(0,0)):
        global Map
        if (MapId(self.head.x + direct[0], self.head.y + direct[1]) in [-1,1,5]):
            if (self.GodMode > 0):
                self.GodMode -= 1
            else:
                if (MapId(self.head.x + self.lastMove[0], self.head.y + self.lastMove[1]) in [-1,1,5]):
                    return
                direct = self.lastMove
        
        self.Moves += 1
        self.Hungry -= 1
        if (self.Hungry <= 0):
            self.Hungry = 10
            Map[self.body[-1][0]][self.body[-1][1]] = 0
            del self.body[-1]
            if (len(self.body) == 1):
                return

        self.lastMove = direct

        self.body.insert(1,self.body[-1])
        self.body[1] = self.head.x, self.head.y

        self.head.x += direct[0]
        self.head.y += direct[1]

        self.body[0] = self.head.x, self.head.y
        Map[self.body[-1][0]][self.body[-1][1]] = 0
        del self.body[-1]

        for x, y in self.body:
            Map[x][y] = 1
        return

    def Render(self, FillColor=0):
        Colors = []
        for i in range(len(self.body)):
            Colors.append([max(Color-(80//self.LenghtLimit)*i, 0) for Color in Player_Color2])
        [pg.draw.rect(self.sc, pg.Color(Colors[k] if FillColor == 0 else FillColor), ((Convert(i),Convert(j)),(RectSize+2,RectSize+2))) for k, (i, j) in enumerate(self.body)]
        pg.draw.rect(self.sc, pg.Color(Player_Color1), ((Convert(self.head.x),Convert(self.head.y)),(RectSize+2,RectSize+2)))
    
    def IsDead(self,Map):
        if (len(self.body) == 1 and self.GodMode > 0):
            self.body.append(self.body[-1])
        if (((MapId(self.body[0][0]+1,self.body[0][1]) in [-1,1,5]) and
            (MapId(self.body[0][0],self.body[0][1]+1) in [-1,1,5]) and
            (MapId(self.body[0][0]-1,self.body[0][1]) in [-1,1,5]) and
            (MapId(self.body[0][0],self.body[0][1]-1) in [-1,1,5]) or
            len(self.body) <= 1) and self.GodMode == 0): return True
        return False

#==============================================================================================================

class Bot():
    def __init__(self, screen, x, y, body=0, Hungry=0, LenghtLimit=30):
        global Map
        self.sc = screen
        self.Direction = set()
        self.Hungry = Hungry
        self.LenghtLimit = LenghtLimit
        self.head = pg.Rect(x, y, RectSize, RectSize)
        if (body == 0):     self.body = [(x, y), (x, y+1), (x, y+2), (x, y+3)]
        else:               self.body = body
        Colors = []
        for i in range(len(self.body)):
            Colors.append([max(Color-(80//self.LenghtLimit)*i, 0) for Color in Bot_Color2])
        [pg.draw.rect(self.sc, pg.Color(Colors[k]), ((Convert(i),Convert(j)),(RectSize+2,RectSize+2))) for k, (i, j) in enumerate(self.body)]
        pg.draw.rect(self.sc, pg.Color(Bot_Color1), ((Convert(self.head.x),Convert(self.head.y)),(RectSize+2,RectSize+2)))
        for x, y in self.body:
            Map[x][y] = 5

    def Move(self, direct):
        global Map
        if (MapId(self.head.x + direct[0], self.head.y + direct[1]) in [-1,1,5] or direct == (0,0)):
            if (MapId(self.head.x + direct[0], self.head.y + direct[1]) in [1,5] or direct == (0,0)):
                direct = self.FindPath(limit=3)
                if (MapId(self.head.x + direct[0], self.head.y + direct[1]) in [-1,1,5] or direct == (0,0)):
                    return "DEAD"
            else:
                return "DEAD"
        
        self.Hungry -= 1
        if (self.Hungry <= 0):
            self.Hungry = 10
            Map[self.body[-1][0]][self.body[-1][1]] = 0
            del self.body[-1]
            if (len(self.body) == 1):
                return "DEAD"

        self.body.insert(1,self.body[-1])
        self.body[1] = self.head.x, self.head.y

        self.head.x += direct[0]
        self.head.y += direct[1]

        self.body[0] = self.head.x, self.head.y
        Map[self.body[-1][0]][self.body[-1][1]] = 0
        del self.body[-1]

        for x, y in self.body:
            Map[x][y] = 5
        return "Live"
    
    def FindPath(self, Apples=((-1,-1)), limit=9998):
        def GrafID(x,y):
            if (x < 0 or y < 0):
                return (9999)
            if (x > ScreenSizeW-1 or y > ScreenSizeH-1):
                return (9999)
            return Graf[x][y]
        
        Graf = []
        for x in range(round(SW/RectSize)):
            Graf.append([])
            for y in range(round(SH/RectSize)):
                Graf[x].append(9999)
        Step = 0
        Path = []
        CheckPath = [self.body[0]]
        BlackPath = []
        Find = True
        Ser = set()
        while Find and len(CheckPath) > 0:
            Step += 1
            for i in range(len(CheckPath)):
                Ser = (CheckPath[0][0], CheckPath[0][1])
                Graf[Ser[0]][Ser[1]] = Step
                del CheckPath[0]

                if (MapId(Ser[0] + 1, Ser[1]) not in [-1,5] and (Ser[0] + 1, Ser[1]) not in BlackPath):
                    BlackPath.append((Ser[0] + 1, Ser[1]))
                    CheckPath.append((Ser[0] + 1, Ser[1]))

                if (MapId(Ser[0] - 1, Ser[1]) not in [-1,5] and (Ser[0] - 1, Ser[1]) not in BlackPath):
                    BlackPath.append((Ser[0] - 1, Ser[1]))
                    CheckPath.append((Ser[0] - 1, Ser[1]))

                if (MapId(Ser[0], Ser[1] + 1) not in [-1,5] and (Ser[0], Ser[1] + 1) not in BlackPath):
                    BlackPath.append((Ser[0], Ser[1] + 1))
                    CheckPath.append((Ser[0], Ser[1] + 1))

                if (MapId(Ser[0], Ser[1] - 1) not in [-1,5] and (Ser[0], Ser[1] - 1) not in BlackPath):
                    BlackPath.append((Ser[0], Ser[1] - 1))
                    CheckPath.append((Ser[0], Ser[1] - 1))
                
                if (Ser in Apples or len(CheckPath) == 0 or Step >= limit):
                    Find = False
                    break
        Ser = list(Ser)
        Path.append((Ser[0], Ser[1]))
        while Ser != self.body[0]:
            if (GrafID(Ser[0] + 1, Ser[1]) < GrafID(Ser[0], Ser[1])):
                Ser[0] += 1
                Path.append((Ser[0], Ser[1]))

            elif (GrafID(Ser[0] - 1, Ser[1]) < GrafID(Ser[0], Ser[1])):
                Ser[0] -= 1
                Path.append((Ser[0], Ser[1]))

            elif (GrafID(Ser[0], Ser[1] + 1) < GrafID(Ser[0], Ser[1])):
                Ser[1] += 1
                Path.append((Ser[0], Ser[1]))

            elif (GrafID(Ser[0], Ser[1] - 1) < GrafID(Ser[0], Ser[1])):
                Ser[1] -= 1
                Path.append((Ser[0], Ser[1]))
            
            else:
                if (len(Path) > 1) :
                    CheckDir = Path[-2]
                else:
                    CheckDir = Path[0]
                MoveDirection = (CheckDir[0] - self.body[0][0], CheckDir[1] - self.body[0][1])

                return MoveDirection
                    
    
    
    def Dead(self):
        for i in self.body:
            Map[i[0]][i[1]] = 0


    def Render(self):
        Colors = []
        for i in range(len(self.body)):
            Colors.append([max(Color-(80//self.LenghtLimit)*i, 0) for Color in Bot_Color2])
        [pg.draw.rect(self.sc, pg.Color(Colors[k]), ((Convert(i),Convert(j)),(RectSize+2,RectSize+2))) for k, (i, j) in enumerate(self.body)]
        pg.draw.rect(self.sc, pg.Color(Bot_Color1), ((Convert(self.head.x),Convert(self.head.y)),(RectSize+2,RectSize+2)))

#==============================================================================================================

def BotDead(Check):
    if (Check == "DEAD"):
        return True
    return False

def MapId(x,y):
    if (x < 0 or y < 0):
        return (-1)
    if (x > ScreenSizeW-1 or y > ScreenSizeH-1):
        return (-1)
    return Map[x][y]

def Convert(x):
    return max((x*RectSize+x-1),0)

def RenderApples(Apples, sc, FillColor=0):
    Colors = []
    for i in range(len(Apples[0])):
        Colors.append([min(round(Color+100/len(Apples[0])*i), 255) for Color in Apple_Color])
    [pg.draw.circle(sc, pg.Color(Colors[k] if FillColor == 0 else FillColor), (Convert(i)+RectSize//2+1,Convert(j)+RectSize//2+1),RectSize//2-RectSize//10) for k, (i, j) in enumerate(Apples[0])]

    [pg.draw.circle(sc, pg.Color(GApple_Color), (Convert(i)+RectSize//2+1,Convert(j)+RectSize//2+1),RectSize//2-RectSize//20) for i, j in Apples[1]]
    [pg.draw.circle(sc, pg.Color(Colors[k] if FillColor == 0 else FillColor), (Convert(i)+RectSize//2+1,Convert(j)+RectSize//2+1),RectSize//2-RectSize//7) for k, (i, j) in enumerate(Apples[1])]


#==============================================================================================================

RectSize = 20       # Размер клетки
ScreenSizeW = 70    # Клеток в ширину
ScreenSizeH = 40    # Клеток в высоту
Life = True

SW = (RectSize+1)*ScreenSizeW-1
SH = (RectSize+1)*ScreenSizeH-1

Clock = pg.time.Clock()
Apples = set()
GApples = set()
Bots:Bot = []
Map = []
KeyBoardHistory = ['']
Cheats = True

BG_Color = [200, 225, 255]
SP_Color = [color - 10 for color in BG_Color]
Player_Color1 = [50, 205, 50]
Player_Color2 = [46, 139, 87]
Bot_Color1 = [0, 191, 255]
Bot_Color2 = [100, 149, 237]
Apple_Color = [178, 34, 34]
GApple_Color = [255, 215, 0]

if (__name__ == "__main__"):
    import os
    os.system("start cmd /k python game.py")
    raise SystemExit