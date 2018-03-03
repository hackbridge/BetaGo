from . import GoBackend
import numpy as np
from Shared.Consts import WHITE, BLACK, EMPTY, num_to_char, char_to_num
from Shared.Functions import toggle_player

class GoSimulator:

    def __init__(self, N):
        GoBackend.set_size(N)
        self.N = N
        self.board = GoBackend.Position.initial_state()

    def _board_to_string(self, board):
        board_flat = board.reshape((self.N**2))
        board_str = ''.join(list((map(lambda x: num_to_char[x], board_flat))))
        return board_str


    def set_board_from_prev_boards(self, prev_boards, next_player):
        # last_player = toggle_player(next_player)
        self.set_board(prev_boards[-1], next_player, ko=None) 
        # self.current_player = last_player
        # if np.array_equal(prev_boards[-1], prev_boards[-2]):
        #     self.set_board(prev_boards[-1], next_player, ko=None) 
        # else:
        #     board1 = self._board_to_string(prev_boards[-2])
        #     board2 = self._board_to_string(prev_boards[-1]) 
        #     move = GoBackend.Position.find_move(board1, board2, last_player)
            
        #     assert move is not None

        #     y, x = divmod(move, self.N)
        #     self.play(x, y)
        #     assert np.array_equal(self.get_board(), prev_boards[-1])
        #     self.current_player = last_player 


    def set_board(self, board, next_player, ko=None):
        board_str = self._board_to_string(board)
        ko_flat = None
        if ko is not None:
            ko_flat = ko[0]*self.N + ko[1]
        self.board = GoBackend.Position.set_board(board=board_str,ko=ko_flat)
        self.current_player = next_player

    def play(self, x, y):
        self.board = self.board.play_move(y*self.N+x, self.current_player)
        self.current_player = toggle_player(self.current_player)
        return (self.as_array(), self.current_player)

    def pass_move(self):
        self.current_player = toggle_player(self.current_player)
        return (self.as_array(), self.current_player)

    def as_array(self):
        char_list = list(self.board.board)
        num_list = list(map(lambda x: char_to_num[x], char_list))
        board_array = np.array(num_list).reshape((self.N, self.N))
        return board_array

    def get_legal_moves(self):
        legal = self.board.get_legal_moves()
        return np.array(legal).reshape((self.N,self.N))

    def get_board(self):
        board = [ char_to_num[x] for x in self.board.board ]
        return np.array(board).reshape((self.N,self.N))

    def black_score_lead(self):
        '''Black Score - White Score'''
        return self.board.score()





