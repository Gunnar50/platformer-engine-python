import dataclasses
import enum
from typing import Iterator

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


class InputType(enum.Enum):
  BUTTON = 'button'
  MOUSE = 'mouse'


class InputMappings(pydantic.BaseModel):
  label: str
  type: InputType
  input_name: str
  input_id: int


class InputConfig(pydantic.BaseModel):
  config: list[InputMappings]


@dataclasses.dataclass
class Position(serialisers.Serialiser):
  x: int
  y: int

  def export(self) -> dict[str, int]:
    return {'x': self.x, 'y': self.y}

  def __iter__(self) -> Iterator[int]:
    return iter((self.x, self.y))


class TileType(enum.Enum):
  GRASS = 'grass'
  DIRT = 'dirt'
  BUSH = 'bush'
