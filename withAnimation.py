import pygame
from sys import exit
from random import randint

# ---------------- Player Class ----------------
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.frames = []
        self.load_frames()
        self.index = 0
        self.image = self.frames[self.index]
        self.rect = self.image.get_rect(midbottom=(100, 340))
        self.gravity = 0

        # Jump sound as instance variable
        self.jump_sound = pygame.mixer.Sound('pics/jump.mp3')
        self.jump_sound.set_volume(0.5)

    def load_frames(self):
        player_surface = pygame.image.load('pics/player.png').convert_alpha()
        player_surface = pygame.transform.scale(player_surface, (60, 105))
        self.frames.append(player_surface)

    def apply_gravity(self):
        self.gravity += 1
        self.rect.y += self.gravity
        if self.rect.bottom >= 320:
            self.rect.bottom = 320
            self.gravity = 0

    def jump(self):
        if self.rect.bottom >= 320:
            self.gravity = -21
            self.jump_sound.play()

    def animate(self):
        self.index += 0.1
        if self.index >= len(self.frames):
            self.index = 0
        self.image = self.frames[int(self.index)]

    def update(self):
        self.apply_gravity()
        self.animate()

# ---------------- Obstacle Class ----------------
class Obstacle(pygame.sprite.Sprite):
    def __init__(self, type):
        super().__init__()
        if type == "cat":
            cat1 = pygame.image.load('pics/cat.png').convert_alpha()
            cat2 = pygame.image.load('pics/cat2.png').convert_alpha()
            cat3 = pygame.image.load('pics/cat3.png').convert_alpha()
            self.frames = [
                pygame.transform.scale(cat1, (70, 70)),
                pygame.transform.scale(cat2, (70, 70)),
                pygame.transform.scale(cat2, (70, 70)),
                pygame.transform.scale(cat3, (70, 70)),
                pygame.transform.scale(cat3, (70, 70)),
                pygame.transform.scale(cat3, (70, 70)),
                pygame.transform.scale(cat3, (70, 70)),
                pygame.transform.scale(cat2, (70, 70)),
                pygame.transform.scale(cat2, (70, 70)),
                pygame.transform.scale(cat1, (70, 70)),
            ]
            y_pos = 315

        else:  # bird
            b1 = pygame.image.load('pics/bird1.png').convert_alpha()
            b2 = pygame.image.load('pics/bird2.png').convert_alpha()
            b3 = pygame.image.load('pics/bird3.png').convert_alpha()
            self.frames = [
                pygame.transform.scale(b1, (70, 70)),
                pygame.transform.scale(b2, (70, 70)),
                pygame.transform.scale(b2, (70, 70)),
                pygame.transform.scale(b3, (70, 70)),
                pygame.transform.scale(b3, (70, 70)),
                pygame.transform.scale(b3, (70, 70)),
                pygame.transform.scale(b3, (70, 70)),
                pygame.transform.scale(b3, (70, 70)),
                pygame.transform.scale(b2, (70, 70)),
                pygame.transform.scale(b2, (70, 70)),
                pygame.transform.scale(b1, (70, 70)),
            ]
            y_pos = 200

        self.index = 0
        self.image = self.frames[self.index]
        self.rect = self.image.get_rect(midbottom=(randint(900, 1100), y_pos))

    def animate(self):
        self.index += 0.15
        if self.index >= len(self.frames):
            self.index = 0
        self.image = self.frames[int(self.index)]

    def update(self, speed):
        self.animate()
        self.rect.x -= speed
        if self.rect.x <= -50:
            self.kill()

# ---------------- Helper Functions ----------------
def display_score():
    current_time = int(pygame.time.get_ticks() / 1000) - start_time
    score_surface = test_font.render(f'{current_time}', False, "#000000")
    score_rect = score_surface.get_rect(center=(390, 50))
    screen.blit(score_surface, score_rect)
    return current_time

def get_speed(current_time):
    speed = 4 + (current_time // 5) * 0.1
    return min(speed, 12)

# ---------------- Game Setup ----------------
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

# Music
pygame.mixer.music.load('pics/music.mp3')  
pygame.mixer.music.set_volume(0.3)             
pygame.mixer.music.play(-1) 

# Player
player = pygame.sprite.GroupSingle()
player.add(Player())

# Obstacles
obstacle_group = pygame.sprite.Group()

# Background
sky_surface = pygame.image.load('pics/bg2.jpg').convert()
sky_surface = pygame.transform.scale(sky_surface, (800, 400))
ground_surface = pygame.image.load('pics/ground2.jpg').convert()
ground_surface = pygame.transform.scale(ground_surface, (800, 100))
ground_x = 0
sky_x = 0

# Game over screen assets
character = pygame.image.load('pics/player.png').convert_alpha()
character = pygame.transform.scale(character, (100, 165))
Name = test_font.render('RETRO RUNNER', False, "#FFFFFF")
Replay = replay_font.render("press 'space' to play", False, "#FFFFFF")

# Spawn obstacles
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer, 1300)

# ---------------- Main Game Loop ----------------
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if game_active:
            if event.type == pygame.MOUSEBUTTONDOWN:
                player.sprite.jump()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    player.sprite.jump()

            if event.type == obstacle_timer:
                if randint(0, 1) == 0:
                    obstacle_group.add(Obstacle("cat"))
                else:
                    obstacle_group.add(Obstacle("bird"))
        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_active = True
                start_time = int(pygame.time.get_ticks() / 1000)
                obstacle_group.empty()
                player.sprite.rect.midbottom = (100, 340)
                player.sprite.gravity = 0

    if game_active:
        speed = get_speed(score)

        # Background
        screen.blit(sky_surface, (sky_x, 0))
        screen.blit(sky_surface, (sky_x + sky_surface.get_width(), 0))

        ground_x -= speed
        if ground_x <= -ground_surface.get_width():
            ground_x = 0
        screen.blit(ground_surface, (ground_x, 300))
        screen.blit(ground_surface, (ground_x + ground_surface.get_width(), 300))

        # Score
        score = display_score()

        # Player
        player.update()
        player.draw(screen)

        # Obstacles
        obstacle_group.update(speed)
        obstacle_group.draw(screen)

        # Collision detection (with rect inflation for fairness)
        if pygame.sprite.spritecollide(player.sprite, obstacle_group, False, pygame.sprite.collide_mask):
            game_active = False

    else:
        # Game Over Screen
        screen.fill('#0b1f40')
        screen.blit(character, (350, 100))
        screen.blit(Name, (230, 50))
        obstacle_group.empty()
        player.sprite.rect.midbottom = (100, 340)
        player.sprite.gravity = 0

        score_message = test_font.render(f'Your score is {score}', False, "#FFFFFF")
        if score == 0:
            screen.blit(Replay, (200, 300))
        else:
            screen.blit(score_message, (180, 300))

    pygame.display.update()
    clock.tick(60)
