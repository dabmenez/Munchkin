import pygame
import sys
import os

# Inicialização do Pygame
pygame.init()

# Configurações da Tela
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Munchkin Digital - Tela Inicial")

# Cores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# FPS
FPS = 60
CLOCK = pygame.time.Clock()

# Carregamento de Fontes
FONT_PATH = os.path.join("assets", "fonts", "comicsans.ttf")
if os.path.exists(FONT_PATH):
    FONT = pygame.font.Font(FONT_PATH, 40)
else:
    FONT = pygame.font.SysFont('Arial', 40)

# Função para carregar imagens
def load_image(path, size=None):
    try:
        image = pygame.image.load(path).convert_alpha()
        if size:
            image = pygame.transform.scale(image, size)
        return image
    except pygame.error as e:
        print(f"Erro ao carregar a imagem {path}: {e}")
        return None

# Função para carregar sons
def load_sound(path):
    if os.path.exists(path):
        try:
            return pygame.mixer.Sound(path)
        except pygame.error as e:
            print(f"Erro ao carregar o som {path}: {e}")
            return None
    else:
        print(f"Som não encontrado: {path}")
        return None

# Carregamento de Imagens
BACKGROUND = load_image(os.path.join("assets", "background.jpg"), (SCREEN_WIDTH, SCREEN_HEIGHT))
TITLE = load_image(os.path.join("assets", "title.png"), (450, 250))  # Ajuste o tamanho conforme necessário
LOGO_CHARACTER = load_image(os.path.join("assets", "images", "logo_character.png"), (300, 300))  # Tamanho ajustável

# Carregamento de Sons
CLICK_SOUND = load_sound(os.path.join("assets", "sounds", "click.wav"))

# Opcional: Carregamento e reprodução da música de fundo
def load_music(path):
    if os.path.exists(path):
        try:
            pygame.mixer.music.load(path)
            pygame.mixer.music.set_volume(0.5)
            pygame.mixer.music.play(-1)  # Loop infinito
        except pygame.error as e:
            print(f"Erro ao carregar a música {path}: {e}")
    else:
        print(f"Música de fundo não encontrada: {path}")

# Chame a função para carregar a música de fundo, se desejar
load_music(os.path.join("assets", "sounds", "background_music.mp3"))

# Classe para Botões com Efeito de Hover (Escala)
class ImageButton:
    def __init__(self, image_path, pos, scale=1.0, scale_factor=1.02):
        self.image_path = image_path  # Identifica o botão nos prints
        self.image = load_image(image_path) if image_path else None
        if self.image:
            # Aplicar o scale inicial
            width = int(self.image.get_width() * scale)
            height = int(self.image.get_height() * scale)
            self.original_image = pygame.transform.scale(self.image, (width, height))
            print(f"{image_path} redimensionado para {self.original_image.get_size()}")

            # Criar a imagem escalada para o efeito de hover
            scaled_width = int(width * scale_factor)
            scaled_height = int(height * scale_factor)
            self.scaled_image = pygame.transform.scale(self.original_image, (scaled_width, scaled_height))
            print(f"{image_path} escalado para hover: {self.scaled_image.get_size()}")

            self.current_image = self.original_image
            self.rect = self.current_image.get_rect(center=pos)
        else:
            # Fallback para retângulo padrão caso a imagem falhe ou não seja fornecida
            self.original_image = None
            self.scaled_image = None
            self.current_image = None
            self.rect = pygame.Rect(0, 0, 150, 45)  # Tamanho reduzido
            self.rect.center = pos
            print(f"Botão fallback criado na posição {pos}")

        self.scale_factor = scale_factor
        self.pos = pos
        self.hovered = False

    def draw(self, surface, mouse_pos):
        # Verificar se o mouse está sobre o botão
        if self.rect.collidepoint(mouse_pos):
            if not self.hovered:
                self.hovered = True
                if self.scaled_image:
                    self.current_image = self.scaled_image
                    self.rect = self.current_image.get_rect(center=self.pos)
        else:
            if self.hovered:
                self.hovered = False
                if self.original_image:
                    self.current_image = self.original_image
                    self.rect = self.current_image.get_rect(center=self.pos)

        # Desenhar a imagem atual
        if self.current_image:
            surface.blit(self.current_image, self.rect)
        else:
            # Desenhar retângulo de fallback
            pygame.draw.rect(surface, BLACK, self.rect, border_radius=12)
            text_surf = FONT.render("Button", True, WHITE)
            text_rect = text_surf.get_rect(center=self.rect.center)
            surface.blit(text_surf, text_rect)

    def is_clicked(self, pos):
        clicked = self.rect.collidepoint(pos)
        print(f"Verificando clique no botão {self.image_path if self.image else 'Fallback'}: {clicked} | Posição do clique: {pos} | Retângulo do botão: {self.rect}")
        return clicked

