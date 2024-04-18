class Card:
    def __init__(self, rank, suit, visible=False):
        self.rank = rank
        self.suit = suit
        self.visible = visible

    def __str__(self):
        if self.visible:
            return f"{self.rank} of {self.suit}"
        else:
            return "Hidden Card"

    def flip(self):
        self.visible = not self.visible
