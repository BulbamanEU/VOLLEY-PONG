import pygame
from ball_trajectory import calculate_trajectory
from bounce_values import update_ball
from ball_touch import net_touch, wall_touch
from Rec_class import *
from read_values import *
import read_values
import json
import math
import random


def change_TURN_ON(TURN_ON):
    try:
        with open('saved_values.json', 'r') as json_file:
            data = json.load(json_file)

        data["TURN_ON"] = TURN_ON

        with open('saved_values.json', 'w') as json_file:
            json.dump(data, json_file, indent=4)

    except FileNotFoundError:
        WARNING('saved_values.json')


def calculate_ending_x(start_x, start_y, angle_deg, speed, gravity, end_y):
    angle_rad = math.radians(angle_deg)

    Vx = speed * math.cos(angle_rad)
    Vy = speed * math.sin(angle_rad)

    t = (2 * Vy) / gravity

    dx = Vx * t


    end_x = start_x + dx

    return end_x

def calculate_bar_length(time_elapsed, max_time, max_bar_length):
    return min(max_bar_length, int(max_bar_length * (time_elapsed / max_time)))


def current_coords(traveled_x, traveled_y, invert, dist_wall):
    ball.y -= traveled_y
    if invert:
        ball.x += (dist_wall - traveled_x)
    else:
        ball.x += traveled_x

def draw_text(text, font, color, x, y):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.center = (x, y)
    screen.blit(text_surface, text_rect)

def choose_strength(time):

    if time < 0.5:
        strength = 0
    elif time < 0.8:
        strength = 1
    elif time < 1.1:
        strength = 2
    elif time < 1.5:
        strength = 3
    else:
        strength = 3

    return strength


def draw_outer_box_and_bar(bar_length, max_bar_length):

    outer_box_rect = pygame.Rect(45, 45, max_bar_length + 10, 30)
    pygame.draw.rect(screen, (255,255,0), outer_box_rect, 2)

    bar_rect = pygame.Rect(50, 50, bar_length, 20)
    pygame.draw.rect(screen, (255,255,0), bar_rect)


