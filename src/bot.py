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
            if Moves.check_if_can_move(self.state.me().position, self.path[0], self.state.board, self.state.my_base()):
                x,y = self.path.pop(0)
                Moves.move(x,y, self.state.me())
            else:
                log("CANT MOVE TO MINE")
                Moves.rest()
            if len(self.path) == 0:
                self.current_action = Bot.MINE
            return
        if self.current_action == Bot.GO_TO_MINE:
            ### TODO: check if we have enough energy to move
            if Moves.check_if_can_move(self.state.me().position, self.path[0], self.state.board, self.state.my_base()):
                x,y = self.path.pop(0)
                Moves.move(x,y, self.state.me())
            else:
                log("CANT MOVE TO MINE")
                Moves.rest()
            if len(self.path) == 0:
                self.current_action = Bot.MINE
            return
        if self.current_action == Bot.MINE:
            ### TODO: check if we have enough energy to mine
            if Moves.check_if_can_mine(self.mine, self.state.board):
                x, y = self.mine
                Moves.mine(x, y, self.state.me())
                self.mine_number -= 1
                if self.mine_number == 0:
                    self.current_action = Bot.GO_TO_HOME
                    self.path = find_path_least_moves(self.state.me().position, self.state.my_base(), self.state.board)
                return
            else:
                log("CANT MINE")
                self.current_action = Bot.GO_TO_HOME
                self.path = find_path_least_moves(self.state.me().position, self.state.my_base(), self.state.board)
                if Moves.check_if_can_move(self.state.me().position, self.path[0], self.state.board, self.state.my_base()):
                    x,y = self.path.pop(0)
                    Moves.move(x,y, self.state.me())
                else:
                    log("CANT MOVE HOME")
                    Moves.rest()
                if len(self.path) == 0:
                    self.current_action = Bot.CONVERT
                return
                
        if self.current_action == Bot.GO_TO_HOME:
            ### TODO: check if we have enough energy to move
            log(f"{(self.state.me().position, self.path, self.state.board, self.state.my_base())}")
            if self.path is None:
                self.path = find_path_least_moves(self.state.me().position, self.state.my_base(), self.state.board)
            log(f"{self.path}")
            if len(self.path) > 0 and Moves.check_if_can_move(self.state.me().position, self.path[0], self.state.board, self.state.my_base()):
                x,y = self.path.pop(0)
                Moves.move(x,y, self.state.me())
            else:
                log("CANT MOVE HOME")
                Moves.rest()
            if len(self.path) == 0:
                self.current_action = Bot.CONVERT
            return
        if self.current_action == Bot.CONVERT:
            def go_to_mining(convert=True):
                self.current_action = Bot.GO_TO_MINE
                self.state.find_ores()
                stats = heapq.heappop(self.state.ores)
                self.mine = stats[3]
                self.target = stats[4]
                self.mine_number = stats[5]
                self.path = stats[2]
                if not convert:
                    return
                energy = brain.energy_to_mine(self.state, self.path, self.mine_number, self.mine)
                log(f"energy to mine {energy}, my energy {self.state.me().energy}")
                if energy > 0:
                    Moves.convert((0, 0), (0, 0), (self.state.me().raw_diamonds, self.state.me().raw_minerals), self.state.me())
                else:
                    diamonds, minerals = brain.how_much_energy_to_convert(self.state, energy)
                    Moves.convert((0, 0), (diamonds, minerals), (self.state.me().raw_diamonds - diamonds, self.state.me().raw_minerals - minerals), self.state.me())
                return
            energy = brain.energy_to_block(self.state)
            diamonds, minerals = brain.how_much_energy_to_convert(self.state, energy)  
            xp_to_buy = (self.state.me().raw_diamonds - diamonds) * 25 + (self.state.me().raw_minerals - minerals) * 10
            if energy > 0:
                
                #### TODO: check if we can block him
                if brain.should_block(self.state, xp_to_buy):
                    Moves.convert((0, 0), (0, 0), (self.state.me().raw_diamonds, self.state.me().raw_minerals), self.state.me())
                    log("should block")
                    log(f"{self.state.opponent()}")
                    self.current_action = Bot.BLOCK
                    self.path = self.state.path_to_opponent
                else:
                    log("should not block")
                    go_to_mining()
            elif brain.can_gain_energy(self.state) > -energy:
                
                 ### TODO: check if we can block him
                if brain.should_block(self.state, xp_to_buy):
                    log("should block")
                    Moves.convert((0, 0), (diamonds, minerals), (self.state.me().raw_diamonds - diamonds, self.state.me().raw_minerals - minerals), self.state.me())
                    self.current_action = Bot.BLOCK
                    self.path = self.state.path_to_opponent
                else:
                    log("should not block")
                    go_to_mining()
            else:
                Moves.convert((0, 0), (self.state.me().raw_diamonds, self.state.me().raw_minerals), (0, 0), self.state.me())
                go_to_mining(False)
                
            return
        if self.current_action == Bot.BLOCK:
            if Moves.check_if_can_move(self.state.me().position, self.path[0], self.state.board, self.state.my_base()):
                x,y = self.path.pop(0)
                Moves.move(x,y, self.state.me())
            else:
                log("CANT MOVE BLOCK")
                Moves.rest()
            if len(self.path) == 0:
                self.current_action = Bot.FACTORY
            return
        if self.current_action == Bot.FACTORY:
            if self.state.board[self.state.factory[0]][self.state.factory[1]] == "E":
                x, y = self.state.factory
                Moves.build(x, y)
            else:
                self.current_action = Bot.POSITION
                if Moves.check_if_can_move(self.state.me().position, self.state.me_block, self.state.board, self.state.my_base()):
                    x,y = self.state.me_block
                    Moves.move(x,y, self.state.me())
                    self.current_action = Bot.REST
                else:
                    Moves.rest()
            return
        if self.current_action == Bot.POSITION:
            if Moves.check_if_can_move(self.state.me().position, self.state.me_block, self.state.board):
                x,y = self.state.me_block
                Moves.move(x,y, self.state.me())
                self.current_action = Bot.REST
            else:
                Moves.rest()
            return
        Moves.rest()
        #print("rest", flush=True)