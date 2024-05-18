from game_state.game_state import state
from logger import log
from vectors import Vectors

class Cache:
    vector_board = None


def find_path_least_moves(from_cell, to_cell, board, force_regenerate=False):
    if Cache.vector_board is None or force_regenerate:
        Cache.vector_board = generate_vector_board(from_cell, to_cell, board)
    vector_board = Cache.vector_board
    path = []
    x, y = to_cell
    direction = None
    while (x, y) != from_cell:
        best = None
        for vector in vector_board[x][y].from_vectors:
            new_x, new_y = x - vector[0], y - vector[1]
            if best is None:
                best = new_x, new_y, vector
                continue
            # check for new best
            if vector_board[new_x][new_y].turns < vector_board[best[0]][best[1]].turns:
                best = new_x, new_y, vector
            elif vector_board[new_x][new_y].turns == vector_board[best[0]][best[1]].turns and vector == direction:
                best = new_x, new_y, vector
        if best is None:
            return None
        if direction is None or direction != best[2]:
            direction = best[2]
            path.append((x, y)) 
        x, y = best[0], best[1]
        # best = None
        # for vector in vector_board[x][y].from_vectors:
        #     new_x, new_y = x - vector[0], y - vector[1]
        #     turns = vector_board[new_x][new_y].turns
        #     if direction is None:
        #         direction = vector
        #     if vector != direction:
        #         turns += 1
        #     if best is None:
        #         best = new_x, new_y, turns, vector
        #         continue
        #     if turns < best[2]:
        #         best = new_x, new_y, turns, vector
        #         direction = vector
        #     elif (turns == best[2] and vector == direction):
        #         best = new_x, new_y, turns, vector
        # if best is None:
        #     return None
        
        # if best[2] != vector_board[x][y].turns:
        #     path.append((best[0], best[1]))
        
        # x, y = best[0], best[1]
    return path[::-1]

class VectorCell:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.from_vectors = set()
        self.turns = 0
        self.visited = False
        self.blocked = False
    def __str__ (self):
        return f"{self.turns}"

def generate_vector_board(start, end, board):
    start_x, start_y = start
    vector_board = [[VectorCell(i, j) for j in range(len(board))] for i in range(len(board))]
    queue = [(start_x, start_y)]
    vector_board[start_x][start_y].visited = True
    vector_board[start_x][start_y].from_vectors = Vectors.all()
    while queue:
        x, y = queue.pop(0)
        for vector in Vectors.all():
            if Vectors.oposite(vector) in vector_board[x][y].from_vectors and (x, y) != start:
                continue
            new_x, new_y = x + vector[0], y + vector[1]
            if 0 <= new_x < len(board) and 0 <= new_y < len(board):
                if board[new_x][new_y] != "E" and (new_x, new_y) != end:
                    vector_board[new_x][new_y].blocked = True
                    continue
                vector_board[new_x][new_y].from_vectors.add(vector)
                if vector in vector_board[x][y].from_vectors:
                    if vector_board[new_x][new_y].turns == 0:
                        vector_board[new_x][new_y].turns = vector_board[x][y].turns
                    else:
                        vector_board[new_x][new_y].turns = min(vector_board[x][y].turns, vector_board[new_x][new_y].turns)
                else:
                    if vector_board[new_x][new_y].turns == 0:
                        vector_board[new_x][new_y].turns = vector_board[x][y].turns + 1
                    else:
                        vector_board[new_x][new_y].turns = min(vector_board[x][y].turns + 1, vector_board[new_x][new_y].turns)
                vector_board[new_x][new_y].visited = True
                queue.append((new_x, new_y))
    return vector_board
