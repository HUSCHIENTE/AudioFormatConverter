import os
import concurrent.futures
from tqdm import tqdm
from pydub import AudioSegment
import argparse

def convert_audio_files(input_dir, output_dir, input_format, output_format, max_threads=8):
    input_files = []

    # Create a tqdm progress bar for file traversal
    with tqdm(desc="Scanning Files") as file_bar:
        # Traverse all audio files in the input directory
        for root, _, files in os.walk(input_dir):
            for file in files:
                if file.endswith(f".{input_format}"):
                    input_files.append(os.path.join(root, file))
                    file_bar.update(1)  # Update the file traversal progress

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

        # Create a thread pool
        with concurrent.futures.ThreadPoolExecutor(max_threads) as executor:
            futures = []

            # Submit tasks to the thread pool
            for input_file in input_files:
                future = executor.submit(convert_audio_to_format, input_file, output_dir, output_format)
                future.add_done_callback(lambda p: pbar.update(1))
                futures.append(future)

            # Process the results and display errors
            for future in concurrent.futures.as_completed(futures):
                error_message = future.result()
                if error_message:
                    tqdm.write(error_message)

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
