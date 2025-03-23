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
    self.tile_map: dict[tuple[int, int], Tile] = {}
    self.scene = scene
    self.world_size = world_size
    game_manager_component = self.components_manager.get_game_manager()
    self.tile_blueprints = game_manager_component.get_blueprint_database().tiles
    self.setup_grid()

  def save(self, file_path: pathlib.Path) -> None:
    output = {'tile_map': {}}
    for position in self.tile_map:
      output['tile_map'][str(position)] = {
          'x': self.tile_map[position].position.x,
          'y': self.tile_map[position].position.y,
          'tile_type': self.tile_map[position].components.tile_type.value
      }

    io.write_json(file_path, output)

  def load(self, file_path: pathlib.Path) -> None:
    map_data = io.load_json(file_path)
    for position in map_data['tile_map']:
      tile_data = map_data['tile_map'][position]
      self.create_tile(tile_data['x'], tile_data['y'],
                       api.TileType(tile_data['tile_type']))

  def setup_grid(self):
    for i in range(10):
      # Create example tiles
      self.create_tile(3 + i, 10, api.TileType.GRASS)
      self.create_tile(10, 5 + i, api.TileType.DIRT)

  def create_tile(self, x: int, y: int, tile_type: api.TileType) -> Tile:
    tile = self.tile_blueprints.get(tile_type.value).create_instance(x, y, self)
    self.add_tile(tile)
    return tile

  def remove_tile(self, x: int, y: int) -> Optional[Tile]:
    if (x, y) in self.tile_map:
      return self.tile_map.pop((x, y))

    return None

  def add_tile(self, tile: Tile) -> None:
    self.tile_map.update({(tile.position.x, tile.position.y): tile})

  def get_tile_from_id(self, id: int):
    x, y = id // self.world_size, id % self.world_size
    return self.get_tile(x, y)

  def get_tile_at(self, x: float, y: float) -> Optional[Tile]:
    if x > 0 and y > 0:
      return self.get_tile(int(x), int(y))
    else:
      return None

  def get_tile(self, x: int, y: int) -> Optional[Tile]:
    return self.tile_map.get((x, y))

  def draw_grid(self, screen: pygame.Surface):
    for x in range(0, BuildConfig.window_width, BuildConfig.tile_width):
      pygame.draw.line(screen, (150, 150, 150), (x, 0),
                       (x, BuildConfig.window_height))

    for y in range(0, BuildConfig.window_height, BuildConfig.tile_height):
      pygame.draw.line(screen, (150, 150, 150), (0, y),
                       (BuildConfig.window_width, y))

  def render(self, screen: pygame.Surface):
    self.draw_grid(screen)
    for tile in self.tile_map.values():
      tile.render_tile(screen)

  def get_serialiser(self) -> serialisers.Serialiser:
    return WorldGridSerialiser()


class WorldGridSerialiser(serialisers.Serialiser):

  def export(self, writer) -> None:
    raise NotImplementedError
