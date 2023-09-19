import random
import pygame, sys
from pygame.locals import *
from const import *
from block import *
from utils import *

class BlockGroup(object):
    def GenerateBlockGroupConfig(rowIdx, colIdx):
        shapeIdx = random.randint(0,len(BLOCK_SHAPE) - 1) # 形状
        bType = random.randint(0,BlockType.BlockTypeMax - 1) # 方块颜色
        rotIdx = random.randint(0,len(BLOCK_SHAPE[shapeIdx]) - 1) # 旋转
        configlist = []
        for x in range(len(BLOCK_SHAPE[shapeIdx][rotIdx])):
            config = {
                'blockType': bType,
                'blockshape': shapeIdx,
                'blockRot': rotIdx,
                'blockGroupIdx': x,
                'rowIdx' : rowIdx,
                'colIdx' : colIdx
            }
            configlist.append(config)
        return configlist
    
    def __init__(self, blockGroupType, width:int, heigth:int, blockConfiglist, relPos):
        super().__init__()
        self.blocks:list[Block] = [] # 方块组
        self.blockGroupType = blockGroupType
        self.dropTime = getCurrentTime()
        self.dropinterval = 0
        self.isEliminating = False
        self.pressTime = {} # 初始化各个按键的点击事件
        self.eliminateRow = 0
        self.eliminateTime = 0
        for config in blockConfiglist:
            blk = Block(config['blockType'],config['rowIdx'],config['colIdx'],config['blockshape'],config['blockRot'],config['blockGroupIdx'],width,heigth,relPos) # 单个方块
            if isinstance(blk, Block):
                self.blocks.append(blk)
            else:
                raise TypeError("Only Block objects can be added to blocks list.")


    # 调整 下落方块 和 下一个方块 的位置
    def setBaseIdx(self,baseRow,baseCol):
        for blk in self.blocks:
            blk.setBaseIndex(baseRow, baseCol)


    # 更新区域
    def draw(self,surface):
        for b in self.blocks:
            b.draw(surface)

    # 更新整个方块组
    def updateGroup(self):
        oldTime = self.dropTime
        curTime = getCurrentTime()
        diffTime = curTime - oldTime
        if self.blockGroupType == BlockGroupType.DROP:
            if diffTime >= self.dropinterval:
                self.dropTime = curTime # 更新时间
                for b in self.blocks:
                    b.drop()
            self.keyDownHandler()
        for block in self.blocks:
            block.updateBlink()

        # 消除
        if self.IsEliminating():
            if getCurrentTime() - self.eliminateTime > BLINK_TIME:
                tmpBlocks = []
                for block in self.blocks:
                    if block.getIndex()[0] != self.eliminateRow:
                        if block.getIndex()[0] < self.eliminateRow:
                            block.drop()
                        tmpBlocks.append(block)
                self.blocks = tmpBlocks
                self.setEliminate(False)

    # 封装方块组的坐标和下一个时刻的坐标
    def getGroupIndex(self):
        return [block.getIndex() for block in self.blocks]
    
    def getGroupNextIndex(self):
        return [block.getNextIndex() for block in self.blocks]
    
    # 得到方块类
    def getBlocks(self):
        return self.blocks
    
    # 清除方块组
    def clearBlocks(self):
        self.blocks = []

    # 存储下落的方块组
    def addBlocks(self,blk):
        self.blocks.append(blk)

    # 左右移动方块组
    def keyDownHandler(self):
        pressed = pygame.key.get_pressed()
        if pressed[K_LEFT] and self.checkLastTimePressed(K_LEFT):
            can_move = True
            for block in self.blocks: # 判断能否移动
                if block.isLeftBound():
                    can_move = False
                    break
            if can_move:
                for block in self.blocks:
                    block.toLeft()
        if pressed[K_RIGHT] and self.checkLastTimePressed(K_RIGHT):
            can_move = True
            for block in self.blocks: # 判断能否移动
                if block.isRightBound():
                    can_move = False
                    break
            if can_move:
                for block in self.blocks:
                    block.toRight()
        if pressed[K_UP] and self.checkLastTimePressed(K_UP): # 旋转方块组
            for block in self.blocks:
                block.toRotate()

        if pressed[K_DOWN] : # 加速下落
            self.dropinterval = 30
        else:
            self.dropinterval = 800


    # 上一次的按键时间
    def checkLastTimePressed(self, key):
        ret = False
        if getCurrentTime() - self.pressTime.get(key, 0) > 30:
            ret = True
        self.pressTime[key] = getCurrentTime()
        return ret

    # 消除
    def eliminateBlocks(self, row):
        eliminateRow = {}
        for col in range(0,GAME_COL):
            idx = (row, col)
            eliminateRow[idx] = 1

        self.setEliminate(True)
        self.eliminateRow = row

        for blk in self.blocks:
            if eliminateRow.get( blk.getIndex() ):
                blk.startBlink()

    # 执行消除
    def processEliminate(self):
        hash = {}

        allIndex = self.getGroupIndex()
        for idx in allIndex:
            hash[idx] = 1
            
        for row in range(GAME_ROW-1, -1, -1):
            full = True
            for col in range(0,GAME_COL):
                idx = (row,col)
                if not hash.get(idx): # 不在列表中
                    full = False
                    break
            if full:
                self.eliminateBlocks(row)
                return True

    # 消除状态函数
    def setEliminate(self, el):
        self.isEliminating = el
        self.eliminateTime = getCurrentTime() # 更新estimateTime
    
    def IsEliminating(self):
        return self.isEliminating
    