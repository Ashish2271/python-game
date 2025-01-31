import random
import os
os.environ["SDL_AUDIODRIVER"] = "dummy" 
import pygame
pygame.init()

# Game constants
WIDTH = 400
HEIGHT = 600
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (128, 128, 128)
FPS = 60
CHARACTER_SPEED = 5.5  # Add this back
JUMP_HEIGHT = 13       # Add this back
GRAVITY = 0.4          # Add this back
# Game setup
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Platform Game')
timer = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 22)

# Load and scale images
try:
    character = pygame.transform.scale(pygame.image.load('file.png'), (65, 75))
    background = pygame.image.load('jolo.png')
except pygame.error:
    character = pygame.Surface((65, 75))
    character.fill(WHITE)
    background = pygame.Surface((WIDTH, HEIGHT))
    background.fill(GRAY)

# Game state
def reset_game():
    global score, character_x, character_y, platforms, jump, y_change, x_change
    score = 0
    character_x = 170
    character_y = 300
    platforms = [[175, 480, 70, 10], 
                 [85, 340, 70, 10], 
                 [255, 370, 70, 10], 
                 [90, 150, 70, 10]]
    jump = False
    y_change = 0
    x_change = 0

reset_game()

def show_game_over_screen():
    screen.fill(BLACK)
    game_over_text = font.render("Game Over", True, WHITE)
    score_text = font.render(f"Final Score: {score}", True, WHITE)
    restart_text = font.render("Press R to Restart or Q to Quit", True, WHITE)
    screen.blit(game_over_text, (WIDTH//2 - game_over_text.get_width()//2, HEIGHT//2 - 50))
    screen.blit(score_text, (WIDTH//2 - score_text.get_width()//2, HEIGHT//2))
    screen.blit(restart_text, (WIDTH//2 - restart_text.get_width()//2, HEIGHT//2 + 50))
    pygame.display.flip()
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    return True
                elif event.key == pygame.K_q:
                    return False
    return False

def check_collisions(rect_list, is_jumping):
    for platform in rect_list:
        if platform.colliderect([character_x, character_y + 60, 90, 10]) and not is_jumping and y_change > 0:
            return True
    return False

def update_character(y_pos):
    global jump, y_change
    if jump:
        y_change = -JUMP_HEIGHT
        jump = False
    y_pos += y_change
    y_change += GRAVITY
    if y_pos > HEIGHT - 75:
        y_pos = HEIGHT - 75
    return y_pos

def update_platforms(platform_list, y_pos, change):
    global score
    if y_pos < 250 and change < 0:
        for platform in platform_list:
            platform[1] -= change
    for i, platform in enumerate(platform_list):
        if platform[1] > HEIGHT:
            platform_list[i] = [random.randint(10, WIDTH - 80), random.randint(-50, -10), 70, 10]
            score += 1
    return platform_list

def main_game_loop():
    global character_x, character_y, jump, x_change, y_change, score, character, platforms

    running = True
    while running:
        timer.tick(FPS)
        screen.fill(BLACK)
        screen.blit(background, (0, 0))
        screen.blit(character, (character_x, character_y))
        score_text = font.render(f"Score: {score}", True, BLACK)
        screen.blit(score_text, (WIDTH - 120, 20))
        
        clouds = []
        for platform in platforms:
            cloud = pygame.draw.rect(screen, BLACK, platform, 0, 3)
            clouds.append(cloud)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x_change = -CHARACTER_SPEED
                if event.key == pygame.K_RIGHT:
                    x_change = CHARACTER_SPEED
            if event.type == pygame.KEYUP:
                if event.key in (pygame.K_LEFT, pygame.K_RIGHT):
                    x_change = 0
        
        jump = check_collisions(clouds, jump)
        character_x = max(0, min(character_x + x_change, WIDTH - 65))
        character_y = update_character(character_y)
        platforms = update_platforms(platforms, character_y, y_change)

        # Check for Game Over condition
        if character_y == HEIGHT - 75 and not jump:
            restart = show_game_over_screen()
            if restart:
                reset_game()
            else:
                running = False
            continue  # Skip the rest of the loop and restart if needed

        if x_change != 0:
            try:
                character = pygame.transform.scale(pygame.image.load('pascal1.png'), (65, 75))
                if x_change < 0:
                    character = pygame.transform.flip(character, True, False)
            except pygame.error:
                pass
        
        pygame.display.flip()
    
    pygame.quit()

if __name__ == "__main__":
    main_game_loop()