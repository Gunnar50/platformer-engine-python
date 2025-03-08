from src.PlatformerGame.main.configs.build_config import BuildConfig
from src.PlatformerGame.main.game_manager import GameManager
from src.PyEng.main.engine import Engine
from src.shared import api


class LevelEditor:

  def __init__(self) -> None:
    self.engine = Engine.create(BuildConfig)
    self.game_manager = GameManager(self.engine)
    self.input = self.game_manager.components_manager.get_input()

  def run(self) -> None:
    while True:
      self.game_manager.update()
      self.engine.update()

      if self.input.pressed(api.KeyMapping.DOWN):
        print('DOWN')
      if self.input.pressed(api.KeyMapping.MOUSE_LEFT):
        print('MOUSE_LEFT')
        print(self.input.mouse.position)


if __name__ == '__main__':
  LevelEditor().run()
