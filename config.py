# config.py

import pygame

# ======== Caminhos de arquivos ========
BACKGROUND_IMG_PATH     = "assets/background.jpg"
TITLE_IMG_PATH          = "assets/title.png"
FONT_PATH               = "assets/fonts/comicsans.ttf"

BUTTON_PLAY_IMG         = "assets/buttons/play_button.png"
BUTTON_OPTIONS_IMG      = "assets/buttons/options_button.png"
BUTTON_EXIT_IMG         = "assets/buttons/exit_button.png"
BUTTON_LOGO_CHARACTER   = "assets/buttons/logo_character.png"  # agora junto dos botões

BACKGROUND_MUSIC_PATH   = "assets/sounds/background_music.mp3"
CLICK_SOUND_PATH        = "assets/sounds/click.wav"

# ======== Cores ========
BRANCO       = (255, 255, 255)
PRETO        = (0,   0,   0)
CINZA        = (100, 100, 100)
CINZA_ESCURO = (80,  80,  80)

# ======== Dimensões iniciais ========
INIT_WIDTH  = 1280  # ou outra largura
INIT_HEIGHT = 720   # ou outra altura


# ======== Função de Escala de Imagem ========
def scale_image(image, scale_factor):
    """Redimensiona (escalona) a imagem com base em um fator de escala."""
    w, h = image.get_size()
    new_w = int(w * scale_factor)
    new_h = int(h * scale_factor)
    return pygame.transform.scale(image, (new_w, new_h))
