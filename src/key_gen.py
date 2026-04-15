import random as rand


def text_to_strokes(
    text,
    typo_chance=0.1,
    missed_correction_chance=0.3,
    comma_chance=0.15,
    sentence_break_chance=0.2,
    paragraph_chance=0.2,
):
    all_keys = "abcdefghijklmnopqrstuvwxyz"
    keystrokes = []
    words_since_comma = 0
    words_since_dot = 0
    i = 0

    # Cooldowns to space out commas/dots
    min_words_between_commas = rand.randint(3, 5)
    min_words_between_dots = rand.randint(5, 8)

    while i < len(text):
        char = text[i]

        # Handle alphabetic characters (potential typos)
        if char.isalpha() and rand.random() < typo_chance:
            wrong_key = rand.choice(all_keys.replace(char.lower(), ''))
            keystrokes.append(wrong_key)

            if rand.random() < missed_correction_chance:
                # Missed mistake: type a few more chars, then come back
                skip_ahead = rand.randint(3, 8)
                fragment = []
                for j in range(1, skip_ahead):
                    if i + j < len(text):
                        fragment.append(text[i + j])
                        keystrokes.append(text[i + j])

                # Realize the mistake → backspace over fragment + wrong char
                for _ in range(len(fragment) + 1):
                    keystrokes.append("backspace")

                # Re-type fragment (can have new mistakes)
                redo_text = wrong_key + "".join(fragment)
                redo_strokes = text_to_strokes(redo_text, typo_chance, 0, 0, 0, 0)
                keystrokes.extend(redo_strokes[:-1])  # avoid trailing space
                i += skip_ahead
                continue
            else:
                keystrokes.append("backspace")

        keystrokes.append(char)

        # Sentence/word handling
        if char == " ":
            words_since_comma += 1
            words_since_dot += 1

            # Maybe insert a comma (after some words)
            if (
                words_since_comma >= min_words_between_commas
                and rand.random() < comma_chance
            ):
                keystrokes.pop()
                keystrokes.append(",")
                keystrokes.append(" ")
                words_since_comma = 0
                min_words_between_commas = rand.randint(3, 5)

            # Maybe insert sentence break (dot or newline)
            elif (
                words_since_dot >= min_words_between_dots
                and rand.random() < sentence_break_chance
            ):
                keystrokes.pop()
                keystrokes.append(".")
                words_since_dot = 0
                min_words_between_dots = rand.randint(5, 8)

                # Maybe add a line break
                add_line = rand.random() < 0.5
                if add_line:
                    keystrokes.append("\n")
                    if rand.random() < paragraph_chance:
                        keystrokes.append("\n")
                else:
                    keystrokes.append(" ")

                # Find next alpha and capitalize it
                j = i + 1
                while j < len(text) and not text[j].isalpha():
                    j += 1
                if j < len(text):
                    next_char = text[j].upper()
                    keystrokes.append(next_char)
                    i = j  # Skip the lowercase version
                    continue

        i += 1

    keystrokes.append(" ")
    return keystrokes
