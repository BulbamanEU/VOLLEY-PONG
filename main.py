import pygame
from ball_trajectory import calculate_trajectory
from bounce_values import update_ball
from ball_touch import net_touch, wall_touch
from object_creation import screen, ball, visual, player_key, player_mouse, com, NET
from read_values import SCREEN_HEIGHT, SCREEN_WIDTH, SPEED, COM_ANGLE, PLAYER_ANGLE,\
    GRAVITY
import read_values
import json
import math

#reikia padaryti kad kompas pats judetu iki kamuoliuko destination ir atmustu
#reikia padaryti input kokia jega atmusa ta kamuoliuka zaidejas *ideja pvz 3-5 jegu galimybes ir pagal tai kiek laiko laiko mygtuka, tokie nustatymai ir gaunasi, dopadown


def time_spent(func):
    def wrapper(*args, **kwargs):
        start_time = pygame.time.get_ticks() / 1000
        func(*args, **kwargs)
        end_time = pygame.time.get_ticks() / 1000
        elapsed_time = end_time - start_time
        return elapsed_time
    return wrapper

def change_TURN_ON(TURN_ON):
    with open('saved_values.json', 'r') as json_file:
        data = json.load(json_file)

    data["TURN_ON"] = TURN_ON

    with open('saved_values.json', 'w') as json_file:
        json.dump(data, json_file, indent=4)

def calculate_ending_x(start_x, start_y, angle_deg, speed, gravity, end_y):
    angle_rad = math.radians(angle_deg)

    Vx = speed * math.cos(angle_rad)
    Vy = speed * math.sin(angle_rad)

    t = (2 * Vy) / gravity

    dx = Vx * t


    end_x = start_x + dx

    return end_x

def calculate_bar_length(time_elapsed, max_time):
    max_bar_length = 400
    return min(max_bar_length, int(max_bar_length * (time_elapsed / max_time)))

def player_move(speed):
    player_key.rect.move_ip(speed, 0)
    player_key.x += speed
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
    elif time < 1:
        strength = 1
    elif time < 2:
        strength = 2
    elif time < 3:
        strength = 3
    elif time < 4:
        strength = 4

    return strength


