import imageio
from PIL import Image, ImageDraw, ImageFont


def generate_frame(question, progress):
    # Load the background image
    background = Image.open(
        "/Users/alexslavutin/PetProjects/AIContentGeneration/output_images/test_images/54685.jpg"
    )  # Replace 'background.jpg' with your image path

    # Create a blank image with transparent background
    frame = Image.new("RGBA", background.size, (0, 0, 0, 0))

    # Paste the background image onto the frame
    frame.paste(background, (0, 0))

    # # Draw the progress bar
    # progress_width = int(background.width * progress)
    # progress_height = 30  # Adjust the progress bar height as needed
    # progress_bar = Image.new('RGBA', (progress_width, progress_height), (0, 0, 0, 255))
    # frame.paste(progress_bar, (0, background.height - progress_height))

    # Calculate the diameter and radius of the progress circle
    radius = int(min(background.width, background.height) * 0.4)
    diameter = 2 * radius

    # Calculate the position of the progress circle's top-left corner
    x = (background.width - diameter) // 2
    y = (background.height - diameter) // 2

    # Draw the progress circle
    progress_angle = 360 * progress
    start_angle = 90  # Start the progress bar at the top of the circle
    end_angle = start_angle + progress_angle
    progress_bar = Image.new("RGBA", (diameter, diameter), (255, 255, 255, 128))
    draw = ImageDraw.Draw(progress_bar)
    draw.pieslice(
        [(0, 0), (diameter, diameter)], start_angle, end_angle, fill=(0, 0, 0, 255)
    )
    frame.paste(progress_bar, (x, y))

    # Draw the countdown text
    countdown_text = str(
        int(5 - progress * 5)
    )  # Calculate the countdown value for 5-second question
    font_path = (
        "/Users/alexslavutin/PetProjects/AIContentGeneration/data/Montserrat-Bold.ttf"
    )
    font_size = 48  # Adjust the font size as needed
    font = ImageFont.truetype(font_path, font_size)
    text_width, text_height = font.getsize(countdown_text)
    text_position = (
        (background.width - text_width) // 2,
        (background.height - text_height) // 2,
    )

    draw = ImageDraw.Draw(frame)
    draw.text(text_position, countdown_text, font=font, fill=(255, 255, 255, 255))

    # Draw the question text
    question_font_size = 65  # Adjust the question font size as needed
    question_font = ImageFont.truetype(font_path, question_font_size)
    question_text_width, question_text_height = question_font.getsize(question)
    question_text_position = (
        (background.width - question_text_width) // 2,
        (background.height - question_text_height) // 2
        + text_height
        + 30,  # Adjust the vertical position as needed
    )

    draw.text(
        question_text_position, question, font=question_font, fill=(255, 255, 255, 255)
    )

    # Return the frame image
    return frame


# Configure the output video file path and name
output_file = "output.mp4"

# Configure video parameters
fps = 1  # Frames per second (adjust as needed)
duration_per_question = 5  # Duration of each question in seconds
total_questions = 3
total_frames = fps * duration_per_question * total_questions

# Create a list to store frames
frames = []

# Generate frames
for i in range(total_frames):
    question_index = i // (fps * duration_per_question)
    progress = (i % (fps * duration_per_question)) / (fps * duration_per_question)
    question = "Question " + str(question_index + 1)
    frame = generate_frame(question, progress)
    frames.append(frame)

# Save frames as a video file
imageio.mimsave(output_file, frames, fps=fps)

print(f"Video file saved as: {output_file}")
