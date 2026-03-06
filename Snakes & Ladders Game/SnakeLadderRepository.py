class SnakeRepository:
    def __init__(self):
        self.snakes = {}
    
    def save(self, head, tail):
        if head <= tail:
            raise KeyError("Snake head must be after tail")
        self.snakes[head] = tail
    
    def is_snake_head(self, head):
        return head in self.snakes
    
    def get_snake_tail(self, head):
        if not self.is_snake_head(head):
            raise ValueError(f"{head} is not a snake head")
        return self.snakes[head]
    
    def list(self):
        return list(self.snakes.items())
    
class LadderRepository:
    def __init__(self):
        self.ladders = {}
    
    def save(self, start, end):
        if start >= end:
            raise KeyError("Ladder start must be after end")
        self.ladders[start] = end
    
    def is_ladder_start(self, start):
        return start in self.ladders
    
    def get_ladder_end(self, start):
        if not self.is_ladder_start(start):
            raise ValueError(f"{start} is not a ladder start")
        return self.ladders[start]
    
    def list(self):
        return list(self.ladders.items())
    
