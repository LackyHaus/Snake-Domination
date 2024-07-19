from modules import *

def SpawnApple(Count = 1):
    for i in range(Count):
        Spawned = False
        for j in range(1000):
            x,y = randint(0,ScreenSizeW-1),randint(0,ScreenSizeH-1)
            if (Map[x][y] == 0):
                Map[x][y] = 2
                Apples.add((x,y))
                Spawned = True
                break
        if not Spawned:
            return

def SpawnGApple(Count = 1):
    for i in range(Count):
        Spawned = False
        for j in range(1000):
            x,y = randint(0,ScreenSizeW-1),randint(0,ScreenSizeH-1)
            if (Map[x][y] == 0):
                Map[x][y] = 3
                GApples.add((x,y))
                Spawned = True
                break
        if not Spawned:
            return

def SpawnBots(Count = 1):
    for i in range(Count):
        Spawned = False
        for j in range(1000):
            x, y = randint(4, ScreenSizeW-3),randint(4,ScreenSizeH-3)
            if (MapId(x,y) not in [1,5] and MapId(x-1,y-1) not in [1,5] and MapId(x-2,y-2) not in [1,5] and MapId(x-3,y-3) not in [1,5]):
                Bots.append(Bot(sc,x,y))
                for Check in Bots[-1].body:
                    if (Check in Apples):
                        Apples.discard(Check)
                    if (Check in GApples):
                        GApples.discard(Check)
                Bots[i].Direction = Bots[i].FindPath((Apples,GApples))
                Spawned = True
                break
        if not Spawned:
            return

