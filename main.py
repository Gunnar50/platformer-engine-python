from src.PlatformerGame.main.configs.build_config import BuildConfig
from src.PlatformerGame.main.game_manager import GameManager
from src.PyEng.main.engine import Engine
from src.shared import api


class EngineTester:

  def __init__(self) -> None:
    self.engine = Engine.create()

  def update(self) -> None:
    self.engine.update()

  def run(self) -> None:
    while True:
      self.update()


class GameApp:

  def __init__(self) -> None:
    self.engine = Engine.create(BuildConfig)
    self.game_manager = GameManager(self.engine)

  def run(self) -> None:
    while True:
      self.game_manager.update()
      # Update engine
      self.engine.update()
      if self.game_manager.components_manager.get_by_class('Input').pressed(
          api.KeyMapping.UP):
        print('UP')
    # self.game_manager.clean_up()


if __name__ == "__main__":
  # EngineTester().run()
  GameApp().run()
  # GameApp()
