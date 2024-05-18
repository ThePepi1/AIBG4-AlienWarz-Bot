import heapq
import sys
import time
import json
from logger import log
from vectors import Vectors

from find_path import find_path_least_moves, generate_vector_board
from game_state.game_state import state
from game_state.createGraph import createpath
from moves import Moves

class Bot:
    def __init__(self):
        pass

# if __name__ == "__main__":
#     board = [
#         ['E', 'E', 'E', 'D', 'M', 'E', 'E', 'E', 'E', '2'],
#         ['E', 'D', 'E', 'E', 'E', 'M', 'M', 'M', 'E', 'E'],
#         ['E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'M', 'E'],
#         ['D', 'E', 'E', 'E', 'E', 'E', 'M', 'E', 'M', 'E'],
#         ['M', 'E', 'E', 'E', 'D', 'M', 'E', 'E', 'M', 'E'],
#         ['E', 'M', 'E', 'E', 'M', 'E', 'E', 'E', 'M', 'E'],
#         ['E', 'M', 'E', 'M', 'E', 'E', 'E', 'E', 'M', 'E'],
#         ['E', 'M', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E'],
#         ['E', 'E', 'M', 'M', 'M', 'M', 'M', 'E', 'E', 'E'],
#         ['1', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E']
#     ]
#     vector_board = generate_vector_board((9, 0), (1, 8), board)
#     for row in vector_board:
#         for cell in row:
#             print((str(cell.turns) + " " + "".join(map(Vectors.name, cell.from_vectors)) if not cell.blocked else "X") + "\t", end=" ")
#         print()
#     print(find_path_least_moves((9,0), (1,8), board))

class State:
    path_to_base = []
    ore_distances = None
    closest_ore = None
    path = None
    moves = []

def print_board():
    for row in state.board:
        s = ""
        for cell in row:
            s += cell[0] + " "
        log(s)

# def first_move():
#     his_base = state.opponent_base()
#     if his_base == (9,0):
#         State.factory = (8, 0)
#         State.me = (9, 1)
#         State.search = (8, 1)
#     else:
#         State.factory = (0, 8)
#         State.me = (1, 9)
#         State.search = (1, 8)
#     print_board()
#     log(str(state.my_base()) + " " + str(his_base) + " " + str(State.factory) + " " + str(State.me) + " " + str(State.search))
#     State.path_to_base = find_path_least_moves(state.my_base(), State.search, state.board)
#     State.ore_distances = createpath()
#     # log(f"State heap: {State.ore_distances}")
#     _, State.path, State.closest_ore = heapq.heappop(State.ore_distances)
#     log(str(State.closest_ore) +" " + str(State.path) +" " +  str(State.path_to_base))
#     for x, y in State.path:
#         State.moves.append([Moves.move, x, y])
#     for _ in range(4):
#         State.moves.append([Moves.mine, State.closest_ore[0], State.closest_ore[1]])
#     p = State.path[::-1]
#     p.pop(0)
#     p.append(state.my_base())
#     for x, y in p:
#         log(f"move {x} {y}")
#         State.moves.append([Moves.move, x, y])
#     State.moves.append([Moves.convert, (0, 0), (0, 0), (0, 4)])
#     for x, y in State.path_to_base:
#         State.moves.append([Moves.move, x, y])
#     State.moves.append([Moves.build, State.factory[0], State.factory[1]])
#     State.moves.append([Moves.move, State.me[0], State.me[1]])

def first_move():
    his_base = state.opponent_base()
    if his_base == (9,0):
        State.factory = (8, 0)
        State.me = (9, 1)
        State.search = (8, 1)
    else:
        State.factory = (0, 8)
        State.me = (1, 9)
        State.search = (1, 8)
    print_board()
    log(str(state.my_base()) + " " + str(his_base) + " " + str(State.factory) + " " + str(State.me) + " " + str(State.search))
    State.path_to_base = find_path_least_moves(state.my_base(), State.search, state.board)
    State.ore_distances = createpath()




def calculate_move():
    pass

def execute():
    move = State.moves.pop(0)
    move[0](*move[1:])

while True:
    line = sys.stdin.readline().strip()
    state.update(line)
    # state.save() 
    if(state.turn < 2):
        first_move()
    log(f"{len(State.moves)}")
    if len(State.moves) == 0:
        calculate_move()
    execute()
    # print("rest", flush=True)


