# classes/slider.py

import pygame

class Slider:
    """
    Slider para valor 0..100. 
    x,y,w,h => coords base (1280x720)
    """
    def __init__(self, x, y, w, h, initial_value=50):
        self.rect = pygame.Rect(x, y, w, h)
        self.value = initial_value
        self.dragging = False

        self.handle_radius = h // 2
        self.update_handle_x()

    def update_handle_x(self):
        pct = self.value / 100.0
        self.handle_x = self.rect.x + int(pct * self.rect.width)

    def handle_event(self, event, mx_base, my_base):
        """
        Recebe as coords base do mouse, 
        para arrastar o handle.
        """
        if event.type == pygame.MOUSEBUTTONDOWN:
            if (mx_base - self.handle_x)**2 + (my_base - self.rect.centery)**2 <= self.handle_radius**2:
                self.dragging = True

        elif event.type == pygame.MOUSEBUTTONUP:
            self.dragging = False

        elif event.type == pygame.MOUSEMOTION and self.dragging:
            # Move handle
            if mx_base < self.rect.x:
                mx_base = self.rect.x
            if mx_base > self.rect.right:
                mx_base = self.rect.right

            # Recalcula valor
            dist = mx_base - self.rect.x
            pct = dist / self.rect.width
            self.value = int(pct * 100)
            self.update_handle_x()

    def draw(self, surface_base):
        # barra
        pygame.draw.rect(surface_base, (180,180,180), self.rect)
        # handle
        pygame.draw.circle(surface_base, (255,50,50), (self.handle_x, self.rect.centery), self.handle_radius)
