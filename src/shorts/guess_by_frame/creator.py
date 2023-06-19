import argparse
import asyncio
from pathlib import Path
import subprocess
from PIL import Image, ImageOps
from moviepy.editor import *
from moviepy.audio.fx.all import volumex
from src.config import Config
from src.image_search_engine.google_api import GoogleAPISceneEngine

# TODO: Integrate this into Telegram pipeline
# TODO: Change GoogleAPISceneEngine to something related to MoviesAPI

FONT = "/Users/alexslavutin1999/PetProjects/AIContentGeneration/data/VantelyPersonalUse-3zMWG.otf"

def resize_and_save(image_path, resized_image_path):
    img = Image.open(image_path)

    # Ensure img is in RGBA mode which supports transparency
    img = img.convert('RGBA')

    original_width, original_height = img.size
    target_width, target_height = 650, 700

    # Calculate target aspect ratio
    target_ratio = target_width / target_height

    # Calculate the new width and height
    if original_width / original_height > target_ratio:
        # The image is wider than the target aspect ratio, so size will be determined by width
        new_width = target_width
        new_height = round(original_height * target_width / original_width)
    else:
        # The image is taller than the target aspect ratio, so size will be determined by height
        new_height = target_height
        new_width = round(original_width * target_height / original_height)

    # Resize the image
    img = img.resize((new_width, new_height), Image.BICUBIC)

    # Calculate the padding sizes
    padding_sizes = ((target_width - new_width) // 2, (target_height - new_height) // 2)

    # Add padding with transparency
    img = ImageOps.expand(img, padding_sizes, fill=(0, 0, 0, 0))  # Fill with transparent color

    img.save(resized_image_path)



async def run(args):
    print("Starting")
    config = Config()
    # 1. Search for a movie scene and download the image
    engine = GoogleAPISceneEngine(num_frames_per_request=1,
                                  api_key=config.env_variables.google_api_key,
                                  custom_search_cx=config.env_variables.google_cx)

    print("Searching")
    scene = await engine.search(args.movie_name)
    await engine.download(scene, "/Users/alexslavutin1999/PetProjects/AIContentGeneration/output_images/")

    # # Assume the first image in the list is what you need
    downloaded_scene_path = scene[0].path 
    print(downloaded_scene_path)

    poster = await engine.search(args.movie_name, q="Poster for movie")
    await engine.download(poster, "/Users/alexslavutin1999/PetProjects/AIContentGeneration/output_images/")
    downloaded_poster_path =  poster[0].path
    print(downloaded_poster_path)

    scene_image_path = "/Users/alexslavutin1999/PetProjects/AIContentGeneration/output_images/scene.png"
    poster_image_path =  "/Users/alexslavutin1999/PetProjects/AIContentGeneration/output_images/poster.png"
    resize_and_save(downloaded_scene_path,  scene_image_path)
    resize_and_save(downloaded_poster_path,  poster_image_path)


    print("Inserting")
    # 3. Insert the resized image onto the video
    video = VideoFileClip(args.video, audio=False)  # Replace with your video path
    scene = (ImageClip(scene_image_path)
             .set_start(1.5)
             .set_duration(5)
             .set_position(('center', 450)))  # x-coordinate is set to center

    poster = (ImageClip(poster_image_path)
              .set_start(8.5)
              .set_duration(2)
              .set_position(('center', 450)))  # x-coordinate is set to center

    txt_clip = (TextClip(args.movie_name, fontsize=75, color='green', font=FONT)  # You can change the font as per your preference
                .set_start(8.5)
                .set_duration(2)
                .set_position(('center', 1300)))

    video_name = Path(args.movie_name).stem
    final = CompositeVideoClip([video, scene, poster, txt_clip]) #
    output_video_path = f"/Users/alexslavutin1999/PetProjects/AIContentGeneration/data/{video_name}.mp4"
    final.write_videofile(output_video_path, codec='libx264')  
        # Add the audio with ffmpeg
    subprocess.run(["ffmpeg", "-i", output_video_path, "-i",
                    f"/Users/alexslavutin1999/PetProjects/AIContentGeneration/data/quiz_music_1.mp3", "-c:v", "copy", "-c:a",
                    "aac", "-map", "0:v:0", "-map", "1:a:0", 
                    f"/Users/alexslavutin1999/PetProjects/AIContentGeneration/result_videos/{video_name}_with_sound.mp4"])# Replace with your output video path

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--movie_name', type=str, required=True)
    parser.add_argument('--video', type=str, required=True)
    args = parser.parse_args()
    
    asyncio.run(run(args))