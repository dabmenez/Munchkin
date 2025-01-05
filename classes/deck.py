from classes.card import MonsterCard, CurseCard, TreasureCard
from classes.card import Card

class Deck:
    """Representa um baralho genérico."""
    def __init__(self):
        self.cards = []

    def add_card(self, card):
        self.cards.append(card)

    def shuffle(self):
        import random
        random.shuffle(self.cards)

    def draw_card(self):
        return self.cards.pop() if self.cards else None

    def __len__(self):
        return len(self.cards)

class DoorDeck(Deck):
    def __init__(self):
        super().__init__()
        self._create_door_cards()
        self.shuffle()

    def _create_door_cards(self):
        # Adicionando monstros
        self.add_card(MonsterCard(
            nome="3,872 Orcs",
            nivel=10,
            tesouros=3,
            texto_derrota="Jogue um dado. Com 2 ou menos, eles o pisoteiam até a morte. Caso contrário, perca tantos níveis quanto o dado mostrar.",
            texto_vitoria="",
            imagem="assets/cards/Porta/3.872 Orcs.jpg"
        ))

        self.add_card(MonsterCard(
            nome="Amazona",
            nivel=8,
            tesouros=2,
            texto_derrota="Você levou um chute na bunda de uma mulher. Perca sua(s) classe(s). Se já não tinha Classe, perca 3 níveis.",
            texto_vitoria="",
            imagem="assets/cards/Porta/Amazon.jpg"
        ))

        self.add_card(MonsterCard(
            nome="Tia Paladina",
            nivel=18,
            tesouros=4,
            texto_derrota="Perde a armadura. Perder três níveis devido a um espancamento quase fatal.",
            texto_vitoria="",
            imagem="assets/cards/Porta/Auntie Paladin.jpg"
        ))

        self.add_card(MonsterCard(
            nome="Bullrog",
            nivel=18,
            tesouros=5,
            texto_derrota="Você é esfolado até a morte.",
            texto_vitoria="",
            imagem="assets/cards/Porta/Bullrog.jpeg"
        ))

        self.add_card(MonsterCard(
            nome="Lodo Babando",
            nivel=1,
            tesouros=1,
            texto_derrota="Descarte os calçados que você está usando. Perca um nível se não tiver calçados.",
            texto_vitoria="",
            imagem="assets/cards/Porta/Drooling Slime.jpg"
        ))

        self.add_card(MonsterCard(
            nome="Pé Grande",
            nivel=12,
            tesouros=3,
            texto_derrota="Pisoteia você e come seu chapéu. Perca o capacete que você estava usando.",
            texto_vitoria="",
            imagem="assets/cards/Porta/Bigfoot.jpg"
        ))

        self.add_card(CurseCard(
            nome="Mude de Sexo",
            efeitos="-5 no seu próximo combate devido à distração. Depois disso, não há mais penalidade.",
            imagem="assets/cards/Porta/Change Sex.jpeg"
        ))

        self.add_card(CurseCard(
            nome="Amnésia Temporária",
            efeitos="Esqueça sua(s) Classe(s) e Raça(s) até matar um monstro ou ajudar a matá-lo.",
            imagem="assets/cards/Porta/Temporary Amnesia.jpg"
        ))

        self.add_card(MonsterCard(
            nome="Gazebo",
            nivel=8,
            tesouros=2,
            texto_derrota="Não faça nada. Apenas olhe com medo.",
            texto_vitoria="Ganhe 2 tesouros.",
            imagem="assets/cards/Porta/Gazebo.jpeg"
        ))

        self.add_card(MonsterCard(
            nome="Pukaku",
            nivel=6,
            tesouros=2,
            texto_derrota="Perca 1 nível e um item pequeno.",
            texto_vitoria="Você coleta 2 tesouros.",
            imagem="assets/cards/Porta/Pukaku.jpeg"
        ))

class TreasureDeck(Deck):
    def __init__(self):
        super().__init__()
        self._create_treasure_cards()
        self.shuffle()

    def _create_treasure_cards(self):
        # Adicionando tesouros
        self.add_card(TreasureCard(
            nome="Espada Larga",
            bonus=3,
            descricao="Utilizável apenas por fêmeas.",
            imagem="assets/cards/Tesouro/Broad Sword.jpeg"
        ))

        self.add_card(TreasureCard(
            nome="Ralador de Queijo da Paz",
            bonus=3,
            descricao="Utilizável apenas por Clérigos.",
            imagem="assets/cards/Tesouro/Cheese Grater Of Peace.jpeg"
        ))

        self.add_card(TreasureCard(
            nome="Sanduíche de Limburger e Anchova",
            bonus=3,
            descricao="Utilizável apenas por Mercenários.",
            imagem="assets/cards/Tesouro/Limburger And Anchovy Sandwich.jpeg"
        ))

        self.add_card(TreasureCard(
            nome="Poção Explosiva Congelante",
            bonus=3,
            descricao="Usar durante qualquer combate. +3 para qualquer lado.",
            imagem="assets/cards/Tesouro/Freezing Explosive Potion.jpeg"
        ))

        self.add_card(TreasureCard(
            nome="Dado Carregado",
            bonus=0,
            descricao="Jogue após lançar o dado para escolher o resultado.",
            imagem="assets/cards/Tesouro/Loaded Die.jpeg"
        ))

        self.add_card(TreasureCard(
            nome="Poção da Invisibilidade",
            bonus=0,
            descricao="Use quando sua fuga falhar. Você escapa automaticamente.",
            imagem="assets/cards/Tesouro/Invisibility Potion.jpeg"
        ))

        self.add_card(TreasureCard(
            nome="Joelheiras de Fascínio",
            bonus=0,
            descricao="Nenhum jogador de nível superior ao seu pode recusar seu pedido de ajuda contra um monstro.",
            imagem="assets/cards/Tesouro/Kneepads Of Allure.jpeg"
        ))

        self.add_card(TreasureCard(
            nome="Armadura de Flamengante",
            bonus=4,
            descricao="Oferece proteção extra contra monstros do tipo fogo.",
            imagem="assets/cards/Tesouro/Flaming Armor.jpeg"
        ))

        self.add_card(TreasureCard(
            nome="Poção de Halitose",
            bonus=2,
            descricao="Causa danos ao monstro. Usável uma vez.",
            imagem="assets/cards/Tesouro/Potion Of Halitosis.jpeg"
        ))

        self.add_card(TreasureCard(
            nome="Anel de Desejo",
            bonus=0,
            descricao="Cancela qualquer maldição.",
            imagem="assets/cards/Tesouro/Wishing Ring.jpeg"
        ))
