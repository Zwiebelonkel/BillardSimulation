import math
import pygame

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

        pygame.draw.circle(screen, color, (int(self.x), int(self.y)), self.r)

        if speed > 0.2 and lines == "ja":
            direction_line_length = speed * 30 + self.r
            end_x = int(self.x + direction_line_length * self.vx / speed)
            end_y = int(self.y + direction_line_length * self.vy / speed)
            pygame.draw.line(screen, color, (int(self.x), int(self.y)), (end_x, end_y), 2)

def rotate(velocity, theta):
    return [
        velocity[0] * math.cos(theta) - velocity[1] * math.sin(theta),
        velocity[0] * math.sin(theta) + velocity[1] * math.cos(theta)
    ]

