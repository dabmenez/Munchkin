import time
import pygame
import random

from classes.deck import DoorDeck, TreasureDeck, Deck
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

        # Baralhos
        self.door_deck = DoorDeck()
        self.treasure_deck = TreasureDeck()
        self.discard_door = Deck()
        self.discard_treasure = Deck()

        # Controlador de IA
        self.ai_controller = AIController(
            self.opponent,
            self.door_deck,
            self.treasure_deck,
            self.discard_door,
            self.discard_treasure
        )

        # Distribuição inicial
        self._distribute_initial_cards()

        # Fases
        self.game_phase = "FASE_COMPRAR_PORTA"
        self.current_door_card = None

        # Mensagem
        self.message = ""

        # Layout
        self.background_color = (20, 20, 20)
        self.player_area_color = (50, 50, 150)
        self.ai_area_color = (150, 50, 50)
        self.deck_area_color = (139, 69, 19)
        self.treasure_area_color = (255, 215, 0)

        # Botões
        self.restart_button = pygame.Rect(50, 50, 150, 50)
        self.exit_button = pygame.Rect(250, 50, 150, 50)

        self.hand_card_rects = []

    def _distribute_initial_cards(self):
        """Dá 3 cartas de porta e 3 de tesouro ao player e IA."""
        for _ in range(3):
            door_card = self.door_deck.draw_card()
            treasure_card = self.treasure_deck.draw_card()
            if door_card:
                self.player.hand.add_card(door_card)
            if treasure_card:
                self.player.hand.add_card(treasure_card)

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

                # Botões
                if self.restart_button.collidepoint((mx, my)):
                    self.restart_game()
                    return
                elif self.exit_button.collidepoint((mx, my)):
                    self.game.estado = "SAIR"
                    return

                mx_base = int(mx * self.game.base_width / self.game.largura)
                my_base = int(my * self.game.base_height / self.game.altura)

                if self.current_player == self.player:
                    # FASE_COMPRAR_PORTA
                    if self.game_phase == "FASE_COMPRAR_PORTA":
                        door_deck_rect = self._draw_door_deck(self.game.base_surface, self.door_deck, (850, 280))
                        if door_deck_rect.collidepoint((mx_base, my_base)):
                            self.current_door_card = self.door_deck.draw_card()
                            if self.current_door_card:
                                self.message = f"Você revelou: {self.current_door_card.nome}"
                                if isinstance(self.current_door_card, MonsterCard):
                                    self.game_phase = "FASE_ENFRENTAR_MONSTRO"
                                elif isinstance(self.current_door_card, CurseCard):
                                    self.message = "Uma maldição foi ativada!"
                                    self.player.apply_curse(self.current_door_card)
                                    self.discard_door.add_card(self.current_door_card)
                                    self.next_phase()
                                else:
                                    self.player.hand.add_card(self.current_door_card)
                                    self.discard_door.add_card(self.current_door_card)
                                    self.next_phase()
                            else:
                                self.message = "O baralho de portas está vazio!"

                    # FASE_ENFRENTAR_MONSTRO
                    elif self.game_phase == "FASE_ENFRENTAR_MONSTRO":
                        if isinstance(self.current_door_card, MonsterCard):
                            if self.player.level >= self.current_door_card.nivel:
                                self.message = (f"Você derrotou o monstro e ganhou "
                                                f"{self.current_door_card.tesouros} tesouro(s)!")
                                for _ in range(self.current_door_card.tesouros):
                                    t_card = self.treasure_deck.draw_card()
                                    if t_card:
                                        self.player.hand.add_card(t_card)
                                self.discard_door.add_card(self.current_door_card)
                                self.next_phase()
                            else:
                                self.message = ("Você não conseguiu derrotar o monstro! "
                                                "Tentando fugir...")
                                self._attempt_escape()

                    # FASE_COLETAR_TESOURO
                    elif self.game_phase == "FASE_COLETAR_TESOURO":
                        treasure_deck_rect = self._draw_treasure_deck(self.game.base_surface, self.treasure_deck, (1050, 280))
                        if treasure_deck_rect.collidepoint((mx_base, my_base)):
                            t_card = self.treasure_deck.draw_card()
                            if t_card:
                                self.player.hand.add_card(t_card)
                                self.message = f"Você pegou: {t_card.nome}"
                            else:
                                self.message = "O baralho de tesouros está vazio!"
                            self.next_phase()

                    # FASE_DESCARTE
                    elif self.game_phase == "FASE_DESCARTE":
                        # Se quiser implementar descarte manual
                        self.next_phase()

                    # Clique para equipar (cartas da mão)
                    for (rect, card) in self.hand_card_rects:
                        if rect.collidepoint((mx_base, my_base)):
                            if isinstance(card, TreasureCard):
                                self._equip_item(card)
                            break

    def _equip_item(self, card):
        if self.player.equipment.can_equip(card):
            self.player.hand.remove_card(card)
            self.player.equipment.equip_item(card)
            self.message = f"Você equipou o item: {card.nome}"
        else:
            self.message = f"Não foi possível equipar: {card.nome}"

    def _attempt_escape(self):
        """Tenta fugir do monstro (dado 1..6)."""
        dice_roll = random.randint(1, 6)
        if dice_roll <= 3:
            self.message = f"Você fugiu com sucesso! (Dado: {dice_roll})"
            self.next_phase()
        else:
            self.message = (f"Você falhou na fuga! (Dado: {dice_roll}) "
                            f"{self.current_door_card.texto_derrota}")
            self.player.decrease_level()
            self.next_phase()

    def update(self, dt):
        """Atualiza o estado do gameplay."""
        if self.current_player.ia:
            time.sleep(1)
            fase_terminada = self.ai_controller.realizar_turno(self.game_phase)
            if self.ai_controller.message:
                self.message = self.ai_controller.message
            if fase_terminada:
                self.next_phase()

    def next_phase(self):
        """
        Avança para a próxima fase do jogo.
        """
        if self.game_phase == "FASE_COMPRAR_PORTA":
            self.game_phase = "FASE_ENFRENTAR_MONSTRO"
        elif self.game_phase == "FASE_ENFRENTAR_MONSTRO":
            self.game_phase = "FASE_COLETAR_TESOURO"
        elif self.game_phase == "FASE_COLETAR_TESOURO":
            self.game_phase = "FASE_DESCARTE"
        elif self.game_phase == "FASE_DESCARTE":
            self.game_phase = "FASE_FIM_TURNO"
        elif self.game_phase == "FASE_FIM_TURNO":
            self.end_turn()
            self.game_phase = "FASE_COMPRAR_PORTA"

    def end_turn(self):
        """Alterna o jogador atual."""
        if self.current_player == self.player:
            self.current_player = self.opponent
        else:
            self.current_player = self.player

    def restart_game(self):
        """Reinicia o estado do jogo."""
        self.__init__(self.game)

    def draw(self):
        """Desenha os elementos do gameplay."""
        base_surf = self.game.base_surface
        base_surf.fill(self.background_color)

        # Botões
        pygame.draw.rect(base_surf, (0, 200, 0), self.restart_button)
        restart_text = self.game.fonte.render("Reiniciar", True, (255, 255, 255))
        base_surf.blit(restart_text, (self.restart_button.x + 10, self.restart_button.y + 10))

        pygame.draw.rect(base_surf, (200, 0, 0), self.exit_button)
        exit_text = self.game.fonte.render("Sair", True, (255, 255, 255))
        base_surf.blit(exit_text, (self.exit_button.x + 40, self.exit_button.y + 10))

        # Áreas do jogador e IA
        pygame.draw.rect(base_surf, self.player_area_color, (50, 680, 400, 220))
        pygame.draw.rect(base_surf, self.ai_area_color, (1470, 50, 400, 220))

        # Desenhar baralhos
        self._draw_door_deck(base_surf, self.door_deck, (850, 280))
        self._draw_treasure_deck(base_surf, self.treasure_deck, (1050, 280))

        # Mensagem no topo (centralizado)
        if self.message:
            msg_surf = self.game.fonte.render(self.message, True, (255, 255, 0))
            msg_rect = msg_surf.get_rect(midtop=(self.game.base_width // 2, 150))
            base_surf.blit(msg_surf, msg_rect)

        # Carta revelada
        if self.current_door_card:
            card_rect = pygame.Rect(930, 450, 100, 150)
            pygame.draw.rect(base_surf, (200, 200, 200), card_rect)
            if self.current_door_card.imagem:
                try:
                    card_image = pygame.image.load(self.current_door_card.imagem).convert_alpha()
                    card_image = pygame.transform.scale(card_image, (100, 150))
                    base_surf.blit(card_image, card_rect.topleft)
                except pygame.error:
                    pygame.draw.rect(base_surf, (255, 0, 0), card_rect)

        # Mão do jogador
        self._draw_hand(base_surf, self.player, (50, 920))

        # Itens equipados do jogador
        self._draw_equipped_items(base_surf, self.player, (50, 760))

        # Exibir info do jogador (canto inferior esquerdo)
        self._draw_player_info(base_surf, self.player, (50, 630), ia=False)
        # Exibir info da IA (canto superior direito)
        self._draw_player_info(base_surf, self.opponent, (1300, 60), ia=True)

        # Se quiser ver a mão e itens da IA:
        self._draw_opponent_info(base_surf)

    def _draw_hand(self, surface, player, position):
        x_start, y_position = position
        spacing = 110
        self.hand_card_rects = []

        for i, card in enumerate(player.hand.cards):
            card_rect = pygame.Rect(x_start + i * spacing, y_position, 100, 150)
            pygame.draw.rect(surface, (200, 200, 200), card_rect)
            if card.imagem:
                try:
                    card_img = pygame.image.load(card.imagem).convert_alpha()
                    card_img = pygame.transform.scale(card_img, (100, 150))
                    surface.blit(card_img, card_rect.topleft)
                except pygame.error:
                    pygame.draw.rect(surface, (255, 0, 0), card_rect)
            self.hand_card_rects.append((card_rect, card))

    def _draw_equipped_items(self, surface, player, position):
        x_start, y_start = position
        equip_title = self.game.fonte.render("Equipado:", True, (255, 255, 255))
        surface.blit(equip_title, (x_start, y_start - 30))

        spacing = 110
        for i, item in enumerate(player.equipment.get_equipped()):
            item_rect = pygame.Rect(x_start + i * spacing, y_start, 100, 150)
            pygame.draw.rect(surface, (180, 180, 180), item_rect)
            if item.imagem:
                try:
                    item_img = pygame.image.load(item.imagem).convert_alpha()
                    item_img = pygame.transform.scale(item_img, (100, 150))
                    surface.blit(item_img, item_rect.topleft)
                except pygame.error:
                    pygame.draw.rect(surface, (255, 0, 0), item_rect)

    def _draw_player_info(self, surface, player, position, ia=False):
        x, y = position
        if ia:
            title_surf = self.game.fonte.render(f"IA: {player.name}", True, (255,255,255))
        else:
            title_surf = self.game.fonte.render(f"Jogador: {player.name}", True, (255,255,255))
        level_surf = self.game.fonte.render(f"Nível: {player.level}", True, (255,255,255))

        surface.blit(title_surf, (x, y))
        surface.blit(level_surf, (x, y + 40))

    def _draw_opponent_info(self, surface):
        """
        Exemplo para mostrar a mão e itens equipados da IA na tela.
        Ajuste coords conforme layout.
        """
        # Mão da IA (canto superior direito)
        x_start, y_start = (1480, 300)
        spacing = 80
        for i, card in enumerate(self.opponent.hand.cards):
            c_rect = pygame.Rect(x_start + i*spacing, y_start, 80, 120)
            pygame.draw.rect(surface, (200,200,200), c_rect)
            if card.imagem:
                try:
                    c_img = pygame.image.load(card.imagem).convert_alpha()
                    c_img = pygame.transform.scale(c_img, (80,120))
                    surface.blit(c_img, c_rect.topleft)
                except pygame.error:
                    pygame.draw.rect(surface, (255,0,0), c_rect)

        # Itens equipados da IA (logo abaixo da mão)
        equip_title = self.game.fonte.render("IA Equipado:", True, (255,255,255))
        surface.blit(equip_title, (1480, 430))

        for j, eq_item in enumerate(self.opponent.equipment.get_equipped()):
            eq_rect = pygame.Rect(1480 + j*spacing, 460, 80,120)
            pygame.draw.rect(surface, (180,180,180), eq_rect)
            if eq_item.imagem:
                try:
                    eq_img = pygame.image.load(eq_item.imagem).convert_alpha()
                    eq_img = pygame.transform.scale(eq_img, (80,120))
                    surface.blit(eq_img, eq_rect.topleft)
                except pygame.error:
                    pygame.draw.rect(surface, (255,0,0), eq_rect)

    def _draw_door_deck(self, surface, deck, position):
        x, y = position
        card_back = pygame.Surface((100, 150))
        card_back.fill(self.deck_area_color)
        pygame.draw.rect(card_back, (255, 255, 255), card_back.get_rect(), 3)
        deck_rect = card_back.get_rect(topleft=(x, y))
        surface.blit(card_back, deck_rect.topleft)

        count_surf = self.game.fonte.render(f"{len(deck)}", True, (255, 255, 255))
        count_rect = count_surf.get_rect(midbottom=(x + 50, y + 170))
        surface.blit(count_surf, count_rect)
        return deck_rect

    def _draw_treasure_deck(self, surface, deck, position):
        x, y = position
        card_back = pygame.Surface((100, 150))
        card_back.fill(self.treasure_area_color)
        pygame.draw.rect(card_back, (255, 255, 255), card_back.get_rect(), 3)
        deck_rect = card_back.get_rect(topleft=(x, y))
        surface.blit(card_back, deck_rect.topleft)

        count_surf = self.game.fonte.render(f"{len(deck)}", True, (0, 0, 0))
        count_rect = count_surf.get_rect(midbottom=(x + 50, y + 170))
        surface.blit(count_surf, count_rect)
        return deck_rect
