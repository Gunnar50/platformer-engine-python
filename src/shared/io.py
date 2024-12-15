import json
import os
import pathlib
from typing import Any

from src.shared import exceptions
from src.shared.debug import LOGGER


def load_json(file_path: pathlib.Path) -> Any:
  if os.path.exists(file_path):
    with open(file_path, 'r') as f:
      return json.load(f)
  else:
    LOGGER.error(f'File path {file_path} not found. Exiting...')
    raise exceptions.FilePathNotFound

