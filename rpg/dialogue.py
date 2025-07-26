import pygame
from settings import WHITE, BLACK, WIDTH, HEIGHT

class DialogueBox:
    def __init__(self, screen, font, width, height):
        self.screen = screen
        self.font = font
        self.width = width
        self.height = height
        self.rect = pygame.Rect(20, HEIGHT - height - 20, width, height)
        self.text = ""
        self.visible = False
        self.text_index = 0
        self.displayed_text = ""
        self.done = False
        self.choices = []
        self.selected_choice = 0
        self.await_choice = False

    def start(self, text, choices=None):
        self.text = text
        self.text_index = 0
        self.displayed_text = ""
        self.visible = True
        self.done = False
        self.choices = choices or []
        self.selected_choice = 0
        self.await_choice = len(self.choices) > 0

    def update(self):
        if self.visible and not self.done and not self.await_choice:
            if self.text_index < len(self.text):
                self.text_index += 1
                self.displayed_text = self.text[:self.text_index]

    def draw(self):
        if self.visible:
            pygame.draw.rect(self.screen, BLACK, self.rect)
            pygame.draw.rect(self.screen, WHITE, self.rect, 2)
            lines = self.wrap_text(self.displayed_text, self.font, self.width - 20)
            y_offset = self.rect.y + 10
            for line in lines:
                txt_surf = self.font.render(line, True, WHITE)
                self.screen.blit(txt_surf, (self.rect.x + 10, y_offset))
                y_offset += self.font.get_height() + 2

            if self.await_choice:
                for idx, choice in enumerate(self.choices):
                    color = (255, 255, 0) if idx == self.selected_choice else WHITE
                    choice_surf = self.font.render(choice, True, color)
                    self.screen.blit(choice_surf, (self.rect.x + 40, y_offset))
                    y_offset += self.font.get_height() + 4

    def handle_event(self, event):
        if self.visible and event.type == pygame.KEYDOWN:
            if self.await_choice:
                if event.key == pygame.K_UP:
                    self.selected_choice = (self.selected_choice - 1) % len(self.choices)
                elif event.key == pygame.K_DOWN:
                    self.selected_choice = (self.selected_choice + 1) % len(self.choices)
                elif event.key == pygame.K_RETURN:
                    self.done = True
                    self.visible = False
            else:
                if event.key == pygame.K_RETURN:
                    if not self.done:
                        self.displayed_text = self.text
                        self.done = True
                    else:
                        self.visible = False

    def wrap_text(self, text, font, max_width):
        words = text.split(' ')
        lines = []
        current_line = ""
        for word in words:
            test_line = current_line + word + " "
            if font.size(test_line)[0] <= max_width:
                current_line = test_line
            else:
                lines.append(current_line)
                current_line = word + " "
        lines.append(current_line)
        return lines
              
