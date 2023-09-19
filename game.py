import pygame, sys
from block import *
from blockGroup import *
from const import *

class game(pygame.sprite.Sprite):

    def getRelPos(self):
        return(COL_OFFSET,ROW_OFFSET)
    
    # 画背景
    def drawTwoLines(self,surface):
        offset = GAME_COL*BLOCK_WIDTH
        line_1_start,line_1_end = (COL_OFFSET,0), (COL_OFFSET,GAME_HEIGHT)
        line_2_start,line_2_end = (COL_OFFSET+offset,0), (COL_OFFSET+offset,GAME_HEIGHT)
        pygame.draw.line(surface,WHITE,line_1_start,line_1_end,2)
        pygame.draw.line(surface,WHITE,line_2_start,line_2_end,2)

    
    def __init__(self, surface):
        self.surface = surface
        self.fixBlocGroup = BlockGroup(BlockGroupType.FIXED, BLOCK_WIDTH, BLOCK_HEIGHT, [], self.getRelPos())
        self.dropBlockGroup = None
        self.nextBlockGroup = None
        self.gameOverImage = pygame.image.load( "pic/lose.png" )
        self.isGameOver = False
        self.scorefont = pygame.font.Font(None,30)
        self.score = 0
        self.generateNextBlockGroup()

    # 生成此时下落的方块
    def generateDropBlockGroup(self):
        self.dropBlockGroup = self.nextBlockGroup
        self.dropBlockGroup.setBaseIdx(0,GAME_COL/2-1)
        self.generateNextBlockGroup()

    # 生成下一个方块
    def generateNextBlockGroup(self):
        conf = BlockGroup.GenerateBlockGroupConfig(0,GAME_COL + 3)
        self.nextBlockGroup = BlockGroup(BlockGroupType.DROP, BLOCK_WIDTH, BLOCK_HEIGHT, conf, self.getRelPos())

    # 更新帧
    def update(self):
        if self.isGameOver:
            return
        
        self.fixBlocGroup.updateGroup() # 渲染已经到位方块

        if self.fixBlocGroup.IsEliminating():
            return
        
        if self.dropBlockGroup: # 渲染下落方块
            self.dropBlockGroup.updateGroup()
        else: # 新增一个掉落方块
            self.generateDropBlockGroup() 

        # 碰撞逻辑  
        if self.willCollide():
            blocks = self.dropBlockGroup.getBlocks()
            for block in blocks:
                self.fixBlocGroup.addBlocks(block)
            self.dropBlockGroup.clearBlocks()
            self.dropBlockGroup = None
            if self.fixBlocGroup.processEliminate():
                self.score += 1
        # 查看游戏是否结束
        self.ifGameOver()

    def draw(self):
        # 边界
        self.drawTwoLines(self.surface)
        # 已下落方块
        self.fixBlocGroup.draw(self.surface)
        # 下落中方块和下一个方块
        if self.dropBlockGroup:
            self.dropBlockGroup.draw(self.surface)
        self.nextBlockGroup.draw(self.surface)

        if self.isGameOver:
            rect = self.gameOverImage.get_rect()
            rect.centerx = GAME_WIDTH/2
            rect.centery = GAME_HEIGHT/2
            self.surface.blit(self.gameOverImage,rect)
        
        scoreImage = self.scorefont.render('Score: '+str(self.score), True, (255,255,255))
        self.surface.blit(scoreImage,(10,20))

    def willCollide(self):
        hash = {}
        allIndex = self.fixBlocGroup.getGroupIndex() # 此时所有方块的位置
        for Idx in allIndex:
            hash[Idx] = 1
        dropIdxes = self.dropBlockGroup.getGroupNextIndex() # 下个时刻所有方块的位置

        for dropIdx in dropIdxes:
            if hash.get(dropIdx): # drop碰撞
                return True
            if dropIdx[0] >= GAME_ROW: # 超出范围
                return True
        return False

    # 游戏结束
    def ifGameOver(self):
        allIndex = self.fixBlocGroup.getGroupIndex()
        for index in allIndex:
            if index[0] < 2:
                self.isGameOver = True