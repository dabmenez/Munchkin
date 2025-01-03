import pygame
from config import BRANCO

class ButtonRect:
    """
    Botão simples desenhado como retângulo.
    Usar coordenadas base para x,y,w,h.
    """
    def __init__(self, x, y, w, h, text, font, color_normal, color_hover):
        self.rect = pygame.Rect(x, y, w, h)
        self.text = text
        self.font = font
        self.color_normal = color_normal
        self.color_hover = color_hover
        self.current_color = color_normal

    def draw(self, surface_base):
        pygame.draw.rect(surface_base, self.current_color, self.rect, border_radius=6)
        # Texto centralizado no botão
        text_surf = self.font.render(self.text, True, BRANCO)
        text_rect = text_surf.get_rect(center=self.rect.center)
        surface_base.blit(text_surf, text_rect)

    def check_hover(self, mx_base, my_base):
        if self.rect.collidepoint(mx_base, my_base):
            self.current_color = self.color_hover
        else:
            self.current_color = self.color_normal

    def was_clicked(self, mx_base, my_base):
        return self.rect.collidepoint(mx_base, my_base)
