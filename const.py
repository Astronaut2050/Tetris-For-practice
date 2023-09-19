class BlockType:
    RED = 0
    ORANGE = 1
    YELLOW = 2
    GREEN = 3
    CYAN = 4
    BLUE = 5
    PURPLE = 6
    BlockTypeMax = 7

BLOCK_PIC_POS = {
    BlockType.RED: 'pic/red.png',
    BlockType.ORANGE: 'pic/orange.png',
    BlockType.YELLOW: 'pic/yellow.png',
    BlockType.GREEN: 'pic/green.png',
    BlockType.CYAN: 'pic/cyan.png',
    BlockType.BLUE: 'pic/blue.png',
    BlockType.PURPLE: 'pic/purple.png',
}

BLOCK_SHAPE = [
    [((0,0),(0,1),(1,0),(1,1)),], # 方形
    [((0,0),(0,1),(0,2),(0,3)), ((0,0),(1,0),(2,0),(3,0))], # 长形
    [((0,0),(0,1),(1,1),(1,2)), ((0,1),(1,0),(1,1),(2,0))], # Z形
    [((0,1),(1,0),(1,1),(1,2)), ((0,1),(1,1),(1,2),(2,1)), 
     ((1,0),(1,1),(1,2),(2,1)), ((0,1),(1,0),(1,1),(2,1))]  # 飞机形
]

BLOCK_WIDTH = 32
BLOCK_HEIGHT = 32
GAME_WIDTH = 800
GAME_HEIGHT = 600
COL_OFFSET = 240 # 横向偏移
ROW_OFFSET = 30 # 纵向偏移

GAME_ROW = 17
GAME_COL = 10

BLINK_TIME = 300

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

class BlockGroupType:
    FIXED = 0
    DROP = 1