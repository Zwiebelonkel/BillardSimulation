import pygame
import math
import random
from particle import Particle
from interface import get_user_input

def main():
    pygame.display.set_caption("Billard")
    pygame.init()
    screen = pygame.display.set_mode((int(1270 / 3), int(2540 / 3)))  # Neue Bildschirmgröße
    clock = pygame.time.Clock()
    running = True
    font = pygame.font.Font(None, 25)

    # Startbildschirm
    start_screen = True
    while start_screen:
        screen.fill((0, 0, 0))
        start_text = font.render("Drücke 'S' um zu starten", True, (255, 255, 255))
        screen.blit(start_text, (screen.get_width() / 2 - start_text.get_width() / 2, screen.get_height() / 2 - start_text.get_height() / 2))
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s:
                    start_screen = False

    back_button = pygame.Rect(20, screen.get_height() - 70, 100, 50)
    next_button = pygame.Rect(screen.get_width() - 120, screen.get_height() - 70, 100, 50)
    quit_button = pygame.Rect(screen.get_width() // 2 - 50, screen.get_height() - 70, 100, 50)

    user_inputs = []  # Liste zur Speicherung der Benutzereingaben
    prompts = [
        "Geben Sie den Zoom ein (2 ist Standard): ",
        "Zufälligen Versatz verwenden? (ja oder nein): ",
        "Linien verwenden? (ja oder nein): "
    ]
    input_index = 0
    quit_program = False

    # Schleife zur Verarbeitung der Benutzereingaben für Einstellungen
    while input_index < len(prompts) and not quit_program:
        prompt = prompts[input_index]
        show_back_button = input_index > 0

        buttons = None
        if input_index == 0:
            buttons = [("1", pygame.Rect(100, 300, 50, 50)), ("2", pygame.Rect(200, 300, 50, 50)), ("3", pygame.Rect(300, 300, 50, 50))]
        elif input_index in [1, 2]:
            buttons = [("ja", pygame.Rect(100, 300, 100, 50)), ("nein", pygame.Rect(250, 300, 100, 50))]

        user_input, next_screen, prev_screen, quit_program = get_user_input(prompt, screen, font, back_button, next_button, quit_button, show_back_button, buttons)
        
        if next_screen or buttons:
            if input_index < len(user_inputs):
                user_inputs[input_index] = user_input
            else:
                user_inputs.append(user_input)
            input_index += 1
        elif prev_screen:
            input_index -= 1

    if quit_program:
        pygame.quit()
        exit()

    # Extrahieren der Benutzereinstellungen
    zoom = float(user_inputs[0]) if len(user_inputs) > 0 else 2.0
    radius = 28.6 / zoom  
    mass = 170 
    damping_factor = 0.995  
    random_offset_input = user_inputs[1].lower() if len(user_inputs) > 1 else "nein"
    lines_input = user_inputs[2].lower() if len(user_inputs) > 2 else "nein"
    use_random_offset = random_offset_input == "ja"

    # Partikel für die Simulation erstellen
    particles = []
    canvas_width, canvas_height = screen.get_size()
    center_x = canvas_width // 2
    center_y = canvas_height // 2

    start_x = center_x
    start_y = center_y
    num_rows = 5
    count = 0
    
    for row in range(num_rows):
        for col in range(row + 1):
            while True:
                offset = int(2 * radius) + (random.random() * 5 if use_random_offset else 0) 
                x = start_x - col * offset + row * radius
                y = start_y - row * offset
                new_particle = Particle(x, y, int(radius), 0, 0, mass)
                
                overlap = False
                for particle in particles:
                    if new_particle.distance(particle) < new_particle.r + particle.r:
                        overlap = True
                        break
                
                if not overlap:
                    particles.append(new_particle)
                    count += 1
                    break

            if count >= 15:
                break
        if count >= 15:
            break

    # Benutzerkontrolliertes Partikel
    user_particle = Particle(center_x, canvas_height - 50, int(radius), 0, 0, mass)
    particles.append(user_particle)

    # Hauptsimulationsschleife
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    speed = get_user_input("Geschwindigkeit eingeben: ", screen, font, back_button, next_button, quit_button, False)[0]
                    angle = get_user_input("Winkel eingeben (Grad): ", screen, font, back_button, next_button, quit_button, False)[0]
                    speed = float(speed)
                    angle = float(angle)
                    angle = math.radians(angle)
                    user_particle.vx = speed * math.cos(angle)
                    user_particle.vy = -speed * math.sin(angle)

        screen.fill((0, 0, 0))

        for i, particle in enumerate(particles):
            particle.update(canvas_width, canvas_height, particles, i, damping_factor)
            particle.draw(screen, lines_input)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()
