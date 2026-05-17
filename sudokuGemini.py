import pygame
import random
import copy

# 宣告遊戲視窗長寬
WIDTH = 490
HEIGHT = 600

# 色彩定義
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
LIGHT_BLUE = (173, 216, 230) # 選取格子的背景色

# 遊戲初始化
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("數獨")

# 列出文字
font_name = pygame.font.match_font('arial')
def draw_text(surf, text, size, x, y, color):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.centerx = x
    text_rect.top = y
    surf.blit(text_surface, text_rect)

# 數獨規則檢查 (改良版：傳入特定盤面做檢查)
def is_valid(grid, r, c, num):
    # 檢查橫列與直行
    for i in range(9):
        if grid[r][i] == num or grid[i][c] == num:
            return False
    # 檢查 3x3 九宮格
    box_r, box_c = r // 3 * 3, c // 3 * 3
    for i in range(box_r, box_r + 3):
        for j in range(box_c, box_c + 3):
            if grid[i][j] == num:
                return False
    return True

# 運用回溯法 (Backtracking) 產生完整的數獨解答
def solve_sudoku(grid):
    for r in range(9):
        for c in range(9):
            if grid[r][c] == 0:
                nums = list(range(1, 10))
                random.shuffle(nums) # 打亂順序以產生不同的盤面
                for num in nums:
                    if is_valid(grid, r, c, num):
                        grid[r][c] = num
                        if solve_sudoku(grid):
                            return True
                        grid[r][c] = 0 # 填不下去就退回上一步 (回溯)
                return False
    return True

# 數獨建立程式
def create_sudoku():
    global Number_Fixed, Number_Display, Answer_Grid, mistake, selected_cell
    mistake = 0
    selected_cell = None
    
    # 1. 產生完整解答
    Answer_Grid = [[0]*9 for _ in range(9)]
    solve_sudoku(Answer_Grid)
    
    # 2. 根據解答挖空來產生題目
    Number_Display = copy.deepcopy(Answer_Grid)
    Number_Fixed = [[False]*9 for _ in range(9)] # 記錄該格是否為不可修改的「提示數」
    
    # 決定挖空的格子數量 (這裡設定挖空 40 格，保留 41 個提示)
    holes = 40
    while holes > 0:
        r = random.randint(0, 8)
        c = random.randint(0, 8)
        if Number_Display[r][c] != 0:
            Number_Display[r][c] = 0
            holes -= 1
            
    # 3. 標記不可修改的提示數字
    for r in range(9):
        for c in range(9):
            if Number_Display[r][c] != 0:
                Number_Fixed[r][c] = True

# 繪製畫面邏輯
def draw_grid():
    # 繪製選取的格子背景
    if selected_cell:
        r, c = selected_cell
        pygame.draw.rect(screen, LIGHT_BLUE, (20 + c * 50, 20 + r * 50, 50, 50))

    # 繪製格線
    for i in range(10):
        thickness = 3 if i % 3 == 0 else 1 # 每三格畫粗線，區分九宮格
        # 橫線
        pygame.draw.line(screen, BLACK, (20, 20 + i * 50), (470, 20 + i * 50), thickness)
        # 直線
        pygame.draw.line(screen, BLACK, (20 + i * 50, 20), (20 + i * 50, 470), thickness)
        
    # 繪製數字
    for r in range(9):
        for c in range(9):
            num = Number_Display[r][c]
            if num != 0:
                color = BLACK if Number_Fixed[r][c] else BLUE
                # 如果玩家填錯，顯示紅色
                if not Number_Fixed[r][c] and num != Answer_Grid[r][c]:
                    color = RED
                draw_text(screen, str(num), 36, 20 + c * 50 + 25, 20 + r * 50 + 5, color)

# 遊戲初始化與建立題目
create_sudoku()

# 遊戲主迴圈
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            running = False
            
        # 處理滑鼠點擊：選取格子
        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = pygame.mouse.get_pos()
            # 判斷是否點擊在網格範圍內
            if 20 <= x <= 470 and 20 <= y <= 470:
                c = (x - 20) // 50
                r = (y - 20) // 50
                selected_cell = (r, c)
            else:
                selected_cell = None
                
        # 處理鍵盤輸入
        if event.type == pygame.KEYDOWN and selected_cell:
            r, c = selected_cell
            if not Number_Fixed[r][c]: # 只能修改被挖空的格子
                # 數字鍵 1-9
                if pygame.K_1 <= event.key <= pygame.K_9:
                    num = event.key - pygame.K_0
                    Number_Display[r][c] = num
                    if num != Answer_Grid[r][c]:
                        mistake += 1
                # 獨立數字鍵盤 (Numpad) 1-9
                elif pygame.K_KP1 <= event.key <= pygame.K_KP9:
                    num = event.key - pygame.K_KP1 + 1
                    Number_Display[r][c] = num
                    if num != Answer_Grid[r][c]:
                        mistake += 1
                # Delete 或 Backspace 刪除數字
                elif event.key == pygame.K_BACKSPACE or event.key == pygame.K_DELETE:
                    Number_Display[r][c] = 0

    # 背景塗白
    screen.fill(WHITE)
    
    # 繪製網格與數字
    draw_grid()
    
    # 繪製下方狀態資訊
    draw_text(screen, f"Mistakes: {mistake}", 30, WIDTH // 2, 490, RED if mistake > 0 else BLACK)
    draw_text(screen, "Click to select a cell, type 1-9 to play", 20, WIDTH // 2, 530, BLACK)
    draw_text(screen, "Press ESC to exit", 18, WIDTH // 2, 560, BLACK)
    
    # 檢查是否過關 (將玩家當前盤面與解答比對)
    is_win = True
    for r in range(9):
        for c in range(9):
            if Number_Display[r][c] != Answer_Grid[r][c]:
                is_win = False
                break
    
    if is_win:
        draw_text(screen, "YOU WIN!", 60, WIDTH // 2, HEIGHT // 2 - 30, BLUE)
    
    # 更新畫面
    pygame.display.update()

pygame.quit()