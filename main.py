import os
import json
import re
import subprocess
import whisperx
import torch

AUDIO_FILE = "vocals.wav"
OUTPUT_DIR = "word_clips"
JSON_FILE = "words.json"

DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
COMPUTE_TYPE = "float16" if DEVICE == "cuda" else "int8"

os.makedirs(OUTPUT_DIR, exist_ok=True)


def safe_filename(text):
    text = text.lower().strip()
    text = re.sub(r"[^a-z0-9]+", "_", text)
    return text.strip("_") or "word"


def cut_audio(input_file, start, end, output_file):
    subprocess.run(
        [
            "ffmpeg",
            "-y",
            "-i", input_file,
            "-ss", str(start),
            "-to", str(end),
            "-c:a", "pcm_s16le",
            output_file,
        ],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        check=True,
    )


# 1. Load model
model = whisperx.load_model(
    "large-v3",
    DEVICE,
    compute_type=COMPUTE_TYPE
)

# 2. Transcribe
audio = whisperx.load_audio(AUDIO_FILE)
result = model.transcribe(audio)

# 3. Load alignment model
language_code = result["language"]
align_model, metadata = whisperx.load_align_model(
    language_code=language_code,
    device=DEVICE
)

# 4. Align words
aligned_result = whisperx.align(
    result["segments"],
    align_model,
    metadata,
    audio,
    DEVICE,
    return_char_alignments=False
)

# 5. Extract words
word_items = []
word_index = 1

for segment in aligned_result["segments"]:
    for word in segment.get("words", []):
        if "start" not in word or "end" not in word:
            continue

        word_text = word["word"].strip()
        start = round(float(word["start"]), 3)
        end = round(float(word["end"]), 3)

        filename = f"{word_index:04d}_{safe_filename(word_text)}.wav"
        filepath = os.path.join(OUTPUT_DIR, filename)

        cut_audio(AUDIO_FILE, start, end, filepath)

        word_items.append({
            "index": word_index,
            "word": word_text,
            "start": start,
            "end": end,
            "duration": round(end - start, 3),
            "audio_file": filepath
        })

        word_index += 1

# 6. Save JSON
with open(JSON_FILE, "w", encoding="utf-8") as f:
    json.dump(word_items, f, indent=2, ensure_ascii=False)

print(f"Created {JSON_FILE}")
print(f"Created {len(word_items)} word clips in {OUTPUT_DIR}/")
