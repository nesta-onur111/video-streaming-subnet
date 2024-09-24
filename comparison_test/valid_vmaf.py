import subprocess

# Define the paths to the original and altered video files
original_video = "original.mov"
altered_video = "output_h2652.mov"
output_file = "vmaf_output2.json"

# Construct the FFmpeg command
ffmpeg_command = [
    "ffmpeg",
    "-i", altered_video,
    "-i", original_video,
    "-lavfi", "[0:v]scale=1920:1080:flags=bicubic[main];[1:v]scale=1920:1080:flags=bicubic[ref];[main][ref]libvmaf=log_path=" + output_file,
    "-f", "null", "-"
]

# Execute the command
subprocess.run(ffmpeg_command)