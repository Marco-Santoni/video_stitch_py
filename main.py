import os
from moviepy import VideoFileClip, concatenate_videoclips
from datetime import datetime

def stitch_videos(input_folder, output_path):
    # Get all mp4 files in the input folder
    video_files = [f for f in os.listdir(input_folder) if f.endswith(".mp4")]
    video_files.sort()  # Sort files to maintain order

    # Load video clips
    clips = [VideoFileClip(os.path.join(input_folder, file)) for file in video_files]

    # Concatenate video clips
    final_clip = concatenate_videoclips(clips)

    # Ensure output folder exists
    os.makedirs(output_folder, exist_ok=True)

    final_clip.write_videofile(output_path, codec="libx264", audio_codec="aac")

    # Close all clips
    for clip in clips:
        clip.close()
    final_clip.close()

def upload_to_s3(input_folder, output_path, s3_file_key):
    import boto3
    import yaml

    # Load configuration from config.yaml
    with open("./config.yaml", "r") as config_file:
        config = yaml.safe_load(config_file)

    # Get the S3 bucket name from the configuration
    stitched_bucket_name = config["STITCHED_VIDEO_BUCKET"]
    raw_bucket_name = config["RAW_VIDEO_BUCKET"]

    s3 = boto3.client('s3')
    print("Uploading to S3...")
    
    #s3.upload_file(output_path, stitched_bucket_name, s3_file_key)
    print(f"Uploaded {output_path} to S3 bucket {stitched_bucket_name}")

    # Upload all mp4 files in the input folder to S3
    for file in os.listdir(input_folder):
        if file.endswith(".mp4"):
            file_path = os.path.join(input_folder, file)
            print(f"Uploading {file_path} to S3 bucket {raw_bucket_name}")
            s3.upload_file(file_path, raw_bucket_name, f"{file}")
            print(f"Uploaded {file_path} to S3 bucket {raw_bucket_name}")

def empty_output_folder(output_folder):
    # Remove any existing mp4 files in the output folder
    for file in os.listdir(output_folder):
        if file.endswith(".mp4"):
            os.remove(os.path.join(output_folder, file))

# Example usage
if __name__ == "__main__":
    input_folder = "input"  # Replace with your input folder path
    output_folder = "output"  # Replace with your output folder path

    # Empty the output folder before processing
    empty_output_folder(output_folder)

    # Write the resulting video to the output folder
    output_filename="output"
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    output_filename_with_timestamp = f"{output_filename}_{timestamp}.mp4"

    output_path = os.path.join(output_folder, output_filename_with_timestamp)

    # Call the function to stitch videos
    stitch_videos(input_folder, output_path)

    # Call the function to upload to S3
    upload_to_s3(input_folder, output_path, output_filename_with_timestamp)



    
