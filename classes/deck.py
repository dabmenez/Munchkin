import random
from classes.card import MonsterCard, CurseCard, TreasureCard
# Se você tiver ClassCard, RaceCard, etc., importe também
# from classes.card import ClassCard, RaceCard
# ...
from classes.card import Card

class Deck:
    """Representa um baralho genérico."""
    def __init__(self):
        self.cards = []  # Lista de cartas

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


class DoorDeck(Deck):
    """
    Baralho específico de 'Portas' (Monstros, Maldições, Raças, Classes...).
    """
    def __init__(self):
        super().__init__()
        self._create_door_cards()
        self.shuffle()

    def _create_door_cards(self):
        """
        Exemplo de cartas que entram no baralho de PORTA.
        Ajuste nomes, descrições e efeitos conforme suas regras.
        """
        # 1. Monstro Goblin
        self.add_card(MonsterCard(
            nome="Goblin",
            nivel=1,
            tesouros=1,
            texto_derrota="Você perde 1 nível.",
            texto_vitoria="Você ganha 1 tesouro adicional.",
            imagem="assets/cards/goblin.png"
        ))

        # 2. Monstro "Magia" (só exemplo, caso queira)
        self.add_card(MonsterCard(
            nome="Magia Estranha",
            nivel=2,
            tesouros=1,
            texto_derrota="Você perde 2 níveis.",
            texto_vitoria="Receba 2 tesouros extras.",
            imagem="assets/cards/magia.png"
        ))

        # 3. Carta de Maldição (curse.png)
        self.add_card(CurseCard(
            nome="Maldicao Flecha",
            efeitos="Você perde 1 item equipado.",
            imagem="assets/cards/flecha.png"
        ))

        # 4. Outra Maldição
        self.add_card(CurseCard(
            nome="Perde 1 Nível",
            efeitos="Você perde 1 nível imediatamente.",
            imagem="assets/cards/curse.png"
        ))


class TreasureDeck(Deck):
    """
    Baralho específico de 'Tesouros' (itens, equipamentos, etc.).
    """
    def __init__(self):
        super().__init__()
        self._create_treasure_cards()
        self.shuffle()

    def _create_treasure_cards(self):
        """
        Exemplo de cartas que entram no baralho de TESOURO.
        Ajuste nomes, descrições e efeitos conforme suas regras.
        """
        # 1. Espada +2
        self.add_card(TreasureCard(
            nome="Espada +2",
            bonus=2,
            descricao="Aumenta seu poder em 2.",
            imagem="assets/cards/espada.png"
        ))

        # 2. Escudo +1
        self.add_card(TreasureCard(
            nome="Escudo +1",
            bonus=1,
            descricao="Aumenta sua defesa em 1.",
            imagem="assets/cards/escudo.png"
        ))

        # 3. Poção
        self.add_card(TreasureCard(
            nome="Poção de Cura",
            bonus=0,
            descricao="Cura um jogador em 1 nível.",
            imagem="assets/cards/pocao.png"
        ))

        # 4. Tesouro genérico (tesouro.png)
        self.add_card(TreasureCard(
            nome="Saco de Ouro",
            bonus=0,
            descricao="Pode ser vendido para ganhar 1 nível.",
            imagem="assets/cards/tesouro.png"
        ))
