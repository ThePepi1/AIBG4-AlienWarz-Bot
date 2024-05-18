from game_state.game_state import state


class Brain:
    @staticmethod
    
    
    @staticmethod
    def can_go_mine(path):
        length = Brain.get_path_length(path)
        energy = length * 9 + 4 * 5
        return energy - state.me().energy

    @staticmethod
    def can_go_block(path):
        length = Brain.get_path_length(path)
        energy = length + 1
        return energy - state.me().energy