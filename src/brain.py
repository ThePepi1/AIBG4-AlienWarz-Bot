from utils.path import find_path_least_moves
from state.game_state import GameState
from utils.path import get_path_length

EPSILON = 50

def should_block(state: GameState):
    return False
    moves = len(state.path_to_opponent) + 3
    if state.me().xp > state.opponent().xp:
        return True
    return False

def energy_to_block(state: GameState):
    length = get_path_length(state.me().position, state.path_to_opponent)
    energy = length + 1
    return state.me().energy - energy

def can_gain_energy(state: GameState):
    return state.me().raw_diamonds * 100 + state.me().raw_minerals * 250

def how_much_energy_to_convert(state: GameState, energy):
    minerals = state.me().raw_minerals
    while minerals > 0 and energy < 0:
        energy += 250
        minerals -= 1
    if energy > 0:
        return (0, state.me().raw_minerals - minerals)
    diamonds = state.me().raw_diamonds
    while diamonds > 0 and energy < 0:
        energy += 100
        diamonds -= 1
    if energy > 0:
        return (state.me().raw_diamonds - diamonds, state.me().raw_minerals - minerals)
    return (0, 0)
    
def energy_to_mine(state: GameState, path, dig, ore):
    x, y = ore
    if state.board[x][y][0] == "M":
        energy = 5
        weight = 2
    else:
        weight = 5
        energy = 6
    length = get_path_length(state.me().position, path)
    energy = length * (1 + 1 + dig * weight) + dig * energy
    return  state.me().energy - energy - EPSILON