from SnakeLadderRepository import SnakeRepository, LadderRepository

class Board:
    def __init__(self, board_size=100):
        self.size = board_size
        self.snake_repository = SnakeRepository()
        self.ladder_repository = LadderRepository()
    
    def add_snake(self, snake_head, snake_tail):
        try:
            if not 1 <= snake_head < self.size or not 1<= snake_tail < self.size:
                raise KeyError("Snake cannot be beyond board limits")
            self.snake_repository.save(snake_head, snake_tail)
        except Exception as err:
            raise err

    def add_ladder(self, ladder_start, ladder_end):
        try:
            if not 1 <= ladder_start < self.size or not 1<= ladder_end < self.size:
                raise KeyError("Ladder cannot be beyond board limits")
            self.ladder_repository.save(ladder_start, ladder_end)
        except Exception as err:
            raise err

    def get_new_position(self, position):

        if self.snake_repository.is_snake_head(position):
            return self.snake_repository.get_snake_tail(position), "They got bit by snake :("

        if self.ladder_repository.is_ladder_start(position):
            return self.ladder_repository.get_ladder_end(position), "They climbed a ladder :)"

        return position, ""
    