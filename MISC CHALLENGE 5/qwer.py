from PIL import Image
import math
import os
import numpy as np
import subprocess
import tempfile
import sys

def file_to_binary(input_file_path):
    """Convert file to binary string"""
    file_size = os.path.getsize(input_file_path)
    print(f"File size: {file_size} bytes")

    binary_string = ""
    chunk_size = 1024
    total_chunks = math.ceil(file_size / chunk_size)
    
    with open(input_file_path, "rb") as f:
        for i in range(total_chunks):
            chunk = f.read(chunk_size)
            if not chunk:
                break
            binary_string += "".join(f"{byte:08b}" for byte in chunk)
            print(f"Processed {i+1}/{total_chunks} chunks ({((i+1)/total_chunks)*100:.1f}%)", end='\r')
    
    print(f"\nBinary string length: {len(binary_string)} bits")
    return binary_string

def binary_to_video(bin_string, output_video_path, width=1920, height=1080, pixel_size=4, fps=24):
    """Convert binary string to video using ffmpeg"""
    # If output path is a directory, create a default filename
    if os.path.isdir(output_video_path):
        output_video_path = os.path.join(output_video_path, "output_video.mp4")
        print(f"Output path is a directory, using: {output_video_path}")
    
    num_pixels = len(bin_string)
    pixels_per_image = (width // pixel_size) * (height // pixel_size)
    num_images = math.ceil(num_pixels / pixels_per_image)

    print(f"Creating {num_images} frames...")

    temp_dir = tempfile.mkdtemp()
    frame_files = []

    for i in range(num_images):
        start_index = i * pixels_per_image
        end_index = min(start_index + pixels_per_image, num_pixels)
        binary_digits = bin_string[start_index:end_index]

        if len(binary_digits) < pixels_per_image:
            binary_digits += '0' * (pixels_per_image - len(binary_digits))

        img = Image.new('RGB', (width, height), color='white')

        for row_index in range(height // pixel_size):
            row_start = row_index * (width // pixel_size)
            row_end = row_start + (width // pixel_size)
            row = binary_digits[row_start:row_end]

            for col_index, digit in enumerate(row):
                color = (0, 0, 0) if digit == '1' else (255, 255, 255)
                x1 = col_index * pixel_size
                y1 = row_index * pixel_size
                x2 = x1 + pixel_size
                y2 = y1 + pixel_size
                img.paste(color, (x1, y1, x2, y2))

        frame_path = os.path.join(temp_dir, f"frame_{i:06d}.png")
        img.save(frame_path)
        frame_files.append(frame_path)
        print(f"Created frame {i+1}/{num_images} ({((i+1)/num_images)*100:.1f}%)", end='\r')

    print(f"\nCreating video from {num_images} frames...")

    try:
        ffmpeg_cmd = [
            'ffmpeg', '-y', '-framerate', str(fps),
            '-i', os.path.join(temp_dir, 'frame_%06d.png'),
            '-c:v', 'libx264', '-pix_fmt', 'yuv420p',
            output_video_path
        ]
        result = subprocess.run(ffmpeg_cmd, check=True, capture_output=True, text=True)
        print(f"✓ Video created successfully: {output_video_path}")
        
        # Clean up
        for frame_file in frame_files:
            os.remove(frame_file)
        os.rmdir(temp_dir)
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"✗ FFmpeg error: {e}")
        print(f"FFmpeg stderr: {e.stderr}")
        print(f"Frames saved in: {temp_dir}")
        return False
    except FileNotFoundError:
        print("✗ FFmpeg not found. Please install ffmpeg with: sudo apt install ffmpeg")
        print(f"Frames saved in: {temp_dir}")
        return False

def main():
    print("File to Video Converter")
    print("=" * 30)
    
    input_Data = input("1. Convert file to video\n2. Exit\nChoose option (1-2): ")

    if input_Data == "1":
        input_file = input("Enter input file path: ").strip()
        output_video = input("Enter output video path (can be directory or full path): ").strip()
        
        if not os.path.exists(input_file):
            print("✗ Input file not found!")
            return
        
        binary_string = file_to_binary(input_file)
        success = binary_to_video(binary_string, output_video)
        
        if success:
            print("Conversion completed successfully!")
        else:
            print("Conversion failed. Check the error messages above.")
        
    elif input_Data == "2":
        print("Goodbye!")
    else:
        print("✗ Invalid option!")

if __name__ == "__main__":
    main()
