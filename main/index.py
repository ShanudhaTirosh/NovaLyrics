import pygame
import time
import sys
import threading
import os
from config import LYRICS_DATA, COLORS, RESET, BOLD, UNDERLINE, SONG_TITLE, ARTIST, AUDIO_FILE

# Set UTF-8 encoding for terminal output to support emojis
if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')


def get_terminal_width():
    try:
        return os.get_terminal_size().columns
    except:
        return 80  # Default fallback width

def clear_screen():

    os.system('cls' if os.name == 'nt' else 'clear')

def print_banner():
    terminal_width = get_terminal_width()

    line1 = f"🎵  NOW PLAYING: {SONG_TITLE}  🎵"
    line2 = f"👤  ARTIST: {ARTIST}"
    border = "=" * 52
    
    padding1 = (terminal_width - len(line1)) // 2
    padding2 = (terminal_width - len(line2)) // 2
    paddingB = (terminal_width - len(border)) // 2
    
    banner = f"""
{" " * paddingB}{COLORS[5]}{BOLD}{border}{RESET}
{" " * padding1}{BOLD}{line1}{RESET}
{" " * padding2}{BOLD}{line2}{RESET}
{" " * paddingB}{COLORS[5]}{BOLD}{border}{RESET}
    """
    print(banner)


def type_lyrics():
    audio_start = time.time()
    color_index = 0
    
    for start_time, line, duration in LYRICS_DATA:
        # Calculate centering padding
        terminal_width = get_terminal_width()

        padding = (terminal_width - len(line) - 2) // 2
        padding_str = " " * max(0, padding)
        
        printed_dots = False
        last_dot_time = time.time()
        
        while time.time() - audio_start < start_time:
            time.sleep(0.01)
            if time.time() - last_dot_time >= 1:
                if not printed_dots:
                    sys.stdout.write(padding_str)
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
        
        # Handle Sinhala grapheme clusters correctly (prevents messy characters)
        import re
        graphemes = re.findall(r'.[\u0D80-\u0DFF]*', line)
        
        # Print line with styling (centered)
        sys.stdout.write(padding_str + f"{color}» ")


        for char in graphemes:
            sys.stdout.write(char)
            sys.stdout.flush()
            time.sleep(duration / len(graphemes) if len(graphemes) > 0 else 0.1)
        sys.stdout.write(RESET + "\n")
        sys.stdout.flush()


def main():
    try:
        # Check if audio file exists
        audio_path = os.path.join(os.path.dirname(__file__), AUDIO_FILE)
        if not os.path.exists(audio_path):
            print(f"{COLORS[0]}Error: Audio file '{AUDIO_FILE}' not found in the 'main' directory.{RESET}")
            return

        clear_screen()
        print_banner()
        
        print(f"{COLORS[3]}Loading audio engine...{RESET}")
        pygame.mixer.init()
        pygame.mixer.music.load(audio_path)
        
        print(f"{COLORS[2]}Starting playback...{RESET}\n")
        pygame.mixer.music.play()

        lyrics_thread = threading.Thread(target=type_lyrics)
        lyrics_thread.daemon = True  # Ensure thread closes on exit
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
