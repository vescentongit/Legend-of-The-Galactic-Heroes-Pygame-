import pygame
from random import randint

pygame.init()

# --- SCREEN & SETTINGS ---
MIN_WIDTH, MIN_HEIGHT = 840, 540 # Updated to 540 to fit menu layout better
screen = pygame.display.set_mode((MIN_WIDTH, MIN_HEIGHT))
pygame.display.set_caption('Legend of the Galactic Heroes')
clock = pygame.time.Clock()
running = True
fullscreen = False

# --- GLOBAL VARIABLES ---
game_state = "menu"
start_time = 0
destroyed = 0
final_score = 0 

# --- ASSETS ---
# Background
bg_original = pygame.image.load('assets/space.jpg').convert_alpha()
background = pygame.transform.scale(bg_original, (screen.get_width(), screen.get_height()))

# Logo / Icon
logo = pygame.image.load('assets/ship.png').convert_alpha()
pygame.display.set_icon(logo)

# Fonts
font_path = 'assets/8bitw.ttf'
textFont = pygame.font.Font(font_path, 12)
titleFont = pygame.font.Font(font_path, 28) 
menuFont = pygame.font.Font(font_path, 22) 
gameOverFont = pygame.font.Font(font_path, 40)

pew = pygame.mixer.Sound('assets/pewfin.mp3') 
explosionsfx = pygame.mixer.Sound('assets/explosionsfx.mp3')

