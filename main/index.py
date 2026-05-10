import pygame
import time
import sys
import threading
import os
import re
from config import LYRICS_DATA, COLORS, RESET, BOLD, UNDERLINE, SONG_TITLE, ARTIST, AUDIO_FILE

# Set UTF-8 encoding for terminal output to support emojis
if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_banner():
    border = "=" * 50
    print(f"{COLORS[5]}{BOLD}{border}{RESET}")
    print(f"{BOLD}🎵  NOW PLAYING: {SONG_TITLE}{RESET}")
    print(f"{BOLD}👤  ARTIST: {ARTIST}{RESET}")
    print(f"{COLORS[5]}{BOLD}{border}{RESET}\n")

def type_lyrics():
    audio_start = time.time()
    color_index = 0
    
    for start_time, line, duration in LYRICS_DATA:
        printed_dots = False
        last_dot_time = time.time()
        
        # Wait for the lyric line to start
        while time.time() - audio_start < start_time:
            time.sleep(0.01)
            if time.time() - last_dot_time >= 1:
                sys.stdout.write(f"{COLORS[2]}.{RESET}")
                sys.stdout.flush()
                last_dot_time = time.time()
                printed_dots = True
        
        if printed_dots:
            sys.stdout.write('\n')
            sys.stdout.flush()
        
        # Get color for this line
        color = COLORS[color_index % len(COLORS)]
        color_index += 1
        
        # Handle Sinhala grapheme clusters correctly
        graphemes = re.findall(r'.[\u0D80-\u0DFF]*', line)
        
        # Print line (Left Aligned for maximum compatibility)
        sys.stdout.write(f"{color}» ")
        for char in graphemes:
            sys.stdout.write(char)
            sys.stdout.flush()
            time.sleep(duration / len(graphemes) if len(graphemes) > 0 else 0.1)
        sys.stdout.write(RESET + "\n")
        sys.stdout.flush()

def main():
    try:
        audio_path = os.path.join(os.path.dirname(__file__), AUDIO_FILE)
        if not os.path.exists(audio_path):
            print(f"{COLORS[0]}Error: Audio file '{AUDIO_FILE}' not found.{RESET}")
            return

        clear_screen()
        print_banner()
        
        print(f"{COLORS[3]}Loading audio engine...{RESET}")
        pygame.mixer.init()
        pygame.mixer.music.load(audio_path)
        
        print(f"{COLORS[2]}Starting playback...{RESET}\n")
        pygame.mixer.music.play()

        lyrics_thread = threading.Thread(target=type_lyrics)
        lyrics_thread.daemon = True
        lyrics_thread.start()

        while pygame.mixer.music.get_busy():
            time.sleep(1)

        lyrics_thread.join(timeout=1)
        print(f"\n{BOLD}{COLORS[5]}✨ Song finished! - by Shanudha Tirosh ✨{RESET}")

    except KeyboardInterrupt:
        print(f"\n\n{COLORS[1]}Playback stopped by user.{RESET}")
        pygame.mixer.music.stop()
    except Exception as e:
        print(f"\n{COLORS[0]}An unexpected error occurred: {e}{RESET}")
    finally:
        pygame.quit()

if __name__ == "__main__":
    main()
