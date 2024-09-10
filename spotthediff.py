import pygame
import random

pygame.init()

# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Set the dimensions of the game window
WINDOW_WIDTH = 600
WINDOW_HEIGHT = 400

# Set the position of the two images
IMAGE1_X = 50
IMAGE2_X = 350
IMAGE_Y = 50

# Load the two images
image1 = pygame.image.load("image1.jpg")
image2 = pygame.image.load("image2.jpg")

# Define the positions of the differences
differences = [(100, 200), (250, 100), (400, 300)]

# Set up the game window
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Spot the Difference")

# Set up the font
font = pygame.font.SysFont(None, 30)

# Set up the score counter
score = 0
score_text = font.render("Score: " + str(score), True, BLACK)

# Loop until the user clicks the close button
done = False
while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # Check if the user clicked on a difference
            pos = pygame.mouse.get_pos()
            for diff in differences:
                if (IMAGE1_X + diff[0], IMAGE_Y + diff[1]) == pos or (IMAGE2_X + diff[0], IMAGE_Y + diff[1]) == pos:
                    score += 1
                    score_text = font.render("Score: " + str(score), True, BLACK)

    # Draw the images and the differences
    window.fill(WHITE)
    window.blit(image1, (IMAGE1_X, IMAGE_Y))
    window.blit(image2, (IMAGE2_X, IMAGE_Y))
    for diff in differences:
        pygame.draw.circle(window, BLACK, (IMAGE1_X + diff[0], IMAGE_Y + diff[1]), 5)
        pygame.draw.circle(window, BLACK, (IMAGE2_X + diff[0], IMAGE_Y + diff[1]), 5)

    # Draw the score
    window.blit(score_text, (10, 10))

    # Update the screen
    pygame.display.flip()

# Clean up
pygame.quit()
