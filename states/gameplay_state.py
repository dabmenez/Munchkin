# states/gameplay_state.py

import pygame
from config import PRETO, BRANCO

class GameplayState:
    def __init__(self, game):
        self.game = game

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                self.game.estado = "SAIR"
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.game.estado = "MENU"

    def update(self, dt):
        pass

    def draw(self):
        base_surf = self.game.base_surface
        base_surf.fill(PRETO)

        # Texto central
        text_surf = self.game.fonte.render("Tela de Jogo - Pressione ESC para voltar", True, BRANCO)
        text_rect = text_surf.get_rect(center=(640, 360))  # Centro da base (1280x720)
        base_surf.blit(text_surf, text_rect)
