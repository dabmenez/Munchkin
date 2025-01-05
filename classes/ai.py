import random
from classes.card import MonsterCard, CurseCard, TreasureCard

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
        self.message = ""  # Mensagem para exibir no GameplayState

    def realizar_turno(self, game_phase):
        """
        Realiza as ações do turno da IA com base no estado atual (fase) do jogo.
        Retorna True se a IA terminou a ação nesta fase e está pronta para avançar.
        """
        self.message = ""

        if game_phase == "FASE_COMPRAR_PORTA":
            self._comprar_carta_porta()
            return True  # Terminou ação de comprar porta

        elif game_phase == "FASE_ENFRENTAR_MONSTRO":
            self._enfrentar_monstro()
            return True

        elif game_phase == "FASE_COLETAR_TESOURO":
            self._coletar_tesouro()
            return True

        elif game_phase == "FASE_DESCARTE":
            self._descartar_cartas_extras()
            return True

        return False  # default

    def _comprar_carta_porta(self):
        card = self.door_deck.draw_card()
        if card:
            self.message = f"IA comprou carta de porta: {card.nome}"
            if isinstance(card, MonsterCard):
                self.message += " [Monstro]"
                self.player.hand.add_card(card)
            elif isinstance(card, CurseCard):
                self.message += " [Maldição]"
                # Sofre efeitos
                self.player.decrease_level()
            else:
                # Qualquer outra carta de porta
                self.player.hand.add_card(card)
        else:
            self.message = "IA tentou comprar do baralho de portas, mas está vazio!"

    def _enfrentar_monstro(self):
        """
        A IA decide se enfrenta ou foge do monstro que possua na mão.
        """
        encontrou_monstro = False
        for card in self.player.hand.cards:
            if isinstance(card, MonsterCard):
                encontrou_monstro = True
                if self.player.level >= card.nivel:
                    self.message = (f"IA derrotou o monstro {card.nome} "
                                    f"e ganhou {card.tesouros} tesouro(s).")
                    self.player.increase_level()  # Ex: +1 nível
                    # Compra tesouros
                    for _ in range(card.tesouros):
                        t_card = self.treasure_deck.draw_card()
                        if t_card:
                            self.player.hand.add_card(t_card)
                    self.player.hand.remove_card(card)
                    break
                else:
                    self.message = f"IA não consegue derrotar {card.nome}. Tentando fugir..."
                    self._fugir(card)
                    self.player.hand.remove_card(card)
                    break
        if not encontrou_monstro:
            self.message = "IA não tinha monstro para enfrentar."

    def _fugir(self, monstro):
        dice_roll = random.randint(1, 6)
        if dice_roll <= 3:
            self.message += f" Fugiu com sucesso! (Dado {dice_roll})"
        else:
            self.message += f" Falhou na fuga! (Dado {dice_roll}) {monstro.texto_derrota}"
            self.player.decrease_level()

    def _coletar_tesouro(self):
        self.message = "IA está coletando tesouros."
        # Exemplo: IA pega 2 tesouros
        for _ in range(2):
            t_card = self.treasure_deck.draw_card()
            if t_card:
                self.player.hand.add_card(t_card)
                self.message += f" Pegou {t_card.nome}."
        # Tentar equipar itens
        self._tentar_equipar_itens()

    def _tentar_equipar_itens(self):
        """
        Faz a IA equipar todos os TreasureCards possíveis.
        Aqui é bem simples: todo TreasureCard que can_equip, a IA equipa.
        """
        for card in self.player.hand.cards[:]:
            if isinstance(card, TreasureCard):
                if self.player.equipment.can_equip(card):
                    self.player.hand.remove_card(card)
                    self.player.equipment.equip_item(card)
                    self.message += f" (Equipa {card.nome})"

    def _descartar_cartas_extras(self):
        self.message = "IA está descartando cartas extras."
        while len(self.player.hand.cards) > 5:
            card = self.player.hand.cards.pop(0)
            self.discard_door.add_card(card)
            self.message += f" Descartou {card.nome}."
