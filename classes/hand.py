from classes.card import Card

class Hand:
    """Representa a mão do jogador."""
    def __init__(self):
        self.cards = []  # Lista de cartas na mão do jogador

    def add_card(self, card):
        """Adiciona uma carta à mão."""
        if isinstance(card, Card):
            self.cards.append(card)

    def remove_card(self, card):
        """Remove uma carta específica da mão."""
        if card in self.cards:
            self.cards.remove(card)

    def show_hand(self):
        """Retorna uma lista textual das cartas na mão."""
        return [str(card) for card in self.cards]

    def __len__(self):
        """Retorna o número de cartas na mão."""
        return len(self.cards)
