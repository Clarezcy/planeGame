import pygame
import time
import math

# 初始化 Pygame
pygame.init()

# 设置窗口
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("飞机大战 - 增强版")

# 颜色定义
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
PURPLE = (128, 0, 128)

# 字体
font = pygame.font.SysFont("Arial", 24)

# 玩家飞机属性
player_x = WINDOW_WIDTH // 2
player_y = WINDOW_HEIGHT - 50
player_width = 50
player_height = 30
player_speed = 10  # 正常速度
player_speed_fast = 20  # 加速速度
player_health = 100  # 角色初始血量

# 靶子属性（三个靶子）
targets = [
    {"x": WINDOW_WIDTH // 2 - 25, "y": 50, "width": 50, "height": 50, "speed": 2},  # 原始靶子
    {"x": WINDOW_WIDTH // 4 - 25, "y": 100, "width": 50, "height": 50, "speed": 3},  # 新靶子1
    {"x": 3 * WINDOW_WIDTH // 4 - 25, "y": 150, "width": 50, "height": 50, "speed": 2.5}  # 新靶子2
]

# 子弹列表
bullets = []
bullet_speed = -5

# 黄色子弹属性
yellow_bullets = []
yellow_bullet_speed = -5
yellow_bullet_width = 12  # 增大到原来的三倍
yellow_bullet_height = 30  # 增大到原来的三倍
yellow_shot_interval = 3  # 每3秒发射一次
last_yellow_shot = time.time()

# 紫色炮弹属性
purple_bombs = []
purple_bomb_speed = -3
purple_bomb_size = 20  # 巨大紫色炮弹大小
purple_bomb_timer = {}  # 存储紫色区域的持续时间和位置
last_purple_shot = time.time()
purple_shot_interval = 2  # 每2秒可发射一次紫色炮弹

# 伤害显示
damage_texts = []  # 存储多个伤害显示（位置、文本、颜色、时间）
damage_duration = 1  # 伤害显示持续时间

# 自动发射计时
last_auto_shot = time.time()
auto_shot_interval = 2

# 场景虚线属性
line_spacing = 50  # 虚线间距
line_length = 20  # 虚线长度
line_speed = 1  # 虚线向下移动速度（向后感）

# 游戏主循环
clock = pygame.time.Clock()
running = True

while running:
    # 清空屏幕，确保没有残影
    window.fill(BLACK)

    # 处理事件
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                bullet_x = player_x + player_width // 2 - 2
                bullet_y = player_y
                bullets.append({"x": bullet_x, "y": bullet_y, "color": RED})
            if event.key == pygame.K_f and time.time() - last_purple_shot >= purple_shot_interval:
                bomb_x = player_x + player_width // 2 - purple_bomb_size // 2
                bomb_y = player_y
                purple_bombs.append({"x": bomb_x, "y": bomb_y})
                last_purple_shot = time.time()

    # 检测 Shift 键和 WASD 移动
    keys = pygame.key.get_pressed()
    speed = player_speed_fast if keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT] else player_speed

    # WASD 移动
    if keys[pygame.K_w] and player_y > 0:
        player_y -= speed
    if keys[pygame.K_s] and player_y < WINDOW_HEIGHT - player_height:
        player_y += speed
    if keys[pygame.K_a] and player_x > 0:
        player_x -= speed
    if keys[pygame.K_d] and player_x < WINDOW_WIDTH - player_width:
        player_x += speed

    # 靶子移动（水平来回）
    for target in targets:
        target["x"] += target["speed"]
        if target["x"] > WINDOW_WIDTH - target["width"] or target["x"] < 0:
            target["speed"] = -target["speed"]

    # 自动发射蓝色子弹
    current_time = time.time()
    if current_time - last_auto_shot >= auto_shot_interval:
        bullet_x = player_x + player_width // 2 - 2
        bullet_y = player_y
        bullets.append({"x": bullet_x, "y": bullet_y, "color": BLUE})
        last_auto_shot = current_time

    # 自动发射黄色子弹（每3秒，从飞机两端向前放射）
    if current_time - last_yellow_shot >= yellow_shot_interval:
        # 左端黄色子弹（向前直线）
        left_x = player_x
        left_y = player_y
        yellow_bullets.append({"x": left_x, "y": left_y, "color": YELLOW})
        # 右端黄色子弹（向前直线）
        right_x = player_x + player_width
        right_y = player_y
        yellow_bullets.append({"x": right_x, "y": right_y, "color": YELLOW})
        last_yellow_shot = current_time

    # 更新普通子弹位置并检测碰撞
    for bullet in bullets[:]:
        bullet["y"] += bullet_speed
        for target in targets[:]:
            if (bullet["x"] >= target["x"] and bullet["x"] <= target["x"] + target["width"] and
                bullet["y"] >= target["y"] and bullet["y"] <= target["y"] + target["height"]):
                if bullet["color"] == RED:
                    damage_texts.append({"text": "1", "color": RED, "pos": [target["x"] + target["width"] // 2 - 10, target["y"] - 20], "timer": time.time() + damage_duration})
                elif bullet["color"] == BLUE:
                    damage_texts.append({"text": "2", "color": BLUE, "pos": [target["x"] + target["width"] // 2 - 10, target["y"] - 20], "timer": time.time() + damage_duration})
                bullets.remove(bullet)
                break
        if bullet["y"] < 0 or bullet["y"] > WINDOW_HEIGHT:
            bullets.remove(bullet)

    # 更新黄色子弹位置并检测碰撞
    for yellow_bullet in yellow_bullets[:]:
        yellow_bullet["y"] += yellow_bullet_speed
        for target in targets[:]:
            if (yellow_bullet["x"] >= target["x"] and yellow_bullet["x"] <= target["x"] + target["width"] and
                yellow_bullet["y"] >= target["y"] and yellow_bullet["y"] <= target["y"] + target["height"]):
                damage_texts.append({"text": "3", "color": YELLOW, "pos": [target["x"] + target["width"] // 2 - 10, target["y"] - 20], "timer": time.time() + damage_duration})
                yellow_bullets.remove(yellow_bullet)
                break
        if yellow_bullet["y"] < 0 or yellow_bullet["y"] > WINDOW_HEIGHT:
            yellow_bullets.remove(yellow_bullet)

    # 更新紫色炮弹位置并检测碰撞
    for bomb in purple_bombs[:]:
        bomb["y"] += purple_bomb_speed
        for target in targets[:]:
            if (bomb["x"] + purple_bomb_size >= target["x"] and bomb["x"] <= target["x"] + target["width"] and
                bomb["y"] + purple_bomb_size >= target["y"] and bomb["y"] <= target["y"] + target["height"]):
                purple_bomb_timer[(bomb["x"] + purple_bomb_size // 2, bomb["y"] + purple_bomb_size // 2)] = time.time() + 3  # 留下紫色区域3秒
                purple_bombs.remove(bomb)
                break
        if bomb["y"] < 0 or bomb["y"] > WINDOW_HEIGHT:
            purple_bombs.remove(bomb)

    # 更新紫色区域效果（每0.3秒对碰到的靶子造成1点伤害）
    current_time = time.time()
    for pos, end_time in list(purple_bomb_timer.items()):
        if current_time > end_time:
            del purple_bomb_timer[pos]
        else:
            damage_interval = 0.3
            if current_time - (end_time - 3) >= damage_interval:
                for target in targets[:]:
                    if (math.sqrt((pos[0] - (target["x"] + target["width"] // 2))**2 + 
                                 (pos[1] - (target["y"] + target["height"] // 2))**2) <= purple_bomb_size):
                        damage_texts.append({"text": "1", "color": PURPLE, "pos": [target["x"] + target["width"] // 2 - 10, target["y"] - 20], "timer": time.time() + damage_duration})
                purple_bomb_timer[pos] = end_time  # 重置时间以控制间隔

    # 绘制场景虚线（两边连续虚线，向下移动）
    for y in range(-line_length, WINDOW_HEIGHT, line_spacing):
    # 左边虚线
        pygame.draw.line(window, WHITE, (10, y), (10, y + line_length), 2)
    # 右边虚线
        pygame.draw.line(window, WHITE, (WINDOW_WIDTH - 10, y), (WINDOW_WIDTH - 10, y + line_length), 2)
    # 虚线向下移动（向后感）
    for y in range(-line_length, WINDOW_HEIGHT, line_spacing):
        if y < WINDOW_HEIGHT:
            pygame.draw.line(window, WHITE, (10, y + line_speed), (10, y + line_length + line_speed), 2)
            pygame.draw.line(window, WHITE, (WINDOW_WIDTH - 10, y + line_speed), (WINDOW_WIDTH - 10, y + line_length + line_speed), 2)
    # 绘制
    # 画靶子
    for target in targets:
        pygame.draw.rect(window, WHITE, (target["x"], target["y"], target["width"], target["height"]))
    # 画玩家飞机（三角形）
    points = [(player_x, player_y + player_height),
              (player_x + player_width, player_y + player_height),
              (player_x + player_width // 2, player_y)]
    pygame.draw.polygon(window, WHITE, points)
    # 画普通子弹
    for bullet in bullets:
        pygame.draw.rect(window, bullet["color"], (bullet["x"], bullet["y"], 4, 10))
    # 画黄色子弹（增大三倍）
    for yellow_bullet in yellow_bullets:
        pygame.draw.rect(window, yellow_bullet["color"], (yellow_bullet["x"] - yellow_bullet_width // 2, yellow_bullet["y"], yellow_bullet_width, yellow_bullet_height))
    # 画紫色炮弹
    for bomb in purple_bombs:
        pygame.draw.rect(window, PURPLE, (bomb["x"], bomb["y"], purple_bomb_size, purple_bomb_size))
    # 画紫色区域
    for pos, end_time in purple_bomb_timer.items():
        pygame.draw.circle(window, PURPLE, (int(pos[0]), int(pos[1])), purple_bomb_size, 2)
    # 画角色血条
    pygame.draw.rect(window, RED, (player_x, player_y + player_height + 5, player_width * (player_health / 100), 10))
    pygame.draw.rect(window, WHITE, (player_x, player_y + player_height + 5, player_width, 10), 2)  # 血条边框
    # 画伤害文字
    for damage in damage_texts[:]:
        if time.time() > damage["timer"]:
            damage_texts.remove(damage)
        else:
            text_surface = font.render(damage["text"], True, damage["color"])
            window.blit(text_surface, damage["pos"])

    # 更新显示
    pygame.display.flip()
    clock.tick(60)

# 退出
pygame.quit()