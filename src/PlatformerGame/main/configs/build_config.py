from src.PlatformerGame.main.configs.game_config import GameConfig


class BuildConfig(GameConfig):
  """Build Configs"""
  window_width = 1280
  window_height = 720
  title = f'Platform Engine - Version: {GameConfig.version}'
  fullscreen = 0
  cheats = True
  is_editor = False

  # World settings
  map_width = 10
  map_height = 10
  tile_width = 16
  tile_height = 16


class EditorConfig(GameConfig):
  """Level Editor Configs"""
  window_width = 1280
  window_height = 720
  title = f'Level Editor - Version: {GameConfig.version}'
  fullscreen = 0
  is_editor = True

  # World settings
  map_width = 10
  map_height = 10
  tile_width = 16
  tile_height = 16
