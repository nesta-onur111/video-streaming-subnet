import ffmpeg

def encode_to_h265(input_file, output_file, crf_value=28):  #crf_value contains 0-51
    try:
        (
            ffmpeg
            .input(input_file)
            .output(output_file, vcodec='libx265', crf=crf_value)
            .run(overwrite_output=True)
        )
        print(f"Encoding completed: {output_file}")
    except ffmpeg.Error as e:
        print("An error occurred:", e.stderr.decode())

# Example usage
input_video = 'original.mov'  # Replace with your input video file
output_video = 'output_h2652.mov'  # Output file name
crf_value = 51  # Adjust this value to control compression

encode_to_h265(input_video, output_video, crf_value)