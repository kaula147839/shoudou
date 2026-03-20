import pygame
import random

# 宣告遊戲視窗長寬
WIDTH = 490
HEIGHT = 600

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)

# 遊戲初始化
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("數獨")

# 列出文字
font_name = pygame.font.match_font('arial')
def draw_text(surf, text, size, x, y,color):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.centerx = x
    text_rect.top = y
    surf.blit(text_surface, text_rect)

# 數獨建立程式
def create_sudoku():
    global Number_Fixed,Number_Player,choose,mistake
    Number_Fixed = [[0]*9 for i in range(9)]
    Number_Player = [[0]*9 for i in range(9)]
    choose = [[False]*9 for i in range(9)]
    mistake = 0



# 遊戲主迴圈
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            running = False

    screen.fill(WHITE)
    # draw_text(screen, "Sudoku", 50, WIDTH // 2, HEIGHT // 2 - 50)
    # draw_text(screen, "Press ESC to close the game", 30, WIDTH // 2, HEIGHT // 2 + 10)
    pygame.display.update()

pygame.quit() 