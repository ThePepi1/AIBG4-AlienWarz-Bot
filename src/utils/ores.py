import heapq
from utils.vectors import Vectors
from utils.path import find_path_least_moves, get_path_length
from utils.logger import log

# energy to dig, weight, xp, energy gain
M_STATS = (5, 2, 10, 250) 
D_STATS = (6, 5, 25, 100)

def find_ores(me, board):
    ores = []
    for i in range(10):
        for j in range(10):
            if board[i][j][0] in "MD":
                type, dig, till_replantish = board[i][j].split("_")
                dig = int(dig)
                if dig == 0:
                    continue
                stats = M_STATS if type == "M" else D_STATS
                calculated_stats = calculate_stats(me, board, (i, j), dig, stats)
                if calculated_stats is None:
                    continue
                heapq.heappush(ores, calculated_stats)

    return ores



def calculate_stats( me, board, ore, dig, stats):
    x, y = ore
    best_path = None            # (path, moves, squeers, mining position)
    for vector in Vectors.all():
        new_x = x + vector[0]
        new_y = y + vector[1]
        if new_x < 0 or new_y < 0 or new_x >= 10 or new_y >= 10:
            continue
        if board[new_x][new_y][0] != "E":
            continue
        path = find_path_least_moves(me.position, (new_x, new_y), board)
        if path is None or len(path) == 0:
            continue
        path_length = get_path_length(me.position, path)
        if best_path is None or len(path) < best_path[1] or (len(path) == best_path[1] and path_length < best_path[2]):
            best_path = path, len(path), path_length, (new_x, new_y)
    if best_path is None:
        return None
    path, moves, squeers, mining_position = best_path
    DIG_ENERGY, WEIGHT, XP, ENERGY_GAIN = stats
    can_dig = min(8 // WEIGHT, dig)
    energy_to_dig = DIG_ENERGY * can_dig
    energy_to_get_to_ore = squeers
    energy_to_get_back = squeers * min(can_dig * WEIGHT + 1, 8)
    total_energy = energy_to_dig + energy_to_get_to_ore + energy_to_get_back 
    xp_gain = XP * can_dig
    how_good = xp_gain / moves
    return (-how_good, total_energy, path, ore, mining_position, can_dig)








def find_oponents_ores(him, base, board):
    ores = []
    for i in range(10):
        for j in range(10):
            if board[i][j][0] in "MD":
                type, dig, till_replantish = board[i][j].split("_")
                dig = int(dig)
                if dig == 0:
                    continue
                stats = M_STATS if type == "M" else D_STATS
                calculated_stats = calculate_op_stats(him, base, board, (i, j), dig, stats)
                if calculated_stats is None:
                    continue
                heapq.heappush(ores, calculated_stats)

    return ores



def calculate_op_stats( him, base, board, ore, dig, stats):
    x, y = ore
    best_path = None            # (path, moves, squeers, mining position)
    for vector in Vectors.all():
        new_x = x + vector[0]
        new_y = y + vector[1]
        if new_x < 0 or new_y < 0 or new_x >= 10 or new_y >= 10:
            continue
        if board[new_x][new_y][0] != "E":
            continue
        path = find_path_least_moves(him.position, (new_x, new_y), board)
        if path is None or len(path) == 0:
            continue
        path_length = get_path_length(him.position, path)
        if best_path is None or len(path) < best_path[1] or (len(path) == best_path[1] and path_length < best_path[2]):
            best_path = path, len(path), path_length, (new_x, new_y)
    if best_path is None:
        return None
    path, moves, squeers, mining_position = best_path
    path_to_base = find_path_least_moves(mining_position, base, board)
    if path_to_base is None:
        return None
    DIG_ENERGY, WEIGHT, XP, ENERGY_GAIN = stats
    can_dig = min(8 // WEIGHT, dig)
    energy_to_dig = DIG_ENERGY * can_dig
    energy_to_get_to_ore = squeers
    energy_to_get_back = squeers * min(can_dig * WEIGHT + 1, 8)
    total_energy = energy_to_dig + energy_to_get_to_ore + energy_to_get_back 
    xp_gain = XP * can_dig
    how_good = moves + can_dig + len(path_to_base)
    return (how_good, total_energy, path, ore, mining_position, can_dig, xp_gain)