from game_state.player import Player
import json
import os
import logger
class GameState:
    def __init__(self) -> None:
        self.turn = 0
        self.firstPlayerTurn = True
        self.board = None
        self.player1 = Player()
        self.player2 = Player()

    def update(self, json_data):
        parsed_data = json.loads(json_data)
        self.turn = parsed_data["turn"]
        self.board = parsed_data["board"]
        self.firstPlayerTurn = parsed_data["firstPlayerTurn"]
        self.player1.update(parsed_data["player1"])
        self.player2.update(parsed_data["player2"])

    def me(self):
        return self.player1 if self.firstPlayerTurn else self.player2

    def opponent(self):
        return self.player2 if self.firstPlayerTurn else self.player1
    
    def my_base(self):
        if self.firstPlayerTurn:
            return (9, 0)
        else:
            return (0, 9)
    def opponent_base(self):
        if self.firstPlayerTurn:
            return (0, 9)
        else:
            return (9, 0)

    def __str__(self) -> str:
        return json.dumps({
            "turn": self.turn,
            "board": self.board,
            "player1": json.loads(str(self.player1)),
            "player2": json.loads(str(self.player2))
        })
    # def save(self):
    #     folder = "logs"
    #     if not os.path.exists(folder):
    #         os.makedirs(folder)
    #     name = f"game_state_{self.me().name}_{self.turn}.json"
    #     with open(os.path.join(folder, name), "w") as f:
    #         f.write(str(self))

state = GameState()