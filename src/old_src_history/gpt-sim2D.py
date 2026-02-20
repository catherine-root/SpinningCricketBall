# TODO : create virtual environment to run this in - pygame, ...
import pygame, sys, math

# Initialize
pygame.init()
screen = pygame.display.set_mode((600, 400))
clock = pygame.time.Clock()

# Physics
dt = 0.02
g = 9.81
e = 0.8
y = 50
vy = 0.0

# Ball parameters
ball_radius = 40
floor_y = 300

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Physics
    vy += g * dt * 50  # scaled for visibility
    y += vy * dt * 50

    if y >= floor_y - ball_radius:
        y = floor_y - ball_radius
        vy = -e * vy

    # Clear screen
    screen.fill((230, 230, 230))

    # Shadow (ellipse that gets smaller as ball rises)
    shadow_width = int(ball_radius * 1.5 - (floor_y - y) * 0.1)
    shadow_width = max(10, shadow_width)
    pygame.draw.ellipse(screen, (100, 100, 100, 120),
                        (300 - shadow_width // 2, floor_y + 5, shadow_width, 15))

    # Ball (shaded circle)
    ball_surface = pygame.Surface((ball_radius * 2, ball_radius * 2), pygame.SRCALPHA)
    pygame.draw.circle(ball_surface, (30, 100, 255), (ball_radius, ball_radius), ball_radius)

    # Add highlight (light source reflection)
    pygame.draw.circle(ball_surface, (200, 220, 255), (ball_radius - 10, ball_radius - 10), ball_radius // 3)

    screen.blit(ball_surface, (300 - ball_radius, int(y - ball_radius)))

    # Update
    pygame.display.flip()
    clock.tick(60)
