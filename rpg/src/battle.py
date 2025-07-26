class Battle:
    def __init__(self, player, enemy):
        self.player = player
        self.enemy = enemy
        self.turn = "player"

    def player_turn(self):
        # Lógica del turno del jugador
        pass

    def enemy_turn(self):
        # Lógica del turno del enemigo
        pass

    def battle(self):
        while self.player.is_alive() and self.enemy.is_alive():
            if self.turn == "player":
                self.player_turn()
                self.turn = "enemy"
            else:
                self.enemy_turn()
                self.turn = "player"
