from abc import ABC, abstractmethod


class SceneSearchEngine(ABC):
    def __init__(self, movie_name, num_frames_per_request):
        self.movie_name = movie_name
        self.num_frames_per_request = num_frames_per_request

    @abstractmethod
    def search(self):
        pass

    @abstractmethod
    def download(self, download_path):
        pass
