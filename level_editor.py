from numpy import tile
from src.PlatformerGame.main.configs.build_config import EditorConfig
from src.PlatformerGame.main.game_manager import GameManager
from src.PyEng.main.engine import Engine
from src.shared import key_mappings


class LevelEditor:

  def __init__(self) -> None:
    self.engine = Engine.create(EditorConfig)
    self.game_manager = GameManager(self.engine)
    self.input = self.game_manager.components_manager.get_input()
    self.scene = self.game_manager.current_session.get_scene()

  def run(self) -> None:
    while True:
      self.game_manager.update()
      self.engine.update()

      if self.input.pressed(key_mappings.EditorMapping.UP):
        print('UP')
      if self.input.pressed(key_mappings.EditorMapping.MOUSE_LEFT):
        mx, my = self.input.mouse.get_position()
        print(mx, my)
        self.scene.world_grid.create_tile(mx, my, 'grass')

      if self.input.holding(
          key_mappings.EditorMapping.CONTROL) and self.input.pressed(
              key_mappings.EditorMapping.UP):
        print('CONTROL + UP')


if __name__ == '__main__':
  LevelEditor().run()
