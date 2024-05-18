class Vectors:
    UP = (-1, 0)
    DOWN = (1, 0)
    LEFT = (0, -1)
    RIGHT = (0, 1)

    @staticmethod
    def all():
        return [Vectors.UP, Vectors.DOWN, Vectors.LEFT, Vectors.RIGHT]
    @staticmethod
    def oposite(vector):
        if vector == Vectors.UP:
            return Vectors.DOWN
        if vector == Vectors.DOWN:
            return Vectors.UP
        if vector == Vectors.LEFT:
            return Vectors.RIGHT
        if vector == Vectors.RIGHT:
            return Vectors.LEFT
        return None
    
    @staticmethod
    def name(vector):
        if vector == Vectors.UP:
            return "U"
        if vector == Vectors.DOWN:
            return "D"
        if vector == Vectors.LEFT:
            return "L"
        if vector == Vectors.RIGHT:
            return "R"
        return None