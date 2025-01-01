# classes/card.py

class Card:
    """Classe base para todas as cartas."""
    def __init__(self, nome, descricao, imagem=None):
        """
        nome: Nome da carta
        descricao: Descrição ou efeito da carta
        imagem: Caminho para a imagem da carta (opcional)
        """
        self.nome = nome
        self.descricao = descricao
        self.imagem = imagem

    def __str__(self):
        """Representação textual da carta."""
        return f"{self.nome}: {self.descricao}"


class MonsterCard(Card):
    """Representa uma carta de monstro."""
    def __init__(self, nome, nivel, tesouros, texto_derrota, texto_vitoria, imagem=None):
        """
        nome: Nome do monstro
        nivel: Nível do monstro
        tesouros: Quantidade de tesouros que o monstro concede ao ser derrotado
        texto_derrota: Efeito ou penalidade ao perder para o monstro
        texto_vitoria: Recompensa adicional ao vencer o monstro
        imagem: Caminho para a imagem da carta (opcional)
        """
        super().__init__(nome, f"Monstro Nível {nivel}", imagem)
        self.nivel = nivel
        self.tesouros = tesouros
        self.texto_derrota = texto_derrota
        self.texto_vitoria = texto_vitoria

    def aplicar_efeitos_derrota(self, jogador):
        """Aplica os efeitos de derrota ao jogador."""
        print(f"{jogador.name} sofreu derrota contra {self.nome}: {self.texto_derrota}")

    def aplicar_efeitos_vitoria(self, jogador):
        """Aplica os efeitos de vitória ao jogador."""
        print(f"{jogador.name} venceu {self.nome} e recebeu: {self.texto_vitoria}")


class TreasureCard(Card):
    """Representa uma carta de tesouro."""
    def __init__(self, nome, bonus, descricao, imagem=None):
        """
        nome: Nome do tesouro
        bonus: Bônus que o tesouro concede ao jogador
        descricao: Descrição ou efeito do tesouro
        imagem: Caminho para a imagem da carta (opcional)
        """
        super().__init__(nome, descricao, imagem)
        self.bonus = bonus

    def aplicar_bonus(self, jogador):
        """Aplica o bônus ao jogador."""
        print(f"{jogador.name} equipou {self.nome} e ganhou +{self.bonus} de poder.")


class CurseCard(Card):
    """Representa uma carta de maldição."""
    def __init__(self, nome, efeitos, imagem=None):
        """
        nome: Nome da maldição
        efeitos: Descrição do efeito da maldição
        imagem: Caminho para a imagem da carta (opcional)
        """
        super().__init__(nome, efeitos, imagem)
        self.efeitos = efeitos

    def aplicar_maldicao(self, jogador):
        """Aplica os efeitos da maldição ao jogador."""
        print(f"{jogador.name} foi amaldiçoado: {self.efeitos}")
