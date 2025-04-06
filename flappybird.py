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


class Bird(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.images = []
        self.index = 0
        self.counter = 0
        for num in range(1,4):
            bird = pygame.image.load("C:/Pygame2/images/flappybird/bird"+str(num)+".png")
            self.images.append(bird)
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)
    def update(self):
        self.counter = self.counter + 1
        flapcooldown = 5
        if self.counter > flapcooldown:
            self.counter = 0
            self.index = self.index + 1
            if self.index >= len(self.images):
                self.index = 0
            self.image = self.images[self.index]




birdgroup = pygame.sprite.Group()
bird = Bird(150,936//2)
birdgroup.add(bird)



run = True

while run:

    

    clock.tick(fps)
    screen.blit(bg,(0,0))
    screen.blit(ground,(groundscroll,768))
    groundscroll = groundscroll - scrollspeed
    if abs(groundscroll) > 35:
        groundscroll = 0


    birdgroup.draw(screen)
    pygame.display.flip() 
    bird.update()
    
    for event in pygame.event.get():
        if event.type == QUIT:
            quit()
    pygame.display.flip()

