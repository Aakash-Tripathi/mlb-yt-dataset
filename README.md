# MLB-YouTube Dataset Fork

This repository is a fork of the original \[[MLB-YouTube Dataset repository by AJ Piergiovanni](https://arxiv.org/abs/1804.03247)\], which provides datasets, code, and models for fine-grained activity recognition in baseball videos.

> [!NOTE]
> Please note: This fork was created because the original repository became stale and required updates to work with modern dependencies and tooling. Users looking for the latest functionality, stability, or who want to contribute to ongoing improvements should use this repository.

## Purpose of This Fork
The original MLB-YouTube Dataset repository has been inactive for several years, making it challenging to use with newer Python and package dependencies. This fork aims to:

- Modernize and maintain the codebase.
- Provide a functional setup compatible with recent dependencies.
- Allow direct installation using pip install for easier use.

For any questions or more details about the original project, please visit and refer to the original repository: https://github.com/piergiaj/mlb-youtube.

## Installation
To install this forked version:

```bash
pip install git+https://github.com/Aakash-Tripathi/mlb-yt-dataset
```

> [!NOTE]
> This package requires ``ffmpeg`` to be installed on your system. Please refer to the official [FFmpeg website](https://www.ffmpeg.org/) for installation instructions.

## Usage
### Downloading Videos
This package allows users to download and process MLB video datasets directly from YouTube. After installing, import the package to download videos, segment clips, or extract continuous clips:

```python
import mlb_dataset as mlb

# Example of downloading videos
download_results = mlb.download_all_videos("path/to/manifest.json", "data/raw")
```

### Extracting Clips

#### Segmented Clips: Run the following to extract segmented clips for activity recognition.

```python
mlb.extract_segmented_clips("path/to/manifest.json", "data/raw", "data/segmented")
```
#### Continuous Clips: Run the following to extract continuous clips for activity classification.

```python
mlb.extract_continuous_clips("path/to/manifest.json", "data/raw", "data/continuous")
```

## Credits and Citations
The MLB-YouTube dataset was originally created by AJ Piergiovanni and Michael S. Ryoo and introduced in their research paper:

```bibtex
@inproceedings{mlbyoutube2018,
  title={Fine-grained Activity Recognition in Baseball Videos},
  booktitle={CVPR Workshop on Computer Vision in Sports},
  author={AJ Piergiovanni and Michael S. Ryoo},
  year={2018}
}
```

This forked version of the repository is maintained independently for usability purposes. Please refer to the original repository for further references, academic citations, or any in-depth questions regarding the dataset.