from Board import Board
from collections import deque
from Player import Player

class GameManager:
    def __init__(self):
        self.players = deque()
        self.board = Board()
        self.is_active = True
        self.winner = None

    def add_player(self, name, start_pos=0):
        if start_pos > self.board.size:
            raise ValueError("Start position of player cannot be greater than the size of the board")
        self.players.append(Player(name, start_position=start_pos))

    def turn(self):
        
        current_player = self.players.popleft()
        dice_roll = current_player.play()
        old_position = current_player.position
        new_position = current_player.position + dice_roll
        if new_position > self.board.size:
            return_msg = f"{current_player.name} cannot move. Must get a {self.board.size - current_player.position} to win!"
            return return_msg
        
        new_position, pos_msg = self.board.get_new_position(new_position)
        
        if new_position < self.board.size:
            current_player.position = new_position
            return_msg = f"{current_player.name} moved from {old_position} to {new_position}."
            return_msg += pos_msg
            self.players.append(current_player)
            return return_msg

        if new_position == self.board.size:
            current_player.position = new_position
            return_msg = f"{current_player.name} reached {self.board.size}! Winner!!!"
            self.is_active = False
            self.winner = current_player
            return return_msg
        

        
if __name__ == '__main__':
    gameManager = GameManager()
    gameManager.add_player("Saksham")
    gameManager.add_player("Shreshtha")
    gameManager.board._add_snake(62, 5)
    gameManager.board._add_snake(33, 6)
    gameManager.board._add_snake(49, 9)
    gameManager.board._add_snake(88, 16)
    gameManager.board._add_snake(41, 20)
    gameManager.board._add_snake(56, 53)
    gameManager.board._add_snake(98, 64)
    gameManager.board._add_snake(93, 73)
    gameManager.board._add_snake(95, 75)
    gameManager.board._add_ladder(2, 37)
    gameManager.board._add_ladder(27, 46)
    gameManager.board._add_ladder(10, 32)
    gameManager.board._add_ladder(51, 68)
    gameManager.board._add_ladder(61, 79)
    gameManager.board._add_ladder(65, 84)
    gameManager.board._add_ladder(71, 91)
    gameManager.board._add_ladder(81, 100)

    while gameManager.is_active:
        print(gameManager.turn())
    print(f"\nWinner = {gameManager.winner.name}\n")