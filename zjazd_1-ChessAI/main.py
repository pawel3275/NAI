from views.window import MAX_FPS
from utilities.event import EventHandler
from views.window import Window
from views.view_handler import ViewHandler
import pygame

"""
    ChessAI by Pawel Iwinski & Cezary Graban

"""
if __name__ == '__main__':
    """Main game function
    """
    pygame.init()
    game_main_window = Window()
    game_view = ViewHandler()
    clock = pygame.time.Clock()

    # valid_moves = game_view.views[1].game_context.get_valid_moves()
    # square_selection = ()
    # player_clicks = []
    # move_made = False
    while EventHandler.window_code != 2:
        # Event processing
        for event in pygame.event.get():
            eventCode = EventHandler.process_event(event)
            if EventHandler.view_code == 1:
                EventHandler.mouse_board_process(event, game_view)

        game_view.draw_view()

        clock.tick(MAX_FPS)
        pygame.display.flip()
