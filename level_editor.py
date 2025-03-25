import pathlib
from src.PlatformerGame.main.configs.build_config import EditorConfig
from src.PlatformerGame.main.game_manager import GameManager
from src.PyEng.main.engine import Engine
from src.PyEng.main.engine_files import EngineFiles
from src.shared import api, key_mappings


class LevelEditor:

  def __init__(self) -> None:
    self.engine = Engine.create(EditorConfig)
    self.game_manager = GameManager(self.engine)
    self.input = self.game_manager.components_manager.get_input()
    self.scene = self.game_manager.current_session.get_scene()
    self.tile_types = list(api.TileType)
    self.variant = 0
    self.layer = 0
    self.tile_type_index = 0
    self.current_tile_type = self.tile_types[self.tile_type_index]

  def run(self) -> None:
    while True:
      self.game_manager.update()
      self.engine.update()

      # Adding and removing tiles
      if self.input.holding(key_mappings.EditorMapping.MOUSE_RIGHT):
        mx, my = self.input.mouse.get_position()
        self.scene.world_grid.remove_tile(mx, my, self.layer)

      if self.input.holding(key_mappings.EditorMapping.MOUSE_LEFT):
        mx, my = self.input.mouse.get_position()
        self.scene.world_grid.create_tile(mx, my, self.current_tile_type,
                                          self.variant, self.layer)
      # Update tile type
      if self.input.pressed(key_mappings.EditorMapping.UP):
        self.tile_type_index = (self.tile_type_index + 1) % len(self.tile_types)
        self.current_tile_type = self.tile_types[self.tile_type_index]
      if self.input.pressed(key_mappings.EditorMapping.DOWN):
        self.tile_type_index = (self.tile_type_index - 1) % len(self.tile_types)
        self.current_tile_type = self.tile_types[self.tile_type_index]

      # Use if and elif when checking for multiple key presses
      # TODO: Find a better way to handle multiple key presses
      if self.input.pressed(key_mappings.EditorMapping.RIGHT):
        self.scene.world_grid.save(EngineFiles.DATA_FOLDER / 'map.map')
        print('Saved!')
      elif self.input.pressed(key_mappings.EditorMapping.LEFT):
        self.scene.world_grid.load(EngineFiles.DATA_FOLDER / 'map.map')


if __name__ == '__main__':
  LevelEditor().run()
