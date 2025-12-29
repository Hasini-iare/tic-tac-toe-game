import sys
import pygame
from sys import exit
import random

game_width = 360
game_height = 640
bird_x = game_width / 8
bird_y = game_height / 2
bird_width = 34
bird_height = 24

volume = 0.5
muted = False
mute_button = None

class Bird(pygame.Rect):
    def __init__(self, img):
        pygame.Rect.__init__(self, (bird_x, bird_y, bird_width, bird_height))
        self.img = img

pipe_x = game_width
pipe_y = 0
pipe_width = 64
pipe_height = 512

class Pipe(pygame.Rect):
    def __init__(self, img):
        pygame.Rect.__init__(self, (pipe_x, pipe_y, pipe_width, pipe_height))
        self.img = img
        self.passed = False

pygame.init()
pygame.mixer.init()

pygame.mixer.music.load("background.mp3")
pygame.mixer.music.set_volume(volume)
pygame.mixer.music.play(-1)

window = pygame.display.set_mode((game_width, game_height))
pygame.display.set_caption("Flappy Bird")
clock = pygame.time.Clock()

background_image = pygame.image.load("flappybirdbg.png")
bird_image = pygame.image.load("flappybird.png")
bird_image = pygame.transform.scale(bird_image, (bird_width, bird_height))
top_pipe_image = pygame.image.load("toppipe.png")
top_pipe_image = pygame.transform.scale(top_pipe_image, (pipe_width, pipe_height))
bottom_pipe_image = pygame.image.load("bottompipe.png")
bottom_pipe_image = pygame.transform.scale(bottom_pipe_image, (pipe_width, pipe_height))

game_over_sound = pygame.mixer.Sound("gameover.wav")

font_big = pygame.font.SysFont("ocraextended", 36)
font = pygame.font.SysFont("ocraextended", 24)

bird = Bird(bird_image)
pipes = []
velocity_x = -2
velocity_y = 0
gravity = 0.4
score = 0
game_over = False
game_started = False

def load_high_score():
    try:
        with open("highscore.txt", "r") as f:
            return int(f.read())
    except:
        return 0

def save_high_score(s):
    with open("highscore.txt", "w") as f:
        f.write(str(s))

high_score = load_high_score()

def restart_game():
    global velocity_y, score, game_over
    bird.y = game_height / 2
    velocity_y = 0
    pipes.clear()
    score = 0
    game_over = False

def draw_mute_button():
    global mute_button
    mute_button = pygame.Rect(270, 10, 100, 30)
    pygame.draw.rect(window, (200, 200, 200), mute_button)
    label = "Mute" if not muted else "Unmute"
    text = font.render(label, True, (0, 0, 0))
    window.blit(text, (270, 15))

def draw():
    window.blit(background_image, (0, 0))
    window.blit(bird.img, bird)
    for pipe in pipes:
        window.blit(pipe.img, pipe)
    text_render = font.render(str(int(score)), True, (255, 255, 255))
    window.blit(text_render, (5, 5))
    draw_mute_button()

def draw_menu():
    window.blit(background_image, (0, 0))
    title = font_big.render("FLAPPY BIRD", True, (255, 255, 255))
    prompt = font.render("Press SPACE to Start", True, (255, 255, 255))
    window.blit(title, (60, 250))
    window.blit(prompt, (35, 300))
    draw_mute_button()

def draw_game_over():
    overlay = pygame.Surface((340, 300))

    title = font_big.render("GAME OVER", True, (0, 0, 0))
    s1 = font.render(f"Your Score: {int(score)}", True, (0, 0, 0))
    s2 = font.render(f"Highest Score: {high_score}", True, (0, 0, 0))

    window.blit(title, (80, 190))
    window.blit(s1, (80, 250))
    window.blit(s2, (60, 280))

    button = pygame.Rect(110, 330, 140, 40)
    pygame.draw.rect(window, (235, 252, 220), button)
    txt = font.render("Restart", True, (0, 0, 0))
    window.blit(txt, (130, 338))

    draw_mute_button()
    return button

def move():
    global velocity_y, score, game_over, high_score
    velocity_y += gravity
    bird.y += velocity_y
    bird.y = max(bird.y, 0)

    if bird.y > game_height:
        game_over = True
        if not muted:
            game_over_sound.play()
        if score > high_score:
            high_score = int(score)
            save_high_score(high_score)
        return

    for pipe in pipes:
        pipe.x += velocity_x
        if not pipe.passed and bird.x > pipe.x + pipe.width:
            score += 0.5
            pipe.passed = True
        if bird.colliderect(pipe):
            game_over = True
            if not muted:
                game_over_sound.play()
            if score > high_score:
                high_score = int(score)
                save_high_score(high_score)
            return

    while pipes and pipes[0].x + pipe_width < 0:
        pipes.pop(0)

def create_pipes():
    random_pipe_y = pipe_y - pipe_height / 4 - random.random() * (pipe_height / 2)
    opening_space = game_height / 4
    top_pipe = Pipe(top_pipe_image)
    top_pipe.y = random_pipe_y
    pipes.append(top_pipe)
    bottom_pipe = Pipe(bottom_pipe_image)
    bottom_pipe.y = top_pipe.y + opening_space + top_pipe.height
    pipes.append(bottom_pipe)

create_pipes_timer = pygame.USEREVENT + 0
pygame.time.set_timer(create_pipes_timer, 1500)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if not game_started:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_started = True

        elif not game_over:
            if event.type == create_pipes_timer:
                create_pipes()
            if event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_SPACE, pygame.K_x, pygame.K_UP):
                    velocity_y = -6

        else:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if restart_btn.collidepoint(event.pos):
                    restart_game()

        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_EQUALS, pygame.K_PLUS):
                volume = min(1.0, volume + 0.1)
                if not muted:
                    pygame.mixer.music.set_volume(volume)
            if event.key == pygame.K_MINUS:
                volume = max(0.0, volume - 0.1)
                if not muted:
                    pygame.mixer.music.set_volume(volume)

        if event.type == pygame.MOUSEBUTTONDOWN:
            if mute_button and mute_button.collidepoint(event.pos):
                muted = not muted
                pygame.mixer.music.set_volume(0 if muted else volume)

    if not game_started:
        draw_menu()
    elif not game_over:
        move()
        draw()
    else:
        restart_btn = draw_game_over()

    pygame.display.update()
    clock.tick(60)
