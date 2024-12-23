# states/menu_state.py

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
        self.bg_original    = pygame.image.load(BACKGROUND_IMG_PATH).convert()
        self.title_original = pygame.image.load(TITLE_IMG_PATH).convert_alpha()

        # Escala as imagens para garantir que não fiquem muito grandes
        self.bg_original    = scale_image(self.bg_original, 0.8)  # Ajuste conforme necessário
        self.title_original = scale_image(self.title_original, 0.5)  # Ajuste conforme necessário

        # Carrega botões de imagem
        play_img    = pygame.image.load(BUTTON_PLAY_IMG).convert_alpha()
        options_img = pygame.image.load(BUTTON_OPTIONS_IMG).convert_alpha()
        exit_img    = pygame.image.load(BUTTON_EXIT_IMG).convert_alpha()
        logo_img    = pygame.image.load(BUTTON_LOGO_CHARACTER).convert_alpha()

        # Escala os botões
        play_img    = scale_image(play_img,    0.4)
        options_img = scale_image(options_img, 0.4)
        exit_img    = scale_image(exit_img,    0.4)
        logo_img    = scale_image(logo_img,    0.3)

        # Posições base (1280x720)
        # Título no topo centralizado
        self.title_rect_base = self.title_original.get_rect(center=(640, 100))

        # Botões alinhados à esquerda
        self.btn_jogar   = ButtonImage(100, 250, play_img)
        self.btn_opcoes  = ButtonImage(100, 350, options_img)
        self.btn_sair    = ButtonImage(100, 450, exit_img)

        # Logo do personagem alinhada à direita
        # Calcula a posição x baseada na largura da base e largura da imagem
        logo_width = logo_img.get_width()
        x_logo = self.game.base_width - logo_width - 100  # 100 pixels de margem à direita
        self.btn_logo = ButtonImage(x_logo, 250, logo_img)

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                self.game.estado = "SAIR"
            elif event.type == pygame.MOUSEMOTION:
                # Converte coord real -> base
                mx_real, my_real = event.pos
                mx_base = int(mx_real * self.game.base_width  / self.game.largura)
                my_base = int(my_real * self.game.base_height / self.game.altura)

                self.btn_jogar.check_hover(mx_base, my_base)
                self.btn_opcoes.check_hover(mx_base, my_base)
                self.btn_sair.check_hover(mx_base, my_base)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mx_real, my_real = event.pos
                mx_base = int(mx_real * self.game.base_width  / self.game.largura)
                my_base = int(my_real * self.game.base_height / self.game.altura)

                self.game.click_sound.play()

                if self.btn_jogar.was_clicked(mx_base, my_base):
                    self.game.estado = "JOGAR"
                elif self.btn_opcoes.was_clicked(mx_base, my_base):
                    self.game.estado = "OPCOES"
                elif self.btn_sair.was_clicked(mx_base, my_base):
                    self.game.estado = "SAIR"

    def update(self, dt):
        pass

    def draw(self):
        # Desenhar no self.game.base_surface
        base_surf = self.game.base_surface

        # Fundo escalado para 1280x720
        bg_scaled = pygame.transform.scale(self.bg_original, (self.game.base_width, self.game.base_height))
        base_surf.blit(bg_scaled, (0, 0))

        # Título
        base_surf.blit(self.title_original, self.title_rect_base)

        # Botões
        self.btn_jogar.draw(base_surf)
        self.btn_opcoes.draw(base_surf)
        self.btn_sair.draw(base_surf)

        # Logo do personagem
        self.btn_logo.draw(base_surf)
