# states/gameplay_state.py

import pygame
from config import PRETO, BRANCO
from classes.deck import Deck
from classes.card import Card
from classes.player import Player

class GameplayState:
    def __init__(self, game):
        self.game = game

        # Inicializa o jogador
        self.player = Player("Jogador 1")

        # Inicializa os baralhos
        self.door_deck = Deck()    # Baralho de Porta
        self.treasure_deck = Deck()  # Baralho de Tesouro
        self._create_decks()

        # Distribui cartas iniciais
        self._distribute_initial_cards()

        # Texto informativo
        self.message = ""

    def _create_decks(self):
        """Cria os baralhos de porta e tesouro."""
        # Baralho de Porta
        door_cards = [
            Card("Monstro: Goblin", 1, "Um goblin fraco.", "assets/cards/goblin.png"),
            Card("Maldição: Perde um Nível", -1, "Perde 1 nível.", "assets/cards/curse.png"),
            Card("Classe: Guerreiro", 0, "Ganha a classe Guerreiro.", "assets/cards/warrior.png"),
        ]
        for card in door_cards:
            card.load_image()
            self.door_deck.add_card(card)

        # Baralho de Tesouro
        treasure_cards = [
            Card("Espada +2", 2, "Aumenta seu poder em 2.", "assets/cards/espada.png"),
            Card("Poção de Cura", 0, "Use para curar um aliado.", "assets/cards/pocao.png"),
            Card("Tesouro: Ouro", 0, "Vale 1 moeda de ouro.", "assets/cards/tesouro.png"),
        ]
        for card in treasure_cards:
            card.load_image()
            self.treasure_deck.add_card(card)

        # Embaralha os baralhos
        self.door_deck.shuffle()
        self.treasure_deck.shuffle()

    def _distribute_initial_cards(self):
        """Dá 3 cartas de cada baralho ao jogador no início do jogo."""
        for _ in range(3):
            door_card = self.door_deck.draw_card()
            treasure_card = self.treasure_deck.draw_card()
            if door_card:
                self.player.hand.add_card(door_card)
            if treasure_card:
                self.player.hand.add_card(treasure_card)

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                self.game.estado = "SAIR"
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.game.estado = "MENU"
                elif event.key == pygame.K_d:  # 'D' para comprar uma carta de porta
                    card = self.door_deck.draw_card()
                    if card:
                        self.player.hand.add_card(card)
                        self.message = f"Você comprou uma carta de porta: {card.name}"
                    else:
                        self.message = "O baralho de portas está vazio!"
                elif event.key == pygame.K_t:  # 'T' para comprar uma carta de tesouro
                    card = self.treasure_deck.draw_card()
                    if card:
                        self.player.hand.add_card(card)
                        self.message = f"Você comprou uma carta de tesouro: {card.name}"
                    else:
                        self.message = "O baralho de tesouros está vazio!"

    def update(self, dt):
        pass

    def draw(self):
        base_surf = self.game.base_surface
        base_surf.fill(PRETO)

        # Texto do jogador
        player_text = f"{self.player.name} - Nível {self.player.level}"
        player_surf = self.game.fonte.render(player_text, True, BRANCO)
        player_rect = player_surf.get_rect(midtop=(self.game.base_width // 2, 20))
        base_surf.blit(player_surf, player_rect)

        # Texto informativo
        msg_surf = self.game.fonte.render(self.message, True, BRANCO)
        msg_rect = msg_surf.get_rect(midtop=(self.game.base_width // 2, 60))
        base_surf.blit(msg_surf, msg_rect)

        # Desenhar o baralho de porta
        self._draw_deck(base_surf, self.door_deck, "Baralho de Porta", (50, 200))

        # Desenhar o baralho de tesouro
        self._draw_deck(base_surf, self.treasure_deck, "Baralho de Tesouro", (250, 200))

        # Desenhar a mão do jogador
        self._draw_hand(base_surf)

    def _draw_deck(self, surface, deck, label, position):
        """Desenha um baralho com o nome e a quantidade de cartas restantes."""
        x, y = position
        card_back = pygame.Surface((100, 150))
        card_back.fill((0, 0, 128))  # Cor azul representando o verso
        pygame.draw.rect(card_back, BRANCO, card_back.get_rect(), 3)

        surface.blit(card_back, (x, y))

        # Texto do baralho
        label_surf = self.game.fonte.render(label, True, BRANCO)
        label_rect = label_surf.get_rect(midtop=(x + 50, y - 30))
        surface.blit(label_surf, label_rect)

        # Quantidade de cartas
        count_surf = self.game.fonte.render(f"{len(deck)} cartas", True, BRANCO)
        count_rect = count_surf.get_rect(midtop=(x + 50, y + 160))
        surface.blit(count_surf, count_rect)

    def _draw_hand(self, surface):
        """Desenha as cartas na mão do jogador."""
        x_start = 50  # Posição inicial na horizontal
        y_position = self.game.base_height - 160  # Altura fixa das cartas
        spacing = 120  # Espaçamento entre as cartas

        for i, card in enumerate(self.player.hand.cards):
            if card.image:
                card_image = pygame.transform.scale(card.image, (100, 150))
                card_rect = card_image.get_rect(topleft=(x_start + i * spacing, y_position))
                surface.blit(card_image, card_rect)
