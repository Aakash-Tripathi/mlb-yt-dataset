import json
import os
import subprocess
import time

from tqdm import tqdm

# Lists to track video download status
skipped_videos = []
downloaded_videos = []
failed_videos = []


def download_video(entry, save_dir, retries=3):
    """
    Downloads a single video from YouTube using `yt-dlp`.

    Parameters:
        entry (dict): Dictionary with a "url" key containing the video URL.
        save_dir (str): Directory to save the downloaded video.
        retries (int): Number of retry attempts for failed downloads.

    Returns:
        str: "Skipped" if video exists, "Downloaded" if successful, or "Failed" if the download fails.
    """
    yturl = entry["url"]
    ytid = yturl.split("=")[-1]
    output_path = os.path.join(save_dir, f"{ytid}.mkv")

    if os.path.exists(output_path):
        skipped_videos.append(ytid)
        return "Skipped"

    command = ["yt-dlp", "--limit-rate", "100M", "-o", output_path, yturl]

    for attempt in range(retries):
        try:
            subprocess.run(
                command, check=True, timeout=600
            )  # Set timeout to prevent hanging
            downloaded_videos.append(ytid)
            return "Downloaded"
        except subprocess.CalledProcessError as e:
            if attempt < retries - 1:
                time.sleep(2)  # Brief pause before retry
            else:
                failed_videos.append((ytid, str(e)))
                return "Failed"


def download_all_videos(manifest_path, save_dir):
    """
    Downloads all videos from a JSON manifest file sequentially.

    Parameters:
        manifest_path (str): Path to JSON file with video URLs.
        save_dir (str): Directory for downloaded videos.

    Returns:
        dict: Summary report with "downloaded", "skipped", and "failed" lists.
    """
    with open(manifest_path, "r") as f:
        data = json.load(f)

    total_videos = len(data)
    print(f"Starting download of {total_videos} videos...")

    with tqdm(total=total_videos, desc="Overall Progress") as pbar:
        for key, entry in data.items():
            download_video(entry, save_dir)  # Process each video one by one
            pbar.update(1)

    return {
        "downloaded": downloaded_videos,
        "skipped": skipped_videos,
        "failed": failed_videos,
    }
