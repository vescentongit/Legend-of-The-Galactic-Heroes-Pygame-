import pygame
pygame.init()
running = True
def yesking():
    return 'yesking'

screen = pygame.display.set_mode((840,540))
ship = pygame.image.load('assets/ship.png')

textFont = pygame.font.Font('assets/8bitw.ttf',28)
textFontSmaller = pygame.font.Font('assets/8bitw.ttf',22)
title = textFont.render('Legend of The Galactic Heroes',False,'White')
titleRect = title.get_rect(center = (420, 180))

startBtn = textFontSmaller.render('Start',False,'White')
startBtnRect = startBtn.get_rect(center = (420, titleRect.centery + 70))

optionsBtn = textFontSmaller.render('Settings',False,'White')
optionsBtnRect = optionsBtn.get_rect(center = (420, startBtnRect.centery + 70))

exitBtn = textFontSmaller.render('Exit',False,'White')
exitBtnRect = exitBtn.get_rect(center = (420, optionsBtnRect.centery + 70))


bg_original = pygame.image.load('assets/space.jpg').convert_alpha()
background = pygame.transform.scale(bg_original, (screen.get_width(), screen.get_height()))

pew = pygame.mixer.Sound('assets/pewfin.mp3')

while running:
    screen.fill((1, 13, 38))
    screen.blit(background,(0,0))
    screen.blit(title,titleRect)
    screen.blit(startBtn,startBtnRect)
    screen.blit(optionsBtn,optionsBtnRect)
    screen.blit(exitBtn,exitBtnRect)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            pew.play(0,1000,200)
            if exitBtnRect.collidepoint(mousePos):
                running = False
    
        if event.type == pygame.MOUSEMOTION:
            mousePos = pygame.mouse.get_pos()
            if startBtnRect.collidepoint(mousePos):
                startBtn = textFontSmaller.render('Start',False,(153, 156, 158))
            else:
                startBtn = textFontSmaller.render('Start',False,'White')
            if optionsBtnRect.collidepoint(mousePos):
                optionsBtn = textFontSmaller.render('Settings',False,(153, 156, 158))
            else:
                optionsBtn = textFontSmaller.render('Settings',False,'White')
            if exitBtnRect.collidepoint(mousePos):
                exitBtn = textFontSmaller.render('Exit',False,(153, 156, 158))
            else:
                exitBtn = textFontSmaller.render('Exit',False,'White')
            

    pygame.display.flip()
            
pygame.quit()