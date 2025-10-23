import time
import winsound
import threading
import keyboard
import pyautogui as pygui
import random as rand

from src.key_gen import text_to_strokes
from src.text_gen import generate_text
from src.type import type_strokes

# Timing
PRE_WAIT = 5
TYPE_DELAY_MIN = 15
TYPE_DELAY_MAX = 30
TYPE_SPEED_MIN = 0.033
TYPE_SPEED_MAX = 0.066

# Simulated errors and text features
TYPO_CHANCE = 0.02
MISSED_CORRECTION_CHANCE = 0.1
COMMA_CHANCE = 0.30
SENTENCE_BREAK_CHANCE = 0.20
PARAGRAPH_CHANCE = 0.30


def play_sound(sound='good', times=1):
    for _ in range(times):
        match sound:
            case 'good':
                winsound.Beep(1000, 200)  # Frequency: 1000Hz, Duration: 200ms
            case 'bad':
                winsound.Beep(400, 200)  # Frequency: 400Hz, Duration: 500ms
            case _:
                print(f"Unknown sound: {sound}")


def type_something():
    text = generate_text()
    strokes = text_to_strokes(text, TYPO_CHANCE, MISSED_CORRECTION_CHANCE, COMMA_CHANCE, SENTENCE_BREAK_CHANCE, PARAGRAPH_CHANCE)
    type_strokes(strokes, TYPE_SPEED_MIN, TYPE_SPEED_MAX)


def stop_listener(stop_flag):
    keyboard.wait('esc')
    play_sound('bad')
    stop_flag['stop'] = True


def main():
    stop_flag = {'stop': False}
    threading.Thread(target=stop_listener, args=(stop_flag,), daemon=True).start()

    for i in range(PRE_WAIT):
        print(PRE_WAIT - i)
        play_sound('good')
        time.sleep(1)
    
    print("Sequence started, press [ESC] to stop")
    play_sound('good', 2)

    times_typed = 0
    start_time = time.time()
    while not stop_flag['stop']:
        times_typed += 1
        print(f"Typing gibberish ({times_typed} times)...")
        type_something()
        sleep_time = rand.uniform(TYPE_DELAY_MIN, TYPE_DELAY_MAX)
        print(f"Sleeping for {sleep_time:.2f} seconds...")
        start = time.time()
        while time.time() - start < sleep_time:
            if stop_flag['stop']:
                break
            time.sleep(0.1)
    end_time = time.time()
    run_time = end_time - start_time
    print(f"Stopped. Typed a total of {times_typed} times. Ran for {run_time:.2f} seconds")
    play_sound('good')
    play_sound('bad')
    input("Press [Enter] to exit")
    play_sound('bad', 2)


if __name__ == '__main__':
    main()