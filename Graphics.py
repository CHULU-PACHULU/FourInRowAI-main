import pygame
from State import State
from Env import Env


WIDTH = 800
HEIGHT = 800
H_WIDTH = 800
H_HEIGHT = 800
M_WIDTH = 702
M_HEIGHT = 602
ROWS, COLS = 7, 6
SQUARE_SIZE = 100
LINE_WIDTH = 2

BLUE = (0,0,255)
LIGHTGRAY = (211,211,211)
BLACK = (0, 0, 0)
RED = (255,0,0)
YELLOW = (255,255,0)
WHITE = (255,255,255)
FPS = 60

class Graphics:
    def __init__(self) -> None:
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.header_surf = pygame.Surface((H_WIDTH, H_HEIGHT))
        self.main_surf = pygame.Surface((M_WIDTH, M_HEIGHT))
        pygame.display.set_caption('Four In A Row')


    def draw(self, state):
        self.header_surf.fill(LIGHTGRAY)
        self.main_surf.fill(BLUE)
        self.draw_Lines()
        self.draw_pieces(state)
        self.screen.blit(self.header_surf, (0,0))
        self.screen.blit(self.main_surf, (50,100))
        self.draw_winner_or_start(state)
        pygame.display.update()


    def draw_Lines(self):
        for i in range(ROWS+1):
            pygame.draw.line(self.main_surf, BLACK, (i * SQUARE_SIZE, 0), 
                             (i * SQUARE_SIZE, HEIGHT), width= LINE_WIDTH)
        for i in range(COLS+1):
            pygame.draw.line(self.main_surf, BLACK, (0, i * SQUARE_SIZE), 
                             (WIDTH, i * SQUARE_SIZE), width= LINE_WIDTH)
            
        for row in range(ROWS):
            for col in range(COLS):
                pygame.draw.circle(self.main_surf,LIGHTGRAY,(row*SQUARE_SIZE+50,col*SQUARE_SIZE+50),40)
                pygame.draw.circle(self.main_surf,BLACK,(row*SQUARE_SIZE+50,col*SQUARE_SIZE+50),40,LINE_WIDTH)
    def draw_pieces(self, state):
        board = state.board
        for row in range(ROWS):
            for col in range(COLS):
                if board[row,col] ==1:
                    pygame.draw.circle(self.main_surf,RED,(row*SQUARE_SIZE+50,col*SQUARE_SIZE+50),40)
                    pygame.draw.circle(self.main_surf,BLACK,(row*SQUARE_SIZE+50,col*SQUARE_SIZE+50),40,LINE_WIDTH)
                elif board[row,col]==-1:
                    pygame.draw.circle(self.main_surf,YELLOW,(row*SQUARE_SIZE+50,col*SQUARE_SIZE+50),40)
                    pygame.draw.circle(self.main_surf,BLACK,(row*SQUARE_SIZE+50,col*SQUARE_SIZE+50),40,LINE_WIDTH)
    def draw_pieces_board(self,board):
        for row in range(ROWS):
            for col in range(COLS):
                if board[row,col] ==1:
                    pygame.draw.circle(self.main_surf,RED,(row*SQUARE_SIZE+50,col*SQUARE_SIZE+50),40)
                    pygame.draw.circle(self.main_surf,BLACK,(row*SQUARE_SIZE+50,col*SQUARE_SIZE+50),40,LINE_WIDTH)
                elif board[row,col]==-1:
                    pygame.draw.circle(self.main_surf,YELLOW,(row*SQUARE_SIZE+50,col*SQUARE_SIZE+50),40)
                    pygame.draw.circle(self.main_surf,BLACK,(row*SQUARE_SIZE+50,col*SQUARE_SIZE+50),40,LINE_WIDTH)

    def draw_animation(self, action, state, color):
        i = 0
        while i<5 and state[action,i+1]==0:
            i=i+1
        height = i
        for i in range(height*8):
            self.header_surf.fill(LIGHTGRAY)
            self.main_surf.fill(BLUE)
            self.draw_Lines()
            self.draw_pieces_board(state)
            if color=="yellow":
                pygame.draw.circle(self.main_surf,YELLOW,(action*SQUARE_SIZE+50,i*14),40)
                pygame.draw.circle(self.main_surf,BLACK,(action*SQUARE_SIZE+50,i*14),40,LINE_WIDTH)
            else:
                pygame.draw.circle(self.main_surf,RED,(action*SQUARE_SIZE+50,i*14),40)
                pygame.draw.circle(self.main_surf,BLACK,(action*SQUARE_SIZE+50,i*14),40,LINE_WIDTH)
            self.screen.blit(self.header_surf, (0,0))
            self.screen.blit(self.main_surf, (50,100))
            pygame.display.update()
            pygame.time.delay(15)


    def draw_winner_or_start(self, state):
        env = Env(State())
        font = pygame.font.Font('freesansbold.ttf', 32)
        if state.end_of_game ==1:
            winner = "winner: red"
            play = "play again?"
        elif state.end_of_game ==-1:
            winner = "winner: yellow"
            play = "play again?"
        elif state.end_of_game ==2:
            winner = "tie"
            play = "play again?"
        elif state.end_of_game==3:
            winner = "FOUR IN A ROW"
            play = "press to play"
        else:
            winner = ""
            play = ""
        text = font.render(winner, True, RED, YELLOW)
        textRect = text.get_rect()
        textRect.center = (400, 40)
        text2 = font.render(play, True, BLACK, WHITE)
        textRect2 = text2.get_rect()
        textRect2.center = (400, 750)
        self.screen.blit(text, textRect)
        self.screen.blit(text2, textRect2)

    def __call__(self, state):
        self.draw(state)
    
    def calc_row(self, pos):
        x, y = pos
        if x<50 or x>750:
            return None
        row = (x+50)//SQUARE_SIZE - 1
        return row