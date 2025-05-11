import pygame
import time
from pygame.locals import*
import random
pygame.init()
pygame.font.init()

WIDTH = 864
HEIGHT = 936

screen = pygame.display.set_mode((WIDTH,HEIGHT))

#images
ground = pygame.image.load("C:/Pygame2/images/flappybird/groundimg.png")
bg = pygame.image.load("C:/Pygame2/images/flappybird/bg.png")


fps = 60

clock = pygame.time.Clock()

groundscroll = 0
scrollspeed = 4
flying = False
Gameover = False
gap = 120
pipefrequency = 1500
lastpipe = pygame.time.get_ticks() - pipefrequency
score = 0
pass_pipe = False

restart = pygame.image.load("C:/Pygame2/images/flappybird/restart.png")



class pipe(pygame.sprite.Sprite):
    def __init__(self,x,y,position):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("C:/Pygame2/images/flappybird/pole.png")
        self.rect = self.image.get_rect()

        if position == 1:
            self.rect.topleft = (x,y+(gap//2))
        elif position == -1:
            self.image = pygame.transform.flip(self.image,False,True)
            self.rect.bottomleft = (x,y-(gap//2))
    def update(self):
        self.rect.x = self.rect.x - scrollspeed
        if self.rect.right < 0:
            self.kill()



class Button(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("C:/Pygame2/images/flappybird/restart.png")
        self.rect = pygame.Rect(x,y,100,100)
        self.rect.center = (x,y)
    def draw(self):
        action = False

        pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(pos):
            print (pos)
            if pygame.mouse.get_pressed()[0] == 1:
                action = True
        screen.blit(self.image,(self.rect.x,self.rect.y))
        return action



class Bird(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.images = []
        self.index = 0
        self.counter = 0
        self.vel = 0
        self.clicked = False
        for num in range(1,4):
            bird = pygame.image.load("C:/Pygame2/images/flappybird/bird"+str(num)+".png")
            self.images.append(bird)
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)
    def update(self):
        if flying == True:
                self.vel = self.vel + 0.5
                if self.vel > 8:
                    self.vel = 8
                if self.rect.bottom < 768:
                    self.rect.y = self.rect.y + self.vel
        if Gameover == False:
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                self.clicked = True
                self.vel = -8
            if pygame.mouse.get_pressed()[0] == 0:
                self.clicked = False
            
                
            

            
            self.counter = self.counter + 1
            flapcooldown = 5
            if self.counter > flapcooldown:
                self.counter = 0
                self.index = self.index + 1
                if self.index >= len(self.images):
                    self.index = 0
                self.image = self.images[self.index]

            self.image = pygame.transform.rotate(self.images[self.index],(self.vel * -2))
        elif Gameover == True:
            self.image = pygame.transform.rotate(self.images[self.index],(-90))




birdgroup = pygame.sprite.Group()
bird = Bird(150,936//2)
birdgroup.add(bird)

polegroup = pygame.sprite.Group()

scorefont = pygame.font.SysFont("Bauhaus 93",45)

restart = Button(432,468)

def displayscore(score):
    displayed_score = scorefont.render(score,True,"white")
    screen.blit(displayed_score,(WIDTH//2,30))



run = True

while run:

    

    clock.tick(fps)
    screen.blit(bg,(0,0))
    screen.blit(ground,(groundscroll,768))


    if Gameover == False and flying == True:
        groundscroll = groundscroll - scrollspeed
        if abs(groundscroll) > 35 and Gameover == False:
            groundscroll = 0

        TIME = pygame.time.get_ticks()
        if TIME - lastpipe > pipefrequency:
            pipeheight = random.randint(-100,100)  
            bottompipe = pipe(WIDTH,HEIGHT//2+pipeheight,1)
            toppipe = pipe(WIDTH,HEIGHT//2+pipeheight,-1)
            lastpipe = pygame.time.get_ticks()
            polegroup.add(bottompipe)
            polegroup.add(toppipe)
            polegroup.draw(screen)

    polegroup.update()
    if bird.rect.bottom > 768:
        Gameover = True
        flying = False

    if pygame.sprite.groupcollide(birdgroup,polegroup,False,False) or bird.rect.top < 0:
        Gameover = True
        flying = False
        velocity = 0
        

    

    birdgroup.draw(screen)
    birdgroup.update()
    polegroup.draw(screen)
    polegroup.update()
    
    #pygame.display.flip() 

      
    pygame.display.update()

    for event in pygame.event.get():
        if event.type == QUIT:
            quit()
        if event.type == MOUSEBUTTONDOWN and flying == False and Gameover == False:
            flying = True

   
    if len(polegroup) > 0:
        if birdgroup.sprites()[0].rect.left > polegroup.sprites()[0].rect.left and birdgroup.sprites()[0].rect.right < polegroup.sprites()[0].rect.right and pass_pipe == False:
            pass_pipe = True
        if pass_pipe == True:
            if birdgroup.sprites()[0].rect.left > polegroup.sprites()[0].rect.right:
                score = score + 1
                pass_pipe = False
    displayscore(str(score))


    if Gameover == True and flying == False:
        restart.draw()






        
    pygame.display.update()