def play(run):
    from Rec_class import ball

    center_y = com.y + com._height/2

    pygame.init()
    end_menu_run = False
    main_menu_run = False

    offset = player_key._height + ball._height/2

    TRAVEL_X, TRAVEL_Y, travelling, invert, ANGLE, strength,\
        dist_wall, pause, start_time, TURN_ON = read_values.get_values()

    clock = pygame.time.Clock()
    if not TURN_ON:
        current_time = pygame.time.get_ticks() / 1000
        pause = current_time - pause
        time_before_pause = 0
    else:
        time_before_pause = pause - start_time
        read_values.get_last_position(ball, com, player_key)
        player_key.rect.center = (player_key.x+player_key.get_width()/2, center_y)
        com.rect.center = (com.x+com.get_width()/2, center_y)
        pause = 0
        read_values.reset_values("starting_position.json", "current_position.json")
        ball, visual.center, travelling, invert, TRAVEL_X, TRAVEL_Y, pause = update_ball(ball, offset)

    key_s_held_time = 0
    max_bar_length = 200
    ending_x = 900

    while run:
        screen.fill((0, 0, 0))

        for object in drawing_objects:
            object.draw(screen)

        if TURN_ON:
            start_time = pygame.time.get_ticks() / 1000
            TURN_ON = False
        if player_key.rect.colliderect(ball.rect):
            if ANGLE == PLAYER_ANGLE:
                run = False
                read_values.reset_field(ball, player_key, com, visual)
                read_values.reset_values()
                end_menu_run = True
            start_time = pygame.time.get_ticks() / 1000
            current_coords(TRAVEL_X, TRAVEL_Y, invert, dist_wall)
            ANGLE = PLAYER_ANGLE
            strength = new_strength
            key_s_held_time = 0
            time_before_pause = 0
            ball, visual.center, travelling, invert, TRAVEL_X, TRAVEL_Y, pause = update_ball(ball, offset)


        if com.rect.colliderect(ball.rect):
            start_time = pygame.time.get_ticks() / 1000
            current_coords(TRAVEL_X, TRAVEL_Y, invert, dist_wall)
            ANGLE = COM_ANGLE
            strength = random.randint(0, 3)
            time_before_pause = 0
            ball, visual.center, travelling, invert, TRAVEL_X, TRAVEL_Y, pause = update_ball(ball, offset)

        if travelling:
            travelling = net_touch(ball, NET, TRAVEL_Y)
            current_time = pygame.time.get_ticks() / 1000
            current_time += time_before_pause - pause
            elapsed_time = current_time - start_time
            TRAVEL_X, TRAVEL_Y = calculate_trajectory(SPEED[strength], GRAVITY, ANGLE[strength], elapsed_time)
            ball.x, invert, dist_wall = wall_touch(ball.x, invert, TRAVEL_X, SCREEN_WIDTH, dist_wall)
        else:
            read_values.reset_field(ball, player_key, com, visual)
            read_values.reset_values()
            run = False
            end_menu_run = True

        if invert:
            ball.rect.center = (ball.x+(dist_wall - TRAVEL_X), ball.y-TRAVEL_Y)
            visual.center = (ball.x+(dist_wall - TRAVEL_X), ball.y-TRAVEL_Y)
        else:
            ball.rect.center = (ball.x + TRAVEL_X, ball.y - TRAVEL_Y)
            visual.center = (ball.x + TRAVEL_X, ball.y - TRAVEL_Y)

        key = pygame.key.get_pressed()

        close_to_wall = 10

        PLAYER_MOVE_SPEED = 3
        if key[pygame.K_a] and player_key.x-close_to_wall > 0:
            player_key.rect.move_ip(-PLAYER_MOVE_SPEED, 0)
            player_key.x += -PLAYER_MOVE_SPEED
        elif key[pygame.K_d] and not player_key.rect.colliderect(NET.rect):
            player_key.rect.move_ip(PLAYER_MOVE_SPEED, 0)
            player_key.x += PLAYER_MOVE_SPEED
        elif key[pygame.K_q]:
            read_values.last_position(ball, com, player_key)
            read_values.update_values(TRAVEL_X, TRAVEL_Y, travelling, invert, ANGLE, strength,\
                                      dist_wall, current_time, start_time, TURN_ON)
            run = False
            main_menu_run = True

        if key[pygame.K_s]:
            key_s_held_time += clock.get_time()
        new_strength = choose_strength(key_s_held_time / 1000)
        bar_length = calculate_bar_length(key_s_held_time / 1000, 1.5, max_bar_length)
        draw_outer_box_and_bar(bar_length, max_bar_length)

        if not invert:
            ending_x = calculate_ending_x(ball.x, ball.y, ANGLE[strength], SPEED[strength], GRAVITY, com.y)
        if ending_x > SCREEN_WIDTH:
            ending_x = SCREEN_WIDTH - (ending_x - SCREEN_WIDTH)

        COM_MOVE_SPEED = 2
        if ANGLE == PLAYER_ANGLE:
            if com.x > ending_x-com.get_width()/2 and not com.rect.colliderect(NET.rect):
                com.rect.move_ip(-COM_MOVE_SPEED, 0)
                com.x += -COM_MOVE_SPEED
            if com.x < ending_x-com.get_width()/2 and com.x+close_to_wall < SCREEN_WIDTH-com.get_width():
                com.rect.move_ip(COM_MOVE_SPEED, 0)
                com.x += COM_MOVE_SPEED

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                read_values.last_position(ball,com,player_key)
                read_values.update_values(TRAVEL_X, TRAVEL_Y, travelling, invert, ANGLE, strength,\
                                          dist_wall, current_time, start_time, True)
                run = False

        pygame.display.flip()
        clock.tick(120)

    if main_menu_run:
        main_menu()
    if end_menu_run:
        end_menu()
    pygame.quit()


def end_menu():
    run = True
    play_run = False
    main_menu_run = False
    font = pygame.font.Font(None, 36)
    name_font = pygame.font.Font(None, 50)
    WHITE = (255, 255, 255)
    while run:
        draw_text("GAME ENDED", name_font, WHITE, SCREEN_WIDTH // 4, SCREEN_HEIGHT // 5)
        draw_text("Press r to play again", font, WHITE, SCREEN_WIDTH // 4, SCREEN_HEIGHT // 2)
        draw_text("Press q to leave", font, WHITE, SCREEN_WIDTH // 4, SCREEN_HEIGHT * 3 // 4)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    run = False
                    play_run = True
                if event.key == pygame.K_q:
                    run = False
                    main_menu_run = True

    if main_menu_run:
        main_menu()
    if play_run:
        play(play_run)
    pygame.quit()

def main_menu():

    pygame.init()

    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)

    font = pygame.font.Font(None, 36)
    name_font = pygame.font.Font(None, 50)

    play_run = False
    run = True
    while run:
        pygame.display.update()
        screen.fill(BLACK)
        draw_text("VOLLEY PONG", name_font, WHITE, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 5)
        draw_text("Main Menu", font, WHITE, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3)
        draw_text("Press SPACE to start", font, WHITE, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        draw_text("Press Q to quit", font, WHITE, SCREEN_WIDTH // 2, SCREEN_HEIGHT * 3 // 4)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                TURN_ON = True
                change_TURN_ON(TURN_ON)
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    run = False
                    play_run = True
                if event.key == pygame.K_q:
                    run = False
                    TURN_ON = True
                    change_TURN_ON(TURN_ON)

    if play_run:
        play(play_run)

    pygame.quit()

main_menu()

pygame.quit()