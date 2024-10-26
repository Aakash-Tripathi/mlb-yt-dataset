import json
import multiprocessing
import os

from mlb_dataset.utils import local_clip


def wrapper(clip, input_directory, output_directory):
    """
    Prepares and processes a video clip by extracting a continuous segment as specified.

    Parameters:
        clip (dict): Dictionary containing details for a clip, including "url", "start", "end", and optionally "clip_name".
            - "url" (str): The video URL, from which the video ID is derived.
            - "start" (int): Start time of the clip segment in seconds.
            - "end" (int): End time of the clip segment in seconds.
            - "clip_name" (str, optional): Custom name for the output clip file.
        input_directory (str): Directory path where input video files are located.
        output_directory (str): Directory path where the output clips will be saved.

    Returns:
        str: Status indicating the result of the clipping operation:
             - "Created" if the clip was successfully created,
             - "Missing Input" if the input file is not found,
             - or "Error: <error message>" if an error occurred during processing.
    """
    duration = (
        clip["end"] - clip["start"]
    )  # Calculate the duration for the clip segment
    video_id = clip["url"].split("=")[-1]  # Extract video ID from the URL
    input_path = os.path.join(
        input_directory, f"{video_id}.mkv.mp4"
    )  # Construct input file path

    # Define output filename, using "clip_name" if available, otherwise default to video ID and segment times
    output_filename = f"{clip.get('clip_name', video_id)}.mp4"
    output_path = os.path.join(
        output_directory, output_filename
    )  # Construct output file path

    # Check if the input file exists
    if not os.path.exists(input_path):
        print(f"Missing input file: {input_path}")
        return "Missing Input"

    # Attempt to create the clip using local_clip function
    result = local_clip(input_path, clip["start"], duration, output_path)
    return "Created" if result is None else f"Error: {result}"


def extract_continuous_clips(manifest_path, input_directory, output_directory):
    """
    Extracts continuous segments from multiple videos as specified in a JSON manifest file.

    Parameters:
        manifest_path (str): Path to the JSON manifest file containing clip information for multiple videos.
                             Each entry should include video URL, start, and end times, and optionally a clip name.
        input_directory (str): Directory path where input video files are located.
        output_directory (str): Directory path where output clips will be saved.

    Returns:
        dict: A summary dictionary with the counts of each result type:
              - "Created": Number of successfully created clips.
              - "Skipped": Number of clips skipped (note: Skipping logic not implemented in wrapper here).
              - "Missing Input": Number of clips with missing input files.
              - "Errors": List of error messages encountered during processing.
    """
    # Load the clip data from the JSON manifest file
    with open(manifest_path, "r") as f:
        data = json.load(f)
        clips = [(data[key], input_directory, output_directory) for key in data.keys()]

    # Initialize summary to keep track of the extraction results
    summary = {"Created": 0, "Skipped": 0, "Missing Input": 0, "Errors": []}

    # Use multiprocessing to extract clips concurrently
    with multiprocessing.Pool(processes=8) as pool:
        for result in pool.starmap(wrapper, clips):
            # Update summary based on the result from each wrapper call
            if result == "Created":
                summary["Created"] += 1
            elif result == "Skipped":
                summary["Skipped"] += 1
            elif result == "Missing Input":
                summary["Missing Input"] += 1
            elif result.startswith("Error"):
                summary["Errors"].append(result)

    # Print and return the summary of extraction results
    print("Summary:", summary)
    return summary
