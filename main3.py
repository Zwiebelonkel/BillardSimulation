import pygame
import math
import random

# Particle class represents a billiard ball
class Particle:
    def __init__(self, x, y, r, vx, vy, mass):
        self.x = x  # x-coordinate of the particle
        self.y = y  # y-coordinate of the particle
        self.r = r  # radius of the particle
        self.vx = vx  # velocity in x direction
        self.vy = vy  # velocity in y direction
        self.mass = mass  # mass of the particle

    @property
    def velocity(self):
        return [self.vx, self.vy]  # returns velocity as a list [vx, vy]

    @property
    def speed(self):
        return math.sqrt(self.vx ** 2 + self.vy ** 2)  # calculates the speed from the velocities

    def distance(self, other_particle):
        dx = self.x - other_particle.x  # difference in x-coordinates
        dy = self.y - other_particle.y  # difference in y-coordinates
        return math.sqrt(dx * dx + dy * dy)  # calculates distance between two particles

    def update(self, canvas_width, canvas_height, particles, start, damping_factor):
        # Handles particle collisions
        for i in range(start + 1, len(particles)):
            other_particle = particles[i]
            if self.distance(other_particle) < self.r + other_particle.r:  # check if particles overlap
                res = [self.vx - other_particle.vx, self.vy - other_particle.vy]  # relative velocity
                if res[0] * (other_particle.x - self.x) + res[1] * (other_particle.y - self.y) >= 0:
                    m1 = self.mass
                    m2 = other_particle.mass
                    theta = -math.atan2(other_particle.y - self.y, other_particle.x - self.x)
                    u1 = rotate(self.velocity, theta)
                    u2 = rotate(other_particle.velocity, theta)
                    v1 = rotate([u1[0] * (m1 - m2) / (m1 + m2) + u2[0] * 2 * m2 / (m1 + m2), u1[1]], -theta)
                    v2 = rotate([u2[0] * (m2 - m1) / (m1 + m2) + u1[0] * 2 * m1 / (m1 + m2), u2[1]], -theta)

                    # Update velocities after collision
                    self.vx = v1[0]
                    self.vy = v1[1]
                    other_particle.vx = v2[0]
                    other_particle.vy = v2[1]

        # Boundary conditions
        if self.x - self.r <= 0:
            self.x = self.r

        if self.x + self.r >= canvas_width:
            self.x = canvas_width - self.r

        if (self.x - self.r <= 0 and self.vx < 0) or (self.x + self.r >= canvas_width and self.vx > 0):
            self.vx = -self.vx

        if self.y - self.r <= 0:
            self.y = self.r

        if self.y + self.r >= canvas_height:
            self.y = canvas_height - self.r

        if (self.y - self.r <= 0 and self.vy < 0) or (self.y + self.r >= canvas_height and self.vy > 0):
            self.vy = -self.vy

        # Apply damping factor to velocities
        self.vx *= damping_factor
        self.vy *= damping_factor

        # Update position
        self.x += self.vx
        self.y += self.vy        

    def draw(self, screen, lines):
        speed = self.speed  # get speed
        color = (min(int(speed * 100), 255), 0, max(255 - int(speed * 100), 0))  # color based on speed

        # Draw the particle
        pygame.draw.circle(screen, color, (int(self.x), int(self.y)), self.r)

        # Draw direction line if speed is above threshold and lines option is "ja"
        if speed > 0.2 and lines == "ja":
            direction_line_length = speed * 30 + self.r
            end_x = int(self.x + direction_line_length * self.vx / speed)
            end_y = int(self.y + direction_line_length * self.vy / speed)
            pygame.draw.line(screen, color, (int(self.x), int(self.y)), (end_x, end_y), 2)

# Function to rotate a velocity vector by a given angle theta
def rotate(velocity, theta):
    return [
        velocity[0] * math.cos(theta) - velocity[1] * math.sin(theta),
        velocity[0] * math.sin(theta) + velocity[1] * math.cos(theta)
    ]

