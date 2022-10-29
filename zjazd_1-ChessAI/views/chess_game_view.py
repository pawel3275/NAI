import os
from views.window import Window, WINDOW_SIZE, BORDER_GAP, DEFAULT_BACKGROUND_COLOR
from game.chess_context import ChessGameContext
from utilities.button import Button, SMALL_BUTTON_SIZE, ON_BUTTON_COLLISION_COLOR, DEFAULT_BUTTON_COLOR
from utilities.event import EventHandler
import pygame

IMG_PATH = "images/default_pieces_and_figures/"
CHESS_PIECE_SIZE = (64, 64)
TILE_SIZE = (64, 64)
BORDER_OFFSET = (128, 128)  # Change to ((WINDOWSIZE - TILE_SIZE[0] * 8) / 2), ... )
BACKGROUND_PATH = "images/"


class ChessGameView(Window):
    """Class containing the info regarding view of the game - like window or board.
    """
    def __init__(self):
        super().__init__()
        self.images = {}
        self.board_rects = []
        self.square_selected = ()
        self.player_clicks = []
        self.move_made = False
        self.present_animations = False
        self.is_game_over = False
        self.limited_draws = False
        self.__load_images()
        self.__create_game_ontext()
        self.__calculate_rect_positions()
        self.__create_button_rect_list(self.screen)

    def __set_background(self):
        """Loads the image to backgrounds and blits the screen to show it
        """
        background = pygame.image.load(BACKGROUND_PATH + "game_background.jpg")
        self.screen.blit(background, (0, 0))
        self.limited_draws = True

    def __load_images(self):
        """Loads the images of chess figures
        """
        # Load pieces and figures as surfaces from image folder.
        for filename in os.listdir(IMG_PATH):
            image_name = os.path.splitext(filename)[0]
            self.images[image_name] = pygame.transform.scale(pygame.image.load(IMG_PATH + filename), CHESS_PIECE_SIZE)

    def __create_game_ontext(self):
        """Constructs the game context class used to play the game
        """
        self.game_context = ChessGameContext()
        self.valid_moves = self.game_context.get_valid_moves()

    def __draw_board(self):
        """Draws the game board for a game view state
        """
        global colors
        white_color = pygame.Color("white")
        grey_color = pygame.Color("gray")
        colors = [white_color, grey_color]
        for i in range(8):
            for j in range(8):
                if (i + j) % 2 == 0:
                    color = white_color
                else:
                    color = grey_color

                board_rect = pygame.Rect(j * TILE_SIZE[0] + BORDER_OFFSET[0], i * TILE_SIZE[1] + BORDER_OFFSET[1],
                                         TILE_SIZE[0], TILE_SIZE[1])

                self.board_rects.append(board_rect)
                pygame.draw.rect(self.screen, color, board_rect)

    def __highlight_squares(self):
        """For a specific available move - the square for a piece/figure is highlighted
        """
        if self.square_selected != ():
            row, column = self.square_selected
            if 0 < row < 9 and 0 < column < 9:
                if self.game_context.board[row][column][0] == ("w" if self.game_context.white_to_move else "b"):
                    square_surface = pygame.Surface(TILE_SIZE)
                    square_surface.set_alpha(100)
                    square_surface.fill(pygame.Color("blue"))
                    self.screen.blit(square_surface,
                                     ((column * TILE_SIZE[0]) + BORDER_OFFSET[0], (row * TILE_SIZE[1]) + BORDER_OFFSET[1]))
                    square_surface.fill(pygame.Color("yellow"))
                    for move in self.valid_moves:
                        if move.start_row == row and move.start_column == column:
                            self.screen.blit(square_surface,
                                             ((move.end_column * TILE_SIZE[0]) + BORDER_OFFSET[0],
                                              (move.end_row * TILE_SIZE[1]) + BORDER_OFFSET[1]))

    def animate_move(self, move):
        """Performs the animation for a given move
        """
        global colors
        delta_row = move.end_row - move.start_row
        delta_column = move.end_column - move.start_column
        frames_per_square = 10
        frame_count = (abs(delta_row) + abs(delta_column)) * frames_per_square
        for frame in range(frame_count + 1):
            row, column = (
                (move.start_row + delta_row * frame / frame_count,
                 move.start_column + delta_column * frame / frame_count))
            self.__draw_board()
            self.__draw_pieces()
            color = colors[(move.end_row + move.end_column) % 2]
            end_square = pygame.Rect(move.end_column * TILE_SIZE[0] + + BORDER_OFFSET[0],
                                     move.end_row * TILE_SIZE[1] + + BORDER_OFFSET[1], TILE_SIZE[0], TILE_SIZE[1])
            pygame.draw.rect(self.screen, color, end_square)
            if move.piece_captured != "__":
                self.screen.blit(self.images[move.piece_captured], end_square)
            self.screen.blit(self.images[move.piece_moved], pygame.Rect(column * TILE_SIZE[0] + + BORDER_OFFSET[0],
                                                                        row * TILE_SIZE[1] + + BORDER_OFFSET[1],
                                                                        TILE_SIZE[0], TILE_SIZE[1]))
            pygame.display.flip()
            pygame.time.Clock().tick(60)

    def draw_text(self, text):
        """Draws a text on a screen

        Args:
            text (_type_): _description_
        """
        font = pygame.font.SysFont("Helvitica", 32, True, False)
        text_obj = font.render(text, False, pygame.Color("Black"))
        text_location = pygame.Rect(0, 0, 1024, 1080)
        self.screen.blit(text_obj, text_location)

    def __draw_pieces(self):
        """Drawing pieces and figures on a board
        """
        for i in range(8):
            for j in range(8):
                piece = self.game_context.board[i][j]
                if piece != "__":
                    rect = pygame.Rect(j * TILE_SIZE[0] + BORDER_OFFSET[0], i * TILE_SIZE[1] + BORDER_OFFSET[1],
                                       CHESS_PIECE_SIZE[0], CHESS_PIECE_SIZE[1])
                    self.screen.blit(self.images[piece], rect)

    def __calculate_rect_positions(self):
        """Populates grid variables for buttons regarding their positions
        """
        middle_point = (WINDOW_SIZE[0] / 2, WINDOW_SIZE[1] / 2)

        grid_horizontal_left_lane = BORDER_OFFSET[0]
        grid_horizontal_middle_lane = BORDER_OFFSET[0] + TILE_SIZE[0] * 8 + BORDER_GAP
        grid_horizontal_right_lane = WINDOW_SIZE[0] - BORDER_OFFSET[0]

        grid_vertical_top_lane = BORDER_OFFSET[1]
        grid_vertical_middle_lane = BORDER_OFFSET[1] + (TILE_SIZE[1] * 8) / 3  # TODO remove / 3 later
        grid_vertical_bottom_lane = WINDOW_SIZE[1] - BORDER_OFFSET[1]

        self.back_button_pos = (grid_horizontal_middle_lane, grid_vertical_middle_lane)

    def __create_button_rect_list(self, screen):
        """Populates rectangle button list for the given view
        """
        rect_position = (self.back_button_pos, SMALL_BUTTON_SIZE)
        self.window_buttons.append(Button(screen, "id_back_button", rect_position, "BACK"))

    def __check_button_mouse_collision(self):
        """Checks if the mouse button is on collision with a rect
        """
        mouse_pointer_pos = pygame.mouse.get_pos()
        for button in self.window_buttons:
            if button.rect.collidepoint(mouse_pointer_pos):
                button.box_color = ON_BUTTON_COLLISION_COLOR
                if button.id == "id_back_button" and EventHandler.mouse_button_code == 4:
                    EventHandler.on_view_change(0)
            else:
                button.box_color = DEFAULT_BUTTON_COLOR

    def reset_view(self):
        """Resets the whole view to the default background color
        """
        self.background_colour = DEFAULT_BACKGROUND_COLOR
        self.screen.fill(self.background_colour)

    def draw_view(self):
        """Draws the whole view consisting on background, buttons etc.
        """
        if not self.limited_draws:
            self.__set_background()
        self.__draw_board()
        self.__highlight_squares()
        self.__draw_pieces()
        self.__check_button_mouse_collision()
        for button in self.window_buttons:
            button.draw_button()
