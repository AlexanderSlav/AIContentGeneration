from enum import Enum


class ContentTypeRequest(Enum):
    guess_by_scene = "get_scene_from_movie"
    guess_by_dialogue = "get_dialogue_for_movie"
    guess_by_music_theme = "get_music_theme_for_movie"


class StateKeys(Enum):
    GAME_TYPE = "game_type"
