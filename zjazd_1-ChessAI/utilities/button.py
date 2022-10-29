import pygame

SMALL_BUTTON_SIZE = [250, 100]
LARGE_BUTTON_SIZE = [250, 200]
DEFAULT_BUTTON_COLOR = (175, 175, 175)
DEFAULT_BUTTON_TEXT_COLOR = (0, 0, 0)
ON_BUTTON_COLLISION_COLOR = (215, 215, 215)


class Button:
    """Class for buttons in main menu and during the game.
    """
    def __init__(self, screen, button_id, size, text, box_color=DEFAULT_BUTTON_COLOR,
                 text_color=DEFAULT_BUTTON_TEXT_COLOR, font='arial', font_size=35):
        self.screen = screen
        self.id = button_id
        self.box_color = box_color
        self.text_color = text_color
        self.font = pygame.font.SysFont(font, font_size)
        self.text = text
        self.rect = pygame.Rect(size)

    def add_rect(self):
        """Adds button rectangle to the list
        """
        pygame.draw.rect(self.screen, self.box_color, self.rect)

    def add_text(self):
        """Adds button text and blits the screen
        """
        text_surface = self.font.render(self.text, True, self.text_color)
        text_scale_width = (self.rect[2] / len(self.text)) * 1.55
        text_scale_height = self.rect[3] / 3.2
        text_position = (self.rect[0] + text_scale_width, self.rect[1] + text_scale_height)
        self.screen.blit(text_surface, text_position)

    def draw_button(self):
        """Performs the button drawings
        """
        self.add_rect()
        self.add_text()
        pygame.display.update()
