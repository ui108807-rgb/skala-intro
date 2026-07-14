import pygame
import random

# 1. 게임 엔진 및 폰트 초기화
pygame.init()
pygame.font.init()

# 2. 게임판 및 화면 크기 설정
BLOCK_SIZE = 30      # 블록 한 칸의 크기 (픽셀)
GRID_WIDTH = 10      # 게임판 가로 칸 수
GRID_HEIGHT = 20     # 게임판 세로 칸 수
SCREEN_WIDTH = 450   # 전체 화면 가로 너비 (게임판 300px + 점수판 150px)
SCREEN_HEIGHT = 600  # 전체 화면 세로 높이

# 색상 정의 (RGB 값)
BLACK = (0, 0, 0)
GREY = (40, 40, 40)
WHITE = (255, 255, 255)

# 테트리스 블록들의 모양 정의 (2차원 행렬)
SHAPES = [
    [[1, 1, 1, 1]], # I 블록
    [[1, 1], [1, 1]], # O 블록
    [[0, 1, 0], [1, 1, 1], [0, 0, 0]], # T 블록
    [[0, 1, 1], [1, 1, 0], [0, 0, 0]], # S 블록
    [[1, 1, 0], [0, 1, 1], [0, 0, 0]], # Z 블록
    [[1, 0, 0], [1, 1, 1], [0, 0, 0]], # J 블록
    [[0, 0, 1], [1, 1, 1], [0, 0, 0]]  # L 블록
]

# 각 블록에 입힐 어울리는 색상들
COLORS = [
    (0, 255, 255),  # 하늘색
    (255, 255, 0),  # 노란색
    (128, 0, 128),  # 보라색
    (0, 255, 0),    # 초록색
    (255, 0, 0),    # 빨간색
    (0, 0, 255),    # 파란색
    (255, 165, 0)   # 주황색
]

class Piece:
    """현재 떨어지고 있는 블록의 정보(좌표, 모양, 색상)를 담는 클래스"""
    def __init__(self, x, y):
        self.x = x
        self.y = y
        shape_idx = random.randint(0, len(SHAPES) - 1)
        self.shape = SHAPES[shape_idx]
        self.color = COLORS[shape_idx]

def check_collision(piece, grid, adj_x=0, adj_y=0, shape=None):
    """블록이 벽, 바닥 혹은 이미 쌓여 있는 블록과 충돌하는지 검사하는 함수"""
    if shape is None:
        shape = piece.shape
        
    for r, row in enumerate(shape):
        for c, val in enumerate(row):
            if val:
                new_x = piece.x + c + adj_x
                new_y = piece.y + r + adj_y
                
                if new_x < 0 or new_x >= GRID_WIDTH or new_y >= GRID_HEIGHT:
                    return True
                if new_y >= 0 and grid[new_y][new_x] != BLACK:
                    return True
    return False

def clear_lines(grid):
    """꽉 찬 가로 줄을 지우고, 지운 줄 수만큼 점수를 계산하는 함수"""
    new_grid = [row for row in grid if BLACK in row]
    cleared = GRID_HEIGHT - len(new_grid)
    
    for _ in range(cleared):
        new_grid.insert(0, [BLACK for _ in range(GRID_WIDTH)])
        
    return new_grid, cleared

