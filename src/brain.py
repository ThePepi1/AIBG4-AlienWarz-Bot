from utils.path import find_path_least_moves
from state.game_state import GameState
from utils.path import get_path_length
from utils.ores import find_oponents_ores
from utils.logger import log
import heapq

EPSILON = 75

def should_block(state: GameState, additional_xp = 0):
    # return False
    our_xp = state.me().xp + additional_xp
    our_moves = len(state.path_to_opponent) + 3
    if our_xp <= state.opponent().xp:
        return False
    his_moves_to_base = len(find_path_least_moves(state.opponent().position, state.opponent_base(), state.board))
    if our_xp > state.opponent().xp and our_moves < his_moves_to_base:
        log(f"SHOULD BLOCK: our_xp {our_xp} his_xp {state.opponent().xp} our_moves {our_moves} his_moves {his_moves_to_base}")
        return True
    # we can block him before he reaches his base and we have more xp
    his_backpack = state.opponent().raw_diamonds, state.opponent().raw_minerals, \
                state.opponent().processed_diamonds, state.opponent().processed_minerals
    his_backpack_value = (his_backpack[0] + his_backpack[2]) * 25 + (his_backpack[1] + his_backpack[3]) * 10
    # if he can overpower us with his current backpack we should not block him
    if our_xp <= state.opponent().xp + his_backpack_value and our_moves >= his_moves_to_base:
        
        return False
    
    ores = find_oponents_ores(state.opponent(), state.opponent_base(), state.board)
    if len(ores) == 0:
        return True
    while ores:
        stats = heapq.heappop(ores)
        log(f"{stats}")
        xp = stats[6]
        moves = stats[0]
        if moves > our_moves:
            log(f"SHOULD BLOCK: xp {xp} moves {moves} our_xp {our_xp} our_moves {our_moves} Ores")
            return True
        if xp + state.opponent().xp >= our_xp:
            return False
    ### TODO: check factories
    return True


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
        energy_to_dig = 5
    else:
        energy_to_dig = 6
    length = get_path_length(state.me().position, path)
    log(f"FROM ENERGY TO MINE lenght {length} dig {dig} energy to dig {energy_to_dig} backpack {state.me().backpack_capacity}")

    energy = length * (1 + min(1 + state.me().backpack_capacity, 8)) + dig * energy_to_dig
    return  state.me().energy - energy - EPSILON