import pygame

colors_dictionary = {
    "red": (200, 0, 0),
    "green": (0, 200, 0),
    "white": (255, 255, 255),
    "black": (0, 0, 0)
}


class Button:

    all_buttons = []

    def __init__(self, text, text_color, color, center, width, height, screen):
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
        self._update(self.color)
        self.draw()
        Button.all_buttons.append(self)

    @staticmethod
    def pass_event_to_all_buttons(event):
        for button in Button.all_buttons:
            button.handle_event(event)

    def draw(self):
        self._update(self.color)
        self.screen.blit(self.text_surface, self.rect)

    def _update(self, color):
        self.color = color
        pygame.draw.rect(self.screen, self.color, (
            self.center[0] - self.width / 2, self.center[1] - self.height / 2,
            self.width, self.height))
        self.text_surface = self.font.render("Start", True, self.text_color)
        self.rect = self.text_surface.get_rect(center=(self.center[0], self.center[1]))

    def handle_event(self, event):
        print(event)
        if event.type is not pygame.MOUSEBUTTONDOWN:
            return []
        if self.rect.collidepoint(event.pos):
            self._update(colors_dictionary.get("white"))
