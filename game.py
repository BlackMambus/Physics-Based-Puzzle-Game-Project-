import pygame
import pymunk
import pymunk.pygame_util
import math

# Initialize
pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Ball Drop Challenge")
clock = pygame.time.Clock()
draw_options = pymunk.pygame_util.DrawOptions(screen)

# Physics space
space = pymunk.Space()
space.gravity = (0, 900)

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Create static floor
floor = pymunk.Segment(space.static_body, (0, HEIGHT - 50), (WIDTH, HEIGHT - 50), 5)
floor.friction = 1.0
space.add(floor)

# Create target
def create_target(x, y):
    body = pymunk.Body(body_type=pymunk.Body.STATIC)
    body.position = x, y
    shape = pymunk.Circle(body, 20)
    shape.color = RED
    shape.sensor = True
    shape.collision_type = 2
    space.add(body, shape)
    return shape

target = create_target(WIDTH - 100, HEIGHT - 100)

# Create ball
def create_ball(x, y):
    body = pymunk.Body(1, pymunk.moment_for_circle(1, 0, 15))
    body.position = x, y
    shape = pymunk.Circle(body, 15)
    shape.elasticity = 0.6
    shape.friction = 0.5
    shape.color = GREEN
    shape.collision_type = 1
    space.add(body, shape)
    return shape

ball = None
launching = False
start_pos = None

# Collision handler
def hit_target(arbiter, space, data):
    print("🎯 Target Hit!")
    return True

handler = space.add_collision_handler(1, 2)
handler.begin = hit_target

# Game loop
running = True
while running:
    screen.fill(WHITE)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if not ball:
                start_pos = pygame.mouse.get_pos()
                launching = True

        elif event.type == pygame.MOUSEBUTTONUP:
            if launching:
                end_pos = pygame.mouse.get_pos()
                dx = start_pos[0] - end_pos[0]
                dy = start_pos[1] - end_pos[1]
                ball = create_ball(*start_pos)
                ball.body.apply_impulse_at_local_point((dx * 5, dy * 5))
                launching = False

    # Draw launch line
    if launching:
        current_pos = pygame.mouse.get_pos()
        pygame.draw.line(screen, (0, 0, 255), start_pos, current_pos, 2)

    # Update physics
    space.step(1/60.0)
    space.debug_draw(draw_options)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()

