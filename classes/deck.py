# classes/deck.py

import random
from classes.card import Card

class Deck:
    """Representa o baralho do jogo."""
    def __init__(self):
        self.cards = []  # Lista de cartas no baralho

    def add_card(self, card):
        """Adiciona uma carta ao baralho."""
        self.cards.append(card)

    def shuffle(self):
        """Embaralha o baralho."""
        random.shuffle(self.cards)

    def draw_card(self):
        """
        Retira uma carta do topo do baralho.
        Retorna None se o baralho estiver vazio.
        """
        if self.cards:
            return self.cards.pop()
        return None

    def __len__(self):
        """Retorna o número de cartas restantes no baralho."""
        return len(self.cards)
