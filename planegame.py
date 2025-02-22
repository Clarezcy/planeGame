import pygame
import time

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

# 字体
font = pygame.font.SysFont("Arial", 24)

# 玩家飞机属性
player_x = WINDOW_WIDTH // 2
player_y = WINDOW_HEIGHT - 50
player_width = 50
player_height = 30
player_speed = 5
player_speed_fast = 10  # 加速速度

# 靶子属性
target_x = WINDOW_WIDTH // 2 - 10
target_y = 50
target_width = 20
target_height = 20

# 子弹列表
bullets = []
bullet_speed = -5

# 伤害显示
damage_text = ""
damage_timer = 0

# 自动发射计时
last_auto_shot = time.time()
auto_shot_interval = 2

# 游戏主循环
clock = pygame.time.Clock()
running = True

while running:
    # 处理事件
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        # 手动发射红色子弹（空格键）
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                bullet_x = player_x + player_width // 2 - 2
                bullet_y = player_y
                bullets.append({"x": bullet_x, "y": bullet_y, "color": RED})

    # 检测 Shift 键是否按下
    keys = pygame.key.get_pressed()
    speed = player_speed_fast if keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT] else player_speed

    # 移动玩家飞机（WASD）
    if keys[pygame.K_a] and player_x > 0:
        player_x -= speed
    if keys[pygame.K_d] and player_x < WINDOW_WIDTH - player_width:
        player_x += speed
    if keys[pygame.K_w] and player_y > 0:
        player_y -= speed
    if keys[pygame.K_s] and player_y < WINDOW_HEIGHT - player_height:
        player_y += speed

    # 自动发射蓝色子弹（每2秒）
    current_time = time.time()
    if current_time - last_auto_shot >= auto_shot_interval:
        bullet_x = player_x + player_width // 2 - 2
        bullet_y = player_y
        bullets.append({"x": bullet_x, "y": bullet_y, "color": BLUE})
        last_auto_shot = current_time

    # 更新子弹位置并检测碰撞
    for bullet in bullets[:]:
        bullet["y"] += bullet_speed
        # 碰撞检测：子弹与靶子重叠
        if (bullet["x"] >= target_x and bullet["x"] <= target_x + target_width and
            bullet["y"] >= target_y and bullet["y"] <= target_y + target_height):
            if bullet["color"] == RED:
                damage_text = "伤害1"
            elif bullet["color"] == BLUE:
                damage_text = "伤害2"
            damage_timer = time.time() + 1  # 显示1秒
            bullets.remove(bullet)
        elif bullet["y"] < 0:
            bullets.remove(bullet)

    # 绘制
    window.fill(BLACK)  # 清屏
    # 画靶子
    pygame.draw.rect(window, WHITE, (target_x, target_y, target_width, target_height))
    # 画玩家飞机（临时用三角形）
    points = [(player_x, player_y + player_height),
              (player_x + player_width, player_y + player_height),
              (player_x + player_width // 2, player_y)]
    pygame.draw.polygon(window, WHITE, points)
    # 画子弹
    for bullet in bullets:
        pygame.draw.rect(window, bullet["color"], (bullet["x"], bullet["y"], 4, 10))
    # 画伤害文字
    if damage_text and time.time() < damage_timer:
        text_surface = font.render(damage_text, True, RED)
        window.blit(text_surface, (WINDOW_WIDTH // 2 - 50, WINDOW_HEIGHT // 2))

    # 更新显示
    pygame.display.flip()
    clock.tick(60)

# 退出
pygame.quit()