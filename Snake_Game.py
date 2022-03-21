import random
import pygame
import time

pygame.init()

# Game Sound Effects
food = pygame.mixer.Sound('snake_sound/food.ogg')
game_start = pygame.mixer.Sound('snake_sound/game_start.ogg')
crash2 = pygame.mixer.Sound('snake_sound/crash2.ogg')
crash1 = pygame.mixer.Sound('snake_sound/crash1.ogg')
game_over = pygame.mixer.Sound('snake_sound/game_over.mp3')

# Background Images
snake_background = pygame.image.load('snake_images/snake_background.png')
snake_game_over = pygame.image.load('snake_images/snake_game_over.png')
snake_welcome = pygame.image.load('snake_images/snake_welcome.png')

# Define Colours
white = (255, 255, 255)
red = (255, 0, 0)
black = (0, 0, 0)
blue = (0, 0, 255)

# Making Game Window
SCREENWIDTH = 800
SCREENHEIGHT = 500
gameWindow = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))
pygame.display.update()

# Making Game Title
pygame.display.set_caption('Snake')

def text_screen(text, color, font_size, x, y):
    '''Defining Font'''
    font = pygame.font.SysFont(None, font_size)
    screen_text = font.render(text, True, color)
    gameWindow.blit(screen_text, [x, y])

def snake(surface, color, snake_lst, snakeSize):
    for snakeX, snakeY in snake_lst:
        pygame.draw.rect(surface, color, [snakeX, snakeY, snakeSize, snakeSize])

def welcome_screen():
    exitGame = False
    gameOver = False
    while not exitGame:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exitGame = True

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    exitGame = True

                if event.key == pygame.K_RETURN:
                    pygame.mixer.Sound.play(game_start)
                    gameloop()
        gameWindow.blit(snake_welcome,(0, 0))
        pygame.display.update()

# Game Loop
def gameloop():
    # Making Game Specific Variable
    exitGame = False
    gameOver = False
    snake_x = 50
    snake_y = 50
    snake_size = 10
    fps = 30
    velocity_x = 0
    velocity_y = 0
    initial_vel = 5
    score = 0
    snake_len = 1
    snake_list = []
    clock = pygame.time.Clock()
    with open('snake_score.txt','r') as f:
        high_score = f.read()

    food_x = random.randint(10, SCREENWIDTH)
    food_y = random.randint(10, SCREENHEIGHT)

    while not exitGame:
        if gameOver:
            gameWindow.blit(snake_game_over, (0, 0))
            text_screen(f'Your Score : {score}', white, 25, SCREENWIDTH/2.3, SCREENHEIGHT/3.2)

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.QUIT:
                        exitGame = True

                    if event.key == pygame.K_ESCAPE:
                        exitGame = True

                    if event.key == pygame.K_RETURN:
                        pygame.mixer.Sound.play(game_start)
                        gameloop()

        else:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exitGame = True

                if event.type == pygame.K_ESCAPE:
                    exitGame = True

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        velocity_y = -initial_vel
                        velocity_x = 0

                    elif event.key == pygame.K_DOWN:
                        velocity_y = initial_vel
                        velocity_x = 0

                    elif event.key == pygame.K_LEFT:
                        velocity_x = -initial_vel
                        velocity_y = 0

                    elif event.key == pygame.K_RIGHT:
                        velocity_x = initial_vel
                        velocity_y = 0

            snake_x += velocity_x
            snake_y += velocity_y

            if abs(snake_x - food_x) < 10 and abs(snake_y - food_y) < 10:
                food_x = random.randint(10, SCREENWIDTH)
                food_y = random.randint(100, SCREENHEIGHT)
                score += 10
                snake_len += 2
                pygame.mixer.Sound.play(food)

            head = []
            head.append(snake_x)
            head.append(snake_y)
            snake_list.append(head)

            if len(snake_list) > snake_len:
                del snake_list[0]

            if head in snake_list[:-1]:
                gameOver = True
                pygame.mixer.Sound.play(crash2)
                time.sleep(1)
                pygame.mixer.Sound.play(game_over)

            if snake_x < 0 or snake_x > SCREENWIDTH or snake_y < 0 or snake_y > SCREENHEIGHT:
                gameOver = True
                pygame.mixer.Sound.play(crash1)
                time.sleep(1)
                pygame.mixer.Sound.play(game_over)

            if score > int(high_score):
                with open('snake_score.txt','w') as f:
                    f.write(str(score))

            gameWindow.blit(snake_background, (0,0))
            text_screen(f'Score : {score} | High Score : {high_score}', blue, 55, SCREENWIDTH / 5, 7)
            pygame.draw.rect(gameWindow, white, [food_x, food_y, snake_size, snake_size])
            snake(gameWindow, red, snake_list,snake_size)
        pygame.display.update()
        clock.tick(fps)

    pygame.quit()
    quit()

welcome_screen()