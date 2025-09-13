import pygame
import random
pygame.init()

# 游戏窗口
width,height=800,600
basic_size=20
screen=pygame.display.set_mode((width,height))
pygame.display.set_caption("贪吃蛇")

black=(0,0,0)
white=(255,255,255)
red=(255,0,0)
green=(0,255,0)

clock=pygame.time.Clock() #控制游戏帧率


#蛇类
class Snake:
    #初始蛇身
    def __init__(self):
        self.body=[(200,200),(180,200),(160,200)]   #初始蛇身占三块
        self.direction='RIGHT'
        self.grow=False     #是否增长，吃到食物后为True

    #移动
    def move(self):
        head=self.body[0]
        if self.direction=='UP':      head=(head[0], head[1]-basic_size)
        elif self.direction=='DOWN':  head=(head[0], head[1]+basic_size)
        elif self.direction=='LEFT':  head=(head[0]-basic_size, head[1])
        elif self.direction=='RIGHT': head=(head[0]+basic_size, head[1])

    #蛇身跟着动
        self.body.insert(0,head)

        if not self.grow:
            self.body.pop()    #删除最后一块
        else:
            self.grow=False

    #防止反向移动
    def change_direction(self,newdirection):
        if (newdirection == 'UP' and self.direction != 'DOWN') or \
                (newdirection == 'DOWN' and self.direction != 'UP') or \
                (newdirection == 'LEFT' and self.direction != 'RIGHT') or \
                (newdirection == 'RIGHT' and self.direction != 'LEFT'):
            self.direction = newdirection


class Food:
        def __init__(self):
            self.position=self.random_pos()

        def random_pos(self):
            while True:
                x=random.randint(0,(width//basic_size)-1)*basic_size
                y=random.randint(0,(height//basic_size)-1)*basic_size
                if(x,y) not in snake.body:
                    return (x,y)


snake = Snake()
food = Food()
score = 0
game_over = False

while not game_over:
    # 事件处理
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                snake.change_direction('UP')
            elif event.key == pygame.K_DOWN:
                snake.change_direction('DOWN')
            elif event.key == pygame.K_LEFT:
                snake.change_direction('LEFT')
            elif event.key == pygame.K_RIGHT:
                snake.change_direction('RIGHT')

    # 更新游戏状态
    snake.move()

    # 碰撞检测
    head = snake.body[0]
    if (head[0] < 0 or head[0] >= width or
            head[1] < 0 or head[1] >= height or
            head in snake.body[1:]):
        game_over = True

    # 食物检测
    if head == food.position:
        score += 1
        snake.grow = True
        food.position = food.random_pos()

    # 绘制界面
    screen.fill(black)
    for segment in snake.body:
        pygame.draw.rect(screen, green, (*segment, basic_size, basic_size))
    pygame.draw.rect(screen, red, (*food.position, basic_size, basic_size))

    # 显示得分
    font = pygame.font.Font(None, 36)   #创建字体对象
    text = font.render(f"Score: {score}", True, white)
    screen.blit(text, (10, 10))

    pygame.display.flip()
    clock.tick(10)  # 控制游戏速度

pygame.quit()