from PIL import Image

def convert_image_to_youtube_banner(image_path: str, output_path: str):
    desired_size = (2560, 1440)  # Recommended YouTube banner size

    img = Image.open(image_path)
    img.thumbnail(desired_size, Image.ANTIALIAS)

    new_img = Image.new("RGB", desired_size, (255, 255, 255))  # Create a new white image
    new_img.paste(img, ((desired_size[0] - img.size[0]) // 2, 
                        (desired_size[1] - img.size[1]) // 2))  # Paste the scaled image in the center

    new_img.save(output_path, "JPEG")

convert_image_to_youtube_banner("../../Downloads/msg411852252-362666.jpg", "youtube_banner.jpg")

width = 680
height = 910
