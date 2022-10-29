import pygame

WINDOW_SIZE = (1366, 768)
WINDOW_MODE_FLAGS = 0
MAX_FPS = 30
BORDER_GAP = 8
DEFAULT_BACKGROUND_COLOR = (255, 100, 125)


class Window:
    """Class containing main game window attributes.
    """
    def __init__(self):
        """Constructor
        """
        self.window_buttons = []
        self.screen = pygame.display.set_mode(WINDOW_SIZE, WINDOW_MODE_FLAGS)
        self.background_colour = DEFAULT_BACKGROUND_COLOR
        self.screen.fill(self.background_colour)
        pygame.display.set_caption("ChessAI")
        pygame.display.flip()

