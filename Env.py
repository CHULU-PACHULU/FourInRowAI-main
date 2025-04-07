from State import State
import numpy as np

class Env:
    def __init__(self, state = None) -> None:
        self.state = state

    def move (self, action):
        i = 0
        while i<5 and self.state.board[action,i+1]==0:
            i=i+1
        self.state.board[action,i] = self.state.player
        self.switch_players(self.state)
        self.end_of_game(self.state)
        return self.state.board
    
    def action_to_height (self, state, action):
        i = 0
        while i<5 and state.board[action,i+1]==0:
            i=i+1
        return i
    
    
    def legal (self, state: State, action):
        if state.end_of_game==0:
            if state.board[action,0] == 0:
                return True
            return False
        
    
    def next_state (self, state: State, action):
        next_state = state.copy()
        next_state.board[action,self.action_to_height(state,action)] = state.player
        next_state.switch_players()
        self.end_of_game(next_state)
        if next_state.end_of_game == 2:
            reward = 0
        else:
            reward = next_state.end_of_game
        return next_state, reward

    
    def all_legal (self, state: State):
        lst = []
        for i in range(0,7):
            if state.board[i,0]==0:
                lst.append(i)
        return np.array(lst)

    def switch_players (self, state):
        if state.player == 1:
            state.player = -1
        else:
            state.player = 1
    
    def end_of_game (self, state: State):
        for i in range (3):
           for j in range (4):
               if self.check_four(state.board[j:j+4,i:i+4]) == 1:
                   state.end_of_game = 1
                   return True
               elif self.check_four(state.board[j:j+4,i:i+4]) == -1:
                   state.end_of_game = -1
                   return True
        piece_num = np.count_nonzero(state.board)
        if piece_num == 42:
            state.end_of_game = 2
            return True
        state.end_of_game = 0
        return False

    def check_four (self, mini_board):
        row_sum = np.sum(mini_board, axis= 1)
        col_sum = np.sum(mini_board, axis= 0)
        diagonals = [np.trace(mini_board), np.trace(np.fliplr(mini_board))]
        if 4 in row_sum or 4 in col_sum or 4 in diagonals: 
            return 1
        if -4 in row_sum or -4 in col_sum or -4 in diagonals:
            return -1
        return 0