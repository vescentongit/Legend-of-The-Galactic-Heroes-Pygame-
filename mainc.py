import pygame
from random import randint
pygame.init()

# SCREEN AND SETTINGS
running = True
clock = pygame.time.Clock()
MIN_WIDTH,MIN_HEIGHT = 840,540
screen = pygame.display.set_mode((MIN_WIDTH,MIN_HEIGHT))
fullscreen = False

# GLOBAL VARIABLES
start_time = 0
destroyed = 0
gameState = 'menu'
minimizedMenuFont = 28
minimizedMenuFontSmall = 22

# BACKGROUND
bg_original = pygame.image.load('assets/space.jpg').convert_alpha()
background = pygame.transform.scale(bg_original, (screen.get_width(), screen.get_height()))

# LOGO
logo = pygame.image.load('assets/ship.png').convert_alpha()
pygame.display.set_icon(logo)
pygame.display.set_caption('Legend of the Galatic Heroes')

# FONT
textFont = pygame.font.Font('assets/8bitw.ttf',12)
textFontFS = pygame.font.Font('assets/8bitw.ttf',24)

# SFX
pew = pygame.mixer.Sound('assets/pewfin.mp3')
explosionsfx = pygame.mixer.Sound('assets/explosionsfx.mp3')

pygame.Sound.set_volume(pew,0.5)

# GET TIME
def get_elapsed_time():
    return int(pygame.time.get_ticks() / 120) - start_time

# SHIP SPRITE
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

# METEOR SPRITE
class Meteor(pygame.sprite.Sprite):
    global current_time
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
            self.image = pygame.transform.scale(self.image, (80,80))
        
        self.rect = self.image.get_rect(center=oldCenter)
        
    def getSpeed(self, fullscreen):
        elapsed = get_elapsed_time()
        base_speed = 1 + elapsed * 0.05
        if fullscreen:
            base_speed *= 1.001
        return base_speed

    def destroy(self):
        if self.rect.bottom <= 0:
            self.kill()
    
    def update(self):
        self.animationState()
        self.updateSize(fullscreen)
        self.rect.y += self.getSpeed(fullscreen)
        self.destroy()

# BEAM SPRITE
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

# EXPLOSION SPRITE
class Explosion(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.explosionImage = pygame.image.load('assets/explosion.png').convert_alpha()
        self.image = pygame.transform.scale(self.explosionImage, (80, 80))
        self.rect = self.image.get_rect(center=pos)
        self.lifetime = 15
        self.age = 0
        explosionsfx.play()
    
    def updateSize(self, fullscreen):
        oldCenter = self.rect.center
        if fullscreen:
            self.image = pygame.transform.scale(self.explosionImage, (130,140))
        else:
            self.image = pygame.transform.scale(self.explosionImage, (80,80))
        
        self.rect = self.image.get_rect(center=oldCenter)
    
    def update(self):
        self.age += 1
        self.updateSize(fullscreen)
        if self.age >= self.lifetime:
            
            self.kill()

# BEAM COLLISION MECHANIC
def collision(beamGroup, meteorGroup, explosionGroup):
    global destroyed
    for beam in beamGroup:
        hit_meteors = pygame.sprite.spritecollide(beam, meteorGroup, False)
        if hit_meteors:
            for meteor in hit_meteors:
                destroyed += 1
                explosionGroup.add(Explosion(meteor.rect.center))
                meteor.kill()
                beam.kill()

# DISPLAY SCORE FUNCTION
def displayScore():
    if fullscreen:
        current_time = int(pygame.time.get_ticks() / 120) - start_time
        points = (destroyed*40) + current_time
        score_surf = textFontFS.render(f'Points I {points}',False,'White')
        score_rect = score_surf.get_rect(topleft = (0,0))
        screen.blit(score_surf,score_rect)
        return current_time 
    else:
        current_time = int(pygame.time.get_ticks() / 120) - start_time
        points = (destroyed*40) + current_time
        score_surf = textFont.render(f'Points I {points}',False,'White')
        score_rect = score_surf.get_rect(topleft = (0,0))
        screen.blit(score_surf,score_rect)
        return current_time 

# WARSHIP GROUP
warship = pygame.sprite.GroupSingle()
warship.add(Ship())

# BEAM GROUP
beamGroup = pygame.sprite.Group()

# METEOR GROUP
meteorGroup = pygame.sprite.Group()

explosionGroup = pygame.sprite.Group()

# TIMER TO SPAWN METEOR
obstacleTimer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacleTimer,500)

bgMusic = pygame.mixer.Sound('assets/menumusic.mp3')
bgMusic.play(loops = -1)

