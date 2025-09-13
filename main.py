import pygame
import random
import json
import os

pygame.init()

# 游戏窗口
width, height = 800, 600
basic_size = 20
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("贪吃蛇")

# 颜色定义
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
green = (0, 255, 0)
gold = (255, 215, 0)

clock = pygame.time.Clock()

# 文件路径
HIGH_SCORE_FILE = "high_score.json"


class Snake:
    def __init__(self):
        self.reset()

    def reset(self):
        self.body = [(200, 200), (180, 200), (160, 200)]
        self.direction = 'RIGHT'
        self.grow = False

    def move(self):
        head = self.body[0]
        if self.direction == 'UP':
            head = (head[0], head[1] - basic_size)
        elif self.direction == 'DOWN':
            head = (head[0], head[1] + basic_size)
        elif self.direction == 'LEFT':
            head = (head[0] - basic_size, head[1])
        elif self.direction == 'RIGHT':
            head = (head[0] + basic_size, head[1])

        self.body.insert(0, head)
        if not self.grow:
            self.body.pop()
        else:
            self.grow = False

    def change_direction(self, newdirection):
        if (newdirection == 'UP' and self.direction != 'DOWN') or \
                (newdirection == 'DOWN' and self.direction != 'UP') or \
                (newdirection == 'LEFT' and self.direction != 'RIGHT') or \
                (newdirection == 'RIGHT' and self.direction != 'LEFT'):
            self.direction = newdirection


class Food:
    def __init__(self):
        self.position = self.random_pos()

    def random_pos(self):
        while True:
            x = random.randint(0, (width // basic_size) - 1) * basic_size
            y = random.randint(0, (height // basic_size) - 1) * basic_size
            if (x, y) not in snake.body:
                return (x, y)


def load_high_score():
    if os.path.exists(HIGH_SCORE_FILE):
        with open(HIGH_SCORE_FILE, 'r') as f:
            return json.load(f)
    return 0


def save_high_score(score):
    high_score = max(load_high_score(), score)
    with open(HIGH_SCORE_FILE, 'w') as f:
        json.dump(high_score, f)


def game_over_screen(score):
    screen.fill(black)
    font = pygame.font.Font(None, 74)
    text = font.render("GAME OVER", True, gold)
    text_rect = text.get_rect(center=(width // 2, height // 2 - 50))
    screen.blit(text, text_rect)

    score_font = pygame.font.Font(None, 50)
    score_text = score_font.render(f"Score: {score}", True, white)
    score_rect = score_text.get_rect(center=(width // 2, height // 2))
    screen.blit(score_text, score_rect)

    high_score = load_high_score()
    high_score_text = score_font.render(f"High Score: {high_score}", True, white)
    high_score_rect = high_score_text.get_rect(center=(width // 2, height // 2 + 50))
    screen.blit(high_score_text, high_score_rect)

    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return True  # 重新开始
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    exit()


snake = Snake()
food = Food()
score = 0
game_over = False
high_score = load_high_score()

while True:
    if not game_over:
        # 事件处理
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    snake.change_direction('UP')
                elif event.key == pygame.K_DOWN:
                    snake.change_direction('DOWN')
                elif event.key == pygame.K_LEFT:
                    snake.change_direction('LEFT')
                elif event.key == pygame.K_RIGHT:
                    snake.change_direction('RIGHT')


        snake.move()
        head = snake.body[0]

        # 碰撞检测
        if (head[0] < 0 or head[0] >= width or
                head[1] < 0 or head[1] >= height or
                head in snake.body[1:]):
            game_over = True
            save_high_score(score)

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
        font = pygame.font.Font(None, 36)
        text = font.render(f"Score: {score}  High: {load_high_score()}", True, white)
        screen.blit(text, (10, 10))

        pygame.display.flip()
        clock.tick(10)
    else:
        # 游戏结束界面
        if game_over_screen(score):
            snake.reset()
            food = Food()
            score = 0
            game_over = False