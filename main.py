import pygame, sys
from pygame.locals import *
from game import *

pygame.init()
DISPLAYSURF = pygame.display.set_mode(size=(GAME_WIDTH, GAME_HEIGHT))
new_game = game(DISPLAYSURF)

GameOver = False

while not GameOver:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN and new_game.isGameOver == True: # 重新初始化游戏
            if event.key == pygame.K_RETURN:
                pygame.init()
                DISPLAYSURF = pygame.display.set_mode(size=(GAME_WIDTH, GAME_HEIGHT))
                new_game = game(DISPLAYSURF)
                GameOver = False
    
    new_game.update() # 逻辑帧
    DISPLAYSURF.fill(BLACK)
    new_game.draw() # 渲染帧
            

    pygame.display.update()
