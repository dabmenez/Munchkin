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

    def realizar_turno(self, game_phase):
        """
        Realiza as ações do turno da IA com base no estado atual (fase) do jogo.
        Possíveis fases, conforme o diagrama atualizado:
          - FASE_COMPRAR_PORTA
          - FASE_ENFRENTAR_MONSTRO
          - FASE_COLETAR_TESOURO
          - FASE_DESCARTE
          - FASE_FIM_TURNO
        """
        if game_phase == "FASE_COMPRAR_PORTA":
            self._comprar_carta_porta()

        elif game_phase == "FASE_ENFRENTAR_MONSTRO":
            # Substitui a antiga "FASE_ACAO_PORTA"
            self._jogar_carta_da_mao()

        elif game_phase == "FASE_COLETAR_TESOURO":
            self._coletar_tesouro()

        elif game_phase == "FASE_DESCARTE":
            self._descartar_cartas_extras()

        elif game_phase == "FASE_FIM_TURNO":
            # Nesta fase, normalmente a IA não faz nada específico; apenas finaliza o turno
            pass

    def _comprar_carta_porta(self):
        """
        A IA compra uma carta do baralho de portas e decide o que fazer.
        """
        card = self.door_deck.draw_card()
        if card:
            self.player.hand.add_card(card)
            print(f"IA comprou uma carta de porta: {card.nome}")
            if isinstance(card, MonsterCard):
                print(f"IA encontrou um monstro: {card.nome}. (Preparando para combate.)")
        else:
            print("O baralho de portas está vazio!")

    def _jogar_carta_da_mao(self):
        """
        Lógica básica para a IA 'jogar' (ou descartar) a primeira carta da mão.
        No futuro, você pode implementar aqui a lógica de combate, se a carta for um monstro etc.
        """
        if self.player.hand.cards:
            card = self.player.hand.cards.pop(0)
            print(f"IA jogou (descartou) a carta: {card.nome}")
            # Exemplo: se quiser descartar em discard_door:
            self.discard_door.add_card(card)
        else:
            print("IA não tem cartas para jogar.")

    def _coletar_tesouro(self):
        """
        Fase opcional para IA coletar/comprar tesouros
        (caso as regras o permitam após derrotar um monstro).
        """
        # Exemplo mínimo (não faz nada especial):
        print("IA está na fase de COLETAR TESOURO (ainda não implementado).")

    def _descartar_cartas_extras(self):
        """
        A IA descarta cartas extras para manter o limite (ex: 5 cartas).
        """
        while len(self.player.hand.cards) > 5:
            card = self.player.hand.cards.pop(0)
            self.discard_door.add_card(card)
            print(f"IA descartou a carta: {card.nome}")
