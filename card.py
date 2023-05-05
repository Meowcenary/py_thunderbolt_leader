from dataclasses import dataclass
from typing import List
from typing import Tuple

import pygame


@dataclass
class CardTile:
    """Card tile class"""

    width: int
    height: int
    position: Tuple[float, float]
    colour: Tuple[int, ...]
    highlight_offset: int = 3
    max_highlight_ticks: int = 15
    bottom_left: Tuple[int, int] = None
    top_right: Tuple[int, int] = None
    name: str = "Default Name"

    def __post_init__(self):
        self.vertices = self.compute_vertices()
        self.highlight_tick = 0

    def update(self):
        """Updates tile highlights"""
        if self.highlight_tick > 0:
            self.highlight_tick -= 1

    def compute_vertices(self) -> List[Tuple[int, int]]:
        """Returns a list of the card's vertices as x, y tuples"""
        x, y = self.position
        self.bottom_left = (x, y + self.height)
        self.top_right = (x + self.width, y)

        return [
            (x, y),
            self.top_right,
            (x + self.width, y + self.height),
            self.bottom_left
        ]

    def collide_with_point(self, point: Tuple[int, int]) -> bool:
        """Returns True if distance from centre to point is less than horizontal_length"""

        if point[0] > self.bottom_left[0] and point[0] < self.top_right[0] and \
                point[1] < self.bottom_left[1] and point[1] > self.top_right[1]:
            return True
        else:
            return False

    def render(self, screen, font, border_colour=(0, 0, 0)) -> None:
        """Renders the hexagon on the screen"""
        pygame.draw.polygon(screen, self.highlight_colour, self.vertices)
        pygame.draw.aalines(screen, border_colour, closed=True, points=self.vertices)

        ## Temp - Text rendering that should be moved to individual card classes
        text_padding = 3
        text_line_spacing = 20
        font.set_underline(True)
        name_text = font.render(self.name, True, (0, 0, 0))
        stats = ["Aim:", "Speed:", "Cool:"]

        top_left = (self.bottom_left[0] + text_padding, self.bottom_left[1] - self.height + text_padding)
        screen.blit(name_text, top_left)

        font.set_underline(False)
        spacing = text_line_spacing
        for stat in stats:
            text = font.render(stat, True, (0, 0, 0))
            screen.blit(text, (top_left[0], top_left[1] + spacing))
            spacing += text_line_spacing

    def render_highlight(self, screen, border_colour) -> None:
        """Draws a border around the hexagon with the specified colour"""
        self.highlight_tick = self.max_highlight_ticks

    @property
    def highlight_colour(self) -> Tuple[int, ...]:
        """Colour of the card tile when rendering highlight"""
        offset = self.highlight_offset * self.highlight_tick
        brighten = lambda x, y: x + y if x + y < 255 else 255
        return tuple(brighten(x, offset) for x in self.colour)
