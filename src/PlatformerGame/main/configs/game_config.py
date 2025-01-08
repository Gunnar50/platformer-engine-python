from src.PlatformerGame.main.game_state import GameState
from src.PyEng.main.engine_config import EngineConfigs
from src.shared.version import Version


class GameConfig(EngineConfigs):
  """Game Configs"""
  version = Version(0, 0, 0)
  game_speed = 1
  cheats = True
  show_debug = True
  auto_save = True
  session_creator = NotImplemented
  initial_state = GameState.INITIAL
  in_game_state = GameState.IN_GAME
