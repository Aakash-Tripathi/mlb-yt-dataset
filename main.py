import mlb_dataset as mlb

# Download videos
download_results = mlb.download_all_videos(
    "./data/manifest/mlb-youtube-segmented.json", "./data/raw"
)

# Extract segmented clips
segmented_summary = mlb.extract_segmented_clips(
    "./data/manifest/mlb-youtube-segmented.json", "./data/raw", "./data/segmented"
)
print("Segmented Extraction Summary:", segmented_summary)

# Extract continuous clips
continuous_summary = mlb.extract_continuous_clips(
    "./data/manifest/mlb-youtube-continuous.json", "./data/raw", "./data/continuous"
)
print("Continuous Extraction Summary:", continuous_summary)
