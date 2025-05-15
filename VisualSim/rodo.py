import pygame
import math
import os
import sys

# --- Configuration ---
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
ROBOT_RADIUS = 4
SPEED = 2
ROW_SPACING = 30
COLUMN_SPACING = 30
BACKGROUND_IMAGE_FILE = "background.jpg"
NORTH_TRAVEL_DISTANCE = 100  # How far they go north before returning

# --- Initialize Pygame ---
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Robot Swarm Deployment")
clock = pygame.time.Clock()

# --- Load and scale background image ---
if not os.path.exists(BACKGROUND_IMAGE_FILE):
    print(f"Error: {BACKGROUND_IMAGE_FILE} not found.")
    sys.exit(1)

background_image = pygame.image.load(BACKGROUND_IMAGE_FILE)
background_image = pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))

# --- Grid Setup ---
num_cols = SCREEN_WIDTH // COLUMN_SPACING
num_rows = SCREEN_HEIGHT // ROW_SPACING

SOURCE_X = 0
SOURCE_Y = SCREEN_HEIGHT
robots = []

for row in range(num_rows):
    for col in range(num_cols):
        target_x = col * COLUMN_SPACING + COLUMN_SPACING // 2
        target_y = row * ROW_SPACING + ROW_SPACING // 2
        robots.append({
            "x": SOURCE_X,
            "y": SOURCE_Y,
            "target_x": target_x,
            "target_y": target_y,
            "deployed": False,
            "phase": "deploy",  # deploy -> north -> return
            "origin_x": SOURCE_X,
            "origin_y": SOURCE_Y
        })

def move_toward(robot, target_x, target_y):
    dx = target_x - robot["x"]
    dy = target_y - robot["y"]
    dist = math.hypot(dx, dy)
    if dist > SPEED:
        robot["x"] += SPEED * dx / dist
        robot["y"] += SPEED * dy / dist
        return False  # not there yet
    else:
        robot["x"] = target_x
        robot["y"] = target_y
        return True  # arrived

# --- Main Loop ---
running = True
while running:
    screen.blit(background_image, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    all_deployed = True
    all_north = True
    all_returned = True

    for robot in robots:
        if robot["phase"] == "deploy":
            done = move_toward(robot, robot["target_x"], robot["target_y"])
            if done:
                robot["deployed"] = True
            else:
                all_deployed = False

        elif robot["phase"] == "north":
            north_target_y = robot["target_y"] - NORTH_TRAVEL_DISTANCE
            if robot["y"] > north_target_y:
                robot["y"] -= SPEED
                all_north = False

        elif robot["phase"] == "return":
            done = move_toward(robot, robot["origin_x"], robot["origin_y"])
            if not done:
                all_returned = False

        pygame.draw.circle(screen, (255, 0, 0), (int(robot["x"]), int(robot["y"])), ROBOT_RADIUS)

    # Phase transitions
    if all_deployed and robots[0]["phase"] == "deploy":
        for robot in robots:
            robot["phase"] = "north"

    elif all_north and robots[0]["phase"] == "north":
        for robot in robots:
            robot["phase"] = "return"

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
