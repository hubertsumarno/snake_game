import pygame
import time
import random

pygame.init()

# Window settings
dim = 600
rows = 20
window_size = (dim, dim)
window = pygame.display.set_mode(window_size)
pygame.display.set_caption("Snake with pygame by @hubertsumarno")

# Refresh settings
delay = 0.1

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREY = (128, 128, 128)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
TURQUOISE = (64, 224, 208)

# Segment class
class Segment:
    def __init__ (self, x_pos, y_pos, width):
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.width = width

    def draw(self, window):
        GREEN = (0, 255, 0)
        pygame.draw.rect(window, GREEN, (self.x_pos, self. y_pos, self.width, self.width))

# Food class
class Food:
    def __init__ (self, x_pos, y_pos, width):
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.width = width

    def draw(self, window):
        RED = (255, 0, 0)
        pygame.draw.rect(window, RED, (self.x_pos, self. y_pos, self.width, self.width))
    
# Head
width = dim // rows
head = Segment(5 * width, 10 * width, width)
x_change = 0
y_change = 0

# Food
food = Food(14 * width, 10 * width, width)

# Body 
body = []

# Score
score = 0

# Helper Functions
def draw_grid(window, rows, width):
    gap = width // rows
    for i in range(rows):
        pygame.draw.line(window, GREY, (0, i * gap), (width, i * gap))
        for j in range(rows):
            pygame.draw.line(window, GREY, (j * gap, 0), (j * gap, width))


def game_over_text(window):
    over_font = pygame.font.Font('freesansbold.ttf', 64)
    over_text = over_font.render("GAME OVER", True, WHITE)
    restart_font = pygame.font.Font('freesansbold.ttf', 20)
    restart_text = restart_font.render("press 'space' to restart", True, WHITE)
    window.blit(over_text, (100, 250))
    window.blit(restart_text, (200, 320))


def score_text(window):
    score_font = pygame.font.Font('freesansbold.ttf', 24)
    score_text = score_font.render("Score: " + str(score), True, BLUE)
    window.blit(score_text, (5, 5))


# Main Game Loop
running = True
gameover = False
while running:
    # Background and grid
    window.fill(WHITE)
    draw_grid(window, rows, dim)

    # Draw head of snake
    head.draw(window)

    # Draw food
    food.draw(window)

    # Draw body of snake
    for section in body:
        section.draw(window)

    # Display score
    score_text(window)

    # Check for collision with border:
    if head.x_pos < 0 or head.x_pos > dim - width or head.y_pos < 0 or head.y_pos > dim - width:
        gameover = True

    # Check for collision with body:
    for bod in body:
        if bod.x_pos == head.x_pos and bod.y_pos == head.y_pos:
            gameover = True

    # Display game over if collision with border or body
    if gameover:
        window.fill(BLACK)
        x_change = 0
        y_change = 0
        food.x_pos = 14 * width
        food.y_pos = 10 * width
        game_over_text(window)
        score = 0
        body.clear()

    # Check for colliion with food:
    if head.x_pos == food.x_pos and head.y_pos == food.y_pos:
        # Increase segments
        new_segment = Segment(food.x_pos, food.y_pos, width)
        body.append(new_segment)
        
        # Change position of food
        food.x_pos = random.randint(0, 19) * width
        food.y_pos = random.randint(0, 19) * width
        
        # Update score
        score += 1

    # Move end segments first in reverse order
    for index in range(len(body)-1, 0, -1):
        x = body[index - 1].x_pos
        y = body[index - 1].y_pos
        body[index].x_pos = x
        body[index].y_pos = y

    #Move segment zero to where the head is
    if len(body) > 0:
        x = head.x_pos
        y = head.y_pos
        body[0].x_pos = x
        body[0].y_pos = y

    for event in pygame.event.get():
        # Quit game
        if event.type == pygame.QUIT:
            running = False

        # Keystrokes
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT and not gameover:
                if x_change != 1:
                        x_change = -1
                        y_change = 0
            if event.key == pygame.K_RIGHT and not gameover:
                if x_change != -1:
                        x_change = 1
                        y_change = 0
            if event.key == pygame.K_UP and not gameover:
                if y_change != 1:
                    x_change = 0
                    y_change = -1
            if event.key == pygame.K_DOWN and not gameover:
                if y_change != -1:
                    x_change = 0
                    y_change = 1

            # Check for restart
            if event.key == pygame.K_SPACE and gameover:
                x_change = 0
                y_change = 0
                head.x_pos = 5 * width
                head.y_pos = 10 * width
                gameover = False

    head.x_pos += x_change * width
    head.y_pos += y_change * width

    pygame.display.update()
    time.sleep(delay)