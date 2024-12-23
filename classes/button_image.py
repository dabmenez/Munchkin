# classes/button_image.py

import pygame

class ButtonImage:
    """
    Botão que utiliza uma imagem para desenhar e detectar cliques.
    Pode exibir um 'hover' escurecendo a imagem.
    """
    def __init__(self, image_surface, x, y):
        """
        :param image_surface: objeto pygame.Surface já carregado/escalado
        :param x, y: posição (topleft) onde o botão será desenhado
        """
        self.image_original = image_surface
        self.image = self.image_original.copy()
        self.rect = self.image.get_rect(topleft=(x, y))
        self.hovered = False

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def check_hover(self, mouse_pos):
        """Escurece a imagem levemente se o mouse estiver sobre o botão."""
        if self.rect.collidepoint(mouse_pos):
            if not self.hovered:
                self.hovered = True
                darker_img = self.image_original.copy()
                darker_img.fill((150, 150, 150, 50), special_flags=pygame.BLEND_RGBA_MULT)
                self.image = darker_img
        else:
            if self.hovered:
                self.hovered = False
                self.image = self.image_original.copy()

    def was_clicked(self, mouse_pos):
        """Retorna True se o botão foi clicado."""
        return self.rect.collidepoint(mouse_pos)
