# states/menu_state.py

import pygame
from config import (
    BACKGROUND_IMG_PATH, TITLE_IMG_PATH,
    BUTTON_PLAY_IMG, BUTTON_OPTIONS_IMG, BUTTON_EXIT_IMG, BUTTON_LOGO_CHARACTER,
    scale_image
)
from classes.button_image import ButtonImage

class MenuState:
    def __init__(self, game):
        self.game = game

        # Carrega o background e título
        self.bg_image_original = pygame.image.load(BACKGROUND_IMG_PATH).convert()
        
        # Carrega o título e REDUZ um pouco mais
        raw_title = pygame.image.load(TITLE_IMG_PATH).convert_alpha()
        self.title_image_original = scale_image(raw_title, 0.6)  # Ajuste esse 0.6 conforme desejar

        # Carrega botões e logo
        play_img    = pygame.image.load(BUTTON_PLAY_IMG).convert_alpha()
        options_img = pygame.image.load(BUTTON_OPTIONS_IMG).convert_alpha()
        exit_img    = pygame.image.load(BUTTON_EXIT_IMG).convert_alpha()
        logo_img    = pygame.image.load(BUTTON_LOGO_CHARACTER).convert_alpha()

        # Escala tudo para ficar menor (ajuste conforme desejar)
        play_img    = scale_image(play_img,    0.4)
        options_img = scale_image(options_img, 0.4)
        exit_img    = scale_image(exit_img,    0.4)
        logo_img    = scale_image(logo_img,    0.4)

        # ====== POSICIONAMENTO ======
        # Título (desenharemos centralizado no draw, sem “botão”)
        
        # Botões: queremos deixá-los à ESQUERDA.
        # Exemplo: x=100 (ou algo próximo)
        # E espaçados no eixo Y para não ficarem colados
        self.btn_jogar = ButtonImage(
            play_img,
            x=100,
            y=300
        )
        self.btn_opcoes = ButtonImage(
            options_img,
            x=100,
            y=420
        )
        self.btn_sair = ButtonImage(
            exit_img,
            x=100,
            y=540
        )

        # Logo do personagem: queremos na DIREITA.
        # Para posicionar na direita, podemos calcular:
        # x = (largura_da_tela - largura_da_imagem - uma margem)
        screen_w = self.game.largura
        logo_rect = logo_img.get_rect()
        x_logo = screen_w - logo_rect.width - 50  # 50 de margem
        y_logo = 300  # ajuste como quiser (ou alinhe verticalmente a algo)

        self.btn_logo = ButtonImage(
            logo_img,
            x=x_logo,
            y=y_logo
        )

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                self.game.estado = "SAIR"

            elif event.type == pygame.MOUSEMOTION:
                mouse_pos = event.pos
                self.btn_jogar.check_hover(mouse_pos)
                self.btn_opcoes.check_hover(mouse_pos)
                self.btn_sair.check_hover(mouse_pos)

            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                # Se quiser som de clique:
                self.game.click_sound.play()

                if self.btn_jogar.was_clicked(mouse_pos):
                    self.game.estado = "JOGAR"
                elif self.btn_opcoes.was_clicked(mouse_pos):
                    self.game.estado = "OPCOES"
                elif self.btn_sair.was_clicked(mouse_pos):
                    self.game.estado = "SAIR"
    def update(self, dt):
        pass

    def draw(self):
        # Desenha fundo ajustado ao tamanho da janela
        bg_scaled = pygame.transform.scale(
            self.bg_image_original, 
            (self.game.largura, self.game.altura)
        )
        self.game.screen.blit(bg_scaled, (0, 0))

        # Desenha TÍTULO centralizado no topo
        title_rect = self.title_image_original.get_rect(
            center=(self.game.largura // 2, 100)
        )
        self.game.screen.blit(self.title_image_original, title_rect)

        # Desenha botões (na esquerda)
        self.btn_jogar.draw(self.game.screen)
        self.btn_opcoes.draw(self.game.screen)
        self.btn_sair.draw(self.game.screen)

        # Desenha logo (na direita)
        self.btn_logo.draw(self.game.screen)
