# ==========================================================
# SUPER MALAKOR CONVERTER - FULL CODE (EXCLUDE JP REVERSE)
# ==========================================================

# --------------------------
#  DECORATOR FOR SAFE CONVERSION
# --------------------------
def safe_conversion(func):
    """Decorator to safely run converter methods with error handling."""
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as error:
            print(f"[ERROR] {func.__name__} failed:", error)
            return "❌ Conversion Error"
    return wrapper


# ==========================================================
#  ENGLISH MALAKOR
# ==========================================================
class EnglishMalakor:
    VOWELS = "aeiou"
    CONSONANTS = "bcdfghjklmnpqrstvwxyz"

    def is_vowel(self, character: str) -> bool:
        return character.lower() in self.VOWELS

    def split_into_syllables(self, word: str) -> list[str]:
        word_lower = word.lower()
        if len(word_lower) <= 3 or (len(word_lower) >= 2 and word_lower[-2] in self.CONSONANTS and word_lower[-1] == 'e') or word_lower.endswith('y'):
            return [word_lower]

        syllables = []
        index = 0
        while index < len(word_lower):
            start_index = index
            # Leading consonants
            while index < len(word_lower) and word_lower[index] in self.CONSONANTS:
                index += 1
            # At least one vowel
            if index < len(word_lower) and self.is_vowel(word_lower[index]):
                index += 1
            # Trailing consonants until next vowel
            while index < len(word_lower) and (index + 1 >= len(word_lower) or not self.is_vowel(word_lower[index + 1])):
                index += 1
            syllables.append(word_lower[start_index:index])
        return syllables

    @safe_conversion
    def to_malakor(self, word: str) -> str:
        syllables = self.split_into_syllables(word)
        malakor_syllables = []

        for syllable in syllables:
            if not syllable:
                continue

            consonant_cluster = ""
            remainder = syllable
            for cluster_length in range(min(3, len(syllable)), 0, -1):
                if all(char.lower() in self.CONSONANTS for char in syllable[:cluster_length]):
                    consonant_cluster = syllable[:cluster_length]
                    remainder = syllable[cluster_length:]
                    break
            if not consonant_cluster:
                consonant_cluster = syllable[0]
                remainder = syllable[1:]

            if not remainder:
                remainder = consonant_cluster

            malakor_syllables.append(f"{consonant_cluster}a la g{remainder}")

        return " / ".join(malakor_syllables)

    @safe_conversion
    def from_malakor(self, malakor_text: str) -> str:
        malakor_text = malakor_text.lower().strip()
        words = [w.strip() for w in malakor_text.split("/") if w.strip()]
        english_words = []

        for phrase in words:
            tokens = phrase.split()
            reconstructed = ""
            index = 0
            while index < len(tokens):
                if index + 2 < len(tokens) and tokens[index + 1] == "la" and tokens[index + 2].startswith("g"):
                    cluster = tokens[index][:-1] if tokens[index].endswith("a") else tokens[index]
                    remainder = tokens[index + 2][1:]
                    reconstructed += cluster + remainder
                    index += 3
                else:
                    reconstructed += tokens[index]
                    index += 1
            english_words.append(reconstructed)

        return " ".join(english_words)


