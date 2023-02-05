# Bedtime story bot

Do you have a friend who never goes to bed in time?

Move the user to a set channel, the bot will start to play audio and kick them from voice when done.

## Running

I recommend to run it in a docker container. Nativly in wsl might give you unextected errors with audio playback.

### Docker (or podman)

Use the assistant script.
```bash
bash scripts/start-dockerized.sh
```

#### Docker - build and run manually
```bash
# Build
docker build --no-cache -t bedtime-bot .
# Run
docker run -d bedtime-bot:latest
```

### Native - Linux

```bash
# Create venv
bash scripts/create-venv.sh
```

```bash
# Source venv
source venv/bin/activate
```

```bash
# Run - (when venv is sourced)
python3 app/main.py
```

## Audio files

Only tested with mp3 files.

Supports: .aac, .flac, .mp3', .m4a, .opus, .vorbis, .wav

Put audio files in the app/audio directory.


