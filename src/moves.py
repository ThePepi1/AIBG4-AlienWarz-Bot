from logger import log

from game_state.game_state import state
class Moves:
    @staticmethod
    def move(x, y):
        if state.me().isDazed():
            dx = x - state.me().position[0]
            dy = y - state.me().position[1]
            x = state.me().position[0] - dx
            y = state.me().position[1] - dy
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
