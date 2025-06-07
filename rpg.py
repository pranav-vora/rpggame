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
        self.image=pygame.image.load("images/enemy.png")
        self.vx=0
        self.vy=0
        self.surf = pygame.Surface((30,30))
        self.size = self.image.get_size()
        self.image=pygame.transform.scale(self.image, (int(self.size[0]*0.5), int(self.size[1]*0.5)))#enemy size: 98x126
        print(self.image)
        print(self.size)
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
        if time.time()-self.startAttackTime>2:
            self.attacking=True
            self.startAttackTime=time.time()
        # print(time.time()-self.startAttackTime) 
        
        if time.time()-self.startAttackTime>0.1:
            self.attacking=False

    def shortRangeDeath(self):
        if self.isdead==True and self.diedshortrange==True:
            self.image=pygame.image.load("images/enemy_short_range_death.png")

            if time.time()-startDeathTime>2:
                self.image=pygame.image.load("images/enemy.png")
                self.vx=0
                self.vy=0
                self.surf = pygame.Surface((30,30))
                self.size = self.image.get_size()
                self.image=pygame.transform.scale(self.image, (int(self.size[0]*0.5), int(self.size[1]*0.5)))#enemy size: 98x126
                print(self.image)
                print(self.size)
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
    def longRangeDeath(self):
        if self.isdead==True and self.diedshortrange==False:
            # print(time.time()-startDeathTime)
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
            if time.time()-startDeathTime>3:
                self.image=pygame.image.load("images/enemy.png")
                self.vx=0
                self.vy=0
                self.surf = pygame.Surface((30,30))
                self.size = self.image.get_size()
                self.image=pygame.transform.scale(self.image, (int(self.size[0]*0.5), int(self.size[1]*0.5)))#enemy size: 98x126
                print(self.image)
                print(self.size)
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



class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.last_time_attacked=time.time()
        self.image=pygame.image.load("images/player.png") #self addresses the classes attributes
        self.vx=0
        self.vy=0
        self.surf = pygame.Surface((30,30))
        self.size = self.image.get_size()
        print(self.size)
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
        # print(time.time()-self.startAttackTime)
        key_pressed=pygame.key.get_pressed()
        if key_pressed[K_SPACE] and time.time()-self.startAttackTime>2:
            self.attacking=True
            self.shortRangeAttack=True
            self.startAttackTime=time.time()
        if event.type==pygame.KEYDOWN and  event.key == pygame.K_RSHIFT and time.time()-self.startAttackTime>10:
            self.attacking=True
            self.longRangeAttack=True
            self.startAttackTime=time.time()
        # print(time.time()-self.startAttackTime) 
        
        
        if time.time()-self.startAttackTime>0.25:
            self.attacking=False
            self.shortRangeAttack=False
            self.longRangeAttack=False
    def healthBar(self):
        pass
    def execute(self):
        self.move()
        self.swordhitbox()
        self.bodyhitbox()
        self.knockbackhitbox()
        self.isAttacking()
        self.healthBar()

        
            
        
collideList=[]      

