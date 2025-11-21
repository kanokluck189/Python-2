import random
from functools import wraps

# =========================
# Decorator for safe conversion
# =========================
def safe_conversion(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            print(f"❌ Error: {e}")
            return None
    return wrapper

# =========================
# Malakor Converter Class
# =========================
class MalakorConverter:
    def __init__(self):
        self.vowels = "aeiou"
        self.consonants = "bcdfghjklmnpqrstvwxyz"
        self.history = []

    def is_vowel(self, c: str) -> bool:
        return c.lower() in self.vowels

    @safe_conversion
    def split_syllables(self, word: str) -> list[str]:
        word_lower = word.lower()
        syllables = []
        if len(word) <= 3 or word_lower.endswith("y"):
            return [word_lower]

        pos = 0
        while pos < len(word_lower):
            start = pos
            while pos < len(word_lower) and word_lower[pos] in self.consonants:
                pos += 1
            if pos < len(word_lower) and self.is_vowel(word_lower[pos]):
                pos += 1
            while pos < len(word_lower) and (pos + 1 >= len(word_lower) or not self.is_vowel(word_lower[pos + 1])):
                pos += 1
            syllables.append(word_lower[start:pos])
        return syllables

    @safe_conversion
    def to_malakor(self, word: str) -> str:
        syllables = self.split_syllables(word)
        malakor_syllables = []
        for syll in syllables:
            if len(syll) <= 3 or syll.endswith("y"):
                cluster = syll[0]
                remainder = syll[1:]
            else:
                cluster = ""
                for i in range(min(3, len(syll)), 0, -1):
                    if all(c in self.consonants for c in syll[:i]):
                        cluster = syll[:i]
                        break
                if cluster:
                    remainder = syll[len(cluster):]
                else:
                    cluster = syll[0]
                    remainder = syll[1:]
            malakor_syllables.append(f"{cluster}a la g{remainder}")
        malakor_word = " / ".join(malakor_syllables)
        self.history.append({"original": word, "converted": malakor_word})
        return malakor_word

    @safe_conversion
    def from_malakor(self, text: str) -> str:
        text = text.lower().strip()
        words = [w.strip() for w in text.split("/")]
        english_words = []
        for w in words:
            tokens = w.split()
            reconstructed = ""
            i = 0
            while i < len(tokens):
                if i + 2 < len(tokens) and tokens[i + 1] == "la" and tokens[i + 2].startswith("g"):
                    cluster = tokens[i][:-1] if tokens[i].endswith("a") else tokens[i]
                    rest = tokens[i + 2][1:]
                    reconstructed += cluster + rest
                    i += 3
                else:
                    reconstructed += tokens[i]
                    i += 1
            english_words.append(reconstructed)
        return " ".join(english_words)

# =========================
# Quiz Mode
# =========================
WORD_BANK = [
    "cat","dog","fly","sky","shine","wake","high","play","jump","run",
    "love","star","moon","sun","tree","fire","rain","wind","snow","cloud",
    "sea","fish","bird","apple","orange","banana","grape","melon","peach","berry",
    "light","dark","sound","song","dance","music","book","story","dream","hope",
    "mind","heart","friend","family","home","school","game","work","time","life",
    "magic","power","force","energy","speed","skill","luck","trap","path","road",
    "mountain","river","valley","forest","garden","flower","leaf","seed","root","branch",
    "knife","sword","shield","armor","battle","fight","war","peace","king","queen",
    "night","day","morning","evening","summer","winter","spring","autumn","happy","sad",
    "angry","calm","fast","slow","deep","shallow","hot","cold","strong","weak"
]

def quiz_mode(converter: MalakorConverter):
    print("\n⚡🌴 Welcome to Malakor Requiem Quiz Mode! 🌴⚡")
    score = 0
    rounds = 5
    for i in range(rounds):
        word = random.choice(WORD_BANK)
        malakor_word = converter.to_malakor(word)
        print(f"\nQuestion {i+1}: Guess the English word for → {malakor_word}")
        answer = input("Your answer: ").strip().lower()
        if answer == word:
            print("✅ Correct! Stand power +10 💥")
            score += 10
        else:
            print(f"❌ Wrong! The correct answer was: {word}")
    print(f"\n🏆 Quiz finished! Your score: {score}/{rounds*10}\n")

# =========================
# Main Program
# =========================
def main():
    converter = MalakorConverter()
    print("\n⚡🌴 MALAKOR REQUIEM 🌴⚡")
    while True:
        print("\nSelect Mode:")
        print("0 → English → Malakor Eng")
        print("1 → Malakor Eng → English")
        print("2 → Conversion History")
        print("3 → Quiz Mode")
        print("4 → Exit")
        choice = input("Choose mode (0-4): ").strip()
        
        if choice == "0":
            text = input("Enter English word(s): ").strip()
            if text:
                words = text.split()
                result = ' | '.join([converter.to_malakor(w) for w in words])
                print(f"\nMalakor Eng: {result}")
        elif choice == "1":
            text = input("Enter Malakor Eng text: ").strip()
            if text:
                result = converter.from_malakor(text)
                print(f"\nEnglish: {result}")
        elif choice == "2":
            print("\nConversion History:")
            if not converter.history:
                print("No conversions yet.")
            for idx, record in enumerate(converter.history, 1):
                print(f"{idx}. {record['original']} → {record['converted']}")
        elif choice == "3":
            quiz_mode(converter)
        elif choice == "4":
            print("\nGoodbye 👋")
            break
        else:
            print("Invalid choice! Please enter 0-4.")

# =========================
# Run Program
# =========================
if __name__ == "__main__":
    main()
