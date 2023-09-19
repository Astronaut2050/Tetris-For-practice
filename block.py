import pygame
from const import *
from pygame.locals import *
from utils import *

class Block(pygame.sprite.Sprite):
    def __init__(self, blocktype, baseRowIdx, baseColIdx, blockshape, blockRot, blockGroupIdx, width, height, relPos):
        super().__init__()
        self.blocktype = blocktype
        self.blockshape = blockshape
        self.blockRot = blockRot
        self.blockGroupIdx = blockGroupIdx
        self.baseRowIdx = baseRowIdx
        self.baseColIdx = baseColIdx
        self.width = width
        self.height = height
        self.relPos = relPos
        self.blink = False
        self.blinkCount = 0
        self.loadImage()
        self.updateImagePos()

    # 初始图像
    def loadImage(self):
        self.image = pygame.image.load(BLOCK_PIC_POS[self.blocktype])
        self.image = pygame.transform.scale(self.image, (self.width,self.height))

    # 初始位置
    def updateImagePos(self):
        self.rect = self.image.get_rect()
        self.rect.left = self.relPos[0] + self.width * self.colIdx
        self.rect.top = self.relPos[1] + self.height * self.rowIdx

    # 画图
    def draw(self, surface):
        self.updateImagePos()
        if self.blink and self.blinkCount % 2 == 1:
            return
        surface.blit(self.image, self.rect)

    # 方块下落
    def drop(self):
        self.baseRowIdx += 1

    # 获得当前坐标
    def getIndex(self):
        return (int(self.rowIdx),int(self.colIdx))
    
    # 获得下一个坐标
    def getNextIndex(self):
        return (int(self.rowIdx + 1),int(self.colIdx))

    # 是否到达边界
    def isLeftBound(self):
        return self.colIdx == 0
    def isRightBound(self):
        return self.colIdx == GAME_COL - 1

    # 移动代码
    def toLeft(self):
        self.baseColIdx -= 1
    def toRight(self):
        self.baseColIdx += 1

    def getBlockConfigIndex(self):
        return BLOCK_SHAPE[self.blockshape][self.blockRot][self.blockGroupIdx]
    
    @property
    def rowIdx(self):
        return self.baseRowIdx + self.getBlockConfigIndex()[0]
    
    @property
    def colIdx(self):
        return self.baseColIdx + self.getBlockConfigIndex()[1]
    
    # 旋转方块组
    def toRotate(self):
        self.blockRot += 1
        if self.blockRot >= len(BLOCK_SHAPE[self.blockshape]):
            self.blockRot = 0

    # 开始闪烁
    def startBlink(self):
        self.blink = True
        self.blinkTime = getCurrentTime()

    # 更新闪烁
    def updateBlink(self):
        if self.blink:
            diffTime = getCurrentTime() - self.blinkTime
            self.blinkCount = int(diffTime / 30)

    def setBaseIndex(self, baseRowIdx, baseColIdx):
        self.baseRowIdx = baseRowIdx
        self.baseColIdx = baseColIdx