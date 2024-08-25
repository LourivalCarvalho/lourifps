import pygame
import random
import time
import particles_shot
from objects import ClayPigeon, Balloon
from particles_broken_target import ParticlesBrokenTarget
import sys
import config

pygame.init()

# Screen settings
screen_width = config.SCREEN_WIDTH
screen_height = config.SCREEN_HEIGHT
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("LouriFPS - Shoooot!!!")

# Color definitions
white = (255, 255, 255)
black = (0, 0, 0)

# Font loading
font = pygame.font.Font(None, 56)

# Image loading
target_image = pygame.image.load('assets/target.png').convert_alpha()
aim_image = pygame.image.load('assets/aim.png').convert_alpha()
background_image = pygame.image.load('assets/bg_menu.jpg').convert()

# Sound definitions
shot_sounds = [
    pygame.mixer.Sound('assets/shot1.mp3'),
    pygame.mixer.Sound('assets/shot2.mp3'),
    pygame.mixer.Sound('assets/shot3.mp3')
]
hit_sound = pygame.mixer.Sound('assets/shot3.mp3')
reload_sound = pygame.mixer.Sound('assets/reload.mp3')

# Particle system for the smoke and broken target
particle_system = particles_shot.ParticleSystem()
particles_broken_target = ParticlesBrokenTarget()

# Targets 2 and 3
clay_pigeon = ClayPigeon(screen_width, screen_height)
balloon = Balloon(screen_width, screen_height)

highscore = 0

# Highscore load and save txt

def load_highscore():
    global highscore
    try:
        with open('highscore.txt', 'r') as f:
            highscore = int(f.read())
    except FileNotFoundError:
        with open('highscore.txt', 'w') as f:
            f.write('0')
        highscore = 0

def save_highscore(score):
    global highscore
    if score > highscore:
        highscore = score
        with open('highscore.txt', 'w') as f:
            f.write(str(highscore))


#################################
####### Simple High Score #######
#################################
def show_high_scores(screen):
    help_text = (
        ">> Help [?] \n\n"
        "1. Aim at the targets and shoot by clicking the left\n    mouse button.\n"
        "2. Each hit gives you 10 points.\n"
        "3. You have 6 bullets, after which you need to reload\n    by clicking the right mouse button.\n"
        "4. The game lasts 15 seconds, try to get the highest score!\n"
        "5. Press ESC to return to the main menu."
    )

    running = True
    while running:
        screen.fill(black)
        y_offset = 50
        for line in help_text.splitlines():
            text_surface = font.render(line, True, white)
            screen.blit(text_surface, (100, y_offset))
            y_offset += 60

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False

        pygame.display.flip()



###########################
####### Help screen #######
###########################
def show_help(screen):
    help_text = (
        "                           >>>>>>> [?] Help [?] <<<<<<<\n\n"
        "Aim at the targets and shoot by clicking the left mouse button.\n"
        "Square target = 10 points. Balloon or clay pigeon = 20 points.\n"
        "You have 6 bullets, after which you need to reload by clicking\nthe right mouse button.\n"
        "The game lasts 15 seconds, try to get the highest score!\n"
        "Press ESC to return to the main menu."
    )

    running = True
    while running:
        screen.fill(black)
        y_offset = 50
        for line in help_text.splitlines():
            text_surface = font.render(line, True, white)
            screen.blit(text_surface, (40, y_offset))
            y_offset += 77

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False

        pygame.display.flip()



# Function to display the scores screen
# -- next update maybe

# Function to save the score
# -- next update maybe

