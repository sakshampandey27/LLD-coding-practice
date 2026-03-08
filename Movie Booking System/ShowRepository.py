class ShowRepository:
    def __init__(self):
        self.shows = {}
    
    def save(self, show):
        self.shows[show.id] = show
    
    def get(self, show_id):
        if show_id not in self.shows:
            raise KeyError("Show not found")
        return self.shows[show_id]

    def list(self):
        return list(self.shows.values())
