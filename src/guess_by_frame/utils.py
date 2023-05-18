from typing import List

from pydantic import BaseModel


class Scene(BaseModel):
    path_to_image: str
    movie_name: str


class SceneCollector:
    def __init__(self):
        self.confirmed_scenes: List[Scene] = []

    def add_scene(self, confirmed_scene: Scene):
        self.confirmed_scenes.append(confirmed_scene)

    def get_scenes(self):
        return self.confirmed_scenes
