from classes.hand import Hand
from classes.card import Card

class Mochila:
    """
    Representa a mochila do jogador, onde ficam itens
    (normalmente TreasureCards) que não estão equipados no momento.
    """
    def __init__(self):
        self.items = []

    def add_item(self, card: Card):
        self.items.append(card)

    def remove_item(self, card: Card):
        if card in self.items:
            self.items.remove(card)

    def get_items(self):
        return self.items

    def has_item(self, card: Card):
        return card in self.items

    def count_items(self):
        return len(self.items)


class Equipment:
    """
    Representa os itens que estão de fato equipados pelo jogador.
    """
    def __init__(self):
        self.equipped_items = []

    def equip_item(self, card: Card):
        # Lógica básica, sem restrições;
        # se quiser limitar itens por tipo, mãos, etc., faça aqui.
        self.equipped_items.append(card)

    def unequip_item(self, card: Card):
        if card in self.equipped_items:
            self.equipped_items.remove(card)

    def get_equipped(self):
        return self.equipped_items

    def is_equipped(self, card: Card):
        return card in self.equipped_items

    def can_equip(self, card: Card):
        # Retorne True/False conforme regras (ex: se usar 2 mãos, etc.)
        return True


class Player:
    """Representa o jogador no jogo."""
    def __init__(self, name, ia=False):
        self.name = name        # Nome do jogador
        self.level = 1          # Nível inicial
        self.hand = Hand()      # Mão do jogador
        self.mochila = Mochila() # Nova forma de armazenar itens "guardados"
        self.equipment = Equipment() # Itens que estão equipados
        self.ia = ia            # Define se é IA ou jogador humano

    def increase_level(self, amount=1):
        """Aumenta o nível do jogador."""
        self.level += amount

    def decrease_level(self, amount=1):
        """Diminui o nível do jogador (mínimo nível 1)."""
        self.level = max(1, self.level - amount)

    # Métodos de atalho, se quiser manipular a mochila/equipment diretamente:
    def add_to_backpack(self, card: Card):
        """Antigo: 'backpack'. Agora delegamos para Mochila."""
        self.mochila.add_item(card)

    def remove_from_backpack(self, card: Card):
        self.mochila.remove_item(card)

    def equip_item(self, card: Card):
        """Equipe um item (caso as regras permitam)."""
        if self.equipment.can_equip(card):
            self.equipment.equip_item(card)
            print(f"{self.name} equipou {card.nome}")
        else:
            print(f"{self.name} não pode equipar {card.nome} agora.")

    def unequip_item(self, card: Card):
        """Retire o item do 'Equipment'."""
        if self.equipment.is_equipped(card):
            self.equipment.unequip_item(card)
            print(f"{self.name} desequipou {card.nome}")
        else:
            print(f"{self.name} não estava usando {card.nome}.")

    def __str__(self):
        """Representação textual do jogador."""
        return f"{self.name} (Nível: {self.level})"