def play(run):
    from object_creation import ball

    center_y = com.y + com.height/2

    pygame.init()

    offset = player_key.height + ball.height/2

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
        player_key.rect.center = (player_key.x+player_key.width/2, center_y)
        com.rect.center = (com.x+com.width/2, center_y)
        pause = 0
        read_values.reset_values("starting_position.json", "current_position.json")
        ball, visual.center, travelling, invert, TRAVEL_X, TRAVEL_Y, pause = update_ball(ball, offset)

    key_s_held_time = 0
    new_strength = 2
    bar_length = 0

    while run:


        screen.fill((0, 0, 0))
        NET.draw(screen)
        com.draw(screen)
        player_key.draw(screen)
        player_mouse.draw(screen)
        ball.draw(screen)
        visual.draw(screen)

        pos = pygame.mouse.get_pos()
        player_mouse.rect.center = pos

        if TURN_ON:
            start_time = pygame.time.get_ticks() / 1000
            TURN_ON = False

        if player_key.rect.colliderect(ball.rect) or player_mouse.rect.colliderect(ball.rect):
            start_time = pygame.time.get_ticks() / 1000
            current_coords(TRAVEL_X, TRAVEL_Y, invert, dist_wall)
            ANGLE = PLAYER_ANGLE
            strength = new_strength
            key_s_held_time = 0
            time_before_pause = 0
            ball, visual.center, travelling, invert, TRAVEL_X, TRAVEL_Y, pause = update_ball(ball, offset)


        if com.rect.colliderect(ball.rect) or player_mouse.rect.colliderect(ball.rect):
            start_time = pygame.time.get_ticks() / 1000
            current_coords(TRAVEL_X, TRAVEL_Y, invert, dist_wall)
            ANGLE = COM_ANGLE
            time_before_pause = 0
            ball, visual.center, travelling, invert, TRAVEL_X, TRAVEL_Y, pause = update_ball(ball, offset)


        if travelling:
            travelling = net_touch(ball, NET, TRAVEL_Y)
            current_time = pygame.time.get_ticks() / 1000
            current_time += time_before_pause - pause
            elapsed_time = current_time - start_time
            TRAVEL_X, TRAVEL_Y = calculate_trajectory(SPEED[strength], GRAVITY, ANGLE[strength], elapsed_time)
            invert, dist_wall = wall_touch(ball, invert, TRAVEL_X, SCREEN_WIDTH, dist_wall)
        else:
            read_values.reset_field(ball, player_key, com, visual)
            read_values.reset_values()
            end_menu()

        if invert:
            ball.rect.center = (ball.x+(dist_wall - TRAVEL_X), ball.y-TRAVEL_Y)
            visual.center = (ball.x+(dist_wall - TRAVEL_X), ball.y-TRAVEL_Y)
        else:
            ball.rect.center = (ball.x + TRAVEL_X, ball.y - TRAVEL_Y)
            visual.center = (ball.x + TRAVEL_X, ball.y - TRAVEL_Y)


        pygame.display.flip()
        key = pygame.key.get_pressed()

        PLAYER_MOVE_SPEED = 3
        if key[pygame.K_a] and player_key.x > 0:
            player_key.rect.move_ip(-PLAYER_MOVE_SPEED, 0)
            player_key.x += -PLAYER_MOVE_SPEED
        elif key[pygame.K_d] and not player_key.rect.colliderect(NET.rect):
            player_key.rect.move_ip(PLAYER_MOVE_SPEED, 0)
            player_key.x += PLAYER_MOVE_SPEED
        elif key[pygame.K_s]:
            key_s_held_time += clock.get_time()
            new_strength = choose_strength(key_s_held_time/1000)
            bar_length = calculate_bar_length(key_s_held_time/1000, 5)
        elif key[pygame.K_q]:
            #save values
            #save current_time, po to pause priskirta sitam value ir tada pause = current_time - pause
            read_values.last_position(ball, com, player_key)
            read_values.update_values(TRAVEL_X, TRAVEL_Y, travelling, invert, ANGLE, strength,\
                                      dist_wall, current_time, start_time, TURN_ON)
            main_menu()
        print(key_s_held_time)
        pygame.draw.rect(screen, (255, 255, 0), (50, 50, bar_length, 20))
        pygame.display.update()


        ending_x = calculate_ending_x(ball.x, ball.y, ANGLE[strength], SPEED[strength], GRAVITY, com.y + com.height/2)
        COM_MOVE_SPEED = 3
        if ANGLE == PLAYER_ANGLE:
            if ending_x > SCREEN_WIDTH:
                ending_x = SCREEN_WIDTH - (ending_x - SCREEN_WIDTH)
            if com.x > ending_x-com.width/2 and not com.rect.colliderect(NET.rect):
                com.rect.move_ip(-COM_MOVE_SPEED, 0)
                com.x += -COM_MOVE_SPEED
            elif com.x < ending_x-com.width/2 and com.x < SCREEN_WIDTH-com.width:
                com.rect.move_ip(COM_MOVE_SPEED, 0)
                com.x += COM_MOVE_SPEED


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                #save values
                read_values.last_position(ball,com,player_key)
                read_values.update_values(TRAVEL_X, TRAVEL_Y, travelling, invert, ANGLE, strength,\
                                          dist_wall, current_time, start_time, True)
                pygame.quit()


        pygame.display.flip()
        clock.tick(120)


def end_menu():
    run = True
    font = pygame.font.Font(None, 36)
    name_font = pygame.font.Font(None, 50)
    WHITE = (255, 255, 255)
    while run:
        #screen.fill((0, 0, 0))
        draw_text("GAME ENDED", name_font, WHITE, SCREEN_WIDTH // 4, SCREEN_HEIGHT // 5)
        draw_text("Press r to play again", font, WHITE, SCREEN_WIDTH // 4, SCREEN_HEIGHT // 2)
        draw_text("Press q to leave", font, WHITE, SCREEN_WIDTH // 4, SCREEN_HEIGHT * 3 // 4)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    play_run = True
                    play(play_run)
                if event.key == pygame.K_q:
                    main_menu()

#@time_spent
def main_menu():

    pygame.init()

    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)

    font = pygame.font.Font(None, 36)
    name_font = pygame.font.Font(None, 50)

    play_run = False
    menu_ON = True
    while menu_ON:
        pygame.display.update()
        screen.fill(BLACK)
        draw_text("VOLLEY PONG", name_font, WHITE, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 5)
        draw_text("Main Menu", font, WHITE, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3)
        draw_text("Press SPACE to start", font, WHITE, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        draw_text("Press Q to quit", font, WHITE, SCREEN_WIDTH // 2, SCREEN_HEIGHT * 3 // 4)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                #lol
                TURN_ON = True
                change_TURN_ON(TURN_ON)
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    play_run = True
                    play(play_run)
                if event.key == pygame.K_q:
                    #lol
                    TURN_ON = True
                    change_TURN_ON(TURN_ON)
                    pygame.quit()


main_menu()
#run = True
#play(run)
#pygame.quit()