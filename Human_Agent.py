from Env import Env
from State import State
from Graphics import*

class Human_Agent:
    def __init__(self, player, env : Env, graphics: Graphics = None):
        self.player = player
        self.env = env
        self.graphics = graphics

    def get_action (self, events, state = None):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = event.pos
                action = self.calc_row(pos)
                if self.env.legal(self.env.state, action):
                    return action
                return None
    
    def __call__(self, events):
        return self.get_action(events)
    
    def calc_row(self, pos):
        x, y = pos
        if x<50 or x>750:
            return None
        row = (x+50)//SQUARE_SIZE - 1
        return row