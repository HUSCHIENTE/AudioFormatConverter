import os
import concurrent.futures
from tqdm import tqdm
from pydub import AudioSegment
import argparse

def convert_audio_files(input_dir, output_dir, input_format, output_format, max_threads=8):
    input_files = []

    # Traverse all audio files in the input directory
    for root, _, files in os.walk(input_dir):
        for file in files:
            if file.endswith(f".{input_format}"):
                input_files.append(os.path.join(root, file))

    # Define a function to convert audio files to the specified format and update the progress bar
    def convert_audio_to_format_with_progress(input_file, output_dir, output_format, pbar):
        try:
            audio = AudioSegment.from_file(input_file, format=input_format)
            # Get the output file name, e.g., /path/to/output_dir/subfolder/file.wav
            output_file = os.path.join(output_dir, os.path.relpath(input_file, input_dir)[:-len(input_format) - 1] + f".{output_format}")
            os.makedirs(os.path.dirname(output_file), exist_ok=True)  # Create subdirectories
            audio.export(output_file, format=output_format)
        except Exception as e:
            tqdm.write(f"Error converting {input_file}: {str(e)}")
        pbar.update(1)  # Manually update the progress bar

    # Create a tqdm progress bar
    with tqdm(total=len(input_files)) as pbar:
        # Create a thread pool
        with concurrent.futures.ThreadPoolExecutor(max_threads) as executor:
            futures = []

            # Submit tasks to the thread pool
            for input_file in input_files:
                future = executor.submit(convert_audio_to_format_with_progress, input_file, output_dir, output_format, pbar)
                futures.append(future)

            # Wait for all tasks to complete
            for future in concurrent.futures.as_completed(futures):
                pass

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
