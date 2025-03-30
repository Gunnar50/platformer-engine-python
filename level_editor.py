import pathlib
from src.PlatformerGame.main.configs.build_config import EditorConfig
from src.PlatformerGame.main.game_manager import GameManager
from src.PyEng.main.engine import Engine
from src.PyEng.main.engine_files import EngineFiles
from src.shared import api, key_mappings


class LevelEditor:

  def __init__(self) -> None:
    # Initialise the system
    self.engine = Engine.create(EditorConfig)
    self.game_manager = GameManager(self.engine)

    # Get necessary components
    self.window = self.game_manager.components_manager.get_window()
    self.input = self.game_manager.components_manager.get_input()
    self.scene = self.game_manager.current_session.get_scene()
    self.world = self.scene.world_grid

    # Tiles
    self.tiles_blueprint = self.game_manager.get_blueprint_database().tiles
    self.tile_types = list(api.TileType)
    self.variant = 0
    self.layer = 0
    self.update_tile = False
    self.tile_type_index = 0
    self.current_tile_type = self.tile_types[self.tile_type_index]
    self.selected_tile = self.tiles_blueprint.get(self.current_tile_type.value)

    # Mouse position
    self.mx, self.my = 0, 0

  def run(self) -> None:
    while True:
      self.game_manager.update()
      self.engine.update()
      self.mx, self.my = self.input.mouse.get_position()

      # Adding and removing tiles
      if self.input.holding(key_mappings.EditorMapping.MOUSE_RIGHT):
        self.world.remove_tile(self.mx, self.my, self.layer)

      if self.input.holding(key_mappings.EditorMapping.MOUSE_LEFT):
        self.world.create_tile(self.mx, self.my, self.current_tile_type,
                               self.variant, self.layer)

      # TODO: Find a better way to handle multiple key presses
      # Update tile type if control + scroll
      if self.input.holding(key_mappings.EditorMapping.CONTROL):
        if self.input.pressed(key_mappings.EditorMapping.MOUSE_SCROLL_UP):
          self.tile_type_index = (self.tile_type_index + 1) % len(
              self.tile_types)
        elif self.input.pressed(key_mappings.EditorMapping.MOUSE_SCROLL_DOWN):
          self.tile_type_index = (self.tile_type_index - 1) % len(
              self.tile_types)
        self.variant = 0
        self.update_tile = True
      else:
        # Update variant
        if self.input.pressed(key_mappings.EditorMapping.MOUSE_SCROLL_UP):
          self.variant = (self.variant + 1) % len(self.selected_tile.images)
        elif self.input.pressed(key_mappings.EditorMapping.MOUSE_SCROLL_DOWN):
          self.variant = (self.variant - 1) % len(self.selected_tile.images)
        self.update_tile = True

      if self.update_tile:
        self.current_tile_type = self.tile_types[self.tile_type_index]
        self.selected_tile = self.tiles_blueprint.get(
            self.current_tile_type.value)
        self.update_tile = False

      if self.input.pressed(key_mappings.EditorMapping.RIGHT):
        self.scene.world_grid.save(EngineFiles.DATA_FOLDER / 'map.map')
        print('Saved!')
      elif self.input.pressed(key_mappings.EditorMapping.LEFT):
        self.scene.world_grid.load(EngineFiles.DATA_FOLDER / 'map.map')
        print('Loaded!')

      self.selected_tile.render_preview(
          self.window.display,
          self.mx,
          self.my,
          self.variant,
      )


if __name__ == '__main__':
  LevelEditor().run()
