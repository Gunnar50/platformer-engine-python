import pathlib
import sys
import time
from typing import Any

import pygame

from src.PyEng.components.components import SystemComponent
from src.shared import api, io
from src.shared.debug import LOGGER


class InputState:

  def __init__(self, label: str, type: str, input_id: int):
    self.label = label
    self.type = type
    self.input_id = input_id

    self.pressed = False
    self.just_pressed = False
    self.just_released = False
    self.held_since = 0.0

  def update(self):
    self.just_pressed = False
    self.just_released = False

  def press(self):
    self.pressed = True
    self.just_pressed = True
    self.held_since = time.time()

  def unpress(self):
    self.pressed = False
    self.just_released = True


class Input(SystemComponent):

  def __init__(self, key_mappings_path: pathlib.Path):
    SystemComponent.__init__(self)
    self.config: list[dict[str, Any]] = io.load_json(key_mappings_path)
    self.input = {
        api.KeyMapping(mapping['label']): InputState(**mapping)
        for mapping in self.config
    }

    self.keyboard = Keyboard()
    self.mouse = Mouse()

  def pressed(self, key: api.KeyMapping):
    return self.input[key].just_pressed if key in self.input else False

  def holding(self, key):
    return self.input[key].pressed if key in self.input else False

  def released(self, key):
    return self.input[key].just_released if key in self.input else False

  def update(self):
    for state in self.input.values():
      state.update()

    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        pygame.quit()
        sys.exit()

      if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_ESCAPE:
          pygame.quit()
          sys.exit()
        elif event.key == pygame.K_SPACE:
          LOGGER.info(self.input)

        for state in self.input.values():
          if state.type == 'button':
            if event.key == state.input_id:
              state.press()


class Keyboard:
  """Keyboard inputs for main keys"""


class Mouse:
  """Mouse inputs for main keys"""
