import json
import multiprocessing
import os

from tqdm import tqdm

from mlb_dataset.utils import local_clip


def wrapper(clip, input_directory, output_directory):
    """
    Prepares and processes a video clip by extracting a specified segment.

    Parameters:
        clip (dict): Dictionary containing clip details, with "url", "start", and "end" keys.
            - "url" (str): The video URL, from which the video ID is extracted.
            - "start" (int): Start time of the clip segment in seconds.
            - "end" (int): End time of the clip segment in seconds.
        input_directory (str): Path to the directory containing downloaded video files.
        output_directory (str): Path to the directory where the clipped segment will be saved.

    Returns:
        str: Status message indicating the result of the clip extraction:
             "Created" if the clip is successfully created,
             "Skipped" if the output file already exists,
             "Missing Input" if the input file does not exist,
             or "Error: <error message>" if an error occurs during clipping.
    """
    duration = clip["end"] - clip["start"]  # Calculate duration of the clip segment
    video_id = clip["url"].split("=")[-1]  # Extract video ID from the URL
    input_path = os.path.join(
        input_directory, f"{video_id}.mkv.mp4"
    )  # Expected input file path
    output_filename = f"{video_id}_{int(clip['start'])}_{int(clip['end'])}.mp4"
    output_path = os.path.join(
        output_directory, output_filename
    )  # Path for the output clip file

    # Check if the output file already exists
    if os.path.exists(output_path):
        return "Skipped"

    # Check if the input file is available
    if not os.path.exists(input_path):
        print(f"Missing input file: {input_path}")
        return "Missing Input"

    # Attempt to create the clip
    result = local_clip(input_path, clip["start"], duration, output_path)
    return "Created" if result is None else f"Error: {result}"


def extract_segmented_clips(manifest_path, input_directory, output_directory):
    """
    Extracts segments from multiple videos as specified in a JSON manifest file, using multiprocessing.

    Parameters:
        manifest_path (str): Path to the JSON file containing clip information for multiple videos.
                             Each entry must include video URL, start, and end times.
        input_directory (str): Path to the directory containing input video files.
        output_directory (str): Path to the directory where all extracted segments will be saved.

    Returns:
        dict: Summary of the extraction process containing the counts of each result type:
              - "Created": Number of successfully created clips
              - "Skipped": Number of clips skipped due to existing files
              - "Missing Input": Number of clips skipped due to missing input files
              - "Errors": List of error messages encountered during processing
    """
    # Load clip data from the JSON manifest file
    with open(manifest_path, "r") as f:
        data = json.load(f)
        clips = [(data[key], input_directory, output_directory) for key in data.keys()]

    # Initialize summary dictionary to track results of each clip extraction
    summary = {"Created": 0, "Skipped": 0, "Missing Input": 0, "Errors": []}
    with tqdm(total=len(clips), desc="Clipping Progress") as pbar:
        # Use multiprocessing to handle multiple clip extractions concurrently
        with multiprocessing.Pool(processes=8) as pool:
            # Process each clip and update the progress bar
            for result in pool.starmap(wrapper, clips):
                pbar.update(1)
                if result == "Created":
                    summary["Created"] += 1
                elif result == "Skipped":
                    summary["Skipped"] += 1
                elif result == "Missing Input":
                    summary["Missing Input"] += 1
                elif result.startswith("Error"):
                    summary["Errors"].append(result)

    # Display and return the summary of results
    print("Summary:", summary)
    return summary
