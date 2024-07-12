import pygame
import math

def get_user_input(prompt, screen, font, back_button, next_button, quit_button, show_back_button, buttons=None):
    color_inactive = pygame.Color('lightskyblue3')
    color_active = pygame.Color('dodgerblue2')
    color = color_inactive
    active = False
    text = ''
    done = False
    next_screen = False
    prev_screen = False
    quit_program = False

    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if next_button.collidepoint(event.pos):
                    next_screen = True
                    done = True
                if show_back_button and back_button.collidepoint(event.pos):
                    prev_screen = True
                    done = True
                if quit_button.collidepoint(event.pos):
                    quit_program = True
                    done = True
                if buttons:
                    for button_text, button_rect in buttons:
                        if button_rect.collidepoint(event.pos):
                            text = button_text
                            done = True
            if event.type == pygame.KEYDOWN and not buttons:
                if event.key == pygame.K_RETURN:
                    done = True
                elif event.key == pygame.K_BACKSPACE:
                    text = text[:-1]
                else:
                    text += event.unicode

        screen.fill((30, 30, 30))

        if show_back_button:
            back_text = font.render("Zurück", True, pygame.Color('white'))
            pygame.draw.rect(screen, pygame.Color('white'), back_button, 2)
            screen.blit(back_text, (back_button.x + 10, back_button.y + 5))

        next_text = font.render("Weiter", True, pygame.Color('white'))
        quit_text = font.render("Beenden", True, pygame.Color('white'))
        prompt_text = font.render(prompt, True, pygame.Color('white'))

        screen.blit(next_text, (next_button.x + 10, next_button.y + 5))
        screen.blit(quit_text, (quit_button.x + 10, quit_button.y + 5))
        screen.blit(prompt_text, (screen.get_width() / 2 - prompt_text.get_width() / 2, 20))
        pygame.draw.rect(screen, pygame.Color('white'), next_button, 2)
        pygame.draw.rect(screen, pygame.Color('white'), quit_button, 2)

        if buttons:
            for button_text, button_rect in buttons:
                button_text_surface = font.render(button_text, True, pygame.Color('white'))
                pygame.draw.rect(screen, pygame.Color('white'), button_rect, 2)
                screen.blit(button_text_surface, (button_rect.x + 10, button_rect.y + 5))
        else:
            input_box = pygame.Rect(100, 150, 140, 32)
            txt_surface = font.render(prompt + text, True, color)
            width = max(200, txt_surface.get_width() + 10)
            input_box.w = width
            input_box.center = screen.get_rect().center
            screen.blit(txt_surface, (input_box.x + 5, input_box.y + 5))
            pygame.draw.rect(screen, color, input_box, 2)

        pygame.display.flip()

    return text, next_screen, prev_screen, quit_program

