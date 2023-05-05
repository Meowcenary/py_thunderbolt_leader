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
        return [
            (x, y),
            (x + self.width, y),
            (x, y + self.height),
            (x + self.width, y + self.height)
        ]

    def collide_with_point(self, bottom_left: Tuple[int, int], top_right: Tuple[int, int]) -> bool:
        """Returns True if distance from centre to point is less than horizontal_length"""
        return True

    def render(self, screen, border_colour=(0, 0, 0)) -> None:
        """Renders the hexagon on the screen"""
        pygame.draw.polygon(screen, self.highlight_colour, self.vertices)
        pygame.draw.aalines(screen, border_colour, closed=True, points=self.vertices)

    def render_highlight(self, screen, border_colour) -> None:
        """Draws a border around the hexagon with the specified colour"""
        self.highlight_tick = self.max_highlight_ticks

    @property
    def highlight_colour(self) -> Tuple[int, ...]:
        """Colour of the card tile when rendering highlight"""
        offset = self.highlight_offset * self.highlight_tick
        brighten = lambda x, y: x + y if x + y < 255 else 255
        return tuple(brighten(x, offset) for x in self.colour)

    # @property
    # def top_left(self) -> Tuple[float, float]:
