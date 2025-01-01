import pygame

class ButtonImage:
    def __init__(self, x, y, image_surface):
        # Guardamos as coordenadas originais
        self.x = x
        self.y = y

        self.image_original = image_surface
        self.image = image_surface.copy()
        # Rect inicial na posição (x, y)
        self.rect = self.image.get_rect(topleft=(x, y))

        self.hovered = False

    def draw(self, surface):
        surface.blit(self.image, self.rect)

    def check_hover(self, mx, my):
        # Verifica se o mouse está sobre o botão
        if self.rect.collidepoint(mx, my):
            # Se ainda não estava em "hover", aumentar
            if not self.hovered:
                self.hovered = True
                # Salva o centro atual antes de redimensionar
                center_anterior = self.rect.center

                # Redimensiona a imagem
                new_width = int(self.image_original.get_width() * 1.1)
                new_height = int(self.image_original.get_height() * 1.1)
                self.image = pygame.transform.scale(self.image_original, (new_width, new_height))

                # Define o novo rect no mesmo centro que estava
                self.rect = self.image.get_rect(center=center_anterior)
        else:
            # Se o mouse saiu e estava em "hover", restaura
            if self.hovered:
                self.hovered = False
                # Volta à imagem original
                self.image = self.image_original
                # E volta à posição inicial (x, y)
                self.rect = self.image.get_rect(topleft=(self.x, self.y))

    def was_clicked(self, mx, my):
        return self.rect.collidepoint(mx, my)