def draw_window(screen, grid, current_piece, next_piece, score):
    """화면에 모든 그래픽(블록, 격자, 점수판, 다음 블록 미리보기)을 그려주는 함수"""
    screen.fill(BLACK)
    
    # 1. 이미 바닥에 고정된 블록들 그리기
    for r in range(GRID_HEIGHT):
        for c in range(GRID_WIDTH):
            pygame.draw.rect(screen, grid[r][c], (c * BLOCK_SIZE, r * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))
            
    # 2. 현재 조작 중인 떨어지는 블록 그리기
    if current_piece:
        for r, row in enumerate(current_piece.shape):
            for c, val in enumerate(row):
                if val:
                    pygame.draw.rect(screen, current_piece.color, 
                                     ((current_piece.x + c) * BLOCK_SIZE, (current_piece.y + r) * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))
                    
    # 3. 경기장에 격자무늬 실선 그리기
    for r in range(GRID_HEIGHT):
        pygame.draw.line(screen, GREY, (0, r * BLOCK_SIZE), (GRID_WIDTH * BLOCK_SIZE, r * BLOCK_SIZE))
    for c in range(GRID_WIDTH):
        pygame.draw.line(screen, GREY, (c * BLOCK_SIZE, 0), (c * BLOCK_SIZE, GRID_HEIGHT * BLOCK_SIZE))
        
    # 게임 영역과 점수판의 경계선 그리기
    pygame.draw.line(screen, WHITE, (GRID_WIDTH * BLOCK_SIZE, 0), (GRID_WIDTH * BLOCK_SIZE, SCREEN_HEIGHT), 2)
    
    # 4. 우측 상단 점수판 표시
    font = pygame.font.SysFont("malgungothic", 30)
    score_label = font.render("SCORE", True, WHITE)
    score_val = font.render(str(score), True, WHITE)
    
    screen.blit(score_label, (GRID_WIDTH * BLOCK_SIZE + 20, 20))
    screen.blit(score_val, (GRID_WIDTH * BLOCK_SIZE + 20, 60))
    
    # 5. 다음 블록 미리보기(NEXT) 표시
    next_label = font.render("NEXT", True, WHITE)
    screen.blit(next_label, (GRID_WIDTH * BLOCK_SIZE + 20, 150))
    
    PREVIEW_BLOCK_SIZE = 20
    if next_piece:
        for r, row in enumerate(next_piece.shape):
            for c, val in enumerate(row):
                if val:
                    pygame.draw.rect(
                        screen, 
                        next_piece.color, 
                        (GRID_WIDTH * BLOCK_SIZE + 25 + c * PREVIEW_BLOCK_SIZE, 
                         200 + r * PREVIEW_BLOCK_SIZE,
                         PREVIEW_BLOCK_SIZE - 2, 
                         PREVIEW_BLOCK_SIZE - 2)
                    )
    
    pygame.display.update()

def main():
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("파이썬 클래식 테트리스")
    
    # [신규 기능] 배경 음악(BGM) 오디오 믹서 초기화 및 재생
    try:
        pygame.mixer.init()
        pygame.mixer.music.load("테트리스 코드/bgm.mp3")
        pygame.mixer.music.play(-1)  # -1은 무한 반복 재생을 의미합니다.
    except pygame.error:
        print("안내: '테트리스 코드/bgm.mp3' 파일이 없어 오디오 없이 게임을 오프닝합니다.")
    
    grid = [[BLACK for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
    
    current_piece = Piece(GRID_WIDTH // 2 - 1, 0)
    next_piece = Piece(GRID_WIDTH // 2 - 1, 0)
    
    clock = pygame.time.Clock()
    fall_time = 0
    score = 0
    game_over = False
    
    while not game_over:
        keys = pygame.key.get_pressed()
        fall_speed = 0.05 if keys[pygame.K_DOWN] else 0.5
        
        fall_time += clock.tick(60) / 1000 
        if fall_time >= fall_speed:
            fall_time = 0
            if not check_collision(current_piece, grid, adj_y=1):
                current_piece.y += 1
            else:
                for r, row in enumerate(current_piece.shape):
                    for c, val in enumerate(row):
                        if val and current_piece.y + r >= 0:
                            grid[current_piece.y + r][current_piece.x + c] = current_piece.color
                
                grid, cleared_lines = clear_lines(grid)
                score += cleared_lines * 100
                
                current_piece = next_piece
                next_piece = Piece(GRID_WIDTH // 2 - 1, 0)
                
                if check_collision(current_piece, grid):
                    game_over = True
                    
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
                
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    if not check_collision(current_piece, grid, adj_x=-1):
                        current_piece.x -= 1
                elif event.key == pygame.K_RIGHT:
                    if not check_collision(current_piece, grid, adj_x=1):
                        current_piece.x += 1
                elif event.key == pygame.K_UP:
                    rotated_shape = [list(row) for row in zip(*current_piece.shape[::-1])]
                    if not check_collision(current_piece, grid, shape=rotated_shape):
                        current_piece.shape = rotated_shape
                elif event.key == pygame.K_SPACE:
                    while not check_collision(current_piece, grid, adj_y=1):
                        current_piece.y += 1
                    fall_time = fall_speed

        draw_window(screen, grid, current_piece, next_piece, score)
        
    # 게임 오버 시 BGM 정지
    if pygame.mixer.get_init():
        pygame.mixer.music.stop()
        
    font = pygame.font.SysFont("malgungothic", 40)
    over_text = font.render("GAME OVER", True, (255, 0, 0))
    screen.blit(over_text, (SCREEN_WIDTH // 4 - 20, SCREEN_HEIGHT // 2 - 20))
    pygame.display.update()
    pygame.time.delay(2000)
    pygame.quit()

if __name__ == "__main__":
    main()