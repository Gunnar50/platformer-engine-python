import pygame
from src.PyEng.components.components import GameComponent
from src.shared.api import Position, Velocity


class PhysicsEntity(GameComponent):

  def __init__(self, x: int, y: int, entity_type: str) -> None:
    GameComponent.__init__(self)
    self.position = Position(x, y)
    self.velocity = Velocity(0, 0)
    self.acceleration = Velocity(0, 0)
    self.entity_type = entity_type

  def update(self) -> None:
    self.acceleration += self.velocity
    self.position += self.acceleration

  def render(self, screen: pygame.Surface) -> None:
    pass
