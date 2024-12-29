import pygame
class UI:
    def __init__(self, screen, button_font, button_width, button_height, colors):
        """
        Initializes the UI class.

        Args:
            screen (pygame.Surface): The game screen to draw on.
            button_font (pygame.font.Font): Font for buttons.
            button_width (int): Default width of buttons.
            button_height (int): Default height of buttons.
            colors (dict): Dictionary containing color definitions.
        """
        self.screen = screen
        self.button_font = button_font
        self.button_width = button_width
        self.button_height = button_height
        self.colors = colors

    def wrap_text(self, text, font, max_width):
        """
        Wraps text to fit within a certain width.

        Args:
            text (str): The text to wrap.
            font (pygame.font.Font): The font object to use.
            max_width (int): The maximum width of the text.

        Returns:
            list: List of Surfaces, each containing a line of text.
        """
        words = text.split(' ')
        lines = []
        current_line = []
        for word in words:
            test_line = ' '.join(current_line + [word])
            test_surface = font.render(test_line, True, self.colors["WHITE"])
            if test_surface.get_width() > max_width:
                lines.append(' '.join(current_line))
                current_line = [word]
            else:
                current_line.append(word)
        if current_line:
            lines.append(' '.join(current_line))
        return [font.render(line, True, self.colors["WHITE"]) for line in lines]

    def slice_button_map(self, button_map, button_width, button_height):
        """
        Slices a button map into individual button textures.

        Args:
            button_map (pygame.Surface): The button map image.
            button_width (int): Width of each button.
            button_height (int): Height of each button.

        Returns:
            list: List of button textures.
        """
        rows = button_map.get_height() // button_height
        cols = button_map.get_width() // button_width
        textures = []
        for row in range(rows):
            for col in range(cols):
                rect = pygame.Rect(col * button_width, row * button_height, button_width, button_height)
                texture = button_map.subsurface(rect).copy()
                textures.append(texture)
        return textures

    def draw_button_with_texture(self, text, x, y, state, textures):
        """
        Draws a button with a texture and text.

        Args:
            text (str): The text to display on the button.
            x (int): X-coordinate of the button.
            y (int): Y-coordinate of the button.
            state (str): The state of the button (normal, hovered, clicked).
            textures (dict): Dictionary containing button textures for different states.

        Returns:
            pygame.Rect: The rectangle of the button.
        """
        texture = textures[state]
        self.screen.blit(texture, (x, y))

        wrapped_text = self.wrap_text(text, self.button_font, self.button_width - 10)
        total_text_height = sum(line.get_height() for line in wrapped_text)
        start_y = y + (self.button_height - total_text_height) // 2

        for line_surface in wrapped_text:
            line_rect = line_surface.get_rect(center=(x + self.button_width // 2, start_y + line_surface.get_height() // 2))
            self.screen.blit(line_surface, line_rect)
            start_y += line_surface.get_height()

        return pygame.Rect(x, y, self.button_width, self.button_height)
    def draw_textbox(self, dialogues, position, textbox_image, font, text_margin, wrap_width, dialogue_index):
        """
        Simplified text box function to display full dialogue text and switch dialogues on click.

        Args:
            dialogues (list): List of dialogue strings to display.
            position (tuple): (x, y) position of the top-left corner of the text box.
            textbox_image (pygame.Surface): The image for the text box background.
            font (pygame.font.Font): Font for the text inside the text box.
            text_margin (int): Margin around the text inside the text box.
            wrap_width (int): Maximum width for text wrapping.
            dialogue_index (int): Index of the current dialogue line.

        Returns:
            tuple: Updated (dialogue_index, done).
        """
        x, y = position
        self.screen.blit(textbox_image, position)

        # Get current dialogue
        current_dialogue = dialogues[dialogue_index]

        # Wrap the text for the current dialogue
        wrapped_text = self.wrap_text(current_dialogue, font, wrap_width)

        # Render the text inside the box
        current_y = y + text_margin
        for line_surface in wrapped_text:
            self.screen.blit(line_surface, (x + text_margin, current_y))
            current_y += line_surface.get_height()

        # Check if we're on the last dialogue
        done = dialogue_index == len(dialogues) - 1
        return dialogue_index, done


