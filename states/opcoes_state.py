# states/opcoes_state.py

import pygame
from config import BRANCO, PRETO

class OpcoesState:
    def __init__(self, game):
        self.game = game
        self.fonte = self.game.fonte

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                self.game.estado = "SAIR"
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Toca som de clique
                self.game.click_sound.play()
                # Volta ao menu
                self.game.estado = "MENU"

    def update(self, dt):
        pass

    def draw(self):
        self.game.screen.fill(PRETO)
        text_surf = self.fonte.render("Tela de Opções (clique para voltar)", True, BRANCO)
        text_rect = text_surf.get_rect(center=(self.game.largura//2, self.game.altura//2))
        self.game.screen.blit(text_surf, text_rect)
