# -*- coding: utf-8 -*-
"""
Created on Sun Jan 23 13:50:07 2022

@author: richa
"""
import random
from typing import List
from typing import Tuple

import pygame
from hexagon import FlatTopHexagonTile
from hexagon import HexagonTile
from card import CardTile

# pylint: disable=no-member

BLACK = (0, 0, 0)
BROWN = (87, 41, 12)
MEDIUM_TAN = (201, 184, 115)
GREEN = (26, 117, 14)

def create_hexagon(position, radius=100, flat_top=False) -> HexagonTile:
    """Creates a hexagon tile at the specified position"""
    class_ = FlatTopHexagonTile if flat_top else HexagonTile
    return class_(radius, position, colour=MEDIUM_TAN)#colour=get_random_colour())

def get_random_colour(min_=150, max_=255) -> Tuple[int, ...]:
    """Returns a random RGB colour with each component between min_ and max_"""
    return tuple(random.choices(list(range(min_, max_)), k=3))

def init_cards(num=5) -> List[CardTile]:
    card_position = (0, 750)
    leftmost_card = CardTile(150, 250, position=card_position, colour=GREEN)
    cards = [leftmost_card]

    for x in range(num):
        if x:
            card_position = (card_position[0]+150, card_position[1])
            leftmost_card = CardTile(150, 250, position=card_position, colour=GREEN)
            cards.append(leftmost_card)

    return cards

def init_hexagons(num_x=3, num_y=3, flat_top=False) -> List[HexagonTile]:
    """Creates a hexaogonal tile map of size num_x * num_y"""
    # pylint: disable=invalid-name
    leftmost_hexagon = create_hexagon(position=(325, 0), flat_top=flat_top)
    hexagons = [leftmost_hexagon]
    for x in range(num_y):
        if x:
            # alternate between bottom left and bottom right vertices of hexagon above
            index = 2 if x % 2 == 1 or flat_top else 4
            position = leftmost_hexagon.vertices[index]
            leftmost_hexagon = create_hexagon(position, flat_top=flat_top)
            hexagons.append(leftmost_hexagon)

        # place hexagons to the left of leftmost hexagon, with equal y-values.
        hexagon = leftmost_hexagon
        num_hex = num_x if x % 2 == 1 else (num_x - 1)
        for i in range(num_hex):
            x, y = hexagon.position  # type: ignore
            if flat_top:
                if i % 2 == 1:
                    position = (x + hexagon.radius * 3 / 2, y - hexagon.minimal_radius)
                else:
                    position = (x + hexagon.radius * 3 / 2, y + hexagon.minimal_radius)
            else:
                position = (x + hexagon.minimal_radius * 2, y)
            hexagon = create_hexagon(position, flat_top=flat_top)
            hexagons.append(hexagon)

    return hexagons


def render(screen, hexagons, cards, selected_cards, font):
    """Renders game objects on the screen"""
    screen.fill(BROWN)
    game_objects = hexagons + cards
    for game_object in game_objects:
        game_object.render(screen, font)

    # highlight colliding game objects
    colliding_game_objects = colliding_objects(game_objects)
    for game_object in colliding_game_objects + selected_cards:
        # for neighbour in hexagon.compute_neighbours(hexagons):
        #     neighbour.render_highlight(screen, border_colour=(100, 100, 100))
        game_object.render_highlight(screen, border_colour=BLACK)
    pygame.display.flip()

def colliding_objects(g_objects):
    mouse_pos = pygame.mouse.get_pos()
    return [
        g_object for g_object in g_objects if g_object.collide_with_point(mouse_pos)
    ]

def main():
    """Main function"""
    pygame.init()
    font = pygame.font.SysFont("Arial", 12, bold=True)
    screen = pygame.display.set_mode((1000, 1000))
    clock = pygame.time.Clock()
    hexagons = init_hexagons(flat_top=False)
    cards = init_cards()
    selected_cards = []
    terminated = False
    while not terminated:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminated = True
            elif event.type == pygame.MOUSEBUTTONDOWN:
                colliding_cards = colliding_objects(cards)
                if colliding_cards:
                    selected_cards = colliding_cards

        for hexagon in hexagons:
            hexagon.update()

        for card in cards:
            card.update()

        render(screen, hexagons, cards, selected_cards, font)
        clock.tick(50)
    pygame.display.quit()


if __name__ == "__main__":
    main()