def DeadTitle():
    EndTime = round(time()-StartGameTime)
    pg.display.update()
    sleep(.5)

    for i in range(255):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                raise SystemExit

        for j in range(3):
            BG_Color[j] = max(0, BG_Color[j]-1)
        for j in range(3):
            SP_Color[j] = max(0, SP_Color[j]-1)
        for j in range(3):
            Player_Color1[j] = max(0, Player_Color1[j]-1)
        for j in range(3):
            Player_Color2[j] = max(0, Player_Color2[j]-1)
        for j in range(3):
            Bot_Color1[j] = max(0, Bot_Color1[j]-1)
        for j in range(3):
            Bot_Color2[j] = max(0, Bot_Color2[j]-1)
        for j in range(3):
            Apple_Color[j] = max(0, Apple_Color[j]-1)
        for j in range(3):
            GApple_Color[j] = max(0, GApple_Color[j]-1)


        sc.fill(BG_Color)
        RenderApples((Apples, GApples),sc, Apple_Color)
        for x in range(round(SW/RectSize)):
            pg.draw.rect(sc, SP_Color, ((RectSize*(x+1)+x ,0),(1,SH)))
        for y in range(round(SH/RectSize)):
            pg.draw.rect(sc, SP_Color, ((0, RectSize*(y+1)+y),(SW,1)))
        
        for i in Bots:
            i.Render()
        Player.Render()
        
        pg.display.update()
        sleep(.0025)
    sc.fill(BG_Color)

    Game_Over_Color = [0, 0, 0]
    text_rect = pg.font.SysFont('Arial', 50).render("Game Over!", False, Game_Over_Color).get_rect()
    text_rect.center = (SW // 2, SH // 2 - 50)

    for i in range(255):
        Game_Over_Color[0] = min(255, Game_Over_Color[0]+1)
        sc.blit(pg.font.SysFont('Arial',50).render("Game Over!", False, Game_Over_Color),text_rect)
        pg.display.update()
        sleep(.0025)
    
    Stats_Color = [0, 0, 0]
    for i in range(255):
        Stats_Color[0] = Stats_Color[0]+1

        text_rect = pg.font.SysFont('Arial', 50).render(f"Time: {str(timedelta(seconds=EndTime))}", False, Stats_Color).get_rect()
        text_rect.center = (SW // 2, SH // 2)
        sc.blit(pg.font.SysFont('Arial', 50).render(f"Time: {str(timedelta(seconds=EndTime))}", False, Stats_Color), text_rect)

        text_rect = pg.font.SysFont('Arial', 50).render(f"Steps: {Player.Moves}.", False, Stats_Color).get_rect()
        text_rect.center = (SW // 2, SH // 2 + 50)
        sc.blit(pg.font.SysFont('Arial', 50).render(f"Steps: {Player.Moves}", False, Stats_Color), text_rect)

        if (len(Bots) > 0):
            text_rect = pg.font.SysFont('Arial', 50).render(f"Steps: {Player.Moves}.", False, Stats_Color).get_rect()
            text_rect.center = (SW // 2, SH // 2 + 100)
            sc.blit(pg.font.SysFont('Arial', 50).render(f"Bots: {len(Bots)}", False, Stats_Color), text_rect)

        pg.display.update()
        sleep(.0025)

def WinTitle():
    EndTime = round(time()-StartGameTime)
    pg.display.update()
    sleep(.5)

    for i in range(255):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                raise SystemExit
            
        for j in range(3):
            BG_Color[j] = min(255, BG_Color[j]+1)
        for j in range(3):
            SP_Color[j] = min(255, SP_Color[j]+1)
        for j in range(3):
            Player_Color1[j] = min(255, Player_Color1[j]+1)
        for j in range(3):
            Player_Color2[j] = min(255, Player_Color2[j]+1)
        for j in range(3):
            Apple_Color[j] = min(255, Apple_Color[j]+1)
        for j in range(3):
            GApple_Color[j] = min(255, GApple_Color[j]+1)


        sc.fill(BG_Color)
        RenderApples((Apples, GApples),sc)
        for x in range(round(SW/RectSize)):
            pg.draw.rect(sc, SP_Color, ((RectSize*(x+1)+x ,0),(1,SH)))
        for y in range(round(SH/RectSize)):
            pg.draw.rect(sc, SP_Color, ((0, RectSize*(y+1)+y),(SW,1)))
        
        Player.Render(Player_Color2)
        
        pg.display.update()
        sleep(.0025)
    sc.fill(BG_Color)

    You_Win_Color = [255, 255, 255]
    text_rect = pg.font.SysFont('Arial', 50).render("You Win!", False, You_Win_Color).get_rect()
    text_rect.center = (SW // 2, SH // 2 - 50)

    for i in range(255):
        You_Win_Color[0] = You_Win_Color[0]-1
        You_Win_Color[2] = You_Win_Color[2]-1
        sc.blit(pg.font.SysFont('Arial', 50).render("You Win!", False, You_Win_Color), text_rect)
        pg.display.update()
        sleep(.0025)

    Stats_Color = [255, 255, 255]
    for i in range(255):
        Stats_Color[0] = Stats_Color[0]-1
        Stats_Color[2] = Stats_Color[2]-1

        text_rect = pg.font.SysFont('Arial', 50).render(f"Time: {str(timedelta(seconds=EndTime))}", False, Stats_Color).get_rect()
        text_rect.center = (SW // 2, SH // 2)
        sc.blit(pg.font.SysFont('Arial', 50).render(f"Time: {str(timedelta(seconds=EndTime))}", False, Stats_Color), text_rect)

        text_rect = pg.font.SysFont('Arial', 50).render(f"Steps: {Player.Moves}.", False, Stats_Color).get_rect()
        text_rect.center = (SW // 2, SH // 2 + 50)
        sc.blit(pg.font.SysFont('Arial', 50).render(f"Steps: {Player.Moves}", False, Stats_Color), text_rect)
        pg.display.update()
        sleep(.0025)

def CheckCode(List, Base):
    for i, text in enumerate(Base):
        el = []
        for ch in text:
            el.append(ch)
        try:
            Check = List[-len(el):]
            for index, char in enumerate(Check):
                Check[index] = pg.key.name(char)
            if (Check == el):
                return text
        except: continue
    return ""

pg.init()
pg.font.init()

CodeBase = [
    "hello",
    "max",
    "hungry",
    "god",
    "infbody",
    "suicide",
    "killbot"
]

sc = pg.display.set_mode((SW,SH))
pg.display.set_caption(VERSION)
sc.fill(BG_Color)

for x in range(round(SW/RectSize)):
    pg.draw.rect(sc, pg.Color(SP_Color), ((RectSize*(x+1)+x ,0),(1,SH)))

for y in range(round(SH/RectSize)):
    pg.draw.rect(sc, SP_Color, ((0, RectSize*(y+1)+y),(SW,1)))

for x in range(round(SW/RectSize)):
    Map.append([])
    for y in range(round(SH/RectSize)):
        Map[x].append(0)
        

Player:Player_class = Player_class(sc, 4, 3, LenghtLimit=16)
SpawnApple(35)
SpawnGApple(5)
SpawnBots(5)
RenderApples((Apples, GApples),sc)

pg.display.update()

if (len(Bots) == 0):
    WinTitle()
    Life = False

StartGameTime = time()
MoveFrame = 0
while Life:
    for event in pg.event.get():
        if event.type == pg.KEYUP:
            KeyBoardHistory.remove(f"Stop {event.key}")
            while (len(KeyBoardHistory) > 10):
                del [KeyBoardHistory[0]]
            Code = CheckCode(KeyBoardHistory,CodeBase)
            if (Code != "" and Cheats):

                if (Code == "hello"):
                    print("Hello World!")
                elif (Code == "max"):
                    for i in range(Player.LenghtLimit-len(Player.body)):
                        Player.body.append(Player.body[-1])
                elif (Code == "hungry"):
                    Player.Hungry = 9999999
                elif (Code == "god"):
                    Player.GodMode = 9999999
                elif (Code == "infbody"):
                    for i in range(ScreenSizeW*ScreenSizeH):
                        Player.body.append(Player.body[-1])
                        Player.LenghtLimit = ScreenSizeW*ScreenSizeH
                elif (Code == "suicide"):
                    Player.body = [Player.head]
                    Player.GodMode = 0
                elif (Code == "killbot"):
                    Bots = []
                
        if event.type == pg.KEYDOWN or event.type == pg.KEYMAPCHANGED:
            if (KeyBoardHistory[-1] != f"Stop {event.key}"):
                KeyBoardHistory.append(event.key)
                KeyBoardHistory.append(f"Stop {event.key}")
            
            
            if (len(Player.dMove) < 5):
                if event.key in [pg.K_w, pg.K_UP] and Player.dMove[-1] != "Up":
                    Player.dMove.append("Up")
                elif event.key in [pg.K_s, pg.K_DOWN] and Player.dMove[-1] != "Down":
                    Player.dMove.append("Down")
                elif event.key in [pg.K_d, pg.K_RIGHT] and Player.dMove[-1] != "Right":
                    Player.dMove.append("Right")
                elif event.key in [pg.K_a, pg.K_LEFT] and Player.dMove[-1] != "Left":
                    Player.dMove.append("Left")
                    
                if (Player.dMove[0] == "" and len(Player.dMove) > 1):
                    del Player.dMove[0]
            
        
    if (MoveFrame <= 0):
        MoveFrame = 50
        CheckMove = Player.body[0]
        
        if (Player.dMove[0] != ""):
            if (Player.dMove[0] == "Up"):
                Player.Move((0,-1))
            elif (Player.dMove[0] == "Down"):
                Player.Move((0,1))
            elif (Player.dMove[0] == "Right"):
                Player.Move((1,0))
            elif (Player.dMove[0] == "Left"):
                Player.Move((-1,0))

            if (len(Player.dMove) > 1):  
                del Player.dMove[0]
            else:
                Player.dMove[0] = ""
        else:
            Player.Move()



        for i, bt in enumerate(Bots):
            if (BotDead(bt.Move(bt.Direction))):
                Bots[i].Dead()
                del Bots[i]
            if (bt.body[0] in Apples):
                Bonus = max(2 - list(Apples).index(bt.body[0])/(len(Apples)-1) * 2, 1)
                Apples.discard(bt.body[0])
                SpawnApple()
                if (bt.LenghtLimit > len(bt.body)):
                    bt.body.append(bt.body[-1])
                else:
                    NewBody = bt.body[bt.LenghtLimit//2::]
                    Bots.append(Bot(sc, bt.body[-1][0], bt.body[-1][1], NewBody[::-1]))
                    Bots[-1].Direction = bt.FindPath(Apples.union(GApples))

                    for j in bt.body[bt.LenghtLimit//2::]:
                        Map[j[0]][j[1]] = 0
                        
                    del bt.body[bt.LenghtLimit//2::]
                bt.Hungry += 4 * Bonus

            if (bt.body[0] in GApples):
                GApples.discard(bt.body[0])
                SpawnGApple()
                for i in range(3):
                    if (bt.LenghtLimit > len(bt.body)):
                        bt.body.append(bt.body[-1])
                    else:
                        NewBody = bt.body[bt.LenghtLimit//2::]
                        Bots.append(Bot(sc, bt.body[-1][0], bt.body[-1][1], NewBody[::-1]))
                        Bots[-1].Direction = bt.FindPath(Apples.union(GApples))

                        for j in bt.body[bt.LenghtLimit//2::]:
                            Map[j[0]][j[1]] = 0
                        
                        del bt.body[bt.LenghtLimit//2::]
                        break
                bt.Hungry += 5
        

        sc.fill(BG_Color)
        if (Player.body[0] in Apples):
            Bonus = max(2 - list(Apples).index(Player.body[0])/(len(Apples)-1) * 2, 1)
            Apples.discard(Player.body[0])
            SpawnApple()
            if (Player.LenghtLimit > len(Player.body)):
                Player.body.append(Player.body[-1])
            Player.Hungry += 4 * Bonus
        
        if (Player.body[0] in GApples):
            GApples.discard(Player.body[0])
            SpawnGApple()
            for i in range(3):
                if (Player.LenghtLimit > len(Player.body)):
                    Player.body.append(Player.body[-1])
            Player.Hungry += 4
        
        RenderApples((Apples, GApples),sc)
        
        for x in range(round(SW/RectSize)):
            pg.draw.rect(sc, SP_Color, ((RectSize*(x+1)+x ,0),(1,SH)))

        for y in range(round(SH/RectSize)):
            pg.draw.rect(sc, SP_Color, ((0, RectSize*(y+1)+y),(SW,1)))
        
        for i in Bots:
            i.Render()
        Player.Render()

        if (Player.IsDead(Map) or CheckMove == Player.body[0]):
            DeadTitle()
            Life = False
        
        elif (len(Bots) == 0):
            WinTitle()
            Life = False
        
        pg.display.update()

        for bt in Bots:
            bt.Direction = bt.FindPath(Apples.union(GApples))

    MoveFrame -= 1
    Clock.tick(200)
    if event.type == pg.QUIT:
        pg.quit()
        raise SystemExit




while True:
    for event in pg.event.get():
        if ((event.type == pg.QUIT) or event.type == pg.KEYDOWN and event.key == pg.K_SPACE):
            pg.quit()
            raise SystemExit
