import pygame

colors_dictionary = {
    "red": (200, 0, 0),
    "green": (0, 200, 0),
    "white": (255, 255, 255),
    "black": (0, 0, 0)
}


class Button:
    stop_the_game = "Button to stop the game"
    start_the_game = "Button to start the game"

    all_buttons = []

    def __init__(self, action_on_click, text, text_color, color, center, width, height, screen):
        self.action_on_click = action_on_click
        self.text = text
        self.text_color = colors_dictionary.get(text_color)
        self.color = colors_dictionary.get(color)
        self.center = center
        self.width = width
        self.height = height
        self.screen = screen
        self.font = pygame.font.Font("freesansbold.ttf", 20)
        self.text_surface = None
        self.rect = None
        self._update(self.text, self.color)
        self.draw()
        Button.all_buttons.append(self)

    @staticmethod
    def pass_event_to_all_buttons(event):
        list_of_actions_to_do = []
        for button in Button.all_buttons:
            list_of_actions_to_do.append(button.handle_event(event))
        return list_of_actions_to_do

    def draw(self):
        self._update(self.text, self.color)
        self.screen.blit(self.text_surface, self.rect)

    def _update(self, text, color):
        self.color = color
        self.text = text
        pygame.draw.rect(self.screen, self.color, (
            self.center[0] - self.width / 2, self.center[1] - self.height / 2,
            self.width, self.height))
        self.text_surface = self.font.render(self.text, True, self.text_color)
        self.rect = self.text_surface.get_rect(center=(self.center[0], self.center[1]))

    def handle_event(self, event):
        if event.type is not pygame.MOUSEBUTTONDOWN:
            return None
        if self.rect.collidepoint(event.pos):
            return self.action_on_click
