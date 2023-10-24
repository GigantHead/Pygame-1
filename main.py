import pygame
from pygame.locals import *
import random

pygame.init()

#Constants for screen and object dimensions and game colors
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
CELL_SIZE = 10
BODY_COLOR_INNER = (255,255,255)
BODY_COLOR_OUTER = (128,128,128)
FOOD_COLOR = (255,0,0)
FONT = pygame.font.SysFont(None, 40)
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Snake')
player = pygame.Rect((300, 250, 50, 50))
again_rect = pygame.Rect(SCREEN_WIDTH // 2 - 80, SCREEN_HEIGHT // 2, 160, 50)

#Game variables
direction = 1 # 1,2,3,4 up,right,down,left
update_snake = 0
food = [0,0]
new_food = True
new_piece = [0,0]
score = 0
game_over = False
clicked = False

#initial position of the snake - set to the middle of the screen
snake_pos = [[SCREEN_WIDTH//2, SCREEN_HEIGHT//2]]
snake_pos.append([SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + CELL_SIZE])
snake_pos.append([SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + CELL_SIZE * 2])
snake_pos.append([SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + CELL_SIZE * 3])


def draw_score():
    score_txt = 'Score: ' + str(score)
    score_img = FONT.render(score_txt, True, (0,0,255))
    screen.blit(score_img, (0,0))

def check_game_over(game_over) -> bool:
    # Check if the head collides with the rest of the snake's body
    if snake_pos[0] in snake_pos[1:]:
        game_over = True

    # Check for edge collision
    if (
        snake_pos[0][0] < 0
        or snake_pos[0][1] < 0
        or snake_pos[0][0] > SCREEN_WIDTH
        or snake_pos[0][1] > SCREEN_HEIGHT
    ):
        game_over = True
    return game_over
     
def  draw_game_over():
    game_over_txt = 'Game Over!'
    game_over_img = FONT.render(game_over_txt, True, (0,0,255))
    pygame.draw.rect(screen, FOOD_COLOR, (SCREEN_WIDTH // 2 - 80, SCREEN_HEIGHT // 2 - 60, 160, 50))
    screen.blit(game_over_img, (SCREEN_WIDTH // 2 - 80, SCREEN_HEIGHT // 2 - 50))
    
    again_txt = 'Play Again?'
    again_img = FONT.render(again_txt, True, (0,0,255))
    pygame.draw.rect(screen, FOOD_COLOR, again_rect)
    screen.blit(again_img, (SCREEN_WIDTH // 2 - 80, SCREEN_HEIGHT // 2 + 10))


while True:

    #set background 
    screen.fill((0,0,0))
    draw_score()


    for x in snake_pos:
        pygame.draw.rect(screen, BODY_COLOR_OUTER, (x[0], x[1], CELL_SIZE, CELL_SIZE))
        pygame.draw.rect(screen, BODY_COLOR_OUTER, (x[0] + 1, x[1] + 1, CELL_SIZE - 2, CELL_SIZE - 2))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                exit()  # Handle game exit
            elif event.key == pygame.K_UP and direction != 3:
                direction = 1  # Change direction to up
            elif event.key == pygame.K_RIGHT and direction != 4:
                direction = 2  # Change direction to right
            elif event.key == pygame.K_DOWN and direction != 1:
                direction = 3  # Change direction to down
            elif event.key == pygame.K_LEFT and direction != 2:
                direction = 4  # Change direction to left

    if new_food:
        new_food = False
        food[0] = random.randint(0, SCREEN_WIDTH / CELL_SIZE - 1) * CELL_SIZE
        food[1] = random.randint(0, SCREEN_HEIGHT / CELL_SIZE - 1) * CELL_SIZE
        
    pygame.draw.rect(screen, FOOD_COLOR, (food[0],food[1], CELL_SIZE, CELL_SIZE))

    if snake_pos[0] == food:
        new_food = True
        new_piece = list(snake_pos[-1])
        if direction == 1:
            new_piece[1] += CELL_SIZE
        if direction == 2:
            new_piece[1] -= CELL_SIZE
        if direction == 3:
            new_piece[0] += CELL_SIZE
        if direction == 4:
            new_piece[0] -= CELL_SIZE
        snake_pos.append(new_piece)
        score += 1

    if not game_over:
        if update_snake > 99:
            update_snake = 0
            snake_pos = snake_pos[-1:] + snake_pos[:-1]
            if direction == 1: #up
                snake_pos[0][0] = snake_pos[1][0]
                snake_pos[0][1] = snake_pos[1][1] - CELL_SIZE
            if direction == 3: #down
                snake_pos[0][0] = snake_pos[1][0]
                snake_pos[0][1] = snake_pos[1][1] + CELL_SIZE    
            if direction == 2: #right
                snake_pos[0][1] = snake_pos[1][1]
                snake_pos[0][0] = snake_pos[1][0] + CELL_SIZE
            if direction == 4: #left
                snake_pos[0][1] = snake_pos[1][1]
                snake_pos[0][0] = snake_pos[1][0] - CELL_SIZE           
    game_over = check_game_over(game_over)    

    if game_over:
        draw_game_over()
        if event.type == pygame.MOUSEBUTTONDOWN and clicked == False:
            clicked = True
        if event.type == pygame.MOUSEBUTTONUP and clicked == True:
            clicked = False
            pos = pygame.mouse.get_pos()
            if again_rect.collidepoint(pos): 
                direction = 1 # 1,2,3,4 up,right,down,left
                update_snake = 0
                food = [0,0]
                new_food = True
                new_piece = [0,0]
                score = 0
                game_over = False
  
                #initial position of the snake - set to the middle of the screen
                snake_pos = [[SCREEN_WIDTH//2, SCREEN_HEIGHT//2]]
                snake_pos.append([SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + CELL_SIZE])
                snake_pos.append([SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + CELL_SIZE * 2])
                snake_pos.append([SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + CELL_SIZE * 3]) 
                
            
    pygame.display.update()
    update_snake += 1
    
pygame.quit()