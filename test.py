class Player:
    def __init__(self, start_pos):
        self.start_pos = start_pos
        self.pos = start_pos

    def reset(self):
        self.pos += 4
        print(self.pos)
        self.pos = self.start_pos
        print(self.pos)

player = Player(1)
player.reset()
