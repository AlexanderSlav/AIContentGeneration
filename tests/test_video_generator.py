from unittest.mock import MagicMock, patch

import pytest
from pydantic import BaseModel

from src.video_utils import VideoGenerator


class MockConfig(BaseModel):
    image_paths = (
        "/Users/alexslavutin/PetProjects/AIContentGeneration/output_images/test_images"
    )
    output_path = "output.mp4"
    music_path = (
        "/Users/alexslavutin/PetProjects/AIContentGeneration/data/thinking_time.mp3"
    )
    fps = 1
    output_video_codec = "libx264"


test_config = MockConfig()


@pytest.fixture
def mock_image_sequence_clip():
    with patch("moviepy.editor.ImageSequenceClip") as mock:
        yield mock


@pytest.fixture
def mock_audio_file_clip():
    with patch("moviepy.editor.AudioFileClip") as mock:
        yield mock


def test_video_generator(mock_image_sequence_clip, mock_audio_file_clip):
    # Mock the write_videofile method
    mock_clip_instance = mock_image_sequence_clip.return_value
    mock_clip_instance.write_videofile = MagicMock()

    generator = VideoGenerator(test_config)
    generator.generate_video()

    # Assert ImageSequenceClip and AudioFileClip are called with correct arguments
    mock_image_sequence_clip.assert_called_with(test_config)
    mock_audio_file_clip.assert_called_with(test_config.music_path)

    # # Assert write_videofile is called with correct arguments
    # mock_clip_instance.write_videofile.assert_called_with("output.mp4", codec="libx264")
