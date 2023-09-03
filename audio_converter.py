import os
import concurrent.futures
from tqdm import tqdm
from pydub import AudioSegment
import argparse

def convert_audio_files(input_dir, output_dir, input_format, output_format, max_threads=8):
    input_files = []

    def scan_directory(path):
        for entry in os.scandir(path):
            if entry.is_file() and entry.name.endswith(f".{input_format}"):
                input_files.append(entry.path)
                file_bar.update(1)  # Increment the progress for each file found
            elif entry.is_dir():
                scan_directory(entry.path)

    # Create a tqdm progress bar for file traversal
    file_bar = tqdm(total=0, desc="Scanning Files")  # Initialize with total=0
    scan_directory(input_dir)
    file_bar.total = len(input_files)  # Update the total count for the progress bar

    # Create a tqdm progress bar for file conversion
    with tqdm(total=len(input_files), desc="Converting") as pbar:
        # Define a function to convert audio files to the specified format
        def convert_audio_to_format(input_file, output_dir, output_format):
            try:
                audio = AudioSegment.from_file(input_file, format=input_format)
                # Get the output file name, e.g., /path/to/output_dir/subfolder/file.wav
                output_file = os.path.join(output_dir, os.path.relpath(input_file, input_dir)[:-len(input_format) - 1] + f".{output_format}")
                os.makedirs(os.path.dirname(output_file), exist_ok=True)  # Create subdirectories
                audio.export(output_file, format=output_format)
                return None
            except Exception as e:
                return f"Error converting {input_file}: {str(e)}"

        # Create a thread pool for file conversion
        with concurrent.futures.ThreadPoolExecutor(max_threads) as executor:
            futures = []

            # Submit tasks to the thread pool for file conversion
            for input_file in input_files:
                future = executor.submit(convert_audio_to_format, input_file, output_dir, output_format)
                future.add_done_callback(lambda p: pbar.update(1))
                futures.append(future)

            # Wait for all file conversion tasks to complete
            concurrent.futures.wait(futures)

    print("All conversions completed.")

def main():
    parser = argparse.ArgumentParser(description='Convert audio files to specified format.')
    parser.add_argument('input_dir', type=str, help='Input directory containing audio files')
    parser.add_argument('output_dir', type=str, help='Output directory for converted files')
    parser.add_argument('--input_format', type=str, default='m4a', help='Input audio format (default: m4a)')
    parser.add_argument('--output_format', type=str, default='wav', help='Output audio format (default: wav)')
    parser.add_argument('--max_threads', type=int, default=8, help='Maximum number of threads (default: 8)')

    args = parser.parse_args()
    convert_audio_files(args.input_dir, args.output_dir, args.input_format, args.output_format, args.max_threads)

if __name__ == "__main__":
    main()