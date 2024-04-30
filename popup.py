
import pygame

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

def create_popup(screen, message):
    popup_surface = pygame.Surface((400, 200))
    popup_surface.fill(WHITE)
    popup_rect = popup_surface.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2))

    from game import font
    text_surface = font.render(message, True, BLACK)
    text_rect = text_surface.get_rect(center=(popup_rect.width // 2, popup_rect.height // 2))

    popup_surface.blit(text_surface, text_rect)

    screen.blit(popup_surface, popup_rect)
    pygame.display.flip()