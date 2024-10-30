# ClassesGameScript/classes/Monstro.gd
extends Node

class_name Monstro

var nivel: int
var forca: int
var tesouros: int
var fuga_especial: String
var maldicao_ao_perder: Maldicao
var condicoes_peculiares: Dictionary = {}

func enfrentar(jogador):
	pass

func aplicar_maldicao(jogador):
	pass
