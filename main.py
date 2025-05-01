import os
import time
import json
import whisper
import ffmpeg
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# Directory to monitor
WATCH_DIR = "Whisper_project/"

# Track processed files
PROCESSED_FILES_DB = "processed_files.json"

# Load Whisper model (Choose 'base', 'small', 'medium', or 'large' for better accuracy)
model = whisper.load_model("base")

# Load processed files (to prevent reprocessing)
def load_processed_files():
    if os.path.exists(PROCESSED_FILES_DB):
        with open(PROCESSED_FILES_DB, "r") as f:
            return json.load(f)
    return {}

# Save processed files
def save_processed_files(processed_files):
    with open(PROCESSED_FILES_DB, "w") as f:
        json.dump(processed_files, f, indent=4)

# Extract audio from video files
def extract_audio(video_path, output_audio_path):
    try:
        ffmpeg.input(video_path).output(output_audio_path, format="wav", acodec="pcm_s16le", ac=1, ar="16k").run(overwrite_output=True, quiet=True)
        return output_audio_path
    except Exception as e:
        print(f"Error extracting audio from {video_path}: {e}")
        return None

# Transcribe audio using Whisper
def transcribe_audio(file_path):
    print(f"Transcribing: {file_path}")
    result = model.transcribe(file_path)
    transcript_text = result["text"]

    # Save transcript
    output_text_file = file_path.rsplit('.', 1)[0] + ".txt"
    with open(output_text_file, "w", encoding="utf-8") as f:
        f.write(transcript_text)

    print(f"Transcription saved: {output_text_file}")
    return output_text_file

# Process a single media file
def process_file(file_path, processed_files):
    if file_path in processed_files:
        print(f"Skipping already processed file: {file_path}")
        return

    _, ext = os.path.splitext(file_path)
    ext = ext.lower()

    if ext in [".mp3", ".wav", ".m4a", ".aac", ".flac"]:
        output_text = transcribe_audio(file_path)
        processed_files[file_path] = output_text
    elif ext in [".mp4", ".mkv", ".mov", ".flv", ".avi"]:
        audio_path = file_path.rsplit('.', 1)[0] + ".wav"
        extracted_audio = extract_audio(file_path, audio_path)
        if extracted_audio:
            output_text = transcribe_audio(extracted_audio)
            processed_files[file_path] = output_text

    save_processed_files(processed_files)

# Scan directory recursively for media files
def scan_directory(directory, processed_files):
    for root, _, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            process_file(file_path, processed_files)

# Watchdog event handler for real-time monitoring
class MediaFileHandler(FileSystemEventHandler):
    def on_created(self, event):
        if not event.is_directory:
            time.sleep(1)  # Allow file to be fully written
            process_file(event.src_path, processed_files)

# Monitor directory for new files
def monitor_directory():
    observer = Observer()
    event_handler = MediaFileHandler()
    observer.schedule(event_handler, WATCH_DIR, recursive=True)
    observer.start()
    print(f"Monitoring directory: {WATCH_DIR}")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

if __name__ == "__main__":
    if not os.path.exists(WATCH_DIR):
        os.makedirs(WATCH_DIR)

    processed_files = load_processed_files()  # Load previous session data
    scan_directory(WATCH_DIR, processed_files)  # Initial scan for existing files
    monitor_directory()  # Start real-time monitoring