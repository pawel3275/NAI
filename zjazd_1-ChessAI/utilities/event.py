import pygame
from game.move import Move
import artificial_intelligence.SmartMoveFinder as AI

TILE_SIZE = (64, 64)
BORDER_OFFSET = (128, 128)
EVENT_CODES = {
    0: "SUCCESS",
    1: "RUNNING",
    2: "GAME_QUIT",
    3: "ERROR",
    4: "LEFT_MOUSE_BUTTON_PRESSED",
    5: "RIGHT_MOUSE_BUTTON_PRESSED",
    6: "MIDDLE_MOUSE_BUTTON_PRESSED",
    7: "DENSE_PLAY",
    8: "MAIN_MENU"
}


class EventHandler:
    """Class for handling events in game.
    """
    mouse_button_code = 0
    window_code = 0
    view_code = 0

    @staticmethod
    def process_event(event):
        """Processes an event depending on the code of the event by adjusting the event variables

        Args:
            event (Event): _description_
        """
        EventHandler.mouse_button_code = EventHandler.on_mouse_button_down(event)
        EventHandler.window_code = EventHandler.on_window_action(event)

    @staticmethod
    def on_view_change(new_view):
        """On view change perform the action of switching to the new view

        Args:
            new_view (int): Code for the new view.
        """
        EventHandler.view_code = new_view

    '''
        
    '''
    @staticmethod
    def on_window_action(event):
        """On actions connected strictly to window handles the actions

        Args:
            event (int): event number

        Returns:
            int: coresponding pygame event number
        """
        if event.type == pygame.QUIT:
            return 2
        if event.type == pygame.RESIZABLE:
            pass

    @staticmethod
    def mouse_board_process(event, game_view):
        """Handler for mouse operations like clicking and hovering

        Args:
            event (int): event type
            game_view (int): view code
        """
        if EventHandler.view_code == 1:
            current_view = game_view.current_view
            game_context = game_view.current_view.game_context
            game_context.human_turn = (game_context.white_to_move and game_context.player_one) or (
                    not game_context.white_to_move and game_context.player_two)
            if not current_view.is_game_over and game_context.human_turn:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    location = pygame.mouse.get_pos()
                    row = (location[1] - BORDER_OFFSET[1]) // 64
                    col = (location[0] - BORDER_OFFSET[0]) // 64
                    if current_view.square_selected == (row, col):
                        current_view.square_selected = ()
                        current_view.player_clicks = []
                    else:
                        current_view.square_selected = (row, col)
                        current_view.player_clicks.append(current_view.square_selected)
                    if len(current_view.player_clicks) == 2:
                        move = Move(current_view.player_clicks[0], current_view.player_clicks[1],
                                    current_view.game_context.board)
                        print(move.get_chess_notation())
                        if move in current_view.valid_moves:
                            current_view.game_context.make_move(move)
                            current_view.move_made = True
                            current_view.present_animations = True
                            current_view.square_selected = ()
                            current_view.player_clicks = []
                        else:
                            current_view.player_clicks = [current_view.square_selected]
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_u:
                        current_view.game_context.undo_move()
                        current_view.move_made = True
                        current_view.present_animations = False

            # AI handling below
            if not current_view.is_game_over and not game_context.human_turn:
                valid_moves = current_view.game_context.get_valid_moves()
                AI_move = AI.find_best_move(game_context, valid_moves)
                if AI_move is None:
                    AI_move = AI.find_random_move(valid_moves)
                else:
                    print("dupa")
                current_view.game_context.make_move(AI_move)
                current_view.move_made = True
                current_view.present_animations = True

            if current_view.move_made:
                if current_view.present_animations:
                    current_view.animate_move(game_view.current_view.game_context.moveLog[-1])
                current_view.valid_moves = current_view.game_context.get_valid_moves()
                current_view.move_made = False
                current_view.present_animations = False

            if current_view.game_context.checkmate:
                current_view.is_game_over = True
                if current_view.game_context.white_to_move:
                    current_view.draw_text("Black Wins by checkmate!")
                else:
                    current_view.draw_text("White Wins by checkmate!")
            elif current_view.game_context.stalemate:
                current_view.is_game_over = True
                current_view.draw_text("Stalemate")

    @staticmethod
    def on_mouse_button_down(event):
        """Handle all left mouse button actions

        Args:
            event (int): event code

        Returns:
            int: corresponding event number.
        """
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                return 4
            elif event.button == 2:
                return 5
            elif event.button == 3:
                return 6
        return 0
