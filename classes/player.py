# classes/player.py

from classes.hand import Hand

class Player:
    """Representa o jogador no jogo."""
    def __init__(self, name):
        self.name = name            # Nome do jogador
        self.level = 1              # Nível inicial
        self.hand = Hand()          # Mão do jogador
        self.backpack = []          # Mochila do jogador (itens extras)

    def increase_level(self, amount=1):
        """Aumenta o nível do jogador."""
        self.level += amount

    def decrease_level(self, amount=1):
        """Diminui o nível do jogador (mínimo nível 1)."""
        self.level = max(1, self.level - amount)

    def add_to_backpack(self, card):
        """Adiciona uma carta à mochila."""
        self.backpack.append(card)

    def remove_from_backpack(self, card):
        """Remove uma carta específica da mochila."""
        if card in self.backpack:
            self.backpack.remove(card)

    def __str__(self):
        """Representação textual do jogador."""
        return f"{self.name} (Nível: {self.level})"
