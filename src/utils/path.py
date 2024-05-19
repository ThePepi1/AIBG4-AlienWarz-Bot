from utils.logger import log
from utils.vectors import Vectors

class LocalState:
    cache = {}

def log_vector_board(vector_board):
    for row in vector_board:
        s = ""
        for cell in row:
            s += "".join(map(lambda x: Vectors.name(x)[0], cell.from_vectors)) + "\t"
        log(s)

def find_path_least_moves(from_cell, to_cell, board):
    who = board[from_cell[0]][from_cell[1]][0]
    if (from_cell, who) not in LocalState.cache:
        vector_board = generate_vector_board(from_cell, to_cell, board)
        LocalState.cache[(from_cell, who)] = vector_board
    else:
        vector_board = LocalState.cache[(from_cell, who)]
        log(f"cache hit for {from_cell}")       
    log_vector_board(vector_board)
    path = []
    x, y = to_cell
    direction = None
    while (x, y) != from_cell:
        best = None
        if x < 0 or y < 0 or x >= len(board) or y >= len(board):
            log(f"OUT OF BOUNDS 1")
            return None
        for vector in vector_board[x][y].from_vectors:
            new_x, new_y = x - vector[0], y - vector[1]
            if best is None:
                best = new_x, new_y, vector
                continue
            # check for new best
            if new_x < 0 or new_y < 0 or new_x >= len(board) or new_y >= len(board):
                continue
            if vector_board[new_x][new_y].turns < vector_board[best[0]][best[1]].turns:
                best = new_x, new_y, vector
            elif vector_board[new_x][new_y].turns == vector_board[best[0]][best[1]].turns and vector == direction:
                best = new_x, new_y, vector
        if best is None:
            log(f"OUT OF BOUNDS 2")
            return None
        if direction is None or direction != best[2]:
            direction = best[2]
            path.append((x, y)) 
        x, y = best[0], best[1]
    log(f"found_path {path[::-1]}")
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


def get_path_length(my_position, path):
    total = 0
    current = my_position
    i = 0
    while i < len(path):
        next = path[i]
        dx = abs(next[0] - current[0])
        dy = abs(next[1] - current[1])
        squeres = int(dx + dy)
        total += squeres
        current = next
        i += 1
    return total


#board = [['E', 'D_3_0', 'D_3_0', 'D_2_0', 'E', 'M_6_0', 'E', 'E', 'F_2_3', 'B'], ['D_3_0', 'E', 'E', 'E', 'E', 'M_6_0', 'E', 'E', 'E', '2'], ['D_3_0', 'E', 'E', 'E', 'M_6_0', 'M_6_0', 'E', 'E', 'E', 'E'], ['D_3_0', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E'], ['E', 'E', 'M_6_0', 'E', 'E', 'E', 'E', 'E', 'E', 'M_6_0'], ['M_2_0', 'M_6_0', 'M_6_0', 'E', 'E', 'E', 'E', 'E', 'M_6_0', 'D_3_0'], ['E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'M_6_0', 'E'], ['E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E'], ['E', 'E', 'E', 'E', 'E', 'M_6_0', 'M_6_0', 'E', 'E', 'D_3_0'], ['A', 'E', 'E', '1', 'M_2_0', 'D_3_0', 'E', 'E', 'D_3_0', 'E']]
#vb = generate_vector_board((9,2), (9,0), board)
#log_vector_board(vb)