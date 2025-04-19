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
class Background(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__() #adds the sprite attributes to the background class
        self.bgimage=pygame.image.load("pixilart-drawing (1).png")
        self.bgX=0
        self.bgY=0
    def render(self):
        displaysurface.blit(self.bgimage, (self.bgX, self.bgY))
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__() 
        self.image=pygame.image.load("enemy.png")
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
    def move(self):
        self.movementx=player.pos.x-self.pos.x
        self.movementy=player.pos.y-self.pos.y
        if self.movementx>0 and self.movementy>0 and self.bouncing==False:
            self.acc.x=ACC*0.5
            self.acc.y=ACC*0.5
        if self.movementx<0 and self.movementy>0 and self.bouncing==False:
            self.acc.x=-ACC*0.5
            self.acc.y=ACC*0.5
        if self.movementx>0 and self.movementy<0 and self.bouncing==False:
            self.acc.x=ACC*0.5
            self.acc.y=-ACC*0.5
        if self.movementx<0 and self.movementy<0 and self.bouncing==False:
            self.acc.x=-ACC*0.5
            self.acc.y=-ACC*0.5
        if self.bouncing==True:
            self.vel=-self.vel*random.randint(2,5)*5

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


        if self.isdead==False:
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
        self.death()
        self.isattacking()
    def isattacking(self):
        if time.time()-self.startAttackTime>2:
            self.attacking=True
            self.startAttackTime=time.time()
        # print(time.time()-self.startAttackTime) 
        
        if time.time()-self.startAttackTime>0.1:
            self.attacking=False

    def death(self):
        if self.isdead==True:
            self.image=pygame.image.load("enemy_death.png")
            print(time.time()-startDeathTime)
            if time.time()-startDeathTime>2:
                self.image=pygame.image.load("enemy.png")
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



class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.last_time_attacked=time.time()
        self.image=pygame.image.load("player.png") #self addresses the classes attributes
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
        self.lastAttackTime=0
        self.hitboxsword=pygame.draw.rect(displaysurface,(255,0,0), pygame.Rect(self.pos.x+50,self.pos.y+0,40,50))
        self.startAttackTime=time.time()
        self.playerhealth=100
        self.bouncing=False
        self.playerknockbackhitbox=pygame.draw.rect(displaysurface,(255,255,0), pygame.Rect(self.pos.x-400,self.pos.y+0,400,50))   
    def move(self):
        pressed_keys = pygame.key.get_pressed()
        if pressed_keys[K_LEFT] and self.attacking==False and self.bouncing==False:
            self.acc.x =-ACC
            self.playerisflipped=True
        if pressed_keys[K_RIGHT] and self.attacking==False and self.bouncing==False:
            self.acc.x=ACC
            self.playerisflipped=False
        if pressed_keys[K_UP] and self.attacking==False and self.bouncing==False:
            self.acc.y =-ACC
        if pressed_keys[K_DOWN] and self.attacking==False and self.bouncing==False:
            self.acc.y=ACC



        self.acc.x += self.vel.x * FRIC
        self.acc.y += self.vel.y * FRIC
        self.vel += self.acc
        if self.bouncing==True:
            self.vel=-self.vel*random.randint(2,5)*5
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
            self.image=pygame.image.load("player.png")
            self.size = self.image.get_size()
            self.image=pygame.transform.scale(self.image, (int(self.size[0]*0.5), int(self.size[1]*0.5)))
        elif self.playerisflipped==True and self.attacking==False:
            self.image=pygame.image.load("player_flipped.png")
            self.size = self.image.get_size()
            self.image=pygame.transform.scale(self.image, (int(self.size[0]*0.5), int(self.size[1]*0.5)))
        elif self.playerisflipped==False and self.attacking==True:
            self.image=pygame.image.load("player_rotated.png")
            self.size = self.image.get_size()
            self.image=pygame.transform.scale(self.image, (int(self.size[0]*0.5), int(self.size[1]*0.5)))
        else:
            self.image=pygame.image.load("player_flipped_rotated.png")
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
                self.playerknockbackhitbox=pygame.draw.rect(displaysurface,(255,255,0), pygame.Rect(self.pos.x,self.pos.y+0,400,50))  
            else:
                self.playerknockbackhitbox=pygame.draw.rect(displaysurface,(255,255,0), pygame.Rect(self.pos.x-400,self.pos.y+0,400,50))         
    def isAttacking(self):
        key_pressed=pygame.key.get_pressed()
        if key_pressed[K_SPACE] and time.time()-self.startAttackTime>2:
            self.attacking=True
            self.startAttackTime=time.time()
        # print(time.time()-self.startAttackTime) 
        
        
        if time.time()-self.startAttackTime>0.25:
            self.attacking=False

    def execute(self):
        self.move()
        self.swordhitbox()
        self.bodyhitbox()
        self.knockbackhitbox()
        self.isAttacking()

player=Player() #adds an instance of the player class to create a player
enemy=Enemy()
enemy2=Enemy()
background=Background()
while True:
    for event in pygame.event.get():
        if event.type==QUIT:
            pygame.quit()
            sys.exit()
    player.execute()
    enemy.execute()
    enemy2.execute()
    background.render()
    
    #collide detection
    collide=pygame.Rect.colliderect(enemy.hitbox,enemy2.hitbox)
    playercollide1=pygame.Rect.colliderect(enemy.hitbox,player.hitboxsword) #sword
    playercollide2=pygame.Rect.colliderect(enemy2.hitbox,player.hitboxsword) #sword
    playercollide3=pygame.Rect.colliderect(enemy.hitbox,player.hitboxbody) #body
    playercollide4=pygame.Rect.colliderect(enemy2.hitbox,player.hitboxbody) #body
    playercollide5=pygame.Rect.colliderect(enemy.hitbox,player.playerknockbackhitbox) #knockback hitbox
    playercollide6=pygame.Rect.colliderect(enemy2.hitbox,player.playerknockbackhitbox) #knockback hitbox
    print (playercollide5)
    print (playercollide6)
    key_pressed=pygame.key.get_pressed()
    
    if playercollide1 and player.attacking:
        enemy.isdead=True
        startDeathTime=time.time()
    if playercollide2 and player.attacking:
        enemy2.isdead=True
        startDeathTime=time.time()
    if collide:
        enemy.bouncing=True
        enemy2.bouncing=True
        # print("COLLIDE")
    if playercollide3 and enemy.isdead==False and enemy.attacking:
        player.playerhealth-=1
        startLosingHealthTime=time.time()
    if playercollide4 and enemy2.isdead==False and enemy.attacking:
        player.playerhealth-=1
        startLosingHealthTime=time.time()

    if playercollide5 and enemy.isdead==False and player.attacking==True:
        enemy.bouncing=True
    if playercollide6 and enemy.isdead==False and player.attacking==True:
        enemy2.bouncing=True

    if collide==False and playercollide5==False and playercollide6==False:
        enemy.bouncing=False
        enemy2.bouncing=False

    # print ("enemyvelx", enemy.vel.x, "enemyvely", enemy.vel.y, "enemy2velx", enemy2.vel.x,"enemy2vely", enemy2.vel.y)
    # print ("\nenemyposx", enemy.pos.x, "enemyposy", enemy.pos.y, "enemy2posx", enemy2.pos.x,"enemy2posy", enemy2.pos.y)

    displaysurface.blit(player.image,player.rect)
    displaysurface.blit(enemy2.image,enemy2.rect)
    displaysurface.blit(enemy.image,enemy.rect)#displays the player
        
    pygame.display.update()
    FPS_CLOCK  .tick(FPS)
