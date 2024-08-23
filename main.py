import pygame
import random
import time
import shot_particles

# Inicializando o Pygame
pygame.init()

# Configurações da tela
screen_width = 1280
screen_height = 720
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("FPS Game")

# Definição de cores
white = (255, 255, 255)
black = (0, 0, 0)

# Carregamento de fontes
font = pygame.font.Font(None, 48)

# Carregamento de imagens
target_image = pygame.image.load('assets/target.png').convert_alpha()
aim_image = pygame.image.load('assets/aim.png').convert_alpha()
background_image = pygame.image.load('assets/bg_menu.jpg').convert()

# Definição de sons
shot_sound = pygame.mixer.Sound('assets/shot1.mp3')
hit_sound = pygame.mixer.Sound('assets/shot3.mp3')
reload_sound = pygame.mixer.Sound('assets/reload.mp3')

# Crie o sistema de partículas
particle_system = shot_particles.ParticleSystem()

'''# Função para o efeito de partículas ao atirar
def create_particles_shot(pos, screen):
    particles = []
    for _ in range(7):
        velocity = [random.randint(-5, 5), random.randint(-5, 5)]
        particles.append([list(pos), velocity])
    for particle in particles:
        particle[0][0] += particle[1][0]
        particle[0][1] += particle[1][1]
        particle[1][1] += 0.1  # Gravidade
        pygame.draw.circle(screen, white, [int(particle[0][0]), int(particle[0][1])], 3)'''

'''# Função para o efeito de partículas ao explodir o alvo
def create_particles_explode(pos, screen):
    particles = []
    for _ in range(15):
        velocity = [random.randint(-7, 7), random.randint(-7, 7)]
        particles.append([list(pos), velocity])
    for particle in particles:
        particle[0][0] += particle[1][0]
        particle[0][1] += particle[1][1]
        particle[1][1] += 0.2  # Gravidade
        pygame.draw.circle(screen, (255, 0, 0), [int(particle[0][0]), int(particle[0][1])], 5)'''

# Função para mostrar a tela de ajuda
def show_help(screen):
    help_text = (
        "Help: \n\n"
        "1. Aim at the targets and shoot by clicking the left mouse button.\n"
        "2. Each hit gives you 10 points.\n"
        "3. You have 6 bullets, after which you need to reload by clicking the right mouse button.\n"
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

# Função para mostrar a tela de pontuações
# -- next update maybe

# Função para salvar a pontuação
# -- next update maybe

# Função principal do jogo
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

    def new_target():
        target_rect.x = random.randint(0, screen_width - target_rect.width)
        target_rect.y = random.randint(0, max(0, screen_height - target_rect.height))

    new_target()

    #Shot particles
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
                    shot_sound.play()
                    
                    if target_rect.collidepoint(event.pos):
                        hit_sound.play()
                        score += 10
                        ammo -= 1
                        # criar partículas de explosão do target
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

# Função para o menu principal
def main_menu(screen):
    background_position = [0, 0] 
    running = True
    logo_image = pygame.image.load('assets/logo_lourifps.png').convert_alpha()
    logo_rect = logo_image.get_rect()
    logo_rect.center = (screen_width // 2, 200)  # Posição do logotipo

    pygame.mouse.set_visible(1)

    while running:
        screen.fill(black)

        title_text = font.render("FPS Game", True, white)
        new_game_text = font.render("New Game", True, white)
        help_text = font.render("Help", True, white)
        quit_text = font.render("Quit", True, white)

        screen.blit(background_image, background_position) #Parallax
        screen.blit(logo_image, logo_rect)  # Adiciona o logotipo
        screen.blit(title_text, (screen_width // 2 - title_text.get_width() // 2, 300))
        screen.blit(new_game_text, (screen_width // 2 - new_game_text.get_width() // 2, 400))
        screen.blit(help_text, (screen_width // 2 - help_text.get_width() // 2, 500))
        screen.blit(quit_text, (screen_width // 2 - quit_text.get_width() // 2, 600))
        
        

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if new_game_text.get_rect(center=(screen_width // 2, 400)).collidepoint(event.pos):
                    main_game(screen)
                elif help_text.get_rect(center=(screen_width // 2, 500)).collidepoint(event.pos):
                    show_help(screen)
                elif quit_text.get_rect(center=(screen_width // 2, 600)).collidepoint(event.pos):
                    running = False

        pygame.display.flip()

# Execução do menu principal
main_menu(screen)
pygame.quit()