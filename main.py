# main.py

import pygame
import sys

from config import (
    FONT_PATH, INIT_WIDTH, INIT_HEIGHT,
    BACKGROUND_MUSIC_PATH, CLICK_SOUND_PATH
)
from states.menu_state import MenuState
from states.opcoes_state import OpcoesState
from states.gameplay_state import GameplayState

class Game:
    def __init__(self):
        pygame.init()
        # Inicializa áudio
        pygame.mixer.init()

        pygame.display.set_caption("Menu do Jogo - Exemplo")

        self.largura = INIT_WIDTH
        self.altura = INIT_HEIGHT
        self.screen = pygame.display.set_mode((self.largura, self.altura))
        self.clock = pygame.time.Clock()
        self.running = True

        # Estado do jogo: MENU, OPCOES, JOGAR, SAIR
        self.estado = "MENU"

        # Carrega a fonte
        self.fonte = pygame.font.Font(FONT_PATH, 40)

        # ========== Música de fundo ==========
        pygame.mixer.music.load(BACKGROUND_MUSIC_PATH)
        pygame.mixer.music.play(-1)  # loop infinito

        # ========== Som de clique ==========
        self.click_sound = pygame.mixer.Sound(CLICK_SOUND_PATH)

        # ========== Cria instâncias dos estados ==========
        self.menu_state     = MenuState(self)
        self.opcoes_state   = OpcoesState(self)
        self.gameplay_state = GameplayState(self)

    def run(self):
        while self.running:
            dt = self.clock.tick(60) / 1000.0  # delta time em segundos
            events = pygame.event.get()

            # Verifica estado e delega
            if self.estado == "MENU":
                self.menu_state.handle_events(events)
                self.menu_state.update(dt)
                self.menu_state.draw()
            elif self.estado == "OPCOES":
                self.opcoes_state.handle_events(events)
                self.opcoes_state.update(dt)
                self.opcoes_state.draw()
            elif self.estado == "JOGAR":
                self.gameplay_state.handle_events(events)
                self.gameplay_state.update(dt)
                self.gameplay_state.draw()
            elif self.estado == "SAIR":
                self.running = False

            pygame.display.flip()

        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    game = Game()
    game.run()
