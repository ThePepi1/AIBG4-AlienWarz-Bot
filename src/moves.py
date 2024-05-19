from utils.logger import log

class Moves:
    @staticmethod
    def move(x, y, me):
        if me.isDazed():
            log("dazed")
            dx = x - me.position[0]
            dy = y - me.position[1]
            x = me.position[0] - dx
            y = me.position[1] - dy
        log(f"move {x} {y}")
        dx = abs(me.position[0] - x)
        dy = abs(me.position[1] - y)
        de = (dx+dy) * min(1 + me.backpack_capacity, 8)
        me.energy -= de
        log(f"energy change {de}")
        print(f"move {x} {y}", flush=True)
    @staticmethod
    def rest():
        log("rest")
        print("rest", flush=True)
    @staticmethod
    def mine(x, y, me):
        me.energy -= 6
        log(f"mine {x} {y}")
        print(f"mine {x} {y}", flush=True)
    @staticmethod
    def build(x, y):
        log(f"build {x} {y}")
        print(f"build {x} {y}", flush=True)
    @staticmethod
    def convert(coins, energy, xp, me):
        me.energy += energy[0] * 100 + energy[1] * 250
        log(f"conv {coins[0]} diamond {coins[1]} mineral to coins, {energy[0]} diamond {energy[1]} mineral to energy, {xp[0]} diamond {xp[1]} mineral to xp")
        print(f"conv {coins[0]} diamond {coins[1]} mineral to coins, {energy[0]} diamond {energy[1]} mineral to energy, {xp[0]} diamond {xp[1]} mineral to xp", flush=True)
    @staticmethod
    def check_if_can_move(from_cell, to_cell, board, my_base):
        dx = sgn(to_cell[0] - from_cell[0] )
        dy = sgn(to_cell[1] - from_cell[1])
        x, y = from_cell
        while x != to_cell[0] or y != to_cell[1]:
            x += dx
            y += dy
            if board[x][y] != "E" and (x, y) != my_base:
                    return False
        return True
    @staticmethod
    def check_if_can_mine(ore, board):
        x, y = ore
        if board[x][y][0] not in "MD":
            return False
        t, d, r = board[x][y].split("_")
        if d == "0":
            return False
        return True

def sgn(value):
    if value == 0:
        return 0
    if value > 0:
        return 1
    return -1