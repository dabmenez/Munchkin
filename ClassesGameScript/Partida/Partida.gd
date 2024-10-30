# ClassesGameScript/partida/Partida.gd
extends Node

class_name Partida

var jogadores: Array = []
var baralho_portas: Array = []
var baralho_tesouros: Array = []
var turno_atual: Jogador
var estado: String  # Ex: "Em Andamento", "Finalizada"

func proximo_turno():
	pass

func distribuir_cartas():
	pass

func iniciar_partida():
	pass

func finalizar_partida():
	pass

func verificar_vencedor():
	pass
