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
        self.game.screen.fill(PRETO)
        info_surf = self.game.fonte.render("Jogo rodando... (ESC para voltar)", True, BRANCO)
        info_rect = info_surf.get_rect(center=(self.game.largura//2, self.game.altura//2))
        self.game.screen.blit(info_surf, info_rect)
