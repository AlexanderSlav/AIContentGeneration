from typing import List

from moviepy.editor import AudioFileClip, ImageSequenceClip


# TODO recode all images to be one size
class VideoGenerator:
    def __init__(self, config):
        # self.image_paths = config.image_paths
        self.output_path = config.out_video_params.output_path
        self.music_path = config.out_video_params.music_path
        self.fps = config.out_video_params.fps
        self.video_codec = config.out_video_params.output_video_codec

    def generate_video(self, image_paths: List[str]):
        # Create a clip from the image sequence and add music to it
        clip = ImageSequenceClip(image_paths, fps=self.fps)
        audio = AudioFileClip(self.music_path)
        final_clip = clip.set_audio(audio)
        final_clip.write_videofile(self.output_path, codec=self.video_codec)
