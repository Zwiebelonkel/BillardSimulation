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

# Function to handle input for initial speed and angle of the cue ball
def get_initial_conditions(screen, font):
    prompt = "Geben Sie die Anfangsgeschwindigkeit des Queue-Balls ein (0-10): "
    speed, next_screen, _, quit_program = get_user_input(prompt, screen, font, pygame.Rect(10, 10, 100, 32), pygame.Rect(screen.get_width() - 110, 10, 100, 32), pygame.Rect(screen.get_width() / 2 - 50, screen.get_height() / 2 + 100, 100, 32), False)
    if quit_program:
        pygame.quit()
        exit()
    prompt = "Geben Sie den Winkel des Queue-Balls ein (0-360): "
    angle, next_screen, _, quit_program = get_user_input(prompt, screen, font, pygame.Rect(10, 10, 100, 32), pygame.Rect(screen.get_width() - 110, 10, 100, 32), pygame.Rect(screen.get_width() / 2 - 50, screen.get_height() / 2 + 100, 100, 32), False)
    if quit_program:
        pygame.quit()
        exit()

    return float(speed), math.radians(float(angle))

# Main function to run the simulation
def main():
    pygame.init()

    # Set up the display
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Billard Simulation")

    # Set up the clock
    clock = pygame.time.Clock()

    # Set up font for text rendering
    font = pygame.font.Font(None, 24)

    running = True
    start_screen = True

    while start_screen:
        screen.fill((30, 30, 30))
        title_text = font.render("Billard Simulation", True, pygame.Color('white'))
        screen.blit(title_text, (screen.get_width() / 2 - title_text.get_width() / 2, screen.get_height() / 2 - title_text.get_height() / 2))

        # Draw buttons
        next_button = pygame.Rect(screen.get_width() / 2 - 50, screen.get_height() / 2 + 50, 100, 32)
        quit_button = pygame.Rect(screen.get_width() / 2 - 50, screen.get_height() / 2 + 100, 100, 32)
        pygame.draw.rect(screen, pygame.Color('white'), next_button, 2)
        pygame.draw.rect(screen, pygame.Color('white'), quit_button, 2)
        next_text = font.render("Start", True, pygame.Color('white'))
        quit_text = font.render("Beenden", True, pygame.Color('white'))
        screen.blit(next_text, (next_button.x + 10, next_button.y + 5))
        screen.blit(quit_text, (quit_button.x + 10, quit_button.y + 5))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                start_screen = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if next_button.collidepoint(event.pos):
                    start_screen = False
                if quit_button.collidepoint(event.pos):
                    running = False
                    start_screen = False

        pygame.display.flip()

    if not running:
        return

    # Get user inputs for initial conditions
    particle_count, next_screen, _, quit_program = get_user_input("Anzahl der Kugeln: ", screen, font, pygame.Rect(10, 10, 100, 32), pygame.Rect(screen.get_width() - 110, 10, 100, 32), pygame.Rect(screen.get_width() / 2 - 50, screen.get_height() / 2 + 100, 100, 32), False)
    if quit_program:
        pygame.quit()
        exit()
    lines, next_screen, _, quit_program = get_user_input("Richtungsanzeige (ja/nein): ", screen, font, pygame.Rect(10, 10, 100, 32), pygame.Rect(screen.get_width() - 110, 10, 100, 32), pygame.Rect(screen.get_width() / 2 - 50, screen.get_height() / 2 + 100, 100, 32), False)
    if quit_program:
        pygame.quit()
        exit()
    damping_factor, next_screen, _, quit_program = get_user_input("Dämpfungsfaktor (0-1): ", screen, font, pygame.Rect(10, 10, 100, 32), pygame.Rect(screen.get_width() - 110, 10, 100, 32), pygame.Rect(screen.get_width() / 2 - 50, screen.get_height() / 2 + 100, 100, 32), False)
    if quit_program:
        pygame.quit()
        exit()

    # Convert inputs to appropriate types
    particle_count = int(particle_count)
    damping_factor = float(damping_factor)

    # Create particles
    particles = []
    for _ in range(particle_count):
        x = random.randint(20, screen.get_width() - 20)
        y = random.randint(20, screen.get_height() - 20)
        r = random.randint(10, 20)
        vx = random.uniform(-2, 2)
        vy = random.uniform(-2, 2)
        mass = random.uniform(0.5, 2)
        particles.append(Particle(x, y, r, vx, vy, mass))

    # Define pocket positions and size
    pocket_radius = 30
    pockets = [
        (pocket_radius, pocket_radius),
        (screen.get_width() - pocket_radius, pocket_radius),
        (pocket_radius, screen.get_height() - pocket_radius),
        (screen.get_width() - pocket_radius, screen.get_height() - pocket_radius)
    ]

    # Get initial conditions for the cue ball
    cue_ball_speed, cue_ball_angle = get_initial_conditions(screen, font)
    cue_ball = Particle(screen.get_width() / 2, screen.get_height() / 2, 15, cue_ball_speed * math.cos(cue_ball_angle), cue_ball_speed * math.sin(cue_ball_angle), 1)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill((30, 30, 30))

        # Update and draw particles
        for i, particle in enumerate(particles):
            particle.update(screen.get_width(), screen.get_height(), particles, i, damping_factor)

        # Update and draw cue ball
        cue_ball.update(screen.get_width(), screen.get_height(), particles, 0, damping_factor)
        cue_ball.draw(screen, lines)

        # Check for collisions with pockets for all balls
        particles = [p for p in particles if not any(math.hypot(p.x - px, p.y - py) < pocket_radius for px, py in pockets)]
        if any(math.hypot(cue_ball.x - px, cue_ball.y - py) < pocket_radius for px, py in pockets):
            cue_ball = Particle(screen.get_width() / 2, screen.get_height() / 2, 15, cue_ball_speed * math.cos(cue_ball_angle), cue_ball_speed * math.sin(cue_ball_angle), 1)

        for particle in particles:
            particle.draw(screen, lines)

        # Draw pockets
        for px, py in pockets:
            pygame.draw.circle(screen, pygame.Color('black'), (px, py), pocket_radius)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()
