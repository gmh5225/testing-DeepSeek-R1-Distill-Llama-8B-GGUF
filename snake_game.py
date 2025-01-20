import random
import time
import pygame
import sys

# 初始化
pygame.init()
屏幕宽度 = 800
屏幕高度 = 600
蛇 = [
    (100, 100),
    (200, 100)
]
食物 = None
移动方向 = '向右'

def create_snake():
    # 随机生成一个新的蛇头位置（避免初始时重叠）
    global snake
    if len(snake) == 0:
        new_head = (random.randint(1, int(屏幕宽度 / 2)), random.randint(1, int(屏幕高度 / 2)))
        snake.append(new_head)
    else:
        new_head = snake[-1]
        # 检查是否会重叠自己
        for body in snake[:-1]:
            if new_head == body:
                create_snake()
                return
        snake.append(new_head)

def create_food():
    global food
    while True:
        food = (random.randint(1, int(屏幕宽度 / 2)), random.randint(1, int(屏幕高度 / 2)))
        # 检查食物是否在蛇体上
        flag = False
        for body in snake:
            if (body[0], body[1]) == food:
                create_food()
                flag = True
                break
        if not flag:
            return

def game_loop():
    global food, 移动方向, snake
    while True:
        # 绘制屏幕
        screen.fill((0, 0, 0))
        # 绘制蛇
        for i in range(len(snake)):
            x, y = snake[i]
            pygame.draw.rect(screen, (255, 0, 0), (x, y, 1, 1))
        if food:
            x, y = food
            pygame.draw.rect(screen, (0, 255, 0), (x, y, 1, 1))

        # 处理键盘事件
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    if 移动方向 != '向下':
                        移动方向 = '向上'
                elif event.key == pygame.K_DOWN:
                    if 移动方向 != '向上':
                        移动方向 = '向下'
                elif event.key == pygame.K_LEFT:
                    if 移动方向 != '向右':
                        移动方向 = '向左'
                elif event.key == pygame.K_RIGHT:
                    if 移动方向 != '向左':
                        移动方向 = '向右'

        # 更新蛇位置
        head = snake[-1]
        new_head = None
        if 移动方向 == '向上' and head[1] > 1:
            new_head = (head[0], head[1] - 1)
        elif 移动方向 == '向下' and head[1] < screen_height:
            new_head = (head[0], head[1] + 1)
        elif 移动方向 == '向左' and head[0] > 1:
            new_head = (head[0] - 1, head[1])
        elif 移动方向 == '向右' and head[0] < screen_width:
            new_head = (head[0] + 1, head[1])

        # 检查是否撞墙或自己
        if not new_head or new_head in snake[:-1]:
            game_over()

        # 增加蛇长度
        snake.append(new_head)

def game_over():
    global food
    food = None
    for i in range(len(snake)):
        x, y = snake[i]
        pygame.draw.rect(screen, (0, 255, 0), (x, y, 1, 1))
    screen.fill((0, 0, 0))
    font = pygame.font.Font(None, 74)
    text = font.render('游戏结束！', True, (255, 0, 0))
    screen.blit(text, (屏幕宽度 // 2 - 140,屏幕高度 // 2))

    # 等待几秒后退出
    time.sleep(5)
    pygame.quit()
    sys.exit()

# 开始游戏
screen = pygame.display.set_mode((屏幕宽度,屏幕高度))
pygame.display.set_caption('贪吃蛇')
running = True

while running:
    if food is None:
        create_food()
    
    # 检查是否撞到自身或边界（每一帧检查一次）
    for i in range(len(snake)):
        x, y = snake[i]
        if x <= 0 or x >= screen_width or y <= 0 or y >= screen_height:
            game_over()
    
    # 更新游戏状态
    time.sleep(100/60)
    pygame.display.flip()

# 运行完成
print('贪吃蛇游戏结束！')
