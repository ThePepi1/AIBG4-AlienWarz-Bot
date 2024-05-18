from utils.logger import log

class Moves:
    @staticmethod
    def move(x, y, me):
        if me.isDazed():
            dx = x - me().position[0]
            dy = y - me().position[1]
            x = me().position[0] - dx
            y = me().position[1] - dy
        log(f"move {x} {y}")
        print(f"move {x} {y}", flush=True)
    @staticmethod
    def rest():
        log("rest")
        print("rest", flush=True)
    @staticmethod
    def mine(x, y):
        log(f"mine {x} {y}")
        print(f"mine {x} {y}", flush=True)
    @staticmethod
    def build(x, y):
        log(f"build {x} {y}")
        print(f"build {x} {y}", flush=True)
    @staticmethod
    def convert(coins, energy, xp):
        log(f"conv {coins[0]} diamond {coins[1]} mineral to coins, {energy[0]} diamond {energy[1]} mineral to energy, {xp[0]} diamond {xp[1]} mineral to xp")
        print(f"conv {coins[0]} diamond {coins[1]} mineral to coins, {energy[0]} diamond {energy[1]} mineral to energy, {xp[0]} diamond {xp[1]} mineral to xp", flush=True)
    @staticmethod
    def check_if_can_move(from_cell, to_cell, board, my_base):
        dx = to_cell[0] - from_cell[0]
        dy = to_cell[1] - from_cell[1]
        x, y = from_cell
        while x != to_cell[0] or y != to_cell[1]:
            x += dx
            y += dy
            if board[x][y] != "E" and x != my_base[0] and y != my_base[1]:
                    return False
        return True