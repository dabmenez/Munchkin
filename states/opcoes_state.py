import pygame
from config import PRETO, BRANCO, CINZA, CINZA_ESCURO
from classes.slider import Slider
from classes.button_rect import ButtonRect

class OpcoesState:
    def __init__(self, game):
        self.game = game
        self.fonte = self.game.fonte

        self.center_x = self.game.base_width // 2

        # Resoluções disponíveis
        self.resolutions = [
            (800, 600),
            (1280, 720),
            (1920, 1080)
        ]

        # Pega resolução e volume atuais
        current_res = (self.game.largura, self.game.altura)
        if current_res in self.resolutions:
            self.temp_resolution_index = self.resolutions.index(current_res)
        else:
            self.temp_resolution_index = 1

        self.temp_volume = self.game.volume

        # Slider de volume
        self.slider_volume = Slider(self.center_x - 200, 300, 400, 20, initial_value=self.temp_volume)

        # Botões "Voltar" e "Aplicar"
        self.btn_voltar = ButtonRect(300, 500, 150, 50, "Voltar", self.fonte, CINZA, CINZA_ESCURO)
        self.btn_aplicar = ButtonRect(500, 500, 150, 50, "Aplicar", self.fonte, CINZA, CINZA_ESCURO)

        # Botões de resolução
        self.btn_res_esquerda = ButtonRect(self.center_x - 250, 400, 50, 50, "<", self.fonte, CINZA, CINZA_ESCURO)
        self.btn_res_direita = ButtonRect(self.center_x + 200, 400, 50, 50, ">", self.fonte, CINZA, CINZA_ESCURO)

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                self.game.estado = "SAIR"
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = pygame.mouse.get_pos()
                if self.btn_voltar.was_clicked(mx, my):
                    self.game.estado = "MENU"
                elif self.btn_aplicar.was_clicked(mx, my):
                    chosen_res = self.resolutions[self.temp_resolution_index]
                    chosen_vol = self.slider_volume.value
                    self.game.apply_changes(chosen_res, chosen_vol)
                    self.game.estado = "MENU"
                elif self.btn_res_esquerda.was_clicked(mx, my):
                    self.temp_resolution_index = (self.temp_resolution_index - 1) % len(self.resolutions)
                elif self.btn_res_direita.was_clicked(mx, my):
                    self.temp_resolution_index = (self.temp_resolution_index + 1) % len(self.resolutions)

    def update(self, dt):
        pass

    def draw(self):
        base_surf = self.game.base_surface
        base_surf.fill(PRETO)

        # 1) Desenha o título "Opções"
        title = self.fonte.render("Opções", True, BRANCO)
        # Centraliza no topo (x = center_x, y = 100)
        title_rect = title.get_rect(center=(self.center_x, 100))
        base_surf.blit(title, title_rect)

        # 2) Desenha o texto do volume
        volume_text = f"Volume: {self.slider_volume.value}"
        volume_surf = self.fonte.render(volume_text, True, BRANCO)
        volume_rect = volume_surf.get_rect(center=(self.center_x, 250))
        base_surf.blit(volume_surf, volume_rect)

        # 3) Desenha o slider
        self.slider_volume.draw(base_surf)

        # 4) Mostra a resolução selecionada
        w, h = self.resolutions[self.temp_resolution_index]
        res_text = f"{w} x {h}"
        res_surf = self.fonte.render(res_text, True, BRANCO)
        res_rect = res_surf.get_rect(center=(self.center_x, 375))
        base_surf.blit(res_surf, res_rect)

        # 5) Desenha os botões de navegação de resolução
        self.btn_res_esquerda.draw(base_surf)
        self.btn_res_direita.draw(base_surf)

        # 6) Desenha os botões "Voltar" e "Aplicar"
        self.btn_voltar.draw(base_surf)
        self.btn_aplicar.draw(base_surf)

