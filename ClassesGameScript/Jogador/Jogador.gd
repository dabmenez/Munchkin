# ClassesGameScript/jogador/Jogador.gd
extends Node

class_name Jogador

var nome: String
var nivel: int
var sexo: String
var raca: Array = []
var classe: Array = []
var itens: Array = []
var ouro: int
var bonus_total: int
var modificadores: Array = []
var municoes: Array = []

func comprar_carta(baralho):
	pass

func receber_carta(carta):
	pass

func jogar_carta_da_mao(carta):
	pass

func equipar_item(item):
	pass

func desequipar_item(item):
	pass

func vender_itens(itens):
	pass

func subir_nivel(niveis):
	pass

func descer_nivel(niveis):
	pass

func calcular_forca_total():
	pass

func fugir(monstro) -> bool:
	pass

func ajudar_outro_jogador(jogador):
	pass

func sofrer_maldicao(maldicao):
	pass

func trocar_cartas_com_jogador(jogador, cartas_oferecidas, cartas_recebidas):
	pass

func usar_item_usavel(item):
	pass

func alterar_sexo():
	pass
