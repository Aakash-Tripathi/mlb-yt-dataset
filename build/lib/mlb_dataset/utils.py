import subprocess


def local_clip(input_path, start_time, duration, output_path):
    """Extracts a clip from a video using ffmpeg."""
    command = [
        "ffmpeg",
        "-i",
        input_path,
        "-ss",
        str(start_time),
        "-t",
        str(duration),
        "-c:v",
        "copy",
        "-an",
        "-threads",
        "1",
        "-loglevel",
        "panic",
        output_path,
    ]

    try:
        subprocess.check_output(command, stderr=subprocess.STDOUT)
    except subprocess.CalledProcessError as err:
        print(f"Error creating clip {output_path}: {err.output.decode()}")
        return err.output.decode()
