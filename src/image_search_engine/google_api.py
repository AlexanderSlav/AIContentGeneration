import asyncio
import concurrent.futures as futures
from concurrent.futures import ThreadPoolExecutor
from typing import List

from google_images_search import GoogleImagesSearch

from src.image_search_engine.abstract_search_engine import SceneSearchEngine
from src.logger import get_logger

logger = get_logger(__name__)


class GoogleAPISceneEngine(SceneSearchEngine):
    def __init__(
        self,
        num_frames_per_request: int,
        api_key: str,
        custom_search_cx: str,
    ):
        super().__init__(num_frames_per_request=num_frames_per_request)
        self.api_key = api_key
        self.custom_search_cx = custom_search_cx

    async def search(self, movie_name: str, q: str =  "Scene from movie ") -> List:
        """
        Searches for images of movie scenes via Google Images Search.

        Returns:
            List: List of image objects returned from the search.

        """
        # Async call to Google Images Search API
        loop = asyncio.get_event_loop()
        with futures.ThreadPoolExecutor(max_workers=5) as pool:
            results = await loop.run_in_executor(pool, self._search_movie, movie_name, q)

        return results

    def _search_movie(self, movie_name: str, q: str = "Scene from movie ") -> List:
        """
        Searches for scenes of the movie and returns the result.

        Returns:
            List: List of image objects returned from the search.

        """
        logger.debug(f"Searching for {movie_name}")
        gis = GoogleImagesSearch(self.api_key, self.custom_search_cx)

        # Define search params
        _search_params = {
            "q": f"{q}: {movie_name}",
            "num": self.num_frames_per_request,
            "safe": "high",
            "fileType": "jpg|gif|png",
        }

        # Sync call to Google Images Search API
        gis.search(_search_params)

        return gis.results()

    async def download(self, images_to_download: List, download_path: str):
        """
        Downloads images from the search results.

        Args:
            results: List of image objects returned from the search.
            download_path (str): Path to download the images.

        """
        if images_to_download:
            with ThreadPoolExecutor(max_workers=5) as executor:
                loop = asyncio.get_event_loop()
                for image in images_to_download:
                    logger.debug(image.url)
                    try:
                        await loop.run_in_executor(
                            executor, image.download, download_path
                        )
                        logger.debug(
                            f"Image downloaded at {image.path}"
                        )
                    except Exception as e:
                        logger.error(f"Error downloading image: {e}")
                return image.path
