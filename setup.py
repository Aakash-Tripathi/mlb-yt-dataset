from setuptools import find_packages, setup

setup(
    name="mlb_dataset",
    version="0.1.1",
    description="A Python package for downloading and processing MLB dataset videos.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Your Name",
    author_email="aakash.tripathi0304@gmail.com",
    url="https://github.com/Aakash-Tripathi/mlb-yt-dataset",  # Update with your GitHub repo URL
    packages=find_packages(),
    install_requires=["tqdm", "yt-dlp"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.10",
)
