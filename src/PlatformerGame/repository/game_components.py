import dataclasses
import enum

import pygame

from src.PlatformerGame.main.configs.build_config import BuildConfig
from src.PlatformerGame.scene.tile import Tile
from src.PlatformerGame.scene.world_grid import WorldGrid
from src.shared import api
from src.shared.hash_registry import Registrable


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
  tile_type: api.TileType

  def create_instance(
      self,
      position_x: int,
      position_y: int,
      grid: WorldGrid,
      variant: int,
      layer: int,
  ) -> Tile:
    return Tile(
        api.Position(position_x, position_y),
        grid,
        self,
        variant,
        layer,
    )

  def render_preview(
      self,
      screen: pygame.Surface,
      position_x: int,
      position_y: int,
      variant: int,
  ) -> None:
    screen.blit(
        self.images[variant],
        (
            position_x * BuildConfig.tile_width,
            position_y * BuildConfig.tile_height,
        ),
    )
