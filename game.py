import pygame
import time
import random

pygame.init()
pygame.mixer.init()

# Colors
white = (255, 255, 255)
yellow = (255, 255, 102)
black = (0, 0, 0)
red = (213, 50, 80)
green = (0, 255, 0)
blue = (50, 153, 213)
dark_red = (139, 0, 0)

# Display settings
dis_width = 700
dis_height = 600
dis = pygame.display.set_mode((dis_width, dis_height))
pygame.display.set_caption('Змейка 100см')

clock = pygame.time.Clock()
snake_block = 10
snake_speed = 15

font_style = pygame.font.SysFont("bahnschrift", 25)
score_font = pygame.font.SysFont("comicsansms", 35)

# Load images and sounds
background_image = None
snake_image = None
food_image = None
death_sound = None
eat_sound = None

# Ensure paths to images and sounds are correct
image_path = 'telebot.py/a8ea4e4e1db310bc09e2502c118ab689.jpg'
sound_path = 'telebot.py/51187741_comical-mmm-yummy-yummy_by_applehillstudios_preview.mp3'
music_path = 'telebot.py/Aboot-Speed-Up-(TrendyBeatz.com).mp3'

try:
    background_image = pygame.image.load(image_path)
    background_image = pygame.transform.scale(background_image, (dis_width, dis_height))
except Exception as e:
    print(f"Error loading background image: {e}")

try:
    snake_image = pygame.image.load(image_path)
    snake_image = pygame.transform.scale(snake_image, (snake_block, snake_block))
except Exception as e:
    print(f"Error loading snake image: {e}")

try:
    food_image = pygame.image.load(image_path)
    food_image = pygame.transform.scale(food_image, (snake_block, snake_block))
except Exception as e:
    print(f"Error loading food image: {e}")

try:
    death_sound = pygame.mixer.Sound(sound_path)
    eat_sound = pygame.mixer.Sound(sound_path)
except Exception as e:
    print(f"Error loading sound: {e}")

try:
    pygame.mixer.music.load(music_path)
    pygame.mixer.music.play(-1)
except Exception as e:
    print(f"Error loading music: {e}")

def draw_button(text, x, y, w, h, inactive_color, active_color, action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    if x + w > mouse[0] > x and y + h > mouse[1] > y:
        pygame.draw.rect(dis, active_color, (x, y, w, h))
        if click[0] == 1 and action is not None:
            action()
    else:
        pygame.draw.rect(dis, inactive_color, (x, y, w, h))

    button_text = font_style.render(text, True, white)
    dis.blit(button_text, [x + (w / 6), y + (h / 6)])

def quit_game():
    pygame.quit()
    quit()

def game_intro():
    intro = True
    while intro:
        dis.fill(black)
        if background_image:
            dis.blit(background_image, (0, 0))

        message("Добро пожаловать в Змейка 100см", yellow)
        draw_button("Начать", 150, 400, 150, 50, red, dark_red, gameLoop)
        draw_button("Выйти", 400, 400, 150, 50, red, dark_red, quit_game)
        draw_button("Помощь", 275, 470, 150, 50, red, dark_red, show_help)

        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_game()

def show_help():
    help_screen = True
    while help_screen:
        dis.fill(black)
        message("Используйте стрелки для управления змейкой", yellow)
        draw_button("Назад", 300, 400, 150, 50, red, dark_red, game_intro)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_game()

def Your_score(score):
    value = score_font.render("Ваш см: " + str(score), True, black)
    dis.blit(value, [0, 0])

def our_snake(snake_block, snake_list):
    for x in snake_list:
        if snake_image:
            dis.blit(snake_image, (x[0], x[1]))
        else:
            pygame.draw.rect(dis, black, [x[0], x[1], snake_block, snake_block])

def message(msg, color):
    mesg = font_style.render(msg, True, color)
    dis.blit(mesg, [dis_width / 6, dis_height / 3])

def gameLoop():
    game_over = False
    game_close = False

    x1 = dis_width / 2
    y1 = dis_height / 2

    x1_change = 0
    y1_change = 0

    snake_List = []
    Length_of_snake = 1

    foodx = round(random.randrange(0, dis_width - snake_block) / 10.0) * 10.0
    foody = round(random.randrange(0, dis_height - snake_block) / 10.0) * 10.0

    while not game_over:
        while game_close:
            dis.fill(white)
            if background_image:
                dis.blit(background_image, (0, 0))

            message("Ты проиграл!", red)
            Your_score(Length_of_snake - 1)
            draw_button("Заново", 150, 400, 150, 50, red, dark_red, gameLoop)
            draw_button("Выйти", 400, 400, 150, 50, red, dark_red, quit_game)

            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit_game()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        quit_game()
                    if event.key == pygame.K_c:
                        gameLoop()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_game()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x1_change = -snake_block
                    y1_change = 0
                elif event.key == pygame.K_RIGHT:
                    x1_change = snake_block
                    y1_change = 0
                elif event.key == pygame.K_UP:
                    y1_change = -snake_block
                    x1_change = 0
                elif event.key == pygame.K_DOWN:
                    y1_change = snake_block
                    x1_change = 0

        if x1 >= dis_width or x1 < 0 or y1 >= dis_height or y1 < 0:
            game_close = True

        x1 += x1_change
        y1 += y1_change

        dis.fill(blue)
        if background_image:
            dis.blit(background_image, (0, 0))

        if food_image:
            dis.blit(food_image, (foodx, foody))
        else:
            pygame.draw.circle(dis, green, (int(foodx + snake_block / 2), int(foody + snake_block / 2)), snake_block // 2)

        snake_Head = [x1, y1]
        snake_List.append(snake_Head)

        if len(snake_List) > Length_of_snake:
            del snake_List[0]

        for x in snake_List[:-1]:
            if x == snake_Head:
                game_close = True

        our_snake(snake_block, snake_List)
        Your_score(Length_of_snake - 1)

        pygame.display.update()

        if x1 == foodx and y1 == foody:
            foodx = round(random.randrange(0, dis_width - snake_block) / 10.0) * 10.0
            foody = round(random.randrange(0, dis_height - snake_block) / 10.0) * 10.0
            Length_of_snake += 1

        clock.tick(snake_speed)

game_intro()
pygame.quit()