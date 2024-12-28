# classes/card.py

class Card:
    """Representa uma carta do jogo."""
    def __init__(self, name, value, description=None, image_path=None):
        self.name = name          # Nome da carta (ex.: "Espada", "Poção", etc.)
        self.value = value        # Valor ou poder da carta
        self.description = description  # Descrição opcional (efeito, etc.)
        self.image_path = image_path    # Caminho da imagem da carta
        self.image = None               # Será carregada no jogo

    def load_image(self):
        """Carrega a imagem da carta (chamado no estado do jogo)."""
        if self.image_path:
            import pygame
            self.image = pygame.image.load(self.image_path).convert_alpha()

    def __str__(self):
        """Retorna uma representação textual da carta."""
        return f"{self.name} (Valor: {self.value})"
