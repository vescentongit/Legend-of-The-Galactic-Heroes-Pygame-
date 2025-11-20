import pygame
from random import randint
pygame.init()
pygame.mouse.set_visible(False)
running = True
clock = pygame.time.Clock()
MIN_WIDTH,MIN_HEIGHT = 840,500
screen = pygame.display.set_mode((MIN_WIDTH,MIN_HEIGHT))
fullscreen = False

# BACKGROUND
bg_original = pygame.image.load('assets/space.jpg').convert_alpha()
background = pygame.transform.scale(bg_original, (screen.get_width(), screen.get_height()))

# LOGO
logo = pygame.image.load('assets/ship.png').convert_alpha()
pygame.display.set_icon(logo)
pygame.display.set_caption('Legend of the Galatic Heroes')

class Ship(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.imageOriginal = pygame.image.load('assets/ship.png').convert_alpha()
        self.image = pygame.transform.scale(self.imageOriginal, (60,65))
        self.rect = self.image.get_rect(center = ((screen.get_width()/2),(screen.get_height()-100)))
        
    def updateSize(self, fullscreen):
        oldCenter = self.rect.center
        if fullscreen:
            self.image = pygame.transform.scale(self.imageOriginal, (100,110))
        else:
            self.image = pygame.transform.scale(self.imageOriginal, (60,65))
        
        self.rect = self.image.get_rect(center=oldCenter)
    
    def update(self):
        self.updateSize(fullscreen)
            
class Meteor(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        meteor1 = pygame.image.load('assets/meteor.png').convert_alpha()
        meteor2 = pygame.image.load('assets/meteor2.png').convert_alpha()
        meteor3 = pygame.image.load('assets/meteor3.png').convert_alpha()
        meteor4 = pygame.image.load('assets/meteor4.png').convert_alpha()
        
        self.frames = [meteor1, meteor2, meteor3, meteor4]
        self.animationIndex = 0
        self.image = pygame.transform.scale(self.frames[self.animationIndex], (80,80))
        self.rect = self.image.get_rect(midtop = (randint(100,screen.get_width()-100),0))
    
    def animationState(self):
        self.animationIndex += 0.05
        if self.animationIndex >= len(self.frames) : self.animationIndex = 0
        self.image = self.frames[int(self.animationIndex)]
        
    def updateSize(self, fullscreen):
        oldCenter = self.rect.center
        if fullscreen:
            self.image = pygame.transform.scale(self.image, (130,140))
        else:
            self.image = pygame.transform.scale(self.image, (80,85))
        
        self.rect = self.image.get_rect(center=oldCenter)
        
    def getSpeed(self, fullscreen):
        if fullscreen:
            return 6
        else:
            return 3
    
    def destroy(self):
        if self.rect.bottom <= 0:
            self.kill()
    
    def update(self):
        self.animationState()
        self.updateSize(fullscreen)
        self.rect.y += self.getSpeed(fullscreen)
        self.destroy()

class Beam(pygame.sprite.Sprite):
    def __init__(self, startPos):
        super().__init__()
        self.imageOriginal = self.imageOriginal = pygame.image.load('assets/beam.png').convert_alpha()
        self.image = pygame.transform.scale(self.imageOriginal, (7,20))
        self.rect = self.image.get_rect(center = startPos)
    
    def updateSize(self, fullscreen):
        oldCenter = self.rect.center
        if fullscreen:
            self.image = pygame.transform.scale(self.imageOriginal, (14,40))
        else:
            self.image = pygame.transform.scale(self.imageOriginal, (7,20))
        
        self.rect = self.image.get_rect(center=oldCenter)
    
    def getSpeed(self, fullscreen):
        if fullscreen:
            return 10
        else:
            return 5
    
    def destroy(self):
        if self.rect.bottom <= 0:
            self.kill()
    
    def update(self):
        self.updateSize(fullscreen)
        self.rect.y -= self.getSpeed(fullscreen)
        self.destroy()
    

# WARSHIP GROUP
warship = pygame.sprite.GroupSingle()
warship.add(Ship())

# BEAM GROUP
beamGroup = pygame.sprite.Group()

# METEOR GROUP
meteorGroup = pygame.sprite.Group()

obstacleTimer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacleTimer,1000)

# GAME LOOP
while running:
    screen.blit(background, (0,0))
    
    # EVENT HANDLER
    for event in pygame.event.get():
        # QUIT
        if event.type == pygame.QUIT:
            running = False

        # METEOR SPAWNER
        if event.type == obstacleTimer:
            meteorGroup.add(Meteor())
            
        # KEYDOWN
        if event.type == pygame.KEYDOWN:
            
            # FULLSCREEN HANDLER
            if event.key == pygame.K_F11:
                fullscreen = not fullscreen
                if fullscreen:
                    screen = pygame.display.set_mode((0,0),pygame.FULLSCREEN)
                else:
                    screen = pygame.display.set_mode((MIN_WIDTH,MIN_HEIGHT))
                background = pygame.transform.scale(bg_original, (screen.get_width(), screen.get_height()))
            
            # BEAM SPAWNER
            if event.key == pygame.K_SPACE:
                beamGroup.add(Beam(warship.sprite.rect.midtop))
                
        # WARSHIP MOVER
        if event.type == pygame.MOUSEMOTION:
            mousePos = pygame.mouse.get_pos()
            warship.sprite.rect.center = mousePos
            
            # BORDER HANDLER
            if warship.sprite.rect.left <= 0:
                warship.sprite.rect.left = 0
            if warship.sprite.rect.top <= (screen.get_height()*3/4):
                warship.sprite.rect.top = screen.get_height()*3/4
            if warship.sprite.rect.right >= screen.get_width():
                warship.sprite.rect.right = screen.get_width()
            if warship.sprite.rect.bottom >= screen.get_height():
                warship.sprite.rect.bottom = screen.get_height()
                        
    warship.draw(screen)
    warship.update()
    beamGroup.draw(screen)
    beamGroup.update()
    meteorGroup.draw(screen)
    meteorGroup.update()
    
    print(beamGroup)
    
    
    pygame.display.update()
    clock.tick(60)

pygame.quit()