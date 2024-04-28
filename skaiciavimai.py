import pygame
import sys
from object_creation import screen

def draw_text(text, font, color, x, y):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.center = (x, y)
    screen.blit(text_surface, text_rect)

def main_menu():
    from main import play
    from read_values import SCREEN_WIDTH, SCREEN_HEIGHT

    pygame.init()

    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)

    font = pygame.font.Font(None, 36)


    play_run = False
    menu_ON = True
    while menu_ON:
        screen.fill(BLACK)
        draw_text("Main Menu", font, WHITE, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4)
        draw_text("Press SPACE to start", font, WHITE, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        draw_text("Press Q to quit", font, WHITE, SCREEN_WIDTH // 2, SCREEN_HEIGHT * 3 // 4)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                menu_ON = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    play_run = True
                    play(play_run)
                    print("Starting game...")
                if event.key == pygame.K_q:
                    menu_ON = False

main_menu()