import pygame
from config import (
    BACKGROUND_IMG_PATH, TITLE_IMG_PATH,
    BUTTON_PLAY_IMG, BUTTON_OPTIONS_IMG, BUTTON_EXIT_IMG, BUTTON_LOGO_CHARACTER,
    scale_image, PRETO
)
from classes.button_image import ButtonImage


class MenuState:
    def __init__(self, game):
        self.game = game

        # Carrega imagens de fundo e título
        self.bg_original = pygame.image.load(BACKGROUND_IMG_PATH).convert()
        self.title_original = pygame.image.load(TITLE_IMG_PATH).convert_alpha()

        # Escala as imagens
        self.bg_original = scale_image(self.bg_original, 1.5)
        self.title_original = scale_image(self.title_original, 1)

        # Botões
        play_img = scale_image(pygame.image.load(BUTTON_PLAY_IMG).convert_alpha(), 0.6)
        options_img = scale_image(pygame.image.load(BUTTON_OPTIONS_IMG).convert_alpha(), 0.6)
        exit_img = scale_image(pygame.image.load(BUTTON_EXIT_IMG).convert_alpha(), 0.6)
        logo_img = scale_image(pygame.image.load(BUTTON_LOGO_CHARACTER).convert_alpha(), 0.8)

        # Título no topo centralizado
        self.title_rect = self.title_original.get_rect(center=(self.game.base_width // 2, 100))

        # Botões alinhados à esquerda
        self.btn_jogar = ButtonImage(100, 300, play_img)
        self.btn_opcoes = ButtonImage(100, 450, options_img)
        self.btn_sair = ButtonImage(100, 600, exit_img)

        # Logo do personagem alinhado ao centro-direita
        logo_width = logo_img.get_width()
        x_logo = self.game.base_width - logo_width - 100
        y_logo = self.game.base_height // 2 - logo_img.get_height() // 2
        self.btn_logo = ButtonImage(x_logo, y_logo, logo_img)

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                self.game.estado = "SAIR"
            elif event.type == pygame.MOUSEMOTION:
                mx, my = pygame.mouse.get_pos()
                self.btn_jogar.check_hover(mx, my)
                self.btn_opcoes.check_hover(mx, my)
                self.btn_sair.check_hover(mx, my)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = pygame.mouse.get_pos()
                if self.btn_jogar.was_clicked(mx, my):
                    self.game.estado = "JOGAR"
                elif self.btn_opcoes.was_clicked(mx, my):
                    self.game.estado = "OPCOES"
                elif self.btn_sair.was_clicked(mx, my):
                    self.game.estado = "SAIR"

    def update(self, dt):
        pass

    def draw(self):
        base_surf = self.game.base_surface
        base_surf.blit(self.bg_original, (0, 0))
        base_surf.blit(self.title_original, self.title_rect)
        self.btn_jogar.draw(base_surf)
        self.btn_opcoes.draw(base_surf)
        self.btn_sair.draw(base_surf)
        self.btn_logo.draw(base_surf)
