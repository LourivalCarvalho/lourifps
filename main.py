import pygame
import random
import time
import shot_particles
import sys

pygame.init()

# Screen settings
screen_width = 1280
screen_height = 720
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("FPS Game")

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

# Create the particle system
particle_system = shot_particles.ParticleSystem()

# Function to display the help screen
def show_help(screen):
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

# Function to display the scores screen
# -- next update maybe

# Function to save the score
# -- next update maybe

# Main game function
def main_game(screen):
    target_rect = target_image.get_rect()
    aim_rect = aim_image.get_rect()

    time_limit = 15
    start_time = time.time()

    score = 0
    ammo = 6
    running = True

    background_position = [0, 0]
    mouse_x, mouse_y = pygame.mouse.get_pos()
    background_position[0] += (mouse_x - background_position[0]) * 0.01
    background_position[1] += (mouse_y - background_position[1]) * 0.01

    pygame.mouse.set_visible(False)

    # Select a random music track
    musics = ["assets/bg2.mp3", "assets/bg3.mp3", "assets/bg4.mp3"]
    random_music = random.choice(musics)

    # Play the music
    pygame.mixer.music.load(random_music)
    pygame.mixer.music.set_volume(0.7)
    pygame.mixer.music.play(-1)

    def new_target():
        target_rect.x = random.randint(0, screen_width - target_rect.width)
        target_rect.y = random.randint(0, max(0, screen_height - target_rect.height))

    new_target()

    # Shot particles
    particle_system = shot_particles.ParticleSystem()



    while running:

        elapsed_time = time.time() - start_time
        remaining_time = max(0, time_limit - int(elapsed_time))

        screen.blit(background_image, (0, 0))

        screen.blit(target_image, target_rect)

        aim_rect.center = pygame.mouse.get_pos()
        screen.blit(aim_image, aim_rect)

        time_text = font.render(f'Time: {remaining_time}', True, white)
        score_text = font.render(f'Score: {score}', True, white)
        screen.blit(time_text, (20, 20))
        screen.blit(score_text, (20, 60))

        mouse_x, mouse_y = pygame.mouse.get_pos()
        background_position[0] += (mouse_x - background_position[0]) * 0.01
        background_position[1] += (mouse_y - background_position[1]) * 0.01

        for i in range(ammo):
            pygame.draw.circle(screen, white, (10 + i * 20, 680), 10)

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
                        # Add the target explosion particles here
                        new_target()
                    else:
                        ammo -= 1
                elif event.button == 3:
                    reload_sound.play()
                    ammo = 6
        
        particle_system.update()
        particle_system.draw(screen)

        if remaining_time == 0:
            main_menu(screen)
            # -- next update maybe: High Scores, Game Over, etc..

        pygame.display.flip()
        pygame.time.Clock().tick(60)

    pygame.quit()

# Function for the main menu
def main_menu(screen):
    background_position = [0, 0] 
    running = True
    logo_image = pygame.image.load('assets/logo_lourifps.png').convert_alpha()
    logo_rect = logo_image.get_rect()
    logo_rect.center = (screen_width // 2, 200)

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
        screen.fill(black)

        title_text = font.render("FPS Game", True, white)

        screen.blit(background_image, background_position) #Parallax not working yet!!!
        screen.blit(logo_image, logo_rect)
        screen.blit(title_text, (screen_width // 2 - title_text.get_width() // 2, 300))

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