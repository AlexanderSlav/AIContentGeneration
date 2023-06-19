#!/bin/bash

# Define the Python script command
CMD="python src/shorts/guess_by_frame/creator.py --video data/guess_the_movie_background_with_sound.mp4 --movie_name"

# Create an array of the movie list files
MOVIE_LISTS=("movies.txt")

# Loop over the movie list files
for MOVIE_LIST in ${MOVIE_LISTS[@]}; do
  while IFS= read -r MOVIE_NAME; do
    echo "Processing movie: $MOVIE_NAME"
    # Run the Python script with the current movie name
    # $CMD "$MOVIE_NAME"
  done < "$MOVIE_LIST"
done
