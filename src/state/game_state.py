from state.player import Player
import json
from utils.ores import find_ores
from utils.path import find_path_least_moves
from utils.logger import log 

class GameState:
    def __init__(self) -> None:
        self.turn = 0
        self.firstPlayerTurn = True
        self.board = None
        self.player1 = Player()
        self.player2 = Player()
        self.ores = []
        self.path_to_opponent = None
        self.search = None
        self.factory = None
        self.me_block = None
        

    def update(self, json_data):
        parsed_data = json.loads(json_data)
        self.turn = parsed_data["turn"]
        self.board = parsed_data["board"]
        self.firstPlayerTurn = parsed_data["firstPlayerTurn"]
        self.player1.update(parsed_data["player1"])
        self.player2.update(parsed_data["player2"])
        if self.path_to_opponent is None:
            self.search, self.factory, self.me_block = self.oponent_block()
            self.path_to_opponent = find_path_least_moves(self.my_base(), self.search, self.board)
        log(f"{self.turn} {self.firstPlayerTurn} {self.me() == self.player2} {self.my_base()} {self.opponent_base()} {self.oponent_block()}")

    def find_ores(self):
        self.ores = find_ores(self.me(), self.board)

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
        
    def oponent_block(self):
        if self.opponent() == self.player1:
            factory = (8, 0)
            me = (9, 1)
            search = (8, 1)
            return search, factory, me
        else:
            factory = (0, 8)
            me = (1, 9)
            search = (1, 8)
            return search, factory, me

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