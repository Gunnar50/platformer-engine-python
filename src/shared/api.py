import enum

import pydantic
import pygame

from src.shared.types import Coordinate


class RenderObjects(pydantic.BaseModel):
  image: pygame.Surface
  position: Coordinate
  destination_surface: pygame.Surface
  layer: int

  # This is to allow pygame.Surface to be passed as a type
  model_config = pydantic.ConfigDict(arbitrary_types_allowed=True)


class KeyMapping(enum.Enum):
  QUIT = 'quit'
  RIGHT = 'right'
  LEFT = 'left'
  UP = 'up'
  DOWN = 'down'
  MOUSE_LEFT = 'mouse_left'
  MOUSE_MIDDLE = 'mouse_middle'
  MOUSE_RIGHT = 'mouse_right'


class InputType(enum.Enum):
  BUTTON = 'button'
  MOUSE = 'mouse'


class InputMappings(pydantic.BaseModel):
  label: str
  type: InputType
  input_id: int


class InputConfig(pydantic.BaseModel):
  config: list[InputMappings]
