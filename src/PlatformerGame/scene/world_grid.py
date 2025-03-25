import pathlib
from typing import TYPE_CHECKING, Optional

import pygame

from src.PlatformerGame.main.configs.build_config import BuildConfig
from src.PlatformerGame.scene.tile import Tile
from src.PyEng.components.components import GameComponent
from src.PyEng.main.engine import Engine
from src.shared import api, io, serialisers


class Scene(GameComponent):
  WORLD_SIZE = 10

  def __init__(self) -> None:
    GameComponent.__init__(self)
    self.window = Engine.get_instance().window
    self.world_grid = WorldGrid(self, Scene.WORLD_SIZE)

  def update(self):
    pass

  def render(self):
    self.world_grid.render(self.window.display)


class WorldGrid(serialisers.Exportable, GameComponent):

  def __init__(self, scene: Scene, world_size: int) -> None:
    serialisers.Exportable.__init__(self)
    GameComponent.__init__(self)
    self.tile_map: dict[tuple[int, int, int], Tile] = {}
    self.scene = scene
    self.world_size = world_size
    game_manager_component = self.components_manager.get_game_manager()
    self.tile_blueprints = game_manager_component.get_blueprint_database().tiles
    self.setup_grid()

  def reset(self):
    self.tile_map.clear()

  def save(self, file_path: pathlib.Path) -> None:
    output = {'tile_map': []}
    for position in self.tile_map:
      output['tile_map'].append({
          'position': [
              self.tile_map[position].position.x,
              self.tile_map[position].position.y,
          ],
          'layer': self.tile_map[position].layer,
          'variant': self.tile_map[position].variant,
          'tile_type': self.tile_map[position].components.tile_type.value,
      })

    io.write_json(file_path, output)

  def load(self, file_path: pathlib.Path) -> None:
    self.reset()
    map_data = io.load_json(file_path)
    for tile_data in map_data['tile_map']:
      x, y = tile_data['position'][0], tile_data['position'][1]
      layer = tile_data['layer']
      variant = tile_data['variant']
      self.create_tile(x, y, api.TileType(tile_data['tile_type']), variant,
                       layer)

  def setup_grid(self):
    for i in range(10):
      # Create example tiles
      self.create_tile(3 + i, 10, api.TileType.GRASS, 0, 0)
      self.create_tile(10, 5 + i, api.TileType.DIRT, 0, 0)

  def create_tile(
      self,
      x: int,
      y: int,
      tile_type: api.TileType,
      variant: int,
      layer: int,
  ) -> Tile:
    tile_bluprint = self.tile_blueprints.get(tile_type.value)
    tile = tile_bluprint.create_instance(position_x=x,
                                         position_y=y,
                                         grid=self,
                                         variant=variant,
                                         layer=layer)
    self.add_tile(tile)
    return tile

  def remove_tile(self, x: int, y: int, layer: int) -> Optional[Tile]:
    if (x, y, layer) in self.tile_map:
      return self.tile_map.pop((x, y, layer))
    return None

  def add_tile(self, tile: Tile) -> None:
    self.tile_map.update({(tile.position.x, tile.position.y, tile.layer): tile})

  def get_tile_at(self, x: float, y: float, layer: int) -> Optional[Tile]:
    if x > 0 and y > 0:
      return self.get_tile(int(x), int(y), layer)
    else:
      return None

  def get_tile(self, x: int, y: int, layer: int) -> Optional[Tile]:
    return self.tile_map.get((x, y, layer))

  def draw_grid(self, screen: pygame.Surface):
    for x in range(0, BuildConfig.window_width, BuildConfig.tile_width):
      pygame.draw.line(screen, (150, 150, 150), (x, 0),
                       (x, BuildConfig.window_height))

    for y in range(0, BuildConfig.window_height, BuildConfig.tile_height):
      pygame.draw.line(screen, (150, 150, 150), (0, y),
                       (BuildConfig.window_width, y))

  def render(self, screen: pygame.Surface) -> None:
    self.draw_grid(screen)
    positions = sorted(self.tile_map.keys(), key=lambda position: position[2])
    for position in positions:
      if tile := self.tile_map.get(position):
        tile.render_tile(screen)

  def get_serialiser(self) -> serialisers.Serialiser:
    return WorldGridSerialiser()


class WorldGridSerialiser(serialisers.Serialiser):

  def export(self, writer) -> None:
    raise NotImplementedError
