import random

import os
os.environ["SDL_AUDIODRIVER"] = "dummy" 

import pygame

pygame.init()

# Game constants
WIDTH = 400  # Swapped from Height
HEIGHT = 600  # Swapped from Width
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (128, 128, 128)
FPS = 60

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
    # Fallback if images aren't found
    character = pygame.Surface((65, 75))
    character.fill(WHITE)
    background = pygame.Surface((WIDTH, HEIGHT))
    background.fill(GRAY)

# Game state
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
CHARACTER_SPEED = 5.5
JUMP_HEIGHT = 13
GRAVITY = 0.4

def check_collisions(rect_list, is_jumping):
    """Check if character collides with any platform"""
    for platform in rect_list:
        if platform.colliderect([character_x, character_y + 60, 90, 10]) and not is_jumping and y_change > 0:
            return True
    return False

def update_character(y_pos):
    """Update character position with physics"""
    global jump, y_change
    
    if jump:
        y_change = -JUMP_HEIGHT
        jump = False
    
    y_pos += y_change
    y_change += GRAVITY
    
    # Keep character in bounds
    if y_pos > HEIGHT - 75:  # Account for character height
        y_pos = HEIGHT - 75
        jump = True
    
    return y_pos

def update_platforms(platform_list, y_pos, change):
    """Update platform positions and generate new ones"""
    global score
    
    # Scroll platforms when character is high enough
    if y_pos < 250 and change < 0:
        for platform in platform_list:
            platform[1] -= change
    
    # Generate new platforms when old ones go off screen
    for i, platform in enumerate(platform_list):
        if platform[1] > HEIGHT:
            platform_list[i] = [
                random.randint(10, WIDTH - 80),  # x position
                random.randint(-50, -10),        # y position
                70,                              # width
                10                               # height
            ]
            score += 1
    
    return platform_list

def main_game_loop():
    global character_x, character_y, jump, x_change, y_change, score, character, platforms  # Declare platforms as global

    running = True

    while running:
        timer.tick(FPS)
        
        # Draw background and character
        screen.fill(BLACK)
        screen.blit(background, (0, 0))
        screen.blit(character, (character_x, character_y))
        
        # Draw score
        score_text = font.render(f"Score: {score}", True, BLACK)
        screen.blit(score_text, (WIDTH - 120, 20))
        
        # Draw platforms
        clouds = []
        for platform in platforms:
            cloud = pygame.draw.rect(screen, BLACK, platform, 0, 3)
            clouds.append(cloud)
        
        # Handle events
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
        
        # Update game state
        jump = check_collisions(clouds, jump)
        character_x += x_change
        
        # Keep character in bounds horizontally
        character_x = max(0, min(character_x, WIDTH - 65))
        
        character_y = update_character(character_y)

        # Correct global usage: declare first, assign later
        platforms = update_platforms(platforms, character_y, y_change)  # Now it works!
        
        # Update character sprite based on direction
        if x_change != 0:
            try:
                character = pygame.transform.scale(
                    pygame.image.load('pascal1.png'), 
                    (65, 75)
                )
                if x_change < 0:  # Flip sprite when moving left
                    character = pygame.transform.flip(character, True, False)
            except pygame.error:
                pass
        
        pygame.display.flip()
    
    pygame.quit()
if __name__ == "__main__":
    main_game_loop()