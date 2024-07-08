import pygame
import math
import random

class Particle:
    def __init__(self, x, y, r, vx, vy, mass):
        self.x = x
        self.y = y
        self.r = r
        self.vx = vx
        self.vy = vy
        self.mass = mass

    @property
    def velocity(self):
        return [self.vx, self.vy]

    @property
    def speed(self):
        return math.sqrt(self.vx ** 2 + self.vy ** 2)

    def distance(self, other_particle):
        dx = self.x - other_particle.x
        dy = self.y - other_particle.y
        return math.sqrt(dx * dx + dy * dy)

    def update(self, canvas_width, canvas_height, particles, start, damping_factor):
        for i in range(start + 1, len(particles)):
            other_particle = particles[i]
            if self.distance(other_particle) < self.r + other_particle.r:
                res = [self.vx - other_particle.vx, self.vy - other_particle.vy]
                if res[0] * (other_particle.x - self.x) + res[1] * (other_particle.y - self.y) >= 0:
                    m1 = self.mass
                    m2 = other_particle.mass
                    theta = -math.atan2(other_particle.y - self.y, other_particle.x - self.x)
                    u1 = rotate(self.velocity, theta)
                    u2 = rotate(other_particle.velocity, theta)
                    v1 = rotate([u1[0] * (m1 - m2) / (m1 + m2) + u2[0] * 2 * m2 / (m1 + m2), u1[1]], -theta)
                    v2 = rotate([u2[0] * (m2 - m1) / (m1 + m2) + u1[0] * 2 * m1 / (m1 + m2), u2[1]], -theta)

                    self.vx = v1[0]
                    self.vy = v1[1]
                    other_particle.vx = v2[0]
                    other_particle.vy = v2[1]

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

        self.vx *= damping_factor
        self.vy *= damping_factor

        self.x += self.vx
        self.y += self.vy        

    def draw(self, screen, lines):
        speed = self.speed
        color = (min(int(speed * 100), 255), 0, max(255 - int(speed * 100), 0))

        # Zeichne den gefüllten Kreis
        pygame.draw.circle(screen, color, (int(self.x), int(self.y)), self.r)

        # Zeichne eine Linie für die Bewegungsrichtung, wenn die Geschwindigkeit nicht null ist
        if speed > 0.2 and lines == "yes":
            direction_line_length = speed * 30 + self.r
            end_x = int(self.x + direction_line_length * self.vx / speed)
            end_y = int(self.y + direction_line_length * self.vy / speed)
            pygame.draw.line(screen, color, (int(self.x), int(self.y)), (end_x, end_y), 2)

def rotate(velocity, theta):
    return [
        velocity[0] * math.cos(theta) - velocity[1] * math.sin(theta),
        velocity[0] * math.sin(theta) + velocity[1] * math.cos(theta)
    ]

def get_user_input(prompt, screen, font):
    input_box = pygame.Rect(100, 100, 140, 32)
    color_inactive = pygame.Color('lightskyblue3')
    color_active = pygame.Color('dodgerblue2')
    color = color_inactive
    active = False
    text = ''
    done = False

    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if input_box.collidepoint(event.pos):
                    active = not active
                else:
                    active = False
                color = color_active if active else color_inactive
            if event.type == pygame.KEYDOWN:
                if active:
                    if event.key == pygame.K_RETURN:
                        done = True
                    elif event.key == pygame.K_BACKSPACE:
                        text = text[:-1]
                    else:
                        text += event.unicode

        screen.fill((30, 30, 30))
        txt_surface = font.render(prompt + text, True, color)
        width = max(200, txt_surface.get_width()+10)
        input_box.w = width
        screen.blit(txt_surface, (input_box.x+5, input_box.y+5))
        pygame.draw.rect(screen, color, input_box, 2)

        pygame.display.flip()

    return text

def main():
    pygame.display.set_caption("Billiard")
    pygame.init()
    screen = pygame.display.set_mode((int(1270/3), int(2540/3)))  # Angepasst, um sicherzustellen, dass es ganze Zahlen sind
    clock = pygame.time.Clock()
    running = True

    font = pygame.font.Font(None, 32) 
    # Zoom Eingabe über Pygame-Bildschirm
    zoom = float(get_user_input("Enter Zoom (2 by default): ", screen, font))
    radius = 28.6 / zoom  # mm
    mass = 170  # g
    damping_factor = 0.995  # Dämpfungsfaktor (Wert zwischen 0 und 1)
    random_offset_input = get_user_input("Use random offset? (yes or no): ", screen, font).lower()
    lines_input = get_user_input("Use lines? (yes or no): ", screen, font).lower()
    use_random_offset = random_offset_input == "yes"
    particles = []
    canvas_width, canvas_height = screen.get_size()
    center_x = canvas_width // 2
    center_y = canvas_height // 2
    
    # Erzeuge 15 Partikel in einer umgekehrten dreieckigen Formation
    start_x = center_x
    start_y = center_y
    num_rows = 5
    count = 0
    
    for row in range(num_rows):
        for col in range(row + 1):
            while True:
                offset = int(2 * radius) + (random.random() * 5 if use_random_offset else 0)  # Offset für jeden Partikel neu berechnen, wenn random_offset verwendet wird
                x = start_x - col * offset + row * radius
                y = start_y - row * offset
                new_particle = Particle(x, y, int(radius), 0, 0, mass)
                
                # Überprüfen, ob der neue Partikel mit bestehenden Partikeln überlappt
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

    # Erzeuge das vom Benutzer gesteuerte Partikel
    user_particle = Particle(center_x, canvas_height - 50, int(radius), 0, 0, mass)
    particles.append(user_particle)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    speed = get_user_input("Enter speed: ", screen, font)
                    angle = get_user_input("Enter angle (degrees): ", screen, font)
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
