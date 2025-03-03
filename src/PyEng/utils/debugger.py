import pygame

from src.PyEng.components.components import SystemComponent


class Debugger(SystemComponent):

  def __init__(self, debug: bool = False) -> None:
    SystemComponent.__init__(self)
    self.debug: dict = {}
    self.debugging = debug
    self.font = pygame.font.SysFont('Consolas', 10)
    self.register_info('test')
    self.window = self.components_manager.get_window()

  def get_info(self):
    for i, key in enumerate(self.debug):
      text = self.font.render(f'{key}:{self.debug[key]}', True, (255, 255, 255),
                              (0, 0, 0))
      text_rect = text.get_rect()
      text_rect.x = 0
      text_rect.y = 20 * i
      self.window.display.blit(text, text_rect)

  def register_info(self, info: str):
    self.debug[len(self.debug)] = info

  def update(self):
    self.get_info()
