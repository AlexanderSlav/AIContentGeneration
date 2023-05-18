from abc import ABC, abstractmethod


class SceneSearchEngine(ABC):
    def __init__(self, num_frames_per_request: int):
        self.num_frames_per_request: int = num_frames_per_request

    @abstractmethod
    async def search(self):
        pass

    @abstractmethod
    async def download(self, download_path):
        pass
