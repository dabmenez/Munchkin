# states/opcoes_state.py

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
            (1366, 768)
        ]

        # Pega resolução e volume atuais
        current_res = (self.game.largura, self.game.altura)
        if current_res in self.resolutions:
            self.temp_resolution_index = self.resolutions.index(current_res)
        else:
            self.temp_resolution_index = 1  # Default para 1280x720

        self.temp_volume = self.game.volume

        # Slider de volume
        slider_width  = 400
        slider_height = 20
        slider_x = self.center_x - slider_width // 2
        slider_y = 270

        self.slider_volume = Slider(slider_x, slider_y, slider_width, slider_height, initial_value=self.temp_volume)

        # Botões "Voltar" e "Aplicar"
        btn_w = 150
        btn_h = 50
        spacing = 40

        total_w = btn_w * 2 + spacing
        start_x = self.center_x - total_w // 2

        btn_y = 500

        self.btn_voltar = ButtonRect(
            start_x, btn_y, btn_w, btn_h,
            "Voltar", self.fonte, CINZA, CINZA_ESCURO
        )
        self.btn_aplicar = ButtonRect(
            start_x + btn_w + spacing, btn_y, btn_w, btn_h,
            "Aplicar", self.fonte, CINZA, CINZA_ESCURO
        )

        # Botões de resolução
        arrow_w = 50
        arrow_h = 50

        self.btn_res_esquerda = ButtonRect(
            x=self.center_x - 200,  # 100 pixels à esquerda do centro
            y=350,
            w=arrow_w, h=arrow_h,
            text="<", font=self.fonte,
            color_normal=CINZA, color_hover=CINZA_ESCURO
        )
        self.btn_res_direita  = ButtonRect(
            x=self.center_x + 150,  # 50 pixels à direita do centro
            y=350,
            w=arrow_w, h=arrow_h,
            text=">", font=self.fonte,
            color_normal=CINZA, color_hover=CINZA_ESCURO
        )

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                self.game.estado = "SAIR"
            elif event.type == pygame.MOUSEMOTION:
                # Converte coord real -> base
                mx_real, my_real = event.pos
                mx_base = int(mx_real * self.game.base_width  / self.game.largura)
                my_base = int(my_real * self.game.base_height / self.game.altura)

                self.btn_voltar.check_hover(mx_base, my_base)
                self.btn_aplicar.check_hover(mx_base, my_base)
                self.btn_res_esquerda.check_hover(mx_base, my_base)
                self.btn_res_direita.check_hover(mx_base, my_base)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mx_real, my_real = event.pos
                mx_base = int(mx_real * self.game.base_width  / self.game.largura)
                my_base = int(my_real * self.game.base_height / self.game.altura)

                self.game.click_sound.play()

                if self.btn_voltar.was_clicked(mx_base, my_base):
                    self.game.estado = "MENU"
                elif self.btn_aplicar.was_clicked(mx_base, my_base):
                    chosen_res = self.resolutions[self.temp_resolution_index]
                    chosen_vol = self.slider_volume.value
                    self.game.apply_changes(chosen_res, chosen_vol)
                    self.game.estado = "MENU"
                elif self.btn_res_esquerda.was_clicked(mx_base, my_base):
                    self.temp_resolution_index -= 1
                    if self.temp_resolution_index < 0:
                        self.temp_resolution_index = len(self.resolutions) - 1
                elif self.btn_res_direita.was_clicked(mx_base, my_base):
                    self.temp_resolution_index += 1
                    if self.temp_resolution_index >= len(self.resolutions):
                        self.temp_resolution_index = 0

            # Passa eventos para o slider
            if event.type in (pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP, pygame.MOUSEMOTION):
                mx_real, my_real = pygame.mouse.get_pos()
                mx_base = int(mx_real * self.game.base_width  / self.game.largura)
                my_base = int(my_real * self.game.base_height / self.game.altura)
                self.slider_volume.handle_event(event, mx_base, my_base)

    def update(self, dt):
        # Atualiza volume temporário conforme slider
        self.temp_volume = self.slider_volume.value

    def draw(self):
        base_surf = self.game.base_surface
        base_surf.fill(PRETO)

        # ---------- TÍTULO "OPÇÕES" ----------
        titulo_surf = self.fonte.render("Opções", True, BRANCO)
        titulo_rect = titulo_surf.get_rect(center=(self.center_x, 100))
        base_surf.blit(titulo_surf, titulo_rect)

        # ---------- VOLUME ----------
        volume_text = f"Volume: {self.temp_volume}"
        vol_surf = self.fonte.render(volume_text, True, BRANCO)
        vol_rect = vol_surf.get_rect(midbottom=(self.center_x, 250))
        base_surf.blit(vol_surf, vol_rect)

        self.slider_volume.draw(base_surf)

        # ---------- RESOLUÇÃO ----------
        current_res = self.resolutions[self.temp_resolution_index]
        res_text = f"{current_res[0]} x {current_res[1]}"
        res_surf = self.fonte.render(res_text, True, BRANCO)
        res_rect = res_surf.get_rect(center=(self.center_x, 375))
        base_surf.blit(res_surf, res_rect)

        self.btn_res_esquerda.draw(base_surf)
        self.btn_res_direita.draw(base_surf)

        # ---------- BOTÕES VOLTAR / APLICAR ----------
        self.btn_voltar.draw(base_surf)
        self.btn_aplicar.draw(base_surf)
