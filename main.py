import time
import threading
from pynput import keyboard
import pyautogui as pygui
import random as rand
import numpy as np
import sounddevice as sd

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

# Sound definition
SAMPLE_RATE = 44100
GOOD_SOUND = None
BAD_SOUND = None


def make_tone(freq, duration=0.15, volume=1.0):
    t = np.linspace(0, duration, int(SAMPLE_RATE * duration), False)

    wave = (
        np.sin(2 * np.pi * freq * t) +
        0.5 * np.sin(2 * np.pi * freq * 2 * t) +
        0.25 * np.sin(2 * np.pi * freq * 3 * t)
    )

    audio = wave * volume
    return audio.astype(np.float32)


def pregenerate_sounds():
    global GOOD_SOUND, BAD_SOUND
    GOOD_SOUND = make_tone(400, 0.20, 1)
    BAD_SOUND = make_tone(200, 0.25, 1)


def play_sound(sound='good', times=1):
    if sound == 'good':
        audio = GOOD_SOUND
    else:
        audio = BAD_SOUND
    
    for _ in range(times):
        sd.play(audio, SAMPLE_RATE)
        sd.wait()  # Wait until playback is finished


def type_something():
    text = generate_text()
    strokes = text_to_strokes(text, TYPO_CHANCE, MISSED_CORRECTION_CHANCE, COMMA_CHANCE, SENTENCE_BREAK_CHANCE, PARAGRAPH_CHANCE)
    type_strokes(strokes, TYPE_SPEED_MIN, TYPE_SPEED_MAX)


def stop_listener(stop_flag):
    def on_press(key):
        if key == keyboard.Key.esc:
            play_sound('bad')
            print("Stop signal received, stopping...")
            stop_flag['stop'] = True
            return False

    with keyboard.Listener(on_press=on_press) as listener:
        listener.join()


def main():
    pregenerate_sounds()
    stop_flag = {'stop': False}
    
    listener_thread = threading.Thread(target=stop_listener, args=(stop_flag,), daemon=True)
    listener_thread.start()


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