player=Player() #adds an instance of the player class to create a player
enemy=Enemy()
enemy2=Enemy()
enemy3=Enemy()
background=Background()
enemyDict={1:(enemy,[[]]),2:(enemy2,[[]]),3:(enemy3,[[]])}
# the plan is to for every element in enemy list, we want to make each of the elements into a dictionary
#  and set each of the keys to collide detection with the player and other enemies.
while True:
    for event in pygame.event.get():
        if event.type==QUIT:
            pygame.quit()
            sys.exit()
    # for enemies in enemydict:
    #     enemies.execute()
    #     for i in range(len(enemydict)):

    for i in enemyDict.values():
        i[0].execute()  
        print("________")   
    #     for j in range(len(enemyDict)-1):
    #         temp = (pygame.Rect.colliderect(i[0].hitbox,player.hitboxsword))
    #         i[1][0].append(temp)
            
    # print(enemyDict[1])
    print("spacing")
        #     collide=pygame.Rect.colliderect(i[0].hitbox,j[0].hitbox)
        # playercollide1=pygame.Rect.colliderect(enemy.hitbox,player.hitboxsword) #sword
        # playercollide2=pygame.Rect.colliderect(enemy2.hitbox,player.hitboxsword) #sword
        # playercollide3=pygame.Rect.colliderect(enemy.hitbox,player.hitboxbody) #body
        # playercollide4=pygame.Rect.colliderect(enemy2.hitbox,player.hitboxbody) #body
        # playercollide5=pygame.Rect.colliderect(enemy.hitbox,player.playerlongrangehitbox) #long range hitbox
        # playercollide6=pygame.Rect.colliderect(enemy2.hitbox,player.playerlongrangehitbox) #long range hitbox
    player.execute()


    background.render()
    pygame.draw.rect(displaysurface,(255,0,0), (250, 250, 300, 40))
    pygame.draw.rect(displaysurface,(0,255,0), (250, 250, 300 * player.ratio, 40))
    player.ratio=player.playerhealth/player.maxhealth



    #collide detection
    collide=pygame.Rect.colliderect(enemy.hitbox,enemy2.hitbox)
    playercollide1=pygame.Rect.colliderect(enemy.hitbox,player.hitboxsword) #sword
    playercollide2=pygame.Rect.colliderect(enemy2.hitbox,player.hitboxsword) #sword
    playercollide3=pygame.Rect.colliderect(enemy.hitbox,player.hitboxbody) #body
    playercollide4=pygame.Rect.colliderect(enemy2.hitbox,player.hitboxbody) #body
    playercollide5=pygame.Rect.colliderect(enemy.hitbox,player.playerlongrangehitbox) #long range hitbox
    playercollide6=pygame.Rect.colliderect(enemy2.hitbox,player.playerlongrangehitbox) #long range hitbox
    key_pressed=pygame.key.get_pressed()
    
    if playercollide1 and player.shortRangeAttack:
        enemy.diedshortrange=True
        enemy.isdead=True
        startDeathTime=time.time()
    if playercollide2 and player.shortRangeAttack:
        enemy2.diedshortrange=True
        enemy2.isdead=True
        startDeathTime=time.time()
    if collide:
        enemy.bouncing=True
        enemy2.bouncing=True
    if collide==False:
        enemy.bouncing=False
        enemy2.bouncing=False
        # print("COLLIDE")



    if playercollide3 and enemy.isdead==False and enemy.attacking:
        enemy.touchingPlayer=True
        player.playerhealth-=1
        startLosingHealthTime=time.time()
    if playercollide4 and enemy2.isdead==False and enemy.attacking:
        enemy2.touchingPlayer=True
        player.playerhealth-=1
        startLosingHealthTime=time.time()

    if playercollide3==False:
        enemy.touchingPlayer=False
    if playercollide4==False:
        enemy2.touchingPlayer=False

    print(player.playerhealth)

    if playercollide5 and enemy.isdead==False and player.longRangeAttack==True:
        enemy.diedshortrange=False
        enemy.isdead=True
        startDeathTime=time.time()

    if playercollide6 and enemy.isdead==False and player.longRangeAttack==True:
        enemy2.diedshortrange=False
        enemy2.isdead=True
        startDeathTime=time.time()


    # print ("enemyvelx", enemy.vel.x, "enemyvely", enemy.vel.y, "enemy2velx", enemy2.vel.x,"enemy2vely", enemy2.vel.y)
    # print ("\nenemyposx", enemy.pos.x, "enemyposy", enemy.pos.y, "enemy2posx", enemy2.pos.x,"enemy2posy", enemy2.pos.y)

    displaysurface.blit(player.image,player.rect)
    displaysurface.blit(enemy2.image,enemy2.rect)
    displaysurface.blit(enemy.image,enemy.rect)#displays the player   
    pygame.display.update()
    FPS_CLOCK  .tick(FPS)
