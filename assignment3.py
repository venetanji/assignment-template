import pygame
import random
import sys

pygame.init()


# 设置窗口大小为屏幕的一半
window_width = 1000
window_height = 600

# 设置窗口
sc_background = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("Raccoon loves Grape")

# 加载并调整背景图片大小
picture_background = pygame.image.load("images/background.png").convert_alpha()
picture_background = pygame.transform.scale(picture_background, (window_width, window_height))
sc_background.blit(picture_background, (0, 0))

# 定义浣熊类
class Raccoon:
    def __init__(self, x, y):
        self.image = pygame.transform.scale_by(
            pygame.image.load("images/Raccoon.png").convert_alpha(), 0.07)
        self.rect = self.image.get_rect()
        self.rect.left = x
        self.rect.top = y
        self.speed = 10

    def update(self, direction):
        self.rect.left += direction * self.speed

    def draw(self, screen):
        screen.blit(self.image, self.rect)

# 定义葡萄类
class Grape:
    def __init__(self, x, y):
        self.image = pygame.transform.scale_by(
            pygame.image.load("images/Grape.png").convert_alpha(), 0.15)
        self.rect = self.image.get_rect()
        self.speed = 10
        self.move(x, y)

    def move(self, x, y):
        self.rect.x = x
        self.rect.y = y

    def update(self):
        self.rect.y += self.speed

    def draw(self, screen):
        screen.blit(self.image, self.rect)

# 游戏变量
lives = 5
scores = 0
front = pygame.font.Font(None, 30)  # 使用默认字体
clock = pygame.time.Clock()
a = Raccoon(30, window_height - 160)
b = Grape(y=random.randint(-10, 0), x=random.randint(64, 480-32))
paused = False
running = True

# 辅助函数
def draw_text(text, color, x, y):
    image = front.render(text, True, color)
    rect = image.get_rect()
    rect.centerx = x
    rect.centery = y
    sc_background.blit(image, rect)

def coin_move():
    b.move(y=random.randint(0, 10), x=random.randint(64, 480-32))

def handle_input():
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and a.rect.right > 100:
        a.update(-1)
    if keys[pygame.K_RIGHT] and a.rect.left < 480:
        a.update(1)

def handle_coin():
    global lives
    if b.rect.y > window_height:
        lives -= 1
        coin_move()
    else:
        b.update()

def handle_collision():
    global scores
    if a.rect.colliderect(b.rect):
        scores += 1
        b.speed += 0.5
        coin_move()

def check_gameover():
    global lives, scores, paused, running
    if lives == 0:
        sc_background.blit(picture_background, (0, 0))
        draw_text("GAME OVER!", (230, 20, 40), window_width // 2, window_height // 2)
        draw_buttons()
        pygame.display.update()
        paused = True
        while paused:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if restart_button.collidepoint(event.pos):
                        scores = 0
                        lives = 5
                        coin_move()
                        b.speed = 10
                        paused = False
                    elif quit_button.collidepoint(event.pos):
                        paused = False
                        running = False
                if event.type == pygame.QUIT:
                    paused = False
                    running = False

def draw_buttons():
    global restart_button, quit_button
    restart_button = pygame.Rect(window_width // 2 - 100, window_height // 2 + 50, 200, 50)
    quit_button = pygame.Rect(window_width // 2 - 100, window_height // 2 + 110, 200, 50)
    pygame.draw.rect(sc_background, (0, 200, 0), restart_button)
    pygame.draw.rect(sc_background, (200, 0, 0), quit_button)
    draw_text("Restart", (255, 255, 255), window_width // 2, window_height // 2 + 75)
    draw_text("Quit", (255, 255, 255), window_width // 2, window_height // 2 + 135)

def draw():
    sc_background.blit(picture_background, (0, 0))
    draw_text(username, (0, 0, 0), 200, 20)
    draw_text("SCORES: " + str(scores), (0, 0, 0), 100, 20)
    draw_text("LIVES: " + str(lives), (230, 20, 40), 300, 20)
    a.draw(sc_background)
    b.draw(sc_background)
    pygame.display.update()

def get_username():
    input_box = pygame.Rect(window_width // 2 - 100, window_height // 2, 200, 32)
    color_inactive = pygame.Color('white')
    color_active = pygame.Color('purple')
    color = color_inactive
    active = False
    text = ''
    done = False
    font = pygame.font.Font(None, 50)  # 使用默认字体
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if input_box.collidepoint(event.pos):
                    active = not active
                else:
                    active = False
                color = color_active if active else color_inactive
            if event.type == pygame.KEYDOWN:
                if active:
                    if event.key == pygame.K_RETURN:
                        done = True
                    elif event.key == pygame.K_BACKSPACE:
                        text = text[:-1]
                    else:
                        text += event.unicode
        sc_background.blit(picture_background, (0, 0))
        draw_text("Please enter your username:", pygame.Color('purple'), window_width // 2, window_height // 2 - 10)
        txt_surface = front.render(text, True, color)
        width = max(200, txt_surface.get_width() + 10)
        input_box.w = width
        sc_background.blit(txt_surface, (input_box.x + 5, input_box.y + 5))
        pygame.draw.rect(sc_background, color, input_box, 2)
        pygame.display.flip()
        clock.tick(30)
    return text

def play():
    global username, running
    username = get_username()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        handle_input()
        handle_coin()
        handle_collision()
        draw()
        check_gameover()
        clock.tick(30)
    pygame.quit()
    sys.exit()

play()