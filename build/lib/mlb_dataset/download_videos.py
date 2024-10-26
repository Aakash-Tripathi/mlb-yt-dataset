import json
import os
import subprocess
from concurrent.futures import ThreadPoolExecutor, as_completed

from tqdm import tqdm

# Lists to track video download status
skipped_videos = []  # Stores video IDs of already downloaded videos
downloaded_videos = []  # Stores video IDs of successfully downloaded videos
failed_videos = []  # Stores tuples of video IDs and error messages for failed downloads


def download_video(entry, save_dir):
    """
    Downloads a single video from YouTube using `yt-dlp` based on the video URL provided in `entry`.

    Parameters:
        entry (dict): Dictionary containing at least a "url" key with the video URL as its value.
        save_dir (str): Directory where the downloaded video will be saved.

    Returns:
        str: "Skipped" if the video already exists, "Downloaded" if successful, or "Failed" if the download fails.
    """
    yturl = entry["url"]
    ytid = yturl.split("=")[-1]  # Extract YouTube video ID from the URL
    output_path = os.path.join(save_dir, f"{ytid}.mkv")

    # Check if the video already exists
    if os.path.exists(output_path):
        skipped_videos.append(ytid)
        return "Skipped"

    # Command to download the video using `yt-dlp`
    command = ["yt-dlp", "-o", output_path, yturl]

    try:
        # Execute the command
        subprocess.run(command, check=True)
        downloaded_videos.append(ytid)
        return "Downloaded"
    except subprocess.CalledProcessError as e:
        # Log failure information if download fails
        failed_videos.append((ytid, str(e)))
        return "Failed"


def download_all_videos(manifest_path, save_dir):
    """
    Downloads all videos specified in a JSON manifest file in parallel.

    Parameters:
        manifest_path (str): Path to the JSON file containing video URLs in a dictionary format.
        save_dir (str): Directory where all downloaded videos will be saved.

    Returns:
        dict: A summary dictionary containing lists of video IDs under keys "downloaded", "skipped", and "failed".
    """
    # Load manifest data
    with open(manifest_path, "r") as f:
        data = json.load(f)

    total_videos = len(data)
    print(f"Starting download of {total_videos} videos...")

    # Use ThreadPoolExecutor for concurrent downloads
    with ThreadPoolExecutor(max_workers=8) as executor:
        futures = {
            executor.submit(download_video, entry, save_dir): key
            for key, entry in data.items()
        }

        # Initialize progress bar
        with tqdm(total=total_videos, desc="Overall Progress") as pbar:
            for future in as_completed(futures):
                result = future.result()
                pbar.update(1)

    # Return a summary report of the download process
    return {
        "downloaded": downloaded_videos,
        "skipped": skipped_videos,
        "failed": failed_videos,
    }
