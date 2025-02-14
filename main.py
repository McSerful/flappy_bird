import pygame, sys, random

def draw_floor():
    screen.blit(floor_surface, (floor_x_pos, 500))
    screen.blit(floor_surface, (floor_x_pos + 376, 500))

def create_pipe():
    random_pipe_pos = random.choice(pipe_height)
    bottom_pipe = pipe_surface.get_rect(midtop = (600, random_pipe_pos))
    top_pip = pipe_surface.get_rect(midbottom = (600, random_pipe_pos - 250))
    return bottom_pipe, top_pip

def move_pipes(pipes):
    for pipe in pipes:
        pipe.centerx -= 5
    return pipes

def draw_pipes(pipes):
    for pipe in pipes:
        if pipe.bottom >= 500:
            screen.blit(pipe_surface, pipe)
        else:
            flip_pipe = pygame.transform.flip(pipe_surface, False, True)
            screen.blit(flip_pipe, pipe)


def check_collision(pipes):
    for pipe in pipes:
        if bird_rect.colliderect(pipe):
            hit_sound.play()
            die_sound.play()
            return False

    if bird_rect.top <= -100 or bird_rect.bottom >= 400:
        return False

    return True

def rotate_bird(bird):
    new_bird = pygame.transform.rotozoom(bird, -bird_movement * 3, 1)
    return new_bird

def bird_animation():
    new_bird = bird_frames[bird_index]
    new_bird_rect = new_bird.get_rect(center = (100, bird_rect.centery))
    return new_bird, new_bird_rect


def score_display(game_state):
    if game_state == 'main_game':
        score_surface = game_font.render(str(int(score)), False, (250, 250, 250))
        score_rect = score_surface.get_rect(center = (188, 50))
        screen.blit(score_surface, score_rect)
    if game_state == 'game_over':
        score_surface = game_font.render(str(int(score)), False, (250, 250, 250))
        score_rect = score_surface.get_rect(center=(188, 50))
        screen.blit(score_surface, score_rect)

        high_score_surface = game_font2.render(f'HIGH SCORE: {int(score)}', False, (250, 250, 250))
        high_score_rect = score_surface.get_rect(center=(122, 450))
        screen.blit(high_score_surface, high_score_rect)

def update_score(score, high_score):
    if score > high_score:
        high_score = score
    return high_score

pygame.mixer.pre_init(frequency=44100, size=16, channels=1, buffer=600)

pygame.init()
screen = pygame.display.set_mode((376, 600))

# Limiting FPS
clock = pygame.time.Clock()

# Game Variables
gravity = 0.25
bird_movement = 0
game_active = True
score = 0
high_score = 0
game_font = pygame.font.Font('Pixeboy-z8XGD.ttf', 45)
game_font2 = pygame.font.Font('Pixeboy-z8XGD.ttf', 30)

bg_surface = pygame.image.load('images/background-night.png').convert()
bg_surface = pygame.transform.scale2x(bg_surface)

floor_surface = pygame.image.load('images/base.png').convert()
floor_surface = pygame.transform.scale2x(floor_surface)
floor_x_pos = 0

bird_downflap = pygame.transform.scale2x(pygame.image.load('images/yellowbird-downflap.png').convert_alpha())
bird_midflap = pygame.transform.scale2x(pygame.image.load('images/yellowbird-midflap.png').convert_alpha())
bird_upflap = pygame.transform.scale2x(pygame.image.load('images/yellowbird-upflap.png').convert_alpha())
bird_frames = [bird_downflap, bird_midflap, bird_upflap]
bird_index = 0
bird_surface = bird_frames[bird_index]
bird_rect = bird_surface.get_rect(center = (100, 300))

BIRDFLAP = pygame.USEREVENT + 1
pygame.time.set_timer(BIRDFLAP, 200)

#bird_surface = pygame.image.load('images/yellowbird-midflap.png').convert_alpha()
#bird_surface = pygame.transform.scale2x(bird_surface)
#bird_rect = bird_surface.get_rect(center = (100, 300))

pipe_surface = pygame.image.load('images/pipe-green.png')
pipe_surface = pygame.transform.scale2x(pipe_surface)
pipe_list = []
SPAWNPIPE = pygame.USEREVENT
pygame.time.set_timer(SPAWNPIPE, 1200)
pipe_height = [350, 420, 250]

game_over_surface = pygame.transform.scale2x(pygame.image.load('images/message.png'))
game_over_rect = game_over_surface.get_rect(center = (188, 310))

flap_sound = pygame.mixer.Sound('sound/wing.wav')
hit_sound = pygame.mixer.Sound('sound/hit.wav')
die_sound = pygame.mixer.Sound('sound/die.wav')
score_sound = pygame.mixer.Sound('sound/point.wav')

score_sound_countdown = 200

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and game_active is True:
                bird_movement = 0
                bird_movement -= 7
                flap_sound.play()

            if event.key == pygame.K_SPACE and game_active is False:
                game_active = True
                pipe_list.clear()
                bird_rect.center = (100, 300)
                bird_movement = 0
                score = 0



        if event.type == SPAWNPIPE:
            pipe_list.extend(create_pipe())

        if event.type == BIRDFLAP:
            if bird_index < 2:
                bird_index += 1
            else:
                bird_index = 0
            bird_surface, bird_rect = bird_animation()


    screen.blit(bg_surface, (0, -330))

    if game_active is True:

        # Bird
        bird_movement += gravity
        rotated_bird = rotate_bird(bird_surface)
        bird_rect.centery += int(bird_movement)
        screen.blit(rotated_bird, bird_rect)
        game_active = check_collision(pipe_list)


        pipe_list = move_pipes(pipe_list)
        draw_pipes(pipe_list)

        score += 0.01
        score_display('main_game')
        score_sound_countdown -= 1
        if score_sound_countdown == 0:
            score_sound.play()
            score_sound_countdown = 200

    else:

        high_score = update_score(score, high_score)
        score_display('game_over')
        screen.blit(game_over_surface, game_over_rect)


    floor_x_pos -= 1
    draw_floor()

    if floor_x_pos <= -376:
        floor_x_pos = 0

    pygame.display.update()
    clock.tick(100)