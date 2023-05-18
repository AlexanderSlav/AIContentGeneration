import pytest

from src.guess_by_frame.utils import SceneCollector


@pytest.fixture
def scene_collector():
    return SceneCollector()