# Function to handle user input in a graphical interface
def get_user_input(prompt, screen, font, back_button, next_button, quit_button, show_back_button, buttons=None):
    color_inactive = pygame.Color('lightskyblue3')
    color_active = pygame.Color('dodgerblue2')
    color = color_inactive
    active = False
    text = ''
    done = False
    next_screen = False
    prev_screen = False
    quit_program = False

    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if next_button.collidepoint(event.pos):
                    next_screen = True
                    done = True
                if show_back_button and back_button.collidepoint(event.pos):
                    prev_screen = True
                    done = True
                if quit_button.collidepoint(event.pos):
                    quit_program = True
                    done = True
                if buttons:
                    for button_text, button_rect in buttons:
                        if button_rect.collidepoint(event.pos):
                            text = button_text
                            done = True
            if event.type == pygame.KEYDOWN and not buttons:
                if event.key == pygame.K_RETURN:
                    done = True
                elif event.key == pygame.K_BACKSPACE:
                    text = text[:-1]
                else:
                    text += event.unicode

        screen.fill((30, 30, 30))

        # Draw back button if applicable
        if show_back_button:
            back_text = font.render("Zurück", True, pygame.Color('white'))
            pygame.draw.rect(screen, pygame.Color('white'), back_button, 2)
            screen.blit(back_text, (back_button.x + 10, back_button.y + 5))

        next_text = font.render("Weiter", True, pygame.Color('white'))
        quit_text = font.render("Beenden", True, pygame.Color('white'))
        prompt_text = font.render(prompt, True, pygame.Color('white'))

        screen.blit(next_text, (next_button.x + 10, next_button.y + 5))
        screen.blit(quit_text, (quit_button.x + 10, quit_button.y + 5))
        screen.blit(prompt_text, (screen.get_width() / 2 - prompt_text.get_width() / 2, 20))
        pygame.draw.rect(screen, pygame.Color('white'), next_button, 2)
        pygame.draw.rect(screen, pygame.Color('white'), quit_button, 2)

        # Draw buttons or input box
        if buttons:
            for button_text, button_rect in buttons:
                button_text_surface = font.render(button_text, True, pygame.Color('white'))
                pygame.draw.rect(screen, pygame.Color('white'), button_rect, 2)
                screen.blit(button_text_surface, (button_rect.x + 10, button_rect.y + 5))
        else:
            input_box = pygame.Rect(100, 150, 140, 32)
            txt_surface = font.render(prompt + text, True, color)
            width = max(200, txt_surface.get_width() + 10)
            input_box.w = width
            input_box.center = screen.get_rect().center
            screen.blit(txt_surface, (input_box.x + 5, input_box.y + 5))
            pygame.draw.rect(screen, color, input_box, 2)

        pygame.display.flip()

    return text, next_screen, prev_screen, quit_program

# Main function to run the simulation
def main():
    pygame.display.set_caption("Billard")
    pygame.init()
    screen = pygame.display.set_mode((int(1270 / 2), int(2540 / 3)))  # Fenstergröße vergrößert
    clock = pygame.time.Clock()
    running = True

    font = pygame.font.Font(None, 32)

    # Start screen
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

    back_button = pygame.Rect(50, screen.get_height() - 100, 100, 50)
    next_button = pygame.Rect(screen.get_width() - 150, screen.get_height() - 100, 100, 50)
    quit_button = pygame.Rect(screen.get_width() // 2 - 50, screen.get_height() - 100, 100, 50)

    user_inputs = []  # List to store user inputs
    prompts = [
        "Geben Sie den Zoom ein (2 ist Standard): ",
        "Zufälligen Versatz verwenden? (ja oder nein): ",
        "Linien verwenden? (ja oder nein): "
    ]
    input_index = 0
    quit_program = False

    # Loop to handle user inputs for settings
    while input_index < len(prompts) and not quit_program:
        prompt = prompts[input_index]
        show_back_button = input_index > 0

        buttons = None
        if input_index == 0:
            buttons = [("1", pygame.Rect(200, 300, 50, 50)), ("2", pygame.Rect(300, 300, 50, 50)), ("3", pygame.Rect(400, 300, 50, 50))]
        elif input_index in [1, 2]:
            buttons = [("ja", pygame.Rect(300, 300, 100, 50)), ("nein", pygame.Rect(450, 300, 100, 50))]

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

    # Extract user settings
    zoom = float(user_inputs[0]) if len(user_inputs) > 0 else 2.0
    radius = 28.6 / zoom  
    mass = 170 
    damping_factor = 0.995  
    random_offset_input = user_inputs[1].lower() if len(user_inputs) > 1 else "nein"
    lines_input = user_inputs[2].lower() if len(user_inputs) > 2 else "nein"
    use_random_offset = random_offset_input == "ja"

    # Create particles for the simulation
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

    # User-controlled particle
    user_particle = Particle(center_x, canvas_height - 50, int(radius), 0, 0, mass)
    particles.append(user_particle)

    # Main simulation loop
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
