import pygame
import random

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
BALL_SPEED = 5
PADDLE_SPEED = 10
WHITE = (255, 255, 255)
BRICK_WIDTH, BRICK_HEIGHT = 80, 20
NUM_BRICKS_PER_ROW = 10
NUM_BRICK_ROWS = 3

# Create the game window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Breakout")

# Clock for controlling game speed
clock = pygame.time.Clock()

# Initialize game variables
level = 1
score = 0
lives = 5
paddle_width, paddle_height = 100, 10
paddle_x = (WIDTH - paddle_width) // 2
paddle_y = HEIGHT - 2 * paddle_height
ball_radius = 10
ball_x = WIDTH // 2
ball_y = HEIGHT // 2
ball_dx = BALL_SPEED * random.choice((1, -1))
ball_dy = BALL_SPEED

# Initialize bricks
bricks = []
brick_colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255)]


def create_bricks():
    for row in range(NUM_BRICK_ROWS):
        for col in range(NUM_BRICKS_PER_ROW):
            brick_x = col * BRICK_WIDTH
            brick_y = row * BRICK_HEIGHT
            brick_color = brick_colors[row]
            bricks.append(pygame.Rect(brick_x, brick_y, BRICK_WIDTH, BRICK_HEIGHT))


create_bricks()


def draw_text(text, font, color, x, y):
    text_surface = font.render(text, True, color)
    screen.blit(text_surface, (x, y))


# Game over flag
game_over = False

while not game_over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        paddle_x -= PADDLE_SPEED
    if keys[pygame.K_RIGHT]:
        paddle_x += PADDLE_SPEED

    # Move the ball
    ball_x += ball_dx
    ball_y += ball_dy

    # Ball collision with walls
    if ball_x <= 0 or ball_x >= WIDTH:
        ball_dx *= -1
    if ball_y <= 0:
        ball_dy *= -1

    # Ball collision with the paddle
    if (
            ball_y + ball_radius >= paddle_y
            and paddle_x < ball_x < paddle_x + paddle_width
            and ball_dy > 0
    ):
        ball_dy *= -1

    # Ball collision with bricks
    for brick in bricks:
        if brick.colliderect((ball_x - ball_radius, ball_y - ball_radius, 2 * ball_radius, 2 * ball_radius)):
            ball_dy *= -1
            bricks.remove(brick)
            score += 10

    # Level completion
    if len(bricks) == 0:
        level += 1
        create_bricks()
        ball_x = WIDTH // 2
        ball_y = HEIGHT // 2
        ball_dx = BALL_SPEED * random.choice((1, -1))
        ball_dy = BALL_SPEED

    # Game over if the ball goes out of bounds
    if ball_y >= HEIGHT:
        lives -= 1
        if lives == 0:
            game_over = True
        else:
            ball_x = WIDTH // 2
            ball_y = HEIGHT // 2
            ball_dx = BALL_SPEED * random.choice((1, -1))
            ball_dy = BALL_SPEED

    # Clear the screen
    screen.fill((0, 0, 0))

    # Draw the paddle, ball, and bricks
    pygame.draw.rect(screen, WHITE, (paddle_x, paddle_y, paddle_width, paddle_height))
    pygame.draw.circle(screen, WHITE, (ball_x, ball_y), ball_radius)
    for brick in bricks:
        pygame.draw.rect(screen, brick_colors[bricks.index(brick) // NUM_BRICKS_PER_ROW], brick)

    # Draw game info (score, lives, level)
    font = pygame.font.Font(None, 36)
    draw_text(f"Level: {level}", font, WHITE, 10, 10)
    draw_text(f"Score: {score}", font, WHITE, 10, 50)
    draw_text(f"Lives: {lives}", font, WHITE, 10, 90)

    # Update the display
    pygame.display.update()

    # Limit the frame rate
    clock.tick(60)

    if game_over:
        # Ask the player if they want to play again
        font = pygame.font.Font(None, 72)
        draw_text("Game Over", font, WHITE, 280, 250)
        font = pygame.font.Font(None, 36)
        draw_text("Press R to play again", font, WHITE, 300, 320)
        pygame.display.update()

        # Wait for the player to press 'R' to restart
        while game_over:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        game_over = False
                        # Reset the game variables
                        level = 1
                        score = 0
                        lives = 3
                        create_bricks()
                        ball_x = WIDTH // 2
                        ball_y = HEIGHT // 2
                        ball_dx = BALL_SPEED * random.choice((1, -1))
                        ball_dy = BALL_SPEED
