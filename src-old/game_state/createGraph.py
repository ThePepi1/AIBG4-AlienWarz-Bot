from game_state import game_state
from logger import log
from game_state import heap
from find_path import find_path_least_moves
from vectors import Vectors
import heapq
from brain import Brain

def createpath():
    ores = findOres()
    # log(f"Ores: {ores}")
    ores_with_lenght = []
    for ore in ores:
        best = None
        for vector in Vectors.all():
            x, y = ore
            x += vector[0]
            y += vector[1]
            if x < 0 or x >= 10 or y < 0 or y >= 10:
                continue
            if game_state.state.board[x][y] != "E":
                continue
            path = find_path_least_moves(game_state.state.my_base(), (x, y), game_state.state.board)
            # log(f"Path: {path} for ore {ore}")
            if path is None:
                continue
            if best is None:
                best = path
                continue
            if len(path) < len(best):
                best = path
        if best is None:
            continue
        heapq.heappush(ores_with_lenght, (len(best), Brain.get_path_length(best), best, ore))
    # ores_with_lenght.sort()
    # log(f"Ores with length: {ores_with_lenght}")
    return ores_with_lenght

def findOres():
    ors = []
    for i in range(10):
        for j in range(10):
            if game_state.state.board[i][j].startswith("M"):
                ors.append((i, j))
    return ors