# Menu Text Objects
title = titleFont.render('Legend of The Galactic Heroes', False, 'White')
titleRect = title.get_rect(center=(screen.get_width()//2, 180))

# Buttons (We initialize rects here, render text in loop for hover effect)
startBtn = menuFont.render('Start',False,'White')
startBtnRect = startBtn.get_rect(center = (screen.get_width()//2, titleRect.centery + 70))

optionsBtn = menuFont.render('Settings', False, 'White')
optionsBtnRect = optionsBtn.get_rect(center = (screen.get_width()//2, startBtnRect.centery + 70))

exitBtn = menuFont.render('Exit',False,'White')
exitBtnRect = exitBtn.get_rect(center = (screen.get_width()//2, optionsBtnRect.centery + 70))

gameOverText = gameOverFont.render('GAME OVER', False, 'Red')
gameOverRect = gameOverText.get_rect(center=(screen.get_width()//2, screen.get_height()//2))

menuBtnText = menuFont.render('Return to Menu',False,'White')
menuBtnRect = menuBtnText.get_rect(center = (screen.get_width()/2,gameOverRect.centery+120))


# --- GAME CLASSES ---
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
        
        try:
            meteor1 = pygame.image.load('assets/meteor.png').convert_alpha()
            meteor2 = pygame.image.load('assets/meteor2.png').convert_alpha()
            meteor3 = pygame.image.load('assets/meteor3.png').convert_alpha()
            meteor4 = pygame.image.load('assets/meteor4.png').convert_alpha()
            self.frames = [meteor1, meteor2, meteor3, meteor4]
        except:
            
            surf = pygame.Surface((80,80))
            surf.fill('Red')
            self.frames = [surf]

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
        return 6 if fullscreen else 3
    
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
        self.imageOriginal = pygame.image.load('assets/beam.png').convert_alpha()
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
        return 10 if fullscreen else 5
    
    def destroy(self):
        if self.rect.bottom <= 0:
            self.kill()
    
    def update(self):
        self.updateSize(fullscreen)
        self.rect.y -= self.getSpeed(fullscreen)
        self.destroy()

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


def reset_game():
    
    global destroyed, start_time
    destroyed = 0
    start_time = int(pygame.time.get_ticks() / 120) # Sync time
    
    meteorGroup.empty()
    beamGroup.empty()
    explosionGroup.empty()
    
    warship.sprite.rect.center = ((screen.get_width()/2),(screen.get_height()-100))
    
    warship.empty() 
    warship.add(Ship())

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

def displayScore():
    current_time = int(pygame.time.get_ticks() / 120) - start_time
    points = (destroyed*40) + current_time
    score_surf = textFont.render(f'Points I {points}', False, 'White')
    score_rect = score_surf.get_rect(topleft = (0,0))
    screen.blit(score_surf,score_rect)
    return current_time 


warship = pygame.sprite.GroupSingle()
warship.add(Ship())

beamGroup = pygame.sprite.Group()
meteorGroup = pygame.sprite.Group()
explosionGroup = pygame.sprite.Group()

obstacleTimer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacleTimer, 500)

while running:
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            running = False
            
    for event in events:
        if event.type == pygame.MOUSEBUTTONDOWN:
            if startBtnRect.collidepoint(mousePos):
                pew.play()
                reset_game()     # Reset score and enemies
                game_state = "game" # SWITCH STATE
            elif exitBtnRect.collidepoint(mousePos):
                running = False
                
    if game_state == "menu":
        pygame.mouse.set_visible(True)
        mousePos = pygame.mouse.get_pos()
        
        screen.fill((1, 13, 38))
        screen.blit(background,(0,0))
        screen.blit(title, titleRect)

        if startBtnRect.collidepoint(mousePos):
            startBtn = menuFont.render('Start', False, (153, 156, 158))
        else:
            startBtn = menuFont.render('Start', False, 'White')
            
        if optionsBtnRect.collidepoint(mousePos):
            optionsBtn = menuFont.render('Settings', False, (153, 156, 158))
        else:
            optionsBtn = menuFont.render('Settings', False, 'White')
            
        if exitBtnRect.collidepoint(mousePos):
            exitBtn = menuFont.render('Exit', False, (153, 156, 158))
        else:
            exitBtn = menuFont.render('Exit', False, 'White')

        screen.blit(startBtn, startBtnRect)
        screen.blit(optionsBtn, optionsBtnRect)
        screen.blit(exitBtn, exitBtnRect)
        
    elif game_state == "game":
        pygame.mouse.set_visible(False) 
        screen.blit(background, (0,0))
        
        for event in events:
            if event.type == obstacleTimer:
                meteorGroup.add(Meteor())
            
            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_ESCAPE:
                    game_state = "menu"
                    
                if event.key == pygame.K_F11:
                    fullscreen = not fullscreen
                    if fullscreen:
                        screen = pygame.display.set_mode((0,0),pygame.FULLSCREEN)
                    else:
                        screen = pygame.display.set_mode((MIN_WIDTH,MIN_HEIGHT))
                    background = pygame.transform.scale(bg_original, (screen.get_width(), screen.get_height()))
                
                if event.key == pygame.K_SPACE:
                    pew.play()
                    beamGroup.add(Beam(warship.sprite.rect.midtop))
        
        if event.type == pygame.MOUSEMOTION:
            mousePos = pygame.mouse.get_pos()
            warship.sprite.rect.center = mousePos
            
            if warship.sprite.rect.left <= 0: warship.sprite.rect.left = 0
            if warship.sprite.rect.top <= (screen.get_height()*2/5): warship.sprite.rect.top = screen.get_height()*2/5
            if warship.sprite.rect.right >= screen.get_width(): warship.sprite.rect.right = screen.get_width()
            if warship.sprite.rect.bottom >= screen.get_height(): warship.sprite.rect.bottom = screen.get_height()
            

        warship.draw(screen)
        warship.update()
        beamGroup.draw(screen)
        beamGroup.update()
        meteorGroup.draw(screen)
        meteorGroup.update()
        explosionGroup.draw(screen)
        explosionGroup.update()
        collision(beamGroup, meteorGroup, explosionGroup)
        
        if warship.sprite: # Check if ship exists first
            if pygame.sprite.spritecollide(warship.sprite, meteorGroup, False):
                explosionGroup.add(Explosion(warship.sprite.rect.center))
                warship.sprite.kill() # Destroy the ship
                final_score = displayScore() # Save score
                game_state = "game_over" # SWITCH STATE

        displayScore()
        
    elif game_state == "game_over":
        pygame.mouse.set_visible(True) # Show cursor again
        mousePos = pygame.mouse.get_pos()
        
        # Keep drawing the game background (frozen)
        screen.blit(background, (0,0))
        explosionGroup.draw(screen) # Let explosion finish animation
        explosionGroup.update()
        
        # Draw Game Over Text
        screen.blit(gameOverText, gameOverRect)
        
        # Draw Final Score
        scoreText = gameOverFont.render(f'Final Score  {final_score}', False, 'Magenta')
        scoreRect = scoreText.get_rect(center=(screen.get_width()/2, gameOverRect.centery-100))
        screen.blit(scoreText, scoreRect)

        if menuBtnRect.collidepoint(mousePos):
            menuBtnText = menuFont.render('Return to Menu', False, (153, 156, 158))
        else:
            menuBtnText = menuFont.render('Return to Menu', False, 'White')
            
        screen.blit(menuBtnText, menuBtnRect)
        
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if menuBtnRect.collidepoint(mousePos):
                    pew.play()
                    game_state = "menu" # Go back to menu

    pygame.display.update()
    clock.tick(60)

pygame.quit()