# GAME LOOP
while running:
    if gameState == 'menu':
        menuFont = pygame.font.Font('assets/8bitw.ttf', minimizedMenuFont) 
        menuFontSmaller = pygame.font.Font('assets/8bitw.ttf',minimizedMenuFontSmall)
        
        pygame.mouse.set_visible(True)
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
        mousePos = pygame.mouse.get_pos()

        title = menuFont.render('Legend of The Galactic Heroes',False,'White')
        titleRect = title.get_rect(center = (screen.get_width()/2, (screen.get_height()/2)-70))

        startBtn = menuFontSmaller.render('Start',False,'White')
        startBtnRect = startBtn.get_rect(center = (screen.get_width()/2, titleRect.centery + 70))

        exitBtn = menuFontSmaller.render('Exit',False,'White')
        exitBtnRect = exitBtn.get_rect(center = (screen.get_width()/2, startBtnRect.centery + 70))
        
        if startBtnRect.collidepoint(mousePos):
            startBtn = menuFontSmaller.render('Start',False,(153, 156, 158))
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
        if exitBtnRect.collidepoint(mousePos):
            exitBtn = menuFontSmaller.render('Exit',False,(153, 156, 158))
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
            
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                # FULLSCREEN HANDLER
                if event.key == pygame.K_F11:
                    fullscreen = not fullscreen
                    if fullscreen:
                        screen = pygame.display.set_mode((0,0),pygame.FULLSCREEN)
                        minimizedMenuFont = 40
                        minimizedMenuFontSmall = 30
                        
                    else:
                        screen = pygame.display.set_mode((MIN_WIDTH,MIN_HEIGHT))
                        minimizedMenuFont = 28
                        minimizedMenuFontSmall = 22
                    background = pygame.transform.scale(bg_original, (screen.get_width(), screen.get_height()))
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if exitBtnRect.collidepoint(mousePos):
                    running = False
                if startBtnRect.collidepoint(mousePos):
                    gameState = 'game'
                    
        screen.blit(background,(0,0))
        screen.blit(title,titleRect)
        screen.blit(startBtn,startBtnRect)
        screen.blit(exitBtn,exitBtnRect)

    elif gameState == 'game':
        pygame.mouse.set_visible(False)
        screen.blit(background, (0,0))
        # EVENT HANDLER
        for event in pygame.event.get():
            # QUIT
            if event.type == pygame.QUIT:
                running = False
            # METEOR SPAWNER
            if event.type == obstacleTimer:
                    meteorGroup.add(Meteor())
            # KEYBOARD EVENTS
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
                    pew.play()
                    beamGroup.add(Beam(warship.sprite.rect.midtop))
                
                if event.key == pygame.K_ESCAPE:
                    gameState = 'menu'
                    score = displayScore()
                
                
            # MOUSE EVENTS
            if event.type == pygame.MOUSEMOTION:
                mousePos = pygame.mouse.get_pos()
                # WARSHIP MOVER
                warship.sprite.rect.center = mousePos
                # BORDER HANDLER
                if warship.sprite.rect.left <= 0:
                    warship.sprite.rect.left = 0
                if warship.sprite.rect.top <= (screen.get_height()*2/5):
                    warship.sprite.rect.top = screen.get_height()*2/5
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
        explosionGroup.draw(screen)
        explosionGroup.update()
        collision(beamGroup, meteorGroup, explosionGroup)
        if warship.sprite:
            if pygame.sprite.spritecollide(warship.sprite,meteorGroup, False):
        
                explosionGroup.add(Explosion(warship.sprite.rect.center))
                warship.sprite.kill()
                gameState = 'over'
                
        score = displayScore()
                
    elif gameState == 'over':
        mousePos = pygame.mouse.get_pos()
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_F11:
                    fullscreen = not fullscreen
                    if fullscreen:
                        screen = pygame.display.set_mode((0,0),pygame.FULLSCREEN)
                        minimizedMenuFont = 40
                        minimizedMenuFontSmall = 30
                        
                    else:
                        screen = pygame.display.set_mode((MIN_WIDTH,MIN_HEIGHT))
                        minimizedMenuFont = 28
                        minimizedMenuFontSmall = 22
                    background = pygame.transform.scale(bg_original, (screen.get_width(), screen.get_height()))
                    
            if event.type == pygame.MOUSEBUTTONDOWN:
                if goToMenuBtnRect.collidepoint(mousePos):
                    destroyed = 0
                    start_time = int(pygame.time.get_ticks() / 120)

                    meteorGroup.empty()
                    beamGroup.empty()
                    explosionGroup.empty()

                    warship.empty()
                    warship.add(Ship())

                    gameState = 'menu'
        
        menuFont = pygame.font.Font('assets/8bitw.ttf',minimizedMenuFont)
        menuFontSmaller = pygame.font.Font('assets/8bitw.ttf',minimizedMenuFontSmall)
        
        gameOver = menuFont.render('GAME OVER',False,'Red')
        gameOverRect = gameOver.get_rect(center = (screen.get_width()/2, (screen.get_height()/2)-70))

        scoreBtn = menuFontSmaller.render(f'Score {score}',False,'White')
        scoreBtnRect = scoreBtn.get_rect(center = (screen.get_width()/2, gameOverRect.centery + 70))

        goToMenuBtn = menuFontSmaller.render('Back To Menu',False,'White')
        goToMenuBtnRect = goToMenuBtn.get_rect(center = (screen.get_width()/2, scoreBtnRect.centery + 70))
        
        if goToMenuBtnRect.collidepoint(mousePos):
            goToMenuBtn = menuFontSmaller.render('Back To Menu',False,(153, 156, 158))
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
        
        screen.blit(background, (0,0))
        screen.blit(gameOver,gameOverRect)
        screen.blit(scoreBtn,scoreBtnRect)
        screen.blit(goToMenuBtn,goToMenuBtnRect)
        explosionGroup.draw(screen)
        explosionGroup.update()
        
        pygame.mouse.set_visible(True)  
    
    pygame.display.update()
    clock.tick(60)

pygame.quit()