import numpy as np
from datetime import datetime
from game.move import Move


class ChessGameContext:
    """Class for holding the game context and all board information.
    """
    def __init__(self):
        """Constructor for context class. Contains info about game state.
        """
        self.board = np.array([
            ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
            ["bP", "bP", "bP", "bP", "bP", "bP", "bP", "bP"],
            ["__", "__", "__", "__", "__", "__", "__", "__"],
            ["__", "__", "__", "__", "__", "__", "__", "__"],
            ["__", "__", "__", "__", "__", "__", "__", "__"],
            ["__", "__", "__", "__", "__", "__", "__", "__"],
            ["wP", "wP", "wP", "wP", "wP", "wP", "wP", "wP"],
            ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"],
        ])
        self.moveFunctions = {"P": self.get_pawn_moves, "R": self.get_rook_moves, "N": self.get_knight_moves,
                              "B": self.get_bishop_moves, "Q": self.get_queen_moves, "K": self.get_king_moves}
        self.moveLog = []
        self.white_to_move = True
        self.white_king_location = (7, 4)
        self.black_king_location = (0, 4)
        self.checkmate = False
        self.stalemate = False
        self.inCheck = False
        self.enpassant_coord = ()
        # Both below false to see random moves by both AIs
        self.player_one = True  # True when human plays white, false for AI
        self.player_two = False  # True when human plays white, false for AI
        self.human_turn = False

    def __del__(self):
        """Destructor
        
        Save gathered logs on exit.

        """ 
        self.save_log_to_file()


    def save_log_to_file(self):
        """Creates the log file with the data about the game movements
        """
        log_lines = []
        dt_string = "game_log_" + datetime.now().strftime("%d_%m_%Y_%H_%M_%S") + ".csv"
        csv_file = open(dt_string, "a")
        if len(self.moveLog) != 0:
            for move in self.moveLog:
                log_line = str(move.piece_moved) + "_" + str(move.move_chess_notation_id)
                log_lines.append(log_line)

        for element in log_lines:
            csv_file.write(element + "\n")
        csv_file.close()

    def make_move(self, move):
        """Performs a move and updates the board

        Args:
            move (Move): Move object.
        """
        chess_notation_move = move.get_chess_notation()
        self.board[move.start_row][move.start_column] = "__"
        self.board[move.end_row][move.end_column] = move.piece_moved
        self.moveLog.append(move)
        self.white_to_move = not self.white_to_move
        if move.piece_moved == "wK":
            self.white_king_location = (move.end_row, move.end_column)
        elif move.piece_moved == "bK":
            self.black_king_location = (move.end_row, move.end_column)

        if move.is_pawn_promotion:
            self.board[move.end_row][move.end_column] = move.piece_moved[0] + "Q"

        if move.is_enpassant_move:
            self.board[move.start_row][move.end_column] = "__"

        if move.piece_moved[1] == "P" and abs(move.start_row - move.end_row) == 2:
            self.enpassant_coord = ((move.start_row + move.end_row) // 2, move.start_column)
        else:
            self.enpassant_coord = ()

    def undo_move(self):
        """Undoes the last move from the move log
        """
        if len(self.moveLog) != 0:
            move = self.moveLog.pop()
            self.board[move.start_row][move.start_column] = move.piece_moved
            self.board[move.end_row][move.end_column] = move.piece_captured
            self.white_to_move = not self.white_to_move
            if move.piece_moved == "wK":
                self.white_king_location = (move.start_row, move.start_column)
            elif move.piece_moved == "bK":
                self.black_king_location = (move.start_row, move.start_column)

            if move.is_enpassant_move:
                self.board[move.end_row][move.end_column] = "__"
                self.board[move.start_row][move.end_column] = move.piece_captured
                self.enpassant_coord = (move.end_row, move.end_column)

            if move.piece_moved[1] == "P" and abs(move.start_row - move.end_row) == 2:
                self.enpassant_coord = ()

        self.checkmate = False
        self.stalemate = False

    def get_valid_moves(self):
        """Returns the possible moves for a given chess piece.

        Returns:
            list: list of all possible moves for each chess piece.
        """
        temp_enpassant_coord = self.enpassant_coord
        moves = self.get_possible_moves()

        for i in range(len(moves) - 1, -1, -1):
            self.make_move(moves[i])
            self.white_to_move = not self.white_to_move
            if self.in_check():
                moves.remove(moves[i])
            self.white_to_move = not self.white_to_move
            self.undo_move()

        if len(moves) == 0:
            if self.in_check():
                self.checkmate = True
            else:
                self.stalemate = True
        else:
            self.stalemate = False
            self.checkmate = False

        self.enpassant_coord = temp_enpassant_coord
        return moves

    def in_check(self):
        """Checks whether the king is in the check position

        Returns:
            Boolean: True when we are in check and false otherwise.
        """
        if self.white_to_move:
            return self.square_attacked(self.white_king_location[0], self.white_king_location[1])
        else:
            return self.square_attacked(self.black_king_location[0], self.black_king_location[1])

    '''
    '''
    def square_attacked(self, row, column):
        """Handles the square attack and moves the figure to new square deleting the olf one


        Args:
            row (int): Row of a piece.
            column (int): Column of a piece.

        Returns:
            Boolean: True when we are in check and false otherwise.
        """
        self.white_to_move = not self.white_to_move
        opponent_moves = self.get_possible_moves()
        self.white_to_move = not self.white_to_move
        for move in opponent_moves:
            if move.end_row == row and move.end_column == column:
                return True
        return False

    def get_possible_moves(self):
        """Returns the list of all possible moves for each chess piece

        Returns:
            list: list of all possible moves for each chess piece.
        """
        moves = []
        for i in range(len(self.board)):
            for j in range(len(self.board[i])):
                turn = self.board[i][j][0]
                if (turn == "w" and self.white_to_move) or (turn == "b" and not self.white_to_move):
                    piece = self.board[i][j][1]
                    self.moveFunctions[piece](i, j, moves)
        return moves

    def get_pawn_moves(self, row, column, moves_list):
        """Returns the list of all possible moves for pawns

        Args:
            row (int): row on board.
            column (int): column on board.
            moves_list (list): list of moves for each chess pawn.
        """
        if self.white_to_move:
            if self.board[row - 1][column] == "__":
                moves_list.append(Move((row, column), (row - 1, column), self.board))
                if row == 6 and self.board[row - 2][column] == "__":
                    moves_list.append(Move((row, column), (row - 2, column), self.board))
            if column - 1 >= 0:
                if self.board[row - 1][column - 1][0] == "b":
                    moves_list.append(Move((row, column), (row - 1, column - 1), self.board))
                elif (row - 1, column - 1) == self.enpassant_coord:
                    moves_list.append(Move((row, column), (row - 1, column - 1), self.board, is_enpassant_move=True))
            if column + 1 <= 7:
                if self.board[row - 1][column + 1][0] == "b":
                    moves_list.append(Move((row, column), (row - 1, column + 1), self.board))
                elif (row - 1, column + 1) == self.enpassant_coord:
                    moves_list.append(Move((row, column), (row - 1, column + 1), self.board, is_enpassant_move=True))
        else:
            if self.board[row + 1][column] == "__":
                moves_list.append(Move((row, column), (row + 1, column), self.board))
                if row == 1 and self.board[row + 2][column] == "__":
                    moves_list.append(Move((row, column), (row + 2, column), self.board))
            if column - 1 >= 0:
                if self.board[row + 1][column - 1][0] == "w":
                    moves_list.append(Move((row, column), (row + 1, column - 1), self.board))
                elif (row + 1, column - 1) == self.enpassant_coord:
                    moves_list.append(Move((row, column), (row + 1, column - 1), self.board, is_enpassant_move=True))
            if column + 1 <= 7:
                if self.board[row + 1][column + 1][0] == "w":
                    moves_list.append(Move((row, column), (row + 1, column + 1), self.board))
                elif (row + 1, column + 1) == self.enpassant_coord:
                    moves_list.append(Move((row, column), (row + 1, column + 1), self.board, is_enpassant_move=True))

    def get_rook_moves(self, row, column, moves_list):
        """Returns the list of all possible moves for rooks

        Args:
            row (int): row on board.
            column (int): column on board.
            moves_list (list): list of moves for each chess rook.
        """
        directions = ((-1, 0), (0, -1), (1, 0), (0, 1))
        enemy_color = "b" if self.white_to_move else "w"
        for direction in directions:
            for i in range(1, 8):
                end_row = row + direction[0] * i
                end_col = column + direction[1] * i
                if 0 <= end_row < 8 and 0 <= end_col < 8:
                    end_piece = self.board[end_row][end_col]
                    if end_piece == "__":
                        moves_list.append(Move((row, column), (end_row, end_col), self.board))
                    elif end_piece[0] == enemy_color:
                        moves_list.append(Move((row, column), (end_row, end_col), self.board))
                        break
                    else:
                        break
                else:
                    break

    def get_knight_moves(self, row, column, moves_list):
        """Returns the list of all possible moves for knights

        Args:
            row (int): row on board.
            column (int): column on board.
            moves_list (list): list of moves for each chess knights.
        """
        directions = ((-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1))
        ally_color = "w" if self.white_to_move else "b"
        for direction in directions:
            end_row = row + direction[0]
            end_col = column + direction[1]
            if 0 <= end_row < 8 and 0 <= end_col < 8:
                end_piece = self.board[end_row][end_col]
                if end_piece[0] != ally_color:
                    moves_list.append(Move((row, column), (end_row, end_col), self.board))

    def get_bishop_moves(self, row, column, moves_list):
        """Returns the list of all possible moves for bishops

        Args:
            row (int): row on board.
            column (int): column on board.
            moves_list (list): list of moves for each chess bishops.
        """
        directions = ((-1, -1), (-1, 1), (1, -1), (1, 1))
        enemy_color = "b" if self.white_to_move else "w"
        for direction in directions:
            for i in range(1, 8):
                end_row = row + direction[0] * i
                end_col = column + direction[1] * i
                if 0 <= end_row < 8 and 0 <= end_col < 8:
                    end_piece = self.board[end_row][end_col]
                    if end_piece == "__":
                        moves_list.append(Move((row, column), (end_row, end_col), self.board))
                    elif end_piece[0] == enemy_color:
                        moves_list.append(Move((row, column), (end_row, end_col), self.board))
                        break
                    else:
                        break
                else:
                    break

    def get_queen_moves(self, row, column, moves_list):
        """Returns the list of all possible moves for queens

        Args:
            row (int): row on board.
            column (int): column on board.
            moves_list (list): list of moves for each chess queens.
        """
        self.get_rook_moves(row, column, moves_list)
        self.get_bishop_moves(row, column, moves_list)

    def get_king_moves(self, row, column, moves_list):
        """Returns the list of all possible moves for king

        Args:
            row (int): row on board.
            column (int): column on board.
            moves_list (list): list of moves for each chess king.
        """
        directions = ((-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1))
        ally_color = "w" if self.white_to_move else "b"
        for i in range(8):
            end_row = row + directions[i][0]
            end_col = column + directions[i][1]
            if 0 <= end_row < 8 and 0 <= end_col < 8:
                end_piece = self.board[end_row][end_col]
                if end_piece[0] != ally_color:
                    moves_list.append(Move((row, column), (end_row, end_col), self.board))
