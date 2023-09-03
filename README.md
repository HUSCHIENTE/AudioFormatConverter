# AudioFormatConverter
Audio Format Converter is a versatile Python tool for executing audio format conversion operations, allowing users to effortlessly convert audio files between different formats.

## Features

- Converts audio files from one format to another (e.g., from m4a to wav).
- Supports multi-threaded conversion for faster processing.
- Provides progress tracking with a progress bar.

## Installation

1. Clone this repository to your local machine:

   ```shell
   git clone https://github.com/HSUCHIENTE/audio-format-converter.git
2. Install the required dependencies:

   ```shell
   pip install pydub tqdm

## Usage
Convert audio files from one format to another using the following command:

  ```shell
  python audio_converter.py input_dir output_dir --input_format m4a --output_format wav --max_threads 8
  ```

- input_dir : The directory containing audio files to be converted.
- output_dir : The directory where converted files will be saved.
- --input_format : (Optional) The input audio format (default: m4a).
- --output_format : (Optional) The output audio format (default: wav).
- --max_threads : (Optional) Maximum number of threads for concurrent conversion (default: 8).


## Examples
Convert all audio files in the "input_audio" directory to the "output_audio" directory:

  ```shell
python audio_converter.py input_audio output_audio --input_format mp3 --output_format ogg --max_threads 4
  ```


