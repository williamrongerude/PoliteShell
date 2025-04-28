# politeshell.py

import os
import subprocess
from politeness import detect_politeness, classify_politeness, PHRASES

def clean_polite_phrases(command: str) -> str:
    """
    preserve casing of non polite words
    """
    cmd = command
    for phrase in sorted(PHRASES, key=len, reverse=True):  # longest polite phrases first
        lower_cmd = cmd.lower()
        lower_phrase = phrase.lower()
        idx = lower_cmd.find(lower_phrase)
        if idx != -1:
            cmd = cmd[:idx] + cmd[idx + len(phrase):]
    return cmd.strip()


def main():
    print("\n🎩 Welcome to PoliteShell 🎩")
    print("Politeness is required—type 'exit' or Ctrl-D to quit.\n")

    while True:
        try:
            user = input("PoliteShell> ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\nGoodbye, and stay courteous!")
            break

        low = user.lower()
        if low in ("exit", "quit"):
            print("Goodbye, and thank you for your courtesy!")
            break

        score = detect_politeness(user)
        level = classify_politeness(score)

        if level == "rude":
            print("🚫 I'm sorry, but you must ask politely.")
            continue
        if level == "basic_politeness":
            print("🙂 Accepting your command... but remember: a little more politeness never hurts!")
        elif level == "good_politeness":
            print("😊 Thank you for being polite!")
        else:  # exceptional_politeness
            print("🌟 Such wonderful manners! Executing with honor!")

        cmd = clean_polite_phrases(user)
        if not cmd:
            print("⚠️ No command detected after polite words.")
            continue

        # Handle 'cd' internally so it persists
        if cmd.startswith("cd "):
            path = cmd[3:].strip()
            try:
                os.chdir(path)
            except Exception as e:
                print(f"❌ cd error: {e}")
            continue

        # Otherwise forward everything else to the real shell
        subprocess.run(cmd, shell=True)

if __name__ == "__main__":
    main()
