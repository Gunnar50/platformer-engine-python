from pathlib import Path


class EngineFiles:
  # Get the root folder dynamically based on the location of this file
  # Go up 3 levels to 'src' folder
  # All other folder will be relative to 'src'
  ROOT_FOLDER = Path(__file__).resolve().parents[3]

  ASSETS_FOLDER = ROOT_FOLDER / 'assets'
  ERROR_FOLDER = ROOT_FOLDER / 'ErrorLogs'
