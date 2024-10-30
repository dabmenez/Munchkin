# ClassesGameScript/jogador/Usuario.gd
extends Jogador

var jogando: bool = false

func iniciar_jogo():
	jogando = true

func encerrar_jogo():
	jogando = false