##################################
####### Main game function #######
##################################
def main_game(screen):
    
    target_rect = target_image.get_rect()
    aim_rect = aim_image.get_rect()

    time_limit = 15
    start_time = time.time()

    score = 0
    ammo = 6
    running = True

    # BG Parallax
    background_image = pygame.image.load('assets/bg_game.jpg').convert()
    background_position = [0, 0]
    background_width, background_height = background_image.get_size()
    target_position = [0, 0]
    lerp_speed = .01
    running = True


    pygame.mouse.set_visible(False)

    # Select a random music track
    musics = ["assets/bg2.mp3", "assets/bg3.mp3", "assets/bg4.mp3"]
    random_music = random.choice(musics)

    # Play the music
    pygame.mixer.music.load(random_music)
    pygame.mixer.music.set_volume(0.7)
    pygame.mixer.music.play(-1)

    # Target 1
    def new_target():
        target_rect.x = random.randint(0, screen_width - target_rect.width)
        target_rect.y = random.randint(0, max(0, screen_height - target_rect.height))
    new_target()

    # Target 2 e 3
    clay_pigeon.launch(screen_width, screen_height)
    balloon.launch(screen_width, screen_height)

    while running:

        elapsed_time = time.time() - start_time
        remaining_time = max(0, time_limit - int(elapsed_time))

        # Create balloon and clay pigeon 5 seconds before time runs out
        if remaining_time <= 5:
            if not balloon.launched:
                balloon.launch(screen_width, screen_height)
            if not clay_pigeon.launched:
                clay_pigeon.launch(screen_width, screen_height)

        # BG Parallax
        screen.fill(black)
        mouse_x, mouse_y = pygame.mouse.get_pos()
        target_position[0] = screen_width // 2 - background_width // 2 + (mouse_x - screen_width // 2) * 0.05
        target_position[1] = screen_height // 2 - background_height // 2 + (mouse_y - screen_height // 2) * 0.05
        background_position[0] += (target_position[0] - background_position[0]) * lerp_speed
        background_position[1] += (target_position[1] - background_position[1]) * lerp_speed
        screen.blit(background_image, background_position)

        screen.blit(target_image, target_rect)

        aim_rect.center = pygame.mouse.get_pos()
        screen.blit(aim_image, aim_rect)

        time_text = font.render(f'Time: {remaining_time}', True, white)
        score_text = font.render(f'Score: {score}', True, white)
        screen.blit(time_text, (20, 20))
        screen.blit(score_text, (20, 60))

        # Update and draw targets 2 e 3
        clay_pigeon.update()
        balloon.update()
        clay_pigeon.draw(screen)
        balloon.draw(screen)

        for i in range(ammo):
            pygame.draw.circle(screen, white, (514 + i * 42, 690), 20)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1 and ammo > 0:
                    particle_system.add_particles(event.pos[0], event.pos[1], 7)
                    random_shot_sound = random.choice(shot_sounds)
                    random_shot_sound.play()
                    
                    if target_rect.collidepoint(event.pos):
                        hit_sound.play()
                        score += 10
                        ammo -= 1
                        particles_broken_target.create_particles(target_rect.x+125, target_rect.y+125, pygame.image.load('assets/broken_target.png'))
                        new_target()
                    elif clay_pigeon.launched and clay_pigeon.rect.y > 0 and clay_pigeon.rect.collidepoint(event.pos):
                        hit_sound.play()
                        score += 20
                        ammo -= 1
                        particles_broken_target.create_particles(clay_pigeon.rect.x+125, clay_pigeon.rect.y+125, pygame.image.load('assets/target_clay_pigeon_broken.png'))
                        clay_pigeon.launched = False
                    elif balloon.launched and balloon.rect.y > 0 and balloon.rect.collidepoint(event.pos):
                        hit_sound.play()
                        score += 20
                        ammo -= 1
                        particles_broken_target.create_particles(balloon.rect.x+125, balloon.rect.y+125, pygame.image.load('assets/target_balloon_burst.png'))
                        balloon.launched = False
                    else:
                        ammo -= 1
                elif event.button == 3:
                    reload_sound.play()
                    ammo = 6
        
        particle_system.update()
        particle_system.draw(screen)

        particles_broken_target.update()
        particles_broken_target.draw(screen)
        pygame.display.flip()
        pygame.time.Clock().tick(60)

        if remaining_time == 0:
            save_highscore(score)
            main_menu(screen)
            # -- next update maybe: High Scores, Game Over, etc..

        pygame.display.flip()
        pygame.time.Clock().tick(60)

    pygame.quit()

##########################################
####### Function for the main menu #######
##########################################
def main_menu(screen):

    running = True
    logo_image = pygame.image.load('assets/logo_lourifps.png').convert_alpha()
    logo_rect = logo_image.get_rect()
    logo_rect.center = (screen_width // 2, 200)

    background_position = [0, 0]
    background_width, background_height = background_image.get_size()
    target_position = [0, 0]
    lerp_speed = .01
    running = True

    pygame.mouse.set_visible(1)

    music_menu = 'assets/bg1.mp3'
    pygame.mixer.music.load(music_menu)
    pygame.mixer.music.play(-1)

    # Definição dos botões
    button_width = 250
    button_height = 50
    button_radius = 10
    button_color = (255, 255, 255)
    button_hover_color = (200, 200, 200)
    button_text_color = (0, 0, 0)

    new_game_button = pygame.Rect(0, 0, button_width, button_height)
    new_game_button.center = (screen_width // 2, 400)
    help_button = pygame.Rect(0, 0, button_width, button_height)
    help_button.center = (screen_width // 2, 500)
    quit_button = pygame.Rect(0, 0, button_width, button_height)
    quit_button.center = (screen_width // 2, 600)

    while running:

        title_text = font.render("Shoooot!!!", True, white)

        # BG Parallax
        screen.fill(black)
        mouse_x, mouse_y = pygame.mouse.get_pos()
        target_position[0] = screen_width // 2 - background_width // 2 + (mouse_x - screen_width // 2) * 0.05
        target_position[1] = screen_height // 2 - background_height // 2 + (mouse_y - screen_height // 2) * 0.05
        background_position[0] += (target_position[0] - background_position[0]) * lerp_speed
        background_position[1] += (target_position[1] - background_position[1]) * lerp_speed
        screen.blit(background_image, background_position)

        screen.blit(logo_image, logo_rect)
        screen.blit(title_text, (screen_width // 2 - title_text.get_width() // 2, 300))

        # Show highscore in main menu
        load_highscore()
        highscore_text = font.render(f'Highscore: {highscore}', True, white)
        screen.blit(highscore_text, (screen_width - 350, 600))

        # Button definitions
        for button, text, y in [(new_game_button, "New Game", 400), (help_button, "Help", 500), (quit_button, "Quit", 600)]:
            if button.collidepoint(pygame.mouse.get_pos()):
                pygame.draw.rect(screen, button_hover_color, (button.x, button.y, button.width, button.height), border_radius=button_radius)
                button_width_scaled = int(button_width * 1.1)
                button_height_scaled = int(button_height * 1.1)
                button_scaled = pygame.Rect(0, 0, button_width_scaled, button_height_scaled)
                button_scaled.center = (screen_width // 2, y)
                pygame.draw.rect(screen, button_hover_color, button_scaled, border_radius=button_radius)
            else:
                pygame.draw.rect(screen, button_color, (button.x, button.y, button.width, button.height), border_radius=button_radius)

            text_surface = font.render(text, True, button_text_color)
            text_rect = text_surface.get_rect(center=(button.centerx, button.centery))
            screen.blit(text_surface, text_rect)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if new_game_button.collidepoint(event.pos):
                    main_game(screen)
                elif help_button.collidepoint(event.pos):
                    show_help(screen)
                elif quit_button.collidepoint(event.pos):
                    running = False
                    pygame.quit()
                    sys.exit()

        pygame.display.flip()

# Execute the main menu
main_menu(screen)
pygame.quit()
sys.exit()