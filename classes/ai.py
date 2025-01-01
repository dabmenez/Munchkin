# classes/ai.py

from classes.card import MonsterCard, CurseCard

class AIController:
    """
    Classe que controla o comportamento da IA no jogo.
    """
    def __init__(self, player, door_deck, treasure_deck, discard_door, discard_treasure):
        self.player = player
        self.door_deck = door_deck
        self.treasure_deck = treasure_deck
        self.discard_door = discard_door
        self.discard_treasure = discard_treasure

    def realizar_turno(self, game_state):
        """
        Realiza as ações do turno da IA com base no estado atual do jogo.
        """
        if game_state == "FASE_COMPRAR_PORTA":
            self._comprar_carta_porta()
        elif game_state == "FASE_ACAO_PORTA":
            self._jogar_carta_da_mao()
        elif game_state == "FASE_DESCARTE":
            self._descartar_cartas_extras()

    def _comprar_carta_porta(self):
        """
        A IA compra uma carta de porta e decide o que fazer.
        """
        card = self.door_deck.draw_card()
        if card:
            self.player.hand.add_card(card)
            print(f"IA comprou uma carta de porta: {card.nome}")
            if isinstance(card, MonsterCard):
                print(f"IA encontrou um monstro: {card.nome}. Preparando para combate.")
        else:
            print("O baralho de portas está vazio!")

    def _jogar_carta_da_mao(self):
        """
        Lógica básica para a IA jogar uma carta da mão.
        """
        if self.player.hand.cards:
            card = self.player.hand.cards.pop(0)
            print(f"IA jogou a carta: {card.nome}")
        else:
            print("IA não tem cartas para jogar.")

    def _descartar_cartas_extras(self):
        """
        A IA descarta cartas extras para manter o limite.
        """
        while len(self.player.hand.cards) > 5:
            card = self.player.hand.cards.pop(0)
            self.discard_door.add_card(card)
            print(f"IA descartou a carta: {card.nome}")
