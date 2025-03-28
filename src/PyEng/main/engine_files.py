from pathlib import Path


class EngineFiles:
  # Get the root folder dynamically based on the location of this file
  # Go up 3 levels to 'src' folder
  # All other folder will be relative to 'src'
  ROOT_FOLDER = Path(__file__).resolve().parents[3]

  DATA_FOLDER = ROOT_FOLDER / 'data'
  ERROR_FOLDER = ROOT_FOLDER / 'ErrorLogs'

  GUI_FOLDER = DATA_FOLDER / 'GUI'
  SOUNDS_FOLDER = DATA_FOLDER / 'sounds'
  FONT_FOLDER = DATA_FOLDER / 'fonts'
  GAME_MAPPINGS = DATA_FOLDER / 'config/game_mappings.json'
  EDITOR_MAPPINGS = DATA_FOLDER / 'config/level_editor_mappings.json'

  DEFAULT_FONT_ATLAS = FONT_FOLDER / 'default.png'
  DEFAULT_FONT_META = FONT_FOLDER / 'default.fnt'
