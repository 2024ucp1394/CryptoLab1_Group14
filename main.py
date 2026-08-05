import os
from datetime import datetime
from collections import Counter

LOG_FOLDER = "logs"
LOG_FILE = os.path.join(LOG_FOLDER, "activity.log")
DATASET_FOLDER = "datasets"


# ---------------- Logging ----------------

def log_activity(option):
    os.makedirs(LOG_FOLDER, exist_ok=True)

    with open(LOG_FILE, "a") as f:
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        f.write(f"{now} --> {option}\n")


# ---------------- File Analysis ----------------

def analyze_file():

    files = os.listdir(DATASET_FOLDER)

    if not files:
        print("No files found.")
        return

    print("\nAvailable Files:")

    for i, file in enumerate(files, start=1):
        print(f"{i}. {file}")

    choice = int(input("\nChoose file number: "))

    filename = files[choice - 1]
    filepath = os.path.join(DATASET_FOLDER, filename)

    with open(filepath, "r", encoding="utf-8") as f:
        text = f.read()

    characters = len(text)
    words = len(text.split())
    lines = len(text.splitlines())
    unique_characters = len(set(text))

    letters = [c.lower() for c in text if c.isalpha()]
    frequency = Counter(letters)

    print("\n----- Analysis -----")
    print("Characters :", characters)
    print("Words      :", words)
    print("Lines      :", lines)
    print("Unique Chars:", unique_characters)

    print("\nLetter Frequency")

    for letter, count in sorted(frequency.items()):
        print(letter, ":", count)


# ---------------- Menu ----------------

def menu():

    while True:

        print("\n====== CryptoLabX ======")
        print("1. Encrypt")
        print("2. Decrypt")
        print("3. Attack")
        print("4. Analyze File")
        print("5. Exit")

        choice = input("Enter choice: ")

        if choice == "1":
            log_activity("Encrypt")
            print("Coming Soon...")

        elif choice == "2":
            log_activity("Decrypt")
            print("Coming Soon...")

        elif choice == "3":
            log_activity("Attack")
            print("Coming Soon...")

        elif choice == "4":
            log_activity("Analyze")
            analyze_file()

        elif choice == "5":
            log_activity("Exit")
            print("Goodbye!")
            break

        else:
            print("Invalid Choice")


if __name__ == "__main__":
    menu()
