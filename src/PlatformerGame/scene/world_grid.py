from typing import TYPE_CHECKING, Optional

import pygame

from src.PlatformerGame.scene.tile import Tile
from src.PyEng.components.components import GameComponent
from src.shared import serialisers

if TYPE_CHECKING:
  from src.PlatformerGame.main.game_manager import GameManager


class Scene(GameComponent):
  WORLD_SIZE = 10

  def __init__(self) -> None:
    GameComponent.__init__(self)
    self.window = self.components_manager.get_by_class('Window')
    self.world_grid = WorldGrid(self, Scene.WORLD_SIZE)

  def update(self):
    pass

  def render(self):
    self.world_grid.render(self.window.display)


class WorldGrid(serialisers.Exportable, GameComponent):

  def __init__(self, scene: Scene, world_size: int) -> None:
    serialisers.Exportable.__init__(self)
    GameComponent.__init__(self)
    self.tilemap: list[Tile] = []
    self.scene = scene
    self.world_size = world_size
    game_manage_component: GameManager = self.components_manager.get_by_class(
        'GameManager')
    self.tile_blueprints = game_manage_component.get_blueprint_database().tiles
    self.setup_grid()

  def setup_grid(self):
    for i in range(10):
      # Create a grass tile
      tile = self.tile_blueprints.get('grass').create_instance(3 + i, 10, self)
      tile2 = self.tile_blueprints.get('grass').create_instance(10, 5 + i, self)
      self.tilemap.extend([tile, tile2])

  def add_tile(self, tile: Tile) -> None:
    self.tilemap.append(tile)

  def get_tile_from_id(self, id: int):
    x, y = id // self.world_size, id % self.world_size
    return self.get_tile(x, y)

  def get_tile_at(self, x: float, y: float) -> Optional[Tile]:
    if x > 0 and y > 0:
      return self.get_tile(int(x), int(y))
    else:
      return None

  def get_tile(self, x: int, y: int) -> Optional[Tile]:
    if 0 < x < self.world_size and 0 < y < self.world_size:
      return self.tilemap[x][y]
    else:
      return None

  def render(self, screen: pygame.Surface):
    for tile in self.tilemap:
      tile.render_tile(screen)

  def get_serialiser(self) -> serialisers.Serialiser:
    return WorldGridSerialiser()


class WorldGridSerialiser(serialisers.Serialiser):

  def export(self, writer) -> None:
    raise NotImplementedError
