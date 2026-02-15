#!/usr/bin/env bash
set -euo pipefail

# make_tempo_demo_clip.sh
# Purpose: semi-automated demo clip maker for Tempo hackathon.
# - Records macOS screen via ffmpeg (avfoundation)
# - Runs npm demo during capture
# - Crops off the top menu/title bar
#
# Usage:
#   ./scripts/make_tempo_demo_clip.sh tempo_demo_raw.mp4
#   CROP_TOP=110 DURATION=75 ./scripts/make_tempo_demo_clip.sh tempo_demo_raw.mp4
#
# Notes:
# - You MUST have macOS Screen Recording permission for the terminal running this script.
# - This records the whole screen; put the terminal window in front before running.

OUT="${1:-tempo_demo_raw.mp4}"
CROP_TOP="${CROP_TOP:-110}"
DURATION="${DURATION:-75}"
FPS="${FPS:-30}"

WORKDIR="/Users/silkroadcat/.openclaw/workspace"
PROJ="$WORKDIR/projects/tempo-budget-guardian-agent"
RAW="$WORKDIR/$OUT"
CROP="$WORKDIR/${OUT%.mp4}_crop.mp4"
LOG="/tmp/tempo_demo_ffmpeg.log"

if ! command -v ffmpeg >/dev/null 2>&1; then
  echo "ffmpeg not found" >&2
  exit 1
fi
if ! command -v ffprobe >/dev/null 2>&1; then
  echo "ffprobe not found" >&2
  exit 1
fi

cd "$WORKDIR"

# Start screen recording in background
# Device name commonly appears as: "Capture screen 0"
# If this fails, list devices:
#   ffmpeg -f avfoundation -list_devices true -i "" 
# and set SCREEN_DEVICE env to the exact name.
SCREEN_DEVICE="${SCREEN_DEVICE:-Capture screen 0}"

echo "[tempo-clip] Recording $DURATION s @ ${FPS}fps to: $RAW"
rm -f "$RAW" "$CROP" "$LOG" || true

# Start recording
ffmpeg \
  -y \
  -f avfoundation \
  -framerate "$FPS" \
  -i "$SCREEN_DEVICE" \
  -t "$DURATION" \
  -pix_fmt yuv420p \
  "$RAW" \
  >"$LOG" 2>&1 &
FFMPEG_PID=$!

# Give user a moment to focus the right window
sleep 2

echo "[tempo-clip] Running demo (ledger reset + npm run demo)"
cd "$PROJ"
printf '{\n  "events": [],\n  "nonce_state": {}\n}\n' > ledger.example.json

# IMPORTANT: do NOT suppress stdout; we want the output visible in the recorded terminal.
# Also force line-buffering when possible for smoother capture.
if command -v stdbuf >/dev/null 2>&1; then
  stdbuf -oL -eL DEMO_STREAM=1 DEMO_DELAY_MS=${DEMO_DELAY_MS:-800} npm run demo || true
else
  DEMO_STREAM=1 DEMO_DELAY_MS=${DEMO_DELAY_MS:-800} npm run demo || true
fi

echo "[tempo-clip] Showing ledger output (for motion)"
cat ledger.example.json || true
sleep 2

# Wait for recording to finish
wait "$FFMPEG_PID" || true

cd "$WORKDIR"

if [[ ! -f "$RAW" ]]; then
  echo "[tempo-clip] ERROR: raw video not created. See $LOG" >&2
  exit 2
fi

echo "[tempo-clip] Cropping top ${CROP_TOP}px -> $CROP"
ffmpeg -y -i "$RAW" -vf "crop=in_w:in_h-${CROP_TOP}:0:${CROP_TOP}" -c:a copy "$CROP" >>"$LOG" 2>&1 || true

echo "[tempo-clip] Done."
echo "RAW:  $RAW"
echo "CROP: $CROP"
echo "LOG:  $LOG"
