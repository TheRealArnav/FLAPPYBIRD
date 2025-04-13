import pygame
import time
from pygame.locals import*
pygame.init()
pygame.font.init()

screen = pygame.display.set_mode((864,936))

#images
ground = pygame.image.load("C:/Pygame2/images/flappybird/groundimg.png")
bg = pygame.image.load("C:/Pygame2/images/flappybird/bg.png")


fps = 60

clock = pygame.time.Clock()

groundscroll = 0
scrollspeed = 4
flying = False
Gameover = False

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

            self.image = pygame.transform.rotate(self.image,(self.vel * -2))
        elif Gameover == True:
            self.image = pygame.transform.rotate(self.image,(-90))




birdgroup = pygame.sprite.Group()
bird = Bird(150,936//2)
birdgroup.add(bird)



run = True

while run:

    

    clock.tick(fps)
    screen.blit(bg,(0,0))
    screen.blit(ground,(groundscroll,768))
    if Gameover == False:
        groundscroll = groundscroll - scrollspeed
        if abs(groundscroll) > 35 and Gameover == False:
            groundscroll = 0
    if bird.rect.bottom > 768:
        Gameover = True
        flying = False

    

    birdgroup.draw(screen)
    #pygame.display.flip() 
    birdgroup.update()
    
    for event in pygame.event.get():
        if event.type == QUIT:
            quit()
        if event.type == pygame.MOUSEBUTTONDOWN and flying == False and Gameover == False:
            flying = True
    pygame.display.update()

