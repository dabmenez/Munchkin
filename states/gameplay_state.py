import pygame
from classes.deck import Deck
from classes.card import MonsterCard, TreasureCard, CurseCard
from classes.player import Player
from classes.ai import AIController

class GameplayState:
    def __init__(self, game):
        self.game = game

        # Inicializa os jogadores
        self.player = Player("Jogador 1")
        self.opponent = Player("IA", ia=True)
        self.current_player = self.player

        # Inicializa os baralhos
        self.door_deck = Deck()
        self.treasure_deck = Deck()
        self.discard_door = Deck()
        self.discard_treasure = Deck()

        # IA Controller
        self.ai_controller = AIController(
            self.opponent,
            self.door_deck,
            self.treasure_deck,
            self.discard_door,
            self.discard_treasure
        )

        # Criação e distribuição inicial
        self._create_decks()
        self._distribute_initial_cards()

        # Fase do jogo
        self.game_phase = "FASE_COMPRAR_PORTA"  # Primeira fase

        # Mensagem informativa
        self.message = ""

    def _create_decks(self):
        """Cria os baralhos de porta e tesouro com cartas predefinidas."""
        # Baralho de Porta
        door_cards = [
            MonsterCard("Goblin", nivel=1, tesouros=1, texto_derrota="Perde 1 nível", texto_vitoria="Ganha 1 tesouro extra", imagem="assets/cards/goblin.png"),
            CurseCard("Perde 1 Nível", "Você perde 1 nível imediatamente.", imagem="assets/cards/curse.png"),
        ]
        for card in door_cards:
            self.door_deck.add_card(card)

        # Baralho de Tesouro
        treasure_cards = [
            TreasureCard("Espada +2", bonus=2, descricao="Aumenta seu poder em 2.", imagem="assets/cards/espada.png"),
            TreasureCard("Poção de Cura", bonus=0, descricao="Cura um jogador.", imagem="assets/cards/pocao.png"),
        ]
        for card in treasure_cards:
            self.treasure_deck.add_card(card)

        # Embaralha os baralhos
        self.door_deck.shuffle()
        self.treasure_deck.shuffle()

    def _distribute_initial_cards(self):
        """Dá 3 cartas de porta e 3 de tesouro ao jogador e à IA."""
        for _ in range(3):
            # Jogador
            door_card = self.door_deck.draw_card()
            treasure_card = self.treasure_deck.draw_card()
            if door_card:
                self.player.hand.add_card(door_card)
            if treasure_card:
                self.player.hand.add_card(treasure_card)

            # Oponente (IA)
            door_card = self.door_deck.draw_card()
            treasure_card = self.treasure_deck.draw_card()
            if door_card:
                self.opponent.hand.add_card(door_card)
            if treasure_card:
                self.opponent.hand.add_card(treasure_card)

    def handle_events(self, events):
        """Processa os eventos do gameplay."""
        for event in events:
            if event.type == pygame.QUIT:
                self.game.estado = "SAIR"

            elif event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = pygame.mouse.get_pos()
                mx_base = int(mx * self.game.base_width / self.game.largura)
                my_base = int(my * self.game.base_height / self.game.altura)

                # Se for jogador humano e estiver na fase de comprar porta
                if self.current_player == self.player and self.game_phase == "FASE_COMPRAR_PORTA":
                    door_deck_rect = self._draw_door_deck(self.game.base_surface, self.door_deck, (300, 300))
                    if door_deck_rect.collidepoint((mx_base, my_base)):
                        card = self.door_deck.draw_card()
                        if card:
                            self.player.hand.add_card(card)
                            self.message = f"Você comprou: {card.nome}"
                            self.next_phase()  # Avança para próxima fase
                        else:
                            self.message = "O baralho de portas está vazio!"

                # Se for jogador humano e estiver na fase de comprar tesouro
                if self.current_player == self.player and self.game_phase == "FASE_ACAO_PORTA":
                    treasure_deck_rect = self._draw_treasure_deck(self.game.base_surface, self.treasure_deck, (600, 300))
                    if treasure_deck_rect.collidepoint((mx_base, my_base)):
                        card = self.treasure_deck.draw_card()
                        if card:
                            self.player.hand.add_card(card)
                            self.message = f"Você comprou: {card.nome}"
                            self.next_phase()  # Avança para a fase de descarte
                        else:
                            self.message = "O baralho de tesouros está vazio!"

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.game.estado = "MENU"

    def update(self, dt):
        """Atualiza o estado do gameplay."""
        # Se for a vez da IA, ela faz suas jogadas
        if self.current_player.ia:
            self.ai_controller.realizar_turno(self.game_phase)
            self.next_phase()  # Exemplo: avança a fase após a jogada da IA

    def next_phase(self):
        """
        Avança para a próxima fase de turno.
        Você pode adaptar a lógica conforme as regras do jogo.
        """
        if self.game_phase == "FASE_COMPRAR_PORTA":
            self.game_phase = "FASE_ACAO_PORTA"
        elif self.game_phase == "FASE_ACAO_PORTA":
            self.game_phase = "FASE_DESCARTE"
        elif self.game_phase == "FASE_DESCARTE":
            self.game_phase = "FASE_COMPRAR_PORTA"
            self.end_turn()

    def end_turn(self):
        """Alterna o jogador atual."""
        if self.current_player == self.player:
            self.current_player = self.opponent
        else:
            self.current_player = self.player

    def draw(self):
        """Desenha os elementos do gameplay."""
        base_surf = self.game.base_surface
        base_surf.fill((0, 0, 0))

        # 1. Desenhar informações do jogador
        self._draw_player_info(base_surf, self.player, (50, 50))

        # 2. Desenhar informações da IA
        self._draw_player_info(base_surf, self.opponent, (self.game.base_width - 350, 50), ia=True)

        # 3. Desenhar os baralhos (sem texto, cada um com sua cor)
        #    Usamos métodos separados: um para baralho de portas (marrom) e outro para baralho de tesouro (amarelo).
        self._draw_door_deck(base_surf, self.door_deck, (300, 300))
        self._draw_treasure_deck(base_surf, self.treasure_deck, (600, 300))

        # 4. Desenhar a mão do jogador
        self._draw_hand(base_surf, self.player, (100, self.game.base_height - 220))

        # 5. Desenhar a mochila e os itens equipados do jogador
        self._draw_backpack(base_surf, self.player, (100, self.game.base_height - 380))
        self._draw_equipped_items(base_surf, self.player, (600, self.game.base_height - 380))

        # 6. Desenhar mensagem informativa (se existir)
        if self.message:
            msg_surf = self.game.fonte.render(self.message, True, (255, 255, 0))
            base_surf.blit(msg_surf, (50, self.game.base_height - 280))

    def _draw_player_info(self, surface, player, position, ia=False):
        """Desenha informações básicas do jogador/IA."""
        x, y = position
        title = f"IA: {player.name}" if ia else f"Jogador: {player.name}"
        title_surf = self.game.fonte.render(title, True, (255, 255, 255))
        level_surf = self.game.fonte.render(f"Nível: {player.level}", True, (255, 255, 255))

        surface.blit(title_surf, (x, y))
        surface.blit(level_surf, (x, y + 40))

    def _draw_hand(self, surface, player, position):
        """Desenha as cartas na mão do jogador."""
        x_start, y_position = position
        spacing = 120  # Ajuste do espaçamento horizontal

        for i, card in enumerate(player.hand.cards):
            if card.imagem:
                card_image = pygame.image.load(card.imagem).convert_alpha()
                card_image = pygame.transform.scale(card_image, (100, 150))
            else:
                # Caso não tenha imagem, desenhe um placeholder
                card_image = pygame.Surface((100, 150))
                card_image.fill((128, 0, 0))
            card_rect = card_image.get_rect(topleft=(x_start + i * spacing, y_position))
            surface.blit(card_image, card_rect)

    def _draw_backpack(self, surface, player, position):
        """Desenha os itens da mochila do jogador."""
        x_start, y_position = position
        backpack_text = self.game.fonte.render("Mochila", True, (255, 255, 255))
        surface.blit(backpack_text, (x_start, y_position - 30))

        spacing = 120
        for i, item in enumerate(player.backpack):
            if item.imagem:
                item_image = pygame.image.load(item.imagem).convert_alpha()
                item_image = pygame.transform.scale(item_image, (80, 120))
            else:
                item_image = pygame.Surface((80, 120))
                item_image.fill((0, 128, 0))
            item_rect = item_image.get_rect(topleft=(x_start + i * spacing, y_position))
            surface.blit(item_image, item_rect)

    def _draw_equipped_items(self, surface, player, position):
        """Desenha os itens equipados pelo jogador."""
        x_start, y_position = position
        equipped_text = self.game.fonte.render("Itens Equipados", True, (255, 255, 255))
        surface.blit(equipped_text, (x_start, y_position - 30))

        spacing = 120
        for i, item in enumerate(player.equipped_items):
            if item.imagem:
                item_image = pygame.image.load(item.imagem).convert_alpha()
                item_image = pygame.transform.scale(item_image, (80, 120))
            else:
                item_image = pygame.Surface((80, 120))
                item_image.fill((0, 0, 128))
            item_rect = item_image.get_rect(topleft=(x_start + i * spacing, y_position))
            surface.blit(item_image, item_rect)

    def _draw_door_deck(self, surface, deck, position):
        """
        Desenha o baralho de portas em marrom, mostra a quantidade de cartas,
        e retorna o rect para permitir clique.
        """
        x, y = position
        card_back = pygame.Surface((100, 150))
        # Cor marrom (brown)
        card_back.fill((139, 69, 19))
        # Borda branca
        pygame.draw.rect(card_back, (255, 255, 255), card_back.get_rect(), 3)

        deck_rect = card_back.get_rect(topleft=(x, y))
        surface.blit(card_back, deck_rect.topleft)

        # Quantidade de cartas
        count_surf = self.game.fonte.render(f"{len(deck)}", True, (255, 255, 255))
        count_rect = count_surf.get_rect(midbottom=(x + 50, y + 150 + 20))  # um pouco abaixo do baralho
        surface.blit(count_surf, count_rect)

        return deck_rect

    def _draw_treasure_deck(self, surface, deck, position):
        """
        Desenha o baralho de tesouros em amarelo, mostra a quantidade de cartas,
        e retorna o rect para permitir clique.
        """
        x, y = position
        card_back = pygame.Surface((100, 150))
        # Cor amarela
        card_back.fill((255, 255, 0))
        # Borda branca
        pygame.draw.rect(card_back, (255, 255, 255), card_back.get_rect(), 3)

        deck_rect = card_back.get_rect(topleft=(x, y))
        surface.blit(card_back, deck_rect.topleft)

        # Quantidade de cartas
        count_surf = self.game.fonte.render(f"{len(deck)}", True, (0, 0, 0))
        count_rect = count_surf.get_rect(midbottom=(x + 50, y + 150 + 20))  # um pouco abaixo do baralho
        surface.blit(count_surf, count_rect)

        return deck_rect