# Função para exibir o título
def draw_title(surface):
    if TITLE:
        title_rect = TITLE.get_rect(center=(SCREEN_WIDTH//2, 100))
        surface.blit(TITLE, title_rect)
    else:
        # Fallback para desenhar texto se a imagem do título não estiver disponível
        title_text = FONT.render("Munchkin Digital", True, WHITE)
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH//2, 100))
        surface.blit(title_text, title_rect)

# Função para exibir o personagem da logo
def draw_logo_character(surface, logo_y):
    if LOGO_CHARACTER:
        # Ajuste a posição X para mover mais para a esquerda
        logo_x = SCREEN_WIDTH - LOGO_CHARACTER.get_width() - 100  # Ajuste conforme necessário

        # Use o valor Y fornecido para ajustar a altura
        logo_rect = LOGO_CHARACTER.get_rect(midleft=(logo_x, logo_y+190))
        surface.blit(LOGO_CHARACTER, logo_rect)
    else:
        # Fallback para desenhar um círculo se a imagem do personagem não estiver disponível
        pygame.draw.circle(surface, WHITE, (SCREEN_WIDTH - 150, logo_y), 75)
        # Adicionar texto ou outro feedback visual
        text_surf = FONT.render("Logo", True, BLACK)
        text_rect = text_surf.get_rect(center=(SCREEN_WIDTH - 150, logo_y))
        surface.blit(text_surf, text_rect)

# Função para adicionar efeito de fade-in
def fade_in(surface, background, logo_y, duration=1000):
    fade = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    fade.fill((0, 0, 0))
    fade.set_alpha(255)
    surface.blit(background, (0, 0))
    if LOGO_CHARACTER:
        logo_x = SCREEN_WIDTH - LOGO_CHARACTER.get_width() - 100  # Igual ao draw_logo_character
        surface.blit(LOGO_CHARACTER, LOGO_CHARACTER.get_rect(midleft=(logo_x, logo_y)))
    surface.blit(fade, (0, 0))
    pygame.display.flip()
    for alpha in range(255, -1, -5):
        fade.set_alpha(alpha)
        surface.blit(background, (0, 0))
        if LOGO_CHARACTER:
            surface.blit(LOGO_CHARACTER, LOGO_CHARACTER.get_rect(midleft=(logo_x, logo_y)))
        surface.blit(fade, (0, 0))
        pygame.display.flip()
        pygame.time.delay(int(duration / (255 / 5)))  # Distribui o tempo de fade

# Função Principal
def main():
    # Defina a altura desejada para o logo
    logo_y = SCREEN_HEIGHT * 0.25  # 25% da altura da tela (ajuste conforme necessário)

    # Criação dos Botões
    # Ajuste as posições X conforme a necessidade para alinhar à esquerda e dar espaço para o personagem
    button_x = SCREEN_WIDTH//2 - 200  # Deslocamento para a esquerda (ajustado de -150 para -200)
    start_button = ImageButton(
        os.path.join("assets", "buttons", "start_button.png"),
        (button_x, 250),
        scale=0.3,  # Reduzir para 30% do tamanho original
        scale_factor=1.02  # Aumenta 2% ao hover
    )
    options_button = ImageButton(
        os.path.join("assets", "buttons", "options_button.png"),
        (button_x, 350),
        scale=0.3,  # Reduzir para 30% do tamanho original
        scale_factor=1.02
    )
    exit_button = ImageButton(
        os.path.join("assets", "buttons", "exit_button.png"),
        (button_x, 450),
        scale=0.3,  # Reduzir para 30% do tamanho original
        scale_factor=1.02
    )

    # Efeito de fade-in no início
    if BACKGROUND:
        fade_in(SCREEN, BACKGROUND, logo_y)
    else:
        SCREEN.fill(WHITE)
        draw_logo_character(SCREEN, logo_y)
        pygame.display.flip()
        pygame.time.delay(1000)

    running = True
    while running:
        mouse_pos = pygame.mouse.get_pos()
        mouse_pressed = pygame.mouse.get_pressed()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Botão esquerdo do mouse
                    print("Mouse clicado em posição:", event.pos)
                    if start_button.is_clicked(event.pos):
                        if CLICK_SOUND:
                            CLICK_SOUND.play()
                        print("Iniciar Jogo")  # Aqui você pode chamar a função para iniciar o jogo
                        pygame.time.delay(200)  # Pequena pausa para evitar múltiplos cliques

                    if options_button.is_clicked(event.pos):
                        if CLICK_SOUND:
                            CLICK_SOUND.play()
                        print("Abrir Opções")  # Aqui você pode chamar a função para abrir as opções
                        pygame.time.delay(200)

                    if exit_button.is_clicked(event.pos):
                        if CLICK_SOUND:
                            CLICK_SOUND.play()
                        print("Sair do Jogo")
                        running = False

        # Desenho da Tela
        if BACKGROUND:
            SCREEN.blit(BACKGROUND, (0, 0))
        else:
            SCREEN.fill(WHITE)

        # Desenho do Título
        draw_title(SCREEN)

        # Desenho da Imagem do Personagem (Logo) **ANTES** dos Botões
        draw_logo_character(SCREEN, logo_y)

        # Desenho dos Botões **DEPOIS** do Logo
        start_button.draw(SCREEN, mouse_pos)
        options_button.draw(SCREEN, mouse_pos)
        exit_button.draw(SCREEN, mouse_pos)

        # Atualização da Tela
        pygame.display.flip()
        CLOCK.tick(FPS)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
