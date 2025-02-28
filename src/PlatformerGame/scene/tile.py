import enum
from typing import TYPE_CHECKING, Optional

import pygame

from src.PlatformerGame.main.configs.build_config import BuildConfig

if TYPE_CHECKING:
  from src.PlatformerGame.repository.game_components import (Position,
                                                             TileBlueprint,
                                                             TileType)
  from src.PlatformerGame.scene.world_grid import WorldGrid


class Direction(enum.Enum):
  NORTH_WEST = (-1, -1)
  NORTH = (0, -1)
  NORTH_EAST = (1, -1)
  WEST = (-1, 0)
  EAST = (1, 0)
  SOUTH_WEST = (-1, 1)
  SOUTH = (0, 1)
  SOUTH_EAST = (1, 1)

  def __init__(self, relavite_x: int, relavite_y: int) -> None:
    self.relative_x = relavite_x
    self.relative_y = relavite_y

  def get_relative_pos(self) -> tuple[int, int]:
    return self.relative_x, self.relative_y


class GameObject:

  def __init__(
      self,
      position: 'Position',
      world_grid: 'WorldGrid',
  ) -> None:
    self.position = position
    self.grid = world_grid


class Tile(GameObject):

  def __init__(
      self,
      position: 'Position',
      world_grid: 'WorldGrid',
      components: 'TileBlueprint',
  ) -> None:
    GameObject.__init__(self, position, world_grid)
    self.components = components
    self.variant = 0

  def get_neighbours(self) -> list[Optional['Tile']]:
    return [
        self.get_neighbour(Direction.NORTH),
        self.get_neighbour(Direction.EAST),
        self.get_neighbour(Direction.SOUTH),
        self.get_neighbour(Direction.WEST),
    ]

  def get_neighbour(self, direction: Direction) -> Optional['Tile']:
    relative_x, relative_y = direction.get_relative_pos()
    grid_x = self.position.x + relative_x
    grid_y = self.position.y + relative_y
    return self.grid.get_tile(grid_x, grid_y)

  def get_tile_id(self) -> int:
    return (self.position.x * self.grid.world_size) + self.position.y

  def get_position(self) -> 'Position':
    return self.position

  def get_tile_type(self) -> 'TileType':
    return self.components.tile_type

  def render_tile(self, screen: pygame.Surface):
    screen.blit(
        self.components.images[self.variant],
        (
            self.position.x * BuildConfig.tile_width,
            self.position.y * BuildConfig.tile_width,
        ),
    )

  def __str__(self) -> str:
    return f'Tile({self.position.x}, {self.position.y})'

  def __repr__(self) -> str:
    return f'Tile({self.position.x}, {self.position.y}, {self.components.name})'
