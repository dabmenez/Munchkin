import os
import sys
import pygame

# Base path para localizar arquivos, considerando execução normal e executável
BASE_PATH = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))

# Caminhos ajustados
BACKGROUND_IMG_PATH     = os.path.join(BASE_PATH, "assets/background.jpg")
TITLE_IMG_PATH          = os.path.join(BASE_PATH, "assets/title.png")
BUTTON_PLAY_IMG         = os.path.join(BASE_PATH, "assets/buttons/play_button.png")
BUTTON_OPTIONS_IMG      = os.path.join(BASE_PATH, "assets/buttons/options_button.png")
BUTTON_EXIT_IMG         = os.path.join(BASE_PATH, "assets/buttons/exit_button.png")
BUTTON_LOGO_CHARACTER   = os.path.join(BASE_PATH, "assets/buttons/logo_character.png")

BACKGROUND_MUSIC        = os.path.join(BASE_PATH, "assets/sounds/background_music.mp3")
CLICK_SOUND_PATH        = os.path.join(BASE_PATH, "assets/sounds/click.wav")
FONT_PATH               = os.path.join(BASE_PATH, "assets/fonts/comicsans.ttf")

# ======== Cores ========
BRANCO       = (255, 255, 255)
PRETO        = (0,   0,   0)
CINZA        = (100, 100, 100)
CINZA_ESCURO = (80,  80,  80)

# ======== Resolução Base ========
BASE_WIDTH  = 1920
BASE_HEIGHT = 1080

# ======== Função de Escala de Imagem ========
def scale_image(image, factor):
    """Redimensiona (escalona) a imagem com base em um fator de escala."""
    w, h = image.get_size()
    new_w = int(w * factor)
    new_h = int(h * factor)
    return pygame.transform.scale(image, (new_w, new_h))
