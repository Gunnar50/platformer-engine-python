import dataclasses
import enum

import pygame

from src.PlatformerGame.main.configs.build_config import BuildConfig
from src.PlatformerGame.scene.tile import Tile
from src.PlatformerGame.scene.world_grid import WorldGrid
from src.PyEng.components.components import GameComponent
from src.shared.hash_registry import Registrable


@dataclasses.dataclass
class Position(GameComponent):
  x: int
  y: int


class TileType(enum.Enum):
  GRASS = 'grass'
  SOIL = 'soil'
  PATH = 'path'
  SELECTION = 'selection'
  STONE_PATH = 'stone_path'


@dataclasses.dataclass
class Blueprint(Registrable):
  """
  Name: the unique name for this type of blueprint
  Group: the group this blueprint belongs (eg. tile, entities, crop)
  Layer: the layer that is rendered in (crops are rendered on top of tiles)
  Images: tuple containing the loaded images
  """
  name: str
  group: str
  layer: int
  images: list[pygame.Surface]

  def __post_init__(self):
    # Scale images to the correct tile size
    self.images = [
        pygame.transform.scale(
            image, (BuildConfig.tile_width, BuildConfig.tile_height))
        for image in self.images
    ]

  def get_name(self) -> str:
    return self.name


@dataclasses.dataclass
class EntityBlueprint(Blueprint):

  def create_instance(self):
    pass


@dataclasses.dataclass
class ItemBlueprint(Blueprint):

  def create_instance(self):
    pass


@dataclasses.dataclass
class TileBlueprint(Blueprint):
  tile_type: TileType

  def create_instance(
      self,
      position_x: int,
      position_y: int,
      grid: WorldGrid,
  ) -> Tile:
    return Tile(Position(position_x, position_y), grid, self)
