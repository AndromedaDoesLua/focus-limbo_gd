import pygame
import random
import time

# Initialize Pygame
pygame.init()

# Initialize the mixer module
pygame.mixer.init()

# Load the MP3 file
pygame.mixer.music.load('limbo.mp3')

# Play the music
pygame.mixer.music.play(-1)  # -1 means loop indefinitely

# Wait for any potential lag in playing the music
time.sleep(1)

# Set the position to 2 minutes and 58 seconds (178 seconds)
pygame.mixer.music.set_pos(178)

# Screen dimensions
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))

# Colors
white = (255, 255, 255)
green = (0, 255, 0)
red = (255, 0, 0)

# Box dimensions
box_width = 50
box_height = 50
box_margin = 20

# Create 8 boxes in a 2x4 grid
boxes = []
for i in range(4):
    for j in range(2):
        x = (screen_width - (2 * box_width + box_margin)) / 2 + j * (box_width + box_margin)  # Centered
        y = (screen_height - (4 * box_height + 3 * box_margin)) / 2 + i * (box_height + box_margin)  # Centered
        color = white
        boxes.append([x, y, color, x, y, white, i, j])  # The last two values are the row and column

# Choose one box to be the correct one (green)
correct_box_index = random.randint(0, 7)
boxes[correct_box_index][2] = green  # Set the current color to green
boxes[correct_box_index][5] = white  # Set the target color to white

# Function to swap boxes
def swap_boxes():
    # Choose a random box
    box1 = random.choice(boxes)
    # Choose a random neighbor to swap with
    neighbors = [(box1[6] + dx, box1[7] + dy) for dx, dy in [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]]
    neighbors = [box for box in boxes if (box[6], box[7]) in neighbors]
    if neighbors:  # Check if there are any neighbors
        box2 = random.choice(neighbors)
        # Swap their target positions
        box1[3], box2[3] = box2[3], box1[3]
        box1[4], box2[4] = box2[4], box1[4]


# Game loop
running = True
start_ticks = pygame.time.get_ticks()  # Starter tick
swap_count = 0
last_swap_time = pygame.time.get_ticks()
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            x, y = pygame.mouse.get_pos()
            for i, box in enumerate(boxes):
                if box[0] < x < box[0] + box_width and box[1] < y < box[1] + box_height:
                    if i == correct_box_index:
                        box[2] = green
                        pygame.time.wait(3500)
                        running = False
                    else:
                        box[2] = red

    # After 2 seconds, change the color of the correct box to white
    if boxes[correct_box_index][2] == green and pygame.time.get_ticks() - start_ticks > 2000:
        boxes[correct_box_index][2] = white

    # Swap boxes if less than 75 swaps have been made, Ending the movement.
    if swap_count < 40 and pygame.time.get_ticks() - last_swap_time > 350:
        swap_boxes()
        swap_count += 1
        last_swap_time = pygame.time.get_ticks()

    # Move boxes towards their target positions
    for box in boxes:
        if box[0] < box[3]:
            box[0] += 0.25  # Increase the speed of the animation
        elif box[0] > box[3]:
            box[0] -= 0.25
        if box[1] < box[4]:
            box[1] += 0.25
        elif box[1] > box[4]:
            box[1] -= 0.25

    # Draw boxes
    screen.fill((0, 0, 0))
    for box in boxes:
        pygame.draw.rect(screen, box[2], pygame.Rect(box[0], box[1], box_width, box_height))

    pygame.display.flip()

pygame.quit()
