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
        self.pos=vec((random.randint(0,1000),random.randint(0,800)))#vec=vector
        self.vel=vec(0,0)
        self.acc=vec(0,0)
        self.direction="RIGHT"
        displaysurface.blit(self.image, (self.vx, self.vy))
        self.bouncing=False
        self.delete=False
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
        self.acc.x += self.vel.x * FRIC
        self.acc.y += self.vel.y * FRIC
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc
        self.rect.midbottom = self.pos
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image=pygame.image.load("player.png") #self addresses the classes attributes
        self.vx=0
        self.vy=0
        self.surf = pygame.Surface((30,30))
        self.size = self.image.get_size()
        print(self.size)
        self.image=pygame.transform.scale(self.image, (int(self.size[0]*0.5), int(self.size[1]*0.5)))
        self.rect = self.surf.get_rect()
        self.pos=vec((340,240))#vec=vector
        self.vel=vec(0,0)
        self.acc=vec(0,0)
        self.direction="RIGHT"
        displaysurface.blit(self.image, (self.vx, self.vy))
        self.playerisflipped=False
        self.attacking=False
        self.lastAttackTime=0
    def move(self):
        pressed_keys = pygame.key.get_pressed()
        if pressed_keys[K_LEFT]:
            self.acc.x =-ACC
            self.image=pygame.image.load("player_flipped.png")
            self.playerisflipped=True
            self.size = self.image.get_size()
            self.image=pygame.transform.scale(self.image, (int(self.size[0]*0.5), int(self.size[1]*0.5)))
        if pressed_keys[K_RIGHT]:
            self.acc.x=ACC
            self.image=pygame.image.load("player.png")
            self.playerisflipped=False
            self.size = self.image.get_size()
            self.image=pygame.transform.scale(self.image, (int(self.size[0]*0.5), int(self.size[1]*0.5)))
        if pressed_keys[K_UP]:
            self.acc.y =-ACC
        if pressed_keys[K_DOWN]:
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
     
       
    def update(self):
        self.vel.y=0
    def isAttacking(self):
        key_pressed=pygame.key.get_pressed()
        if key_pressed[K_SPACE]:
            self.attacking=True
            print(str(datetime.now(timezone.utc))[11:23])
                  
            print("attacking")
            
        self.attacking=False

        print("not attacking")
    # def move(self):
    #     pressed_keys=pygame.key.get_pressed()
    #     if pressed_keys[pygame.K_w]:
    #         self.pos.y-=3
    #     if pressed_keys[pygame.K_s]:
    #         self.pos.y+=3
    #     if pressed_keys[pygame.K_a]:
    #         self.pos.x+=3
    #     if pressed_keys[pygame.K_d]:
    #         self.pos.x-=3
player=Player() #adds an instance of the player class to create a player
enemy=Enemy()
enemy2=Enemy()
background=Background()
while True:
    for event in pygame.event.get():
        if event.type==QUIT:
            pygame.quit()
            sys.exit()
    player.move()
    enemy.move()
    enemy2.move()
    color=(255,0,0)
    enemy1hitbox=pygame.draw.rect(displaysurface,color, pygame.Rect(enemy.pos.x-20,enemy.pos.y-30,110,130))
    enemy2hitbox=pygame.draw.rect(displaysurface,color, pygame.Rect(enemy2.pos.x-20,enemy2.pos.y-30,110,130))#hitbox of enemy
    background.render()
    if player.playerisflipped==False:
        playerhitbox=pygame.draw.rect(displaysurface,color, pygame.Rect(player.pos.x+50,player.pos.y+0,40,50))
    else:
        playerhitbox=pygame.draw.rect(displaysurface,color, pygame.Rect(player.pos.x-20,player.pos.y+0,40,50))
    collide=pygame.Rect.colliderect(enemy1hitbox,enemy2hitbox)
    playercollide1=pygame.Rect.colliderect(enemy1hitbox,playerhitbox)
    playercollide2=pygame.Rect.colliderect(enemy2hitbox,playerhitbox)
    key_pressed=pygame.key.get_pressed()
    
    player.isAttacking()
    if playercollide1 and key_pressed[K_SPACE]:
        enemy.delete=True
    if playercollide2 and key_pressed[K_SPACE]:
        enemy2.delete=True
    if collide:
        enemy.bouncing=True
        enemy2.bouncing=True
        # print("COLLIDE")

    if collide==False:
        enemy.bouncing=False
        enemy2.bouncing=False
    # print ("enemyvelx", enemy.vel.x, "enemyvely", enemy.vel.y, "enemy2velx", enemy2.vel.x,"enemy2vely", enemy2.vel.y)
    # print ("\nenemyposx", enemy.pos.x, "enemyposy", enemy.pos.y, "enemy2posx", enemy2.pos.x,"enemy2posy", enemy2.pos.y)
    displaysurface.blit(player.image,player.rect)
    if enemy2.delete==False:
        displaysurface.blit(enemy2.image,enemy2.rect)
    if enemy.delete==False:
        displaysurface.blit(enemy.image,enemy.rect)#displays the player
    pygame.display.update()
    FPS_CLOCK.tick(FPS)
