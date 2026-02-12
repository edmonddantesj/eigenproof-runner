#!/usr/bin/env python3
"""
Render terminal log as a scrolling video with green-on-black hacker aesthetic.
Produces individual frames, then ffmpeg merges them with audio.
"""
import os, math
from PIL import Image, ImageDraw, ImageFont

# Config
WIDTH, HEIGHT = 1280, 720
BG_COLOR = (10, 10, 20)       # near-black with slight blue tint
TEXT_COLOR = (0, 255, 120)     # bright green (hacker style)
HIGHLIGHT = (0, 200, 255)     # cyan for headers
ACCENT = (255, 100, 255)      # magenta for important items
FPS = 25
DURATION_SEC = 57  # match the voice duration
FONT_SIZE = 16
LINE_HEIGHT = 20

# Paths
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
LOG_FILE = os.path.join(SCRIPT_DIR, "demo_clean.txt")
FRAMES_DIR = os.path.join(SCRIPT_DIR, "frames")
os.makedirs(FRAMES_DIR, exist_ok=True)

# Load log
with open(LOG_FILE, 'r') as f:
    lines = f.readlines()

# Try to find a monospace font
font = None
font_paths = [
    "/System/Library/Fonts/SFMono-Regular.otf",
    "/System/Library/Fonts/Menlo.ttc",
    "/System/Library/Fonts/Monaco.ttf",
    "/System/Library/Fonts/Supplemental/Courier New.ttf",
]
for fp in font_paths:
    if os.path.exists(fp):
        try:
            font = ImageFont.truetype(fp, FONT_SIZE)
            break
        except:
            continue
if font is None:
    font = ImageFont.load_default()

total_frames = FPS * DURATION_SEC
visible_lines = HEIGHT // LINE_HEIGHT - 2  # leave margin
total_lines = len(lines)

# We'll scroll through all lines over the duration
# Each frame shows a "window" of visible_lines
scroll_per_frame = max(total_lines / total_frames, 0.15)

print(f"Rendering {total_frames} frames, {total_lines} lines, scroll_speed={scroll_per_frame:.2f} lines/frame")

for frame_idx in range(total_frames):
    img = Image.new('RGB', (WIDTH, HEIGHT), BG_COLOR)
    draw = ImageDraw.Draw(img)
    
    # Calculate which lines are visible
    scroll_pos = frame_idx * scroll_per_frame
    start_line = int(scroll_pos)
    
    # Add scanline effect (subtle horizontal lines)
    for y in range(0, HEIGHT, 4):
        draw.line([(0, y), (WIDTH, y)], fill=(15, 15, 30), width=1)
    
    # Draw header bar
    draw.rectangle([(0, 0), (WIDTH, 28)], fill=(20, 20, 40))
    draw.text((10, 5), "⚡ SOLANA SENTINEL V2.1 — Live Devnet Demo", fill=HIGHLIGHT, font=font)
    draw.text((WIDTH - 200, 5), f"Frame {frame_idx+1}/{total_frames}", fill=(100, 100, 120), font=font)
    
    # Draw visible lines
    y_offset = 35
    for i in range(visible_lines):
        line_idx = start_line + i
        if line_idx >= total_lines:
            break
        
        line = lines[line_idx].rstrip('\n')
        
        # Color coding
        color = TEXT_COLOR
        if '✅' in line:
            color = (0, 255, 120)  # bright green
        elif '🚨' in line or 'EMERGENCY' in line:
            color = (255, 80, 80)   # red
        elif '┌' in line or '└' in line or '│' in line or '╔' in line or '╚' in line or '╠' in line or '║' in line:
            color = HIGHLIGHT
        elif '█' in line or '╗' in line or '╝' in line:
            color = (0, 200, 255)
        elif '🐺' in line or '🦊' in line:
            color = ACCENT
        elif 'ℹ' in line:
            color = (120, 180, 120)  # dim green
        elif 'STEP' in line:
            color = (255, 255, 255)  # white for step headers
        elif '🏆' in line or 'COMPLETE' in line:
            color = (255, 215, 0)   # gold
        elif '🐾' in line or 'Aoineco' in line:
            color = (180, 100, 255)  # purple
        
        # Typing animation for the current "active" line
        chars_to_show = len(line)
        if line_idx == start_line + visible_lines - 3:
            # Last few lines get "typing" effect
            progress = (frame_idx % 10) / 10.0
            chars_to_show = max(1, int(len(line) * min(1.0, progress + 0.5)))
        
        draw.text((15, y_offset), line[:chars_to_show], fill=color, font=font)
        y_offset += LINE_HEIGHT
    
    # Blinking cursor at bottom
    if frame_idx % 12 < 6:
        cursor_y = min(y_offset, HEIGHT - 30)
        draw.text((15, cursor_y), "█", fill=TEXT_COLOR, font=font)
    
    # Bottom status bar
    draw.rectangle([(0, HEIGHT - 25), (WIDTH, HEIGHT)], fill=(20, 20, 40))
    pct = int((frame_idx / total_frames) * 100)
    draw.text((10, HEIGHT - 22), f"Network: Solana Devnet | Progress: {pct}%", fill=(100, 180, 100), font=font)
    draw.text((WIDTH - 350, HEIGHT - 22), "Powered by Aoineco & Co. 🐾", fill=(180, 100, 255), font=font)
    
    # Save frame
    img.save(os.path.join(FRAMES_DIR, f"frame_{frame_idx:05d}.png"))
    
    if frame_idx % 100 == 0:
        print(f"  Frame {frame_idx}/{total_frames} rendered")

print(f"✅ All {total_frames} frames rendered to {FRAMES_DIR}")