# ==========================================================
#  JAPANESE MALAKOR
# ==========================================================
class JapaneseMalakor:
    SMALL_TSU = {"っ", "ッ"}
    LONG_VOWEL = "ー"

    DIGRAPHS = [
        "きゃ","きゅ","きょ","しゃ","しゅ","しょ","ちゃ","ちゅ","ちょ",
        "にゃ","にゅ","にょ","ひゃ","ひゅ","ひょ","みゃ","みゅ","みょ",
        "りゃ","りゅ","りょ","ぎゃ","ぎゅ","ぎょ","じゃ","じゅ","じょ",
        "びゃ","びゅ","びょ","ぴゃ","ぴゅ","ぴょ",
        "キャ","キュ","キョ","シャ","シュ","ショ","チャ","チュ","チョ",
        "ニャ","ニュ","ニョ","ヒャ","ヒュ","ヒョ","ミャ","ミュ","ミョ",
        "リャ","リュ","リョ","ギャ","ギュ","ギョ","ジャ","ジュ","ジョ",
        "ビャ","ビュ","ビョ","ピャ","ピュ","ピョ",
    ]

    GROW_HIRA = {"あ":"が","い":"ぎ","う":"ぐ","え":"げ","お":"ご"}
    GROW_KATA = {"あ":"ガ","い":"ギ","う":"グ","え":"ゲ","お":"ゴ"}
    HIRAGANA_VOWELS = set("あいうえお")
    KATAKANA_VOWELS = set("アイウエオ")
    DIGRAPH_G_MAP = {
        "きゃ":"ぎゃ","きゅ":"ぎゅ","きょ":"ぎょ",
        "しゃ":"じゃ","しゅ":"じゅ","しょ":"じょ",
        "ちゃ":"ぢゃ","ちゅ":"ぢゅ","ちょ":"ぢょ",
        "ひゃ":"びゃ","ひゅ":"びゅ","ひょ":"びょ",
        "ぎゃ":"ぎゃ","ぎゅ":"ぎゅ","ぎょ":"ぎょ",
        "じゃ":"じゃ","じゅ":"じゅ","じょ":"じょ",
        "びゃ":"びゃ","びゅ":"びゅ","びょ":"びょ",
        "ぴゃ":"ぴゃ","ぴゅ":"ぴゅ","ぴょ":"ぴょ",
        "キャ":"ギャ","キュ":"ギュ","キョ":"ギョ",
        "シャ":"ジャ","シュ":"ジュ","ショ":"ジョ",
        "チャ":"ヂャ","チュ":"ヂュ","チョ":"ヂョ",
        "ヒャ":"ビャ","ヒュ":"ビュ","ヒョ":"ビョ",
        "ギャ":"ギャ","ギュ":"ギュ","ギョ":"ギョ",
        "ジャ":"ジャ","ジュ":"ジュ","ジョ":"ジョ",
        "ビャ":"ビャ","ビュ":"ビュ","ビョ":"ビョ",
        "ピャ":"ピャ","ピュ":"ピュ","ピョ":"ピョ",
    }

    @staticmethod
    def is_katakana(character: str) -> bool:
        return '\u30A0' <= character <= '\u30FF'

    def split_into_syllables(self, text: str) -> list[str]:
        syllables = []
        i = 0
        while i < len(text):
            if i+1 < len(text) and text[i:i+2] in self.DIGRAPHS:
                syllables.append(text[i:i+2])
                i += 2
            else:
                syllables.append(text[i])
                i += 1
        return syllables

    def detect_script(self, syllable: str) -> str:
        if syllable and self.is_katakana(syllable[0]):
            return "katakana"
        return "hiragana"

    def base_vowel(self, syllable: str) -> str:
        kat_to_hira = {"ア":"あ","イ":"い","ウ":"う","エ":"え","オ":"お"}
        last_char = syllable[-1]
        if last_char in {"ゃ","ャ"}: return "あ"
        if last_char in {"ゅ","ュ"}: return "う"
        if last_char in {"ょ","ョ"}: return "お"
        if last_char in self.HIRAGANA_VOWELS: return last_char
        if last_char in self.KATAKANA_VOWELS: return kat_to_hira.get(last_char, "あ")
        return "あ"

    @safe_conversion
    def to_jpmal(self, text: str) -> str:
        syllables = self.split_into_syllables(text)
        converted = []
        for syl in syllables:
            if syl in self.SMALL_TSU or syl == self.LONG_VOWEL:
                converted.append(syl)
                continue
            script = self.detect_script(syl)
            ra = "ラ" if script == "katakana" else "ら"
            if syl in self.DIGRAPH_G_MAP:
                converted.append(syl[0] + ra + self.DIGRAPH_G_MAP[syl])
                continue
            vowel = self.base_vowel(syl)
            g_kana = self.GROW_KATA[vowel] if script == "katakana" else self.GROW_HIRA[vowel]
            converted.append(syl[0] + ra + g_kana)
        return "".join(converted)


# ==========================================================
#  SUPER MALAKOR CONTROLLER
# ==========================================================
class SuperMalakor:
    def __init__(self):
        self.english_converter = EnglishMalakor()
        self.japanese_converter = JapaneseMalakor()

    @safe_conversion
    def english_to_malakor(self, text: str) -> str:
        return " | ".join(self.english_converter.to_malakor(word) for word in text.split())

    @safe_conversion
    def malakor_to_english(self, text: str) -> str:
        return self.english_converter.from_malakor(text)

    @safe_conversion
    def japanese_to_jpmal(self, text: str) -> str:
        return self.japanese_converter.to_jpmal(text)


# ==========================================================
#  CONSOLE APPLICATION
# ==========================================================
def run_super_malakor_app():
    converter = SuperMalakor()
    print("==== SUPER MALAKOR CONVERTER ====")
    print("Modes:")
    print("0 → English → Malakor Eng")
    print("1 → Malakor Eng → English")
    print("2 → Japanese → JP Malakor")
    print("3 → Exit")

    while True:
        mode = input("\nChoose mode (0-3): ").strip()
        if mode == "3":
            print("\nGoodbye 👋")
            break

        try:
            if mode == "0":
                text = input("Enter English text: ").strip()
                if not text:
                    print("Please enter text!")
                    continue
                print("Malakor Eng:", converter.english_to_malakor(text))

            elif mode == "1":
                text = input("Enter Malakor Eng text: ").strip()
                if not text:
                    print("Please enter text!")
                    continue
                print("English:", converter.malakor_to_english(text))

            elif mode == "2":
                text = input("Enter Japanese text: ").strip()
                if not text:
                    print("Please enter text!")
                    continue
                print("JP Malakor:", converter.japanese_to_jpmal(text))

            else:
                print("Invalid mode! Choose 0-3.")

        except Exception as e:
            print("❌ Error:", e)


# ==========================================================
#  RUN APPLICATION
# ==========================================================
if __name__ == "__main__":
    run_super_malakor_app()
