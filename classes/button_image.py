# classes/button_image.py

import pygame

class ButtonImage:
    """
    Botão que usa uma imagem e um Rect baseado na RESOLUÇÃO BASE.
    Quando for checar clique, você deve converter o mouse (x,y)
    para coordenadas base antes de chamar was_clicked(...).
    """
    def __init__(self, x, y, image_surface):
        """
        x, y: coordenadas na resolução base (1280x720)
        image_surface: pygame.Surface já carregada/escalada
        """
        self.image = image_surface
        self.rect = self.image.get_rect(topleft=(x, y))
        self.hovered = False

        # Guardamos a versão original para escurecer no hover
        self.image_original = self.image.copy()

    def draw(self, surface_base):
        surface_base.blit(self.image, self.rect)

    def check_hover(self, mx_base, my_base):
        """Se o mouse (convertido p/ base) estiver sobre o botão, escurece."""
        if self.rect.collidepoint(mx_base, my_base):
            if not self.hovered:
                self.hovered = True
                darker = self.image_original.copy()
                darker.fill((150,150,150,50), special_flags=pygame.BLEND_RGBA_MULT)
                self.image = darker
        else:
            if self.hovered:
                self.hovered = False
                self.image = self.image_original.copy()

    def was_clicked(self, mx_base, my_base):
        """Retorna True se o mouse base colide com o rect."""
        return self.rect.collidepoint(mx_base, my_base)
