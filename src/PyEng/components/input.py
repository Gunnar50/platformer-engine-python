import pathlib
import sys
import time

import pygame

from src.PyEng.components.components import SystemComponent
from src.shared import api, io
from src.shared.debug import LOGGER


class InputState:

  def __init__(self, label: str, type: api.InputType, input_id: int):
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
    self.config = io.load_model_from_json(key_mappings_path, api.InputConfig)
    self.input = {
        api.KeyMapping(mapping.label):
            InputState(mapping.label, mapping.type, mapping.input_id)
        for mapping in self.config.config
    }

    self.keyboard = Keyboard(self.input)
    self.mouse = Mouse(self.input)

  def pressed(self, key: api.KeyMapping) -> bool:
    return self.input[key].just_pressed if key in self.input else False

  def holding(self, key) -> bool:
    return self.input[key].pressed if key in self.input else False

  def released(self, key) -> bool:
    return self.input[key].just_released if key in self.input else False

  def update(self):
    for state in self.input.values():
      state.update()

    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        pygame.quit()
        sys.exit()

      self.keyboard.update(event)
      self.mouse.update(event)


class Keyboard:

  def __init__(self, input_config: dict[api.KeyMapping, InputState]):
    self.input = input_config

  def update(self, event: pygame.event.Event):
    if event.type == pygame.KEYDOWN:
      if event.key == pygame.K_ESCAPE:
        pygame.quit()
        sys.exit()
      elif event.key == pygame.K_SPACE:
        LOGGER.info(self.input)

      for state in self.input.values():
        if state.type == api.InputType.BUTTON and event.key == state.input_id:
          state.press()

    elif event.type == pygame.KEYUP:
      for state in self.input.values():
        if state.type == api.InputType.BUTTON and event.key == state.input_id:
          state.unpress()


class Mouse:

  def __init__(self, input_config: dict[api.KeyMapping, InputState]):
    self.input = input_config
    self.position = pygame.Vector2(0, 0)
    self.ui_position = pygame.Vector2(0, 0)
    self.movement = pygame.Vector2(0, 0)

  def update(self, event: pygame.event.Event):
    mx, my = pygame.mouse.get_pos()
    self.position = pygame.Vector2(mx, my)
    self.ui_x, self.ui_y = self.position.x // 2, self.position.y // 2

    if event.type == pygame.MOUSEBUTTONDOWN:
      for state in self.input.values():
        if state.type == api.InputType.MOUSE and event.button == state.input_id:
          state.press()

    elif event.type == pygame.MOUSEBUTTONUP:
      for state in self.input.values():
        if state.type == api.InputType.MOUSE and event.button == state.input_id:
          state.unpress()
