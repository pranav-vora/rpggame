import pygame
from pygame.locals import *
import sys
import random
from datetime import datetime, timezone
import time
from tkinter import filedialog
from tkinter import *
pygame.init()
HEIGHT=800
WIDTH=1000
ACC=0.5
FRIC=-0.12
FPS=60
FPS_CLOCK=pygame.time.Clock()
COUNT=0
numberofenemies=1
displaysurface=pygame.display.set_mode((WIDTH, HEIGHT))
vec=pygame.math.Vector2
enemyList=[]
enemyDict={}
gameOver=False
enemiesKilled=0
startTime=time.time()
class Background(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__() #adds the sprite attributes to the background class
        self.bgimage=pygame.image.load("images/pixilart-drawing (1).png")
        self.bgX=0
        self.bgY=0
    def render(self):
        displaysurface.blit(self.bgimage, (self.bgX, self.bgY))
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__() 
        self.enemyInitialize()
    def enemyInitialize(self):
        self.image=pygame.image.load("images/enemy.png")
        self.vx=0
        self.vy=0
        self.surf = pygame.Surface((30,30))
        self.size = self.image.get_size()
        self.image=pygame.transform.scale(self.image, (int(self.size[0]*0.5), int(self.size[1]*0.5)))#enemy size: 98x126

        self.rect = self.surf.get_rect()
        self.pos=vec((random.randint(-500,1500),random.randint(-500,-300)))#vec=vector
        self.vel=vec(0,0)
        self.acc=vec(0,0)
        self.direction="RIGHT"
        displaysurface.blit(self.image, (self.vx, self.vy))
        self.bouncing=False
        self.isdead=False
        self.hitbox=pygame.draw.rect(displaysurface,(255,0,0), pygame.Rect(self.pos.x-20,self.pos.y-30,110,130))
        self.attacking=False
        self.startAttackTime=time.time()
        self.movementblocked=False
        self.diedshortrange=False
        self.touchingPlayer=False
    def move(self):
        self.movementx=player.pos.x-self.pos.x
        self.movementy=player.pos.y-self.pos.y
        if self.movementx>0 and self.movementy>0 and self.bouncing==False:
            self.acc.x=ACC
            self.acc.y=ACC
        if self.movementx<0 and self.movementy>0 and self.bouncing==False:
            self.acc.x=-ACC
            self.acc.y=ACC
        if self.movementx>0 and self.movementy<0 and self.bouncing==False:
            self.acc.x=ACC
            self.acc.y=-ACC
        if self.movementx<0 and self.movementy<0 and self.bouncing==False:
            self.acc.x=-ACC
            self.acc.y=-ACC
        if self.bouncing==True:
            self.vel=-self.vel*random.randint(2,5)*2

        if self.pos.x<-500:
            self.vel.x =0
            self.acc.x=0
            self.pos.x=-500
        if self.pos.x>1500:
            self.vel.x=0
            self.acc.x=0
            self.pos.x=1500
        if self.pos.y<-500:
            self.vel.y=0
            self.acc.y=0
            self.pos.y=-500
        if self.pos.y>1500:
            self.vel.y=0
            self.acc.y=0
            self.pos.y=1500


        if self.isdead==False and self.touchingPlayer==False:
            self.acc.x += self.vel.x * FRIC
            self.acc.y += self.vel.y * FRIC
            self.vel += self.acc
            self.pos += self.vel + 0.5 * self.acc
            if self.pos.x>1500 or self.pos.x<-1500 or self.pos.y>1500 or self.pos.y<-1500:
                self.acc.x=0
                self.acc.y=0
                self.vel.x=0
                self.vel.y=0
                self.pos.x=1000
                self.pos.y=1000
            self.rect.midbottom = self.pos
    def enemyhitbox(self):
        self.hitbox=pygame.draw.rect(displaysurface,(255,0,0), pygame.Rect(self.pos.x-20,self.pos.y-30,110,130))
    def execute(self):
        self.move()
        self.enemyhitbox()
        self.shortRangeDeath()
        self.longRangeDeath()
        self.isattacking()
    def isattacking(self):
        if time.time()-self.startAttackTime>0.5:
            self.attacking=True
            self.startAttackTime=time.time()
        
        if time.time()-self.startAttackTime>0.01:
            self.attacking=False

    def shortRangeDeath(self):
        if self.isdead==True and self.diedshortrange==True:
            self.image=pygame.image.load("images/enemy_short_range_death.png")

            if time.time()-startDeathTime>2:
                self.enemyInitialize()
    def longRangeDeath(self):
        if self.isdead==True and self.diedshortrange==False:
            if time.time()-startDeathTime>0.1:
                self.image=pygame.image.load("images/explosion (1).png")
            if time.time()-startDeathTime>0.2:
                self.image=pygame.image.load("images/explosion (2).png")
            if time.time()-startDeathTime>0.3:
                self.image=pygame.image.load("images/explosion (3).png")
            if time.time()-startDeathTime>0.4:
                self.image=pygame.image.load("images/explosion (4).png")
            if time.time()-startDeathTime>0.5:
                self.image=pygame.image.load("images/explosion (5).png")
            if time.time()-startDeathTime>0.6:
                self.image=pygame.image.load("images/explosion (6).png")
            if time.time()-startDeathTime>0.7:
                self.image=pygame.image.load("images/explosion (7).png")
            if time.time()-startDeathTime>0.8:
                self.image=pygame.image.load("images/explosion (8).png")
            if time.time()-startDeathTime>1:
                self.image=pygame.image.load("images/explosion (9).png")
            if time.time()-startDeathTime>2:
                self.enemyInitialize()



class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.last_time_attacked=time.time()
        self.image=pygame.image.load("images/player.png") #self addresses the classes attributes
        self.vx=0
        self.vy=0
        self.surf = pygame.Surface((30,30))
        self.size = self.image.get_size()
        self.rect = self.surf.get_rect()
        self.pos=vec((340,240))#vec=vector
        self.vel=vec(0,0)
        self.acc=vec(0,0)
        self.direction="RIGHT"
        displaysurface.blit(self.image, (self.vx, self.vy))
        self.playerisflipped=False
        self.attacking=False
        self.shortRangeAttack=False
        self.longRangeAttack=False
        self.lastAttackTime=0
        self.hitboxsword=pygame.draw.rect(displaysurface,(255,0,0), pygame.Rect(self.pos.x+50,self.pos.y+0,40,50))
        self.startAttackTime=time.time()
        self.maxhealth=100
        self.playerhealth=100
        self.ratio=self.playerhealth/self.maxhealth
        self.playerlongrangehitbox=pygame.draw.rect(displaysurface,(255,255,0), pygame.Rect(self.pos.x+450,self.pos.y-50,600,200))
        self.healthbar=pygame.draw.rect(displaysurface,(255,0,0), (250, 250, 300, 40)) ,  pygame.draw.rect(displaysurface,(0,255,0), (250, 250, 300 * self.ratio, 40))

    def move(self):
        pressed_keys = pygame.key.get_pressed()
        if pressed_keys[K_LEFT] and self.attacking==False:
            self.acc.x =-ACC   
            self.playerisflipped=True
        if pressed_keys[K_RIGHT] and self.attacking==False:
            self.acc.x=ACC
            self.playerisflipped=False
        if pressed_keys[K_UP] and self.attacking==False:
            self.acc.y =-ACC
        if pressed_keys[K_DOWN] and self.attacking==False:
            self.acc.y=ACC



        self.acc.x += self.vel.x * FRIC
        self.acc.y += self.vel.y * FRIC
        self.vel += self.acc
        if abs(self.vel.x) < 0.5:  # Stop shaking by setting a threshold
            self.vel.x = 0
            self.acc.x=0
        if abs(self.vel.y) < 0.5:  # Stop shaking by setting a threshold
            self.vel.y = 0
            self.acc.y=0


            
        if self.pos.x<0:
            self.vel.x = 0
            self.acc.x=0
            self.pos.x=0
        if self.pos.x>WIDTH-50:
            self.vel.x=0
            self.acc.x=0
            self.pos.x=WIDTH-50
        if self.pos.y<0:
            self.vel.y=0
            self.acc.y=0
            self.pos.y=0
        if self.pos.y>HEIGHT-70:
            self.vel.y=0
            self.acc.y=0
            self.pos.y=HEIGHT-70
        self.pos += self.vel + 0.5 * self.acc
        self.rect.midbottom = self.pos



        if self.playerisflipped==False and self.attacking==False:
            self.image=pygame.image.load("images/player.png")
            self.size = self.image.get_size()
            self.image=pygame.transform.scale(self.image, (int(self.size[0]*0.5), int(self.size[1]*0.5)))
        elif self.playerisflipped==True and self.attacking==False:
            self.image=pygame.image.load("images/player_flipped.png")
            self.size = self.image.get_size()
            self.image=pygame.transform.scale(self.image, (int(self.size[0]*0.5), int(self.size[1]*0.5)))
        elif self.playerisflipped==False and self.attacking==True:
            self.image=pygame.image.load("images/player_rotated.png")
            self.size = self.image.get_size()
            self.image=pygame.transform.scale(self.image, (int(self.size[0]*0.5), int(self.size[1]*0.5)))
        else:
            self.image=pygame.image.load("images/player_flipped_rotated.png")
            self.size = self.image.get_size()
            self.image=pygame.transform.scale(self.image, (int(self.size[0]*0.5), int(self.size[1]*0.5)))


        

     
    def swordhitbox(self):
        if self.playerisflipped==False:
            self.hitboxsword=pygame.draw.rect(displaysurface,(255,0,0), pygame.Rect(self.pos.x+50,self.pos.y+0,40,50))
        else:
            self.hitboxsword=pygame.draw.rect(displaysurface,(255,0,0), pygame.Rect(self.pos.x-20,self.pos.y+0,40,50))
    def bodyhitbox(self):
        if self.playerisflipped==False:
            self.hitboxbody=pygame.draw.rect(displaysurface,(255,0,0), pygame.Rect(self.pos.x,self.pos.y-25,60,100))
        else:
            self.hitboxbody=pygame.draw.rect(displaysurface,(255,0,0), pygame.Rect(self.pos.x+15,self.pos.y-25,60,100))
    def knockbackhitbox(self):
            if self.playerisflipped==False:
                self.playerlongrangehitbox=pygame.draw.rect(displaysurface,(255,255,0), pygame.Rect(self.pos.x+450,self.pos.y-50,600,200))
            else:

                self.playerlongrangehitbox=pygame.draw.rect(displaysurface,(255,255,0), pygame.Rect(self.pos.x-1000,self.pos.y-50,600,200))
    def isAttacking(self):

        key_pressed=pygame.key.get_pressed()
        if key_pressed[K_SPACE] and time.time()-self.startAttackTime>2:
            self.attacking=True
            self.shortRangeAttack=True
            self.startAttackTime=time.time()
        if event.type==pygame.KEYDOWN and  event.key == pygame.K_LSHIFT and time.time()-self.startAttackTime> 2:
            self.attacking=True
            self.longRangeAttack=True
            self.startAttackTime=time.time()

        
        
        if time.time()-self.startAttackTime>0.25:
            self.attacking=False
            self.shortRangeAttack=False
            self.longRangeAttack=False



            
    def healthBar(self):
        self.ratio=self.playerhealth/self.maxhealth
        self.healthbar=pygame.draw.rect(displaysurface,(255,0,0), (self.pos.x-70, self.pos.y-50, 200, 20)) ,  pygame.draw.rect(displaysurface,(0,255,0), (self.pos.x-70, self.pos.y-50, 200 * player.ratio, 20))




    def execute(self):
        self.move()
        self.swordhitbox()
        self.bodyhitbox()
        self.knockbackhitbox()
        self.isAttacking()


        
            
        
collideList=[]      
player=Player() #adds an instance of the player class to create a player
enemy=Enemy()
enemy2=Enemy()
enemy3=Enemy()
enemy4=Enemy()
background=Background()
enemyDict={1:(enemy,[[]]),2:(enemy2,[[]]),3:(enemy3,[[]]),4:(enemy4,[[]])}
# the plan is to for every element in enemy list, we want to make each of the elements into a dictionary
#  and set each of the keys to collide detection with the player and other enemies.















while gameOver==False:
    for event in pygame.event.get():
        if event.type==QUIT:
            pygame.quit()
            sys.exit()
    # for enemies in enemydict:
    #     enemies.execute()
    #     for i in range(len(enemydict)):

    for i in enemyDict.values():
        i[0].execute()  


    player.execute()




#text for enemies killed and time survived

    gameRunTime=round(time.time()-startTime)
    seconds=str((gameRunTime%60)).zfill(2)
    minutes=str(int(gameRunTime/60)).zfill(2)
    font = pygame.font.Font('freesansbold.ttf', 32)
    enemiesKilledText = font.render("Enemies Killed: "+str(enemiesKilled), True,(0,255,0))
    timeSurvivedText = font.render("Time Survived: "+minutes+":"+seconds, True,(0,255,0))
    enemiesKilledTextRect = enemiesKilledText.get_rect()
    timeSurvivedTextRect=timeSurvivedText.get_rect()

# set the center of the rectangular object.
    enemiesKilledTextRect.center = (500, 50)
    timeSurvivedTextRect.center = (500, 100)



    # enemyhitbox=pygame.draw.rect(displaysurface,(255,0,0), pygame.Rect(enemy.pos.x-20,enemy.pos.y-30,110,130))
    # enemy2hitbox=pygame.draw.rect(displaysurface,(255,0,0), pygame.Rect(enemy2.pos.x-20,enemy2.pos.y-30,110,130))
    # enemy3hitbox=pygame.draw.rect(displaysurface,(255,0,0), pygame.Rect(enemy3.pos.x-20,enemy3.pos.y-30,110,130))
    # enemy4hitbox=pygame.draw.rect(displaysurface,(255,0,0), pygame.Rect(enemy4.pos.x-20,enemy4.pos.y-30,110,130))
    # hitboxsword=pygame.draw.rect(displaysurface,(255,0,0), pygame.Rect(player.pos.x+50,player.pos.y+0,40,50))


    #collide detection 
    collide_1and2=pygame.Rect.colliderect(enemy.hitbox,enemy2.hitbox)
    collide_1and3=pygame.Rect.colliderect(enemy.hitbox,enemy3.hitbox)
    collide_1and4=pygame.Rect.colliderect(enemy.hitbox,enemy4.hitbox)
    collide_2and3=pygame.Rect.colliderect(enemy2.hitbox,enemy3.hitbox)
    collide_2and4=pygame.Rect.colliderect(enemy2.hitbox,enemy4.hitbox)
    collide_3and4=pygame.Rect.colliderect(enemy3.hitbox,enemy4.hitbox)




    playercollide_sword1=pygame.Rect.colliderect(enemy.hitbox,player.hitboxsword) #sword
    playercollide_sword2=pygame.Rect.colliderect(enemy2.hitbox,player.hitboxsword) #sword
    playercollide_sword3=pygame.Rect.colliderect(enemy3.hitbox,player.hitboxsword) #sword
    playercollide_sword4=pygame.Rect.colliderect(enemy4.hitbox,player.hitboxsword) #sword

    playercollide_body1=pygame.Rect.colliderect(enemy.hitbox,player.hitboxbody) #body
    playercollide_body2=pygame.Rect.colliderect(enemy2.hitbox,player.hitboxbody) #body
    playercollide_body3=pygame.Rect.colliderect(enemy3.hitbox,player.hitboxbody) #body
    playercollide_body4=pygame.Rect.colliderect(enemy4.hitbox,player.hitboxbody) #body


    playercollide_lr1=pygame.Rect.colliderect(enemy.hitbox,player.playerlongrangehitbox) #long range hitbox
    playercollide_1r2=pygame.Rect.colliderect(enemy2.hitbox,player.playerlongrangehitbox) #long range hitbox
    playercollide_lr3=pygame.Rect.colliderect(enemy3.hitbox,player.playerlongrangehitbox) #long range hitbox
    playercollide_1r4=pygame.Rect.colliderect(enemy4.hitbox,player.playerlongrangehitbox) #long range hitbox
    key_pressed=pygame.key.get_pressed()
    
    if playercollide_sword1 and player.shortRangeAttack:
        enemy.diedshortrange=True
        enemy.isdead=True
        enemiesKilled+=1
        startDeathTime=time.time()
        player.shortRangeAttack=False
    elif playercollide_sword2 and player.shortRangeAttack:
        enemy2.diedshortrange=True
        enemy2.isdead=True
        enemiesKilled+=1
        startDeathTime=time.time()
        player.shortRangeAttack=False
    elif playercollide_sword3 and player.shortRangeAttack:
        enemy3.diedshortrange=True
        enemy3.isdead=True
        enemiesKilled+=1
        startDeathTime=time.time()
        player.shortRangeAttack=False
    elif playercollide_sword4 and player.shortRangeAttack:
        enemy4.diedshortrange=True
        enemy4.isdead=True
        enemiesKilled+=1
        startDeathTime=time.time()
        player.shortRangeAttack=False


    if collide_1and2:
        enemy.bouncing=True
        enemy2.bouncing=True
    if collide_1and2==False:
        enemy.bouncing=False
        enemy2.bouncing=False

    if collide_1and3:
        enemy.bouncing=True
        enemy3.bouncing=True
    if collide_1and3==False:
        enemy.bouncing=False
        enemy3.bouncing=False

    if collide_1and4:
        enemy.bouncing=True
        enemy4.bouncing=True
    if collide_1and4==False:
        enemy.bouncing=False
        enemy4.bouncing=False

    if collide_2and3:
        enemy2.bouncing=True
        enemy3.bouncing=True
    if collide_2and3==False:
        enemy2.bouncing=False
        enemy3.bouncing=False

    if collide_2and4:
        enemy2.bouncing=True
        enemy4.bouncing=True
    if collide_2and4==False:
        enemy2.bouncing=False
        enemy4.bouncing=False

    if collide_3and4:
        enemy3.bouncing=True
        enemy4.bouncing=True
    if collide_3and4==False:
        enemy3.bouncing=False
        enemy4.bouncing=False



    if playercollide_body1 and enemy.isdead==False and enemy.attacking:
        enemy.touchingPlayer=True
        player.playerhealth-=1
        startLosingHealthTime=time.time()
    if playercollide_body2 and enemy2.isdead==False and enemy2.attacking:
        enemy2.touchingPlayer=True
        player.playerhealth-=1
        startLosingHealthTime=time.time()
    if playercollide_body3 and enemy3.isdead==False and enemy3.attacking:
        enemy3.touchingPlayer=True
        player.playerhealth-=1
        startLosingHealthTime=time.time()
    if playercollide_body4 and enemy4.isdead==False and enemy4.attacking:
        enemy4.touchingPlayer=True
        player.playerhealth-=1
        startLosingHealthTime=time.time()

    if playercollide_body1==False:
        enemy.touchingPlayer=False
    if playercollide_body2==False:
        enemy2.touchingPlayer=False
    if playercollide_body3==False:
        enemy3.touchingPlayer=False
    if playercollide_body4==False:
        enemy4.touchingPlayer=False



    if playercollide_lr1 and enemy.isdead==False and player.longRangeAttack==True:
        enemy.diedshortrange=False
        enemy.isdead=True
        enemiesKilled+=1
        startDeathTime=time.time()
        player.longRangeAttack=False

    if playercollide_1r2 and enemy2.isdead==False and player.longRangeAttack==True:
        enemy2.diedshortrange=False
        enemy2.isdead=True
        enemiesKilled+=1
        startDeathTime=time.time()
        player.longRangeAttack=False
    if playercollide_lr3 and enemy3.isdead==False and player.longRangeAttack==True:
        enemy3.diedshortrange=False
        enemy3.isdead=True
        enemiesKilled+=1
        startDeathTime=time.time()
        player.longRangeAttack=False

    if playercollide_1r4 and enemy4.isdead==False and player.longRangeAttack==True:
        enemy4.diedshortrange=False
        enemy4.isdead=True
        enemiesKilled+=1
        startDeathTime=time.time()
        player.longRangeAttack=False
    background.render()



    def game_over():
        gameOverText=font.render("GAME OVER", True, (0,255,0))
        totalEnemiesKilledText = font.render("You Killed "+str(enemiesKilled)+" Enemies", True,(0,255,0))
        totalTimeSurvivedText = font.render("You Survived For "+totalTimeSurvived, True,(0,255,0))
        gameOverTextRect=gameOverText.get_rect()
        totalEnemiesKilledTextRect=totalEnemiesKilledText.get_rect()
        totalTimeSurvivedTextRect=totalTimeSurvivedText.get_rect()
        gameOverTextRect.center = (500, 350)
        totalEnemiesKilledTextRect.center = (500, 400)
        totalTimeSurvivedTextRect.center = (500,450)
        displaysurface.blit(gameOverText, gameOverTextRect)
        displaysurface.blit(totalEnemiesKilledText,totalEnemiesKilledTextRect)
        displaysurface.blit(totalTimeSurvivedText,totalTimeSurvivedTextRect)
        pygame.display.update()
        time.sleep(5)
        pygame.quit()
        sys.exit()







    if player.playerhealth>0:
        displaysurface.blit(player.image,player.rect)
        displaysurface.blit(enemy2.image,enemy2.rect)
        displaysurface.blit(enemy.image,enemy.rect)  
        displaysurface.blit(enemy3.image,enemy3.rect)
        displaysurface.blit(enemy4.image,enemy4.rect)  
        displaysurface.blit(enemiesKilledText, enemiesKilledTextRect)
        displaysurface.blit(timeSurvivedText, timeSurvivedTextRect)
        player.healthBar()
    else:
        totalTimeSurvived=(minutes+":"+seconds)
        game_over()

    pygame.display.update()
    FPS_CLOCK  .tick(FPS)
