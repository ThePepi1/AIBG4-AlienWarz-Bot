from state.game_state import GameState
import heapq
from moves import Moves
from utils.logger import log
from utils.path import find_path_least_moves
import brain
import time

class Bot:
    REST = 0
    GO_TO_MINE = 1
    GO_TO_HOME = 2
    MINE = 3
    BLOCK = 4
    CONVERT = 5
    NONE = 6
    FACTORY = 7
    POSITION = 8
    def __init__(self):
        self.state = GameState()
        self.current_action = Bot.NONE
        self.mine = None
        self.mine_number = 0
        self.target = None
        self.path = None

    def make_move(self, new_state_json):

        log(f"Start make move")
        start = time.perf_counter()
        self.state.update(new_state_json)
        end = time.perf_counter()
        log(f"update time {end - start}")
        if self.current_action == Bot.NONE:
            self.current_action = Bot.GO_TO_MINE
            self.state.find_ores()
            stats = heapq.heappop(self.state.ores)
            log(f"best path {stats}")
            self.mine = stats[3]
            self.target = stats[4]
            self.mine_number = stats[5]
            self.path = stats[2]
            x,y = self.path.pop(0)
            Moves.move(x,y, self.state.me())
            if len(self.path) == 0:
                self.current_action = Bot.MINE
            return
        if self.current_action == Bot.GO_TO_MINE:
            x, y = self.path.pop(0)
            Moves.move(x, y, self.state.me())
            if len(self.path) == 0:
                self.current_action = Bot.MINE
            return
        if self.current_action == Bot.MINE:
            x, y = self.mine
            Moves.mine(x, y)
            self.mine_number -= 1
            if self.mine_number == 0:
                self.current_action = Bot.GO_TO_HOME
                self.path = find_path_least_moves(self.state.me().position, self.state.my_base(), self.state.board)
            return
        if self.current_action == Bot.GO_TO_HOME:
            x, y = self.path.pop(0)
            Moves.move(x, y, self.state.me())
            if len(self.path) == 0:
                self.current_action = Bot.CONVERT
            return
        if self.current_action == Bot.CONVERT:
            # calucate how much energy we need to convert
            if brain.should_block(self.state):
                log("should block")
                energy = brain.energy_to_block(self.state)
                if energy > 0:
                    Moves.convert((0, 0), (0, 0), (self.state.me().raw_diamonds, self.state.me().raw_minerals))
                    self.current_action = Bot.BLOCK
                    self.path = self.state.path_to_opponent
                elif brain.can_gain_energy(self.state) > -energy:
                    diamonds, minerals = brain.how_much_energy_to_convert(self.state, energy)
                    Moves.convert((0, 0), (diamonds, minerals), (self.state.me().raw_diamonds - diamonds, self.state.me().raw_minerals - minerals))
                    self.current_action = Bot.BLOCK
                    self.path = self.state.path_to_opponent
                else:
                    Moves.convert((0, 0), (self.state.me().raw_diamonds, self.state.me().raw_minerals), (0, 0))
                    self.current_action = Bot.GO_TO_MINE
                    stats = heapq.heappop(self.state.ores)
                    self.mine = stats[3]
                    self.target = stats[4]
                    self.mine_number = stats[5]
                    self.path = stats[2]
            else:
                log("should not block")
                self.current_action = Bot.GO_TO_MINE
                self.state.find_ores()
                stats = heapq.heappop(self.state.ores)
                self.mine = stats[3]
                self.target = stats[4]
                self.mine_number = stats[5]
                self.path = stats[2]
                energy = brain.energy_to_mine(self.state, self.path, self.mine_number, self.mine)
                if energy > 0:
                    Moves.convert((0, 0), (0, 0), (self.state.me().raw_diamonds, self.state.me().raw_minerals))
                else:
                    diamonds, minerals = brain.how_much_energy_to_convert(self.state, energy)
                    Moves.convert((0, 0), (diamonds, minerals), (self.state.me().raw_diamonds - diamonds, self.state.me().raw_minerals - minerals))
            return
        if self.current_action == Bot.BLOCK:
            x, y = self.path.pop(0)
            Moves.move(x, y, self.state.me())
            if len(self.path) == 0:
                self.current_action = Bot.FACTORY
            return
        if self.current_action == Bot.FACTORY:
            x, y = self.state.factory
            Moves.build(x, y)
            self.current_action = Bot.POSITION
            return
        if self.current_action == Bot.POSITION:
            x, y = self.state.me_block
            Moves.move(x, y, self.state.me())
            self.current_action = Bot.REST
            return
        Moves.rest()
        #print("rest", flush=True)