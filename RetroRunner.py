import pygame
from sys import exit
from random import randint

def display_score():
    # Calculate current time elapsed since game start
    current_time = int(pygame.time.get_ticks() / 1000) - start_time
    score_surface = test_font.render(f'{current_time}', False, "#000000")
    score_rect = score_surface.get_rect(center=(390, 50))
    screen.blit(score_surface, score_rect)
    return current_time

def get_speed(current_time):
    """
    Calculate game speed based on elapsed time.
    Base speed is 4 pixels/frame.
    Speed increases by 0.1 every 5 seconds.
    Maximum speed capped at 12 for balance.
    """
    speed = 4 + (current_time // 5) * 0.1
    return min(speed, 12)

def obstacle_movement(obstacle_list, speed):
    """
    Move obstacles left by 'speed' pixels each frame.
    Remove obstacles that move off screen.
    """
    new_list = []
    for surface, rect in obstacle_list:
        rect.x -= speed
        screen.blit(surface, rect)
        if rect.x > -50:
            new_list.append((surface, rect))
    return new_list

def collisions(player, obstacles):
    """
    Check for collision between player and any obstacle.
    Return False if collision detected, True otherwise.
    """
    if obstacles:
        for surface, obstacle_rect in obstacles:
            if player.colliderect(obstacle_rect):
                return False
    return True

pygame.init()
screen = pygame.display.set_mode((800, 400))
pygame.display.set_caption('Retro Runner')
icon = pygame.image.load('pics/player.png')
pygame.display.set_icon(icon)
clock = pygame.time.Clock()
test_font = pygame.font.Font('pics/pixel.ttf', 30)
replay_font = pygame.font.Font('pics/pixel.ttf', 20)
game_active = False
start_time = 0
score = 0

# Load and scale background and ground images
sky_surface = pygame.image.load('pics/bg1.png').convert()
sky_surface = pygame.transform.scale(sky_surface, (800, 400))
ground_surface = pygame.image.load('pics/ground1.jpg').convert()
ground_surface = pygame.transform.scale(ground_surface, (800, 100))
ground_x = 0

# Initialize sky horizontal offset for scrolling
sky_x = 0

# Load and scale obstacle images
doggy_surface = pygame.image.load('pics/doggy.png').convert_alpha()
doggy_surface = pygame.transform.scale(doggy_surface, (50, 50))

bird_surface = pygame.image.load('pics/bird.png').convert_alpha()
bird_surface = pygame.transform.scale(bird_surface, (70, 70))

obstacle_rect_list = []

# Load and scale player image and set initial position on ground
player_surface = pygame.image.load('pics/player.png').convert_alpha()
player_surface = pygame.transform.scale(player_surface, (60, 105))
player_rect = player_surface.get_rect(midbottom=(100, 340))

# Create a smaller collision rect for more accurate collision detection
player_collision_rect = player_rect.inflate(-30, -20)

player_gravity = 0

# Game over screen assets
character = pygame.image.load('pics/player.png').convert_alpha()
character = pygame.transform.scale(character, (100, 165))
Name = test_font.render('RETRO RUNNER', False, "#000000")
Replay = replay_font.render("press 'space' to play", False, "#000000")

# Set up obstacle spawn timer event
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer, 1300)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if game_active:
            # Jump on mouse click if player is on ground
            if event.type == pygame.MOUSEBUTTONDOWN:
                if player_rect.collidepoint(event.pos) and player_rect.bottom >= 320:
                    player_gravity = -21

            # Jump on space key if player is on ground
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and player_rect.bottom >= 320:
                    player_gravity = -21

            # Spawn obstacles periodically
            if event.type == obstacle_timer:
                if randint(0, 2):
                    obstacle_rect_list.append((doggy_surface, doggy_surface.get_rect(midbottom=(randint(900, 1100), 315))))
                else:
                    obstacle_rect_list.append((bird_surface, bird_surface.get_rect(midbottom=(randint(900, 1100), 200))))

        else:
            # Start game on space key press
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_active = True
                start_time = int(pygame.time.get_ticks() / 1000)
                obstacle_rect_list.clear()  # clear obstacles on restart
                player_rect.midbottom = (100, 340)
                player_gravity = 0

    if game_active:
        # Calculate current speed based on elapsed time (score)
        speed = get_speed(score)

        # Move sky left by half the speed for parallax effect
        sky_x -= speed * 0.5
        if sky_x <= -sky_surface.get_width():
            sky_x = 0

        # Draw two sky surfaces side by side for seamless scrolling
        screen.blit(sky_surface, (sky_x, 0))
        screen.blit(sky_surface, (sky_x + sky_surface.get_width(), 0))

        # Move ground left by current speed, loop ground image
        ground_x -= speed
        if ground_x <= -ground_surface.get_width():
            ground_x = 0

        screen.blit(ground_surface, (ground_x, 300))
        screen.blit(ground_surface, (ground_x + ground_surface.get_width(), 300))

        # Display current score/time
        score = display_score()

        # Apply gravity to player and update position
        player_gravity += 1
        player_rect.y += player_gravity
        if player_rect.bottom >= 320:
            player_rect.bottom = 320
            player_gravity = 0  # reset gravity when on ground

        screen.blit(player_surface, player_rect)

        # Update collision rect position to match player_rect
        player_collision_rect = player_rect.inflate(-30, -20)

        # Move obstacles with current speed
        obstacle_rect_list = obstacle_movement(obstacle_rect_list, speed)

        # Check for collisions; end game if collision detected
        game_active = collisions(player_collision_rect, obstacle_rect_list)

    else:
        # Game over screen
        screen.fill('orange')
        screen.blit(character, (350, 100))
        screen.blit(Name, (230, 50))
        obstacle_rect_list.clear()
        player_rect.midbottom = (100, 340)
        player_gravity = 0

        score_message = test_font.render(f'Your score is {score}', False, "#000000")

        if score == 0:
            screen.blit(Replay, (200, 300))
        else:
            screen.blit(score_message, (180, 300))

    pygame.display.update()
    clock.tick(60)
