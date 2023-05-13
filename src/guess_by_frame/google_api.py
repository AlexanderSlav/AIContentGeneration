from typing import List

from google_images_search import GoogleImagesSearch

from src.guess_by_frame.abstract_search_engine import SceneSearchEngine
from src.logger import get_logger

logger = get_logger(__name__)


class GoogleAPISceneEngine(SceneSearchEngine):
    def __init__(
        self,
        movie_name: str,
        num_frames_per_request: int,
        api_key: str,
        custom_search_cx: str,
    ):
        """
        Initializes a GoogleAPISceneEngine instance.

        Args:
            movie_name (str): Name of the movie for image search.
            num_frames_per_request (int): Number of images to return per request.
            api_key (str): Google API key.
            custom_search_cx (str): Custom search engine ID from Google CSE.

        """
        super().__init__(movie_name, num_frames_per_request)
        self.api_key = api_key
        self.custom_search_cx = custom_search_cx

    def search(self) -> List:
        """
        Searches for images of movie scenes via Google Images Search.

        Returns:
            List: List of image objects returned from the search.

        """
        logger.debug(f"Searching for {self.movie_name} movie scene")
        gis = GoogleImagesSearch(self.api_key, self.custom_search_cx)

        # Define search params
        _search_params = {
            "q": f"Scene from {self.movie_name} film",
            "num": self.num_frames_per_request,
            "safe": "high",
            "fileType": "jpg|gif|png",
        }

        gis.search(search_params=_search_params)
        return gis.results()

    def download(self, download_path: str):
        """
        Downloads images from the search results.

        Args:
            download_path (str): Path to download the images.

        """
        results = self.search()
        if results:
            for image in results:
                logger.debug(image.url)
                try:
                    image.download(download_path)
                    logger.debug(f"Image downloaded at {download_path}/{image.path}")
                except Exception as e:
                    logger.error(f"Error downloading image: {e}")
