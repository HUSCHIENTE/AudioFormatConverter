# AudioFormatConverter
Audio Format Converter is a versatile Python tool for executing audio format conversion operations, allowing users to effortlessly convert audio files between different formats.

## Features

- Converts audio files from one format to another (e.g., from m4a to wav).
- Supports multi-threaded conversion for faster processing.
- Provides progress tracking with a progress bar.

## Installation

1. Clone this repository to your local machine:

   ```shell
   git clone https://github.com/HUSCHIENTE/AudioFormatConverter.git
2. Install the required dependencies:

   ```shell
   pip install pydub tqdm
   
   #Getting ffmpeg set up
   apt-get install ffmpeg libavcodec-extra

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
- --target_sample_rate (int) : Target sample rate (default: None, no change).
- --show_scanning_progress : (Optional) This flag, when included in the command, enables the display of a progress bar during the scanning phase of audio files. By default, it's set to False, meaning that no scanning progress bar is displayed. Users can include this flag to see the progress of the scanning process if desired.


