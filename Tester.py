from Env import Env
from State import State
from Human_Agent import Human_Agent
from Random_Agent import Random_Agent
from DQN_Agent import DQN_Agent

class Tester:
    def __init__(self, env, player1, player2) -> None:
        self.env = env
        self.player1 = player1
        self.player2 = player2


    def test(self,num):
        red_win = 0
        yellow_win = 0
        tie = 0
        
        for n in range(num):
            state = State()
            player = self.player1
            while not self.env.end_of_game(state):
                action = player.get_action(state=state)
                if action == None:
                    while action == None:
                        action = player.get_action(state=state)
                state, _ = self.env.next_state(state,action)
                player = self.switch_players(player)
            if state.end_of_game == 1:
                red_win +=1
            elif state.end_of_game == -1:
                yellow_win += 1
            else:
                tie +=1
            state.reset() 
        return red_win, yellow_win,tie

    def switch_players(self,player):
        if player == self.player1:
            return self.player2
        else:
            return self.player1
