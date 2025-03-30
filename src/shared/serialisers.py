import abc
from typing import Any


class Serialiser(abc.ABC):

  @abc.abstractmethod
  def export(self) -> Any:
    pass
