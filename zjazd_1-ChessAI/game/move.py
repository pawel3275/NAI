class Move:
    """Move class containg info about a possible moves on a board for a given piece
    """
    ranks_to_rows = {"1": 7, "2": 6, "3": 5, "4": 4, "5": 3, "6": 2, "7": 1, "8": 0}
    rows_to_ranks = {v: k for k, v in ranks_to_rows.items()}
    files_to_columns = {"a": 0, "b": 1, "c": 2, "d": 3, "e": 4, "f": 5, "g": 6, "h": 7}
    columns_to_files = {v: k for k, v in files_to_columns.items()}

    def __init__(self, start_square, end_square, board, is_enpassant_move=False):
        """Constructor

        Args:
            start_square (tuple): start coords of a square
            end_square (tuple): end coords of a square
            board (matrix 2x2): board of the game from game context
            is_enpassant_move (bool, optional): Info if move is en passant. Defaults to False.
        """
        self.start_row = start_square[0]
        self.start_column = start_square[1]
        self.end_row = end_square[0]
        self.end_column = end_square[1]
        self.piece_moved = board[self.start_row][self.start_column]
        self.piece_captured = board[self.end_row][self.end_column]
        self.is_pawn_promotion = False
        self.move_chess_notation_id = ""

        if (self.piece_moved == "wP" and self.end_row == 0) or (self.piece_moved == "bP" and self.end_row == 7):
            self.isPawnPromotion = True

        self.is_enpassant_move = is_enpassant_move
        if self.is_enpassant_move:
            self.piece_captured = "wP" if self.piece_moved == "bP" else "bP"

        self.move_id = self.start_row * 1000 + self.start_column * 100 + self.end_row * 10 + self.end_column

    def __eq__(self, other):
        """Equal operation override.

        Args:
            other (Move): Move

        Returns:
            Boolean: True if id of move is the same, false otherwise.
        """
        if isinstance(other, Move):
            return self.move_id == other.move_id
        return False

    def get_chess_notation(self):
        """Converts the rows and columns to the chess notation

        Returns:
            str: chess notation.
        """
        self.move_chess_notation_id = self.get_rank_file(self.start_row, self.start_column) + self.get_rank_file(self.end_row, self.end_column)
        return self.move_chess_notation_id

    def get_rank_file(self, row, column):
        """Converts the rows and columns to files

        Args:
            row (int): number of row
            column (int): number of column

        Returns:
            str: rank of the move.
        """
        return self.columns_to_files[column] + self.rows_to_ranks[row]
