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
      self.engine.update()

      if Engine.get_instance().input.pressed(api.KeyMapping.DOWN):
        print('DOWN')
      if self.engine.get_instance().input.pressed(api.KeyMapping.MOUSE_LEFT):
        print('MOUSE_LEFT')
        print(Engine.get_instance().input.mouse.position)

    # self.game_manager.clean_up()


if __name__ == "__main__":
  # EngineTester().run()
  GameApp().run()
  # GameApp()
