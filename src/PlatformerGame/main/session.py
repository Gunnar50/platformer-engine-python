from src.PlatformerGame.scene.world_grid import Scene
from src.PyEng.components.components import GameComponent


class GameSession(GameComponent):

  def __init__(self) -> None:
    self.scene = Scene()

  def update(self):
    self.scene.update()
    self.scene.render()
    # self.renderer.render_scene(self.scene)
