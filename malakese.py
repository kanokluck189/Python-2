# ==========================
#  Japanese Romaji Mapper
# ==========================

HIRAGANA_ROMAJI = {
    "あ":"a","い":"i","う":"u","え":"e","お":"o",
    "か":"ka","き":"ki","く":"ku","け":"ke","こ":"ko",
    "さ":"sa","し":"shi","す":"su","せ":"se","そ":"so",
    "た":"ta","ち":"chi","つ":"tsu","て":"te","と":"to",
    "な":"na","に":"ni","ぬ":"nu","ね":"ne","の":"no",
    "は":"ha","ひ":"hi","ふ":"fu","へ":"he","ほ":"ho",
    "ま":"ma","み":"mi","む":"mu","め":"me","も":"mo",
    "や":"ya","ゆ":"yu","よ":"yo",
    "ら":"ra","り":"ri","る":"ru","れ":"re","ろ":"ro",
    "わ":"wa","を":"wo","ん":"n",
    "が":"ga","ぎ":"gi","ぐ":"gu","げ":"ge","ご":"go",
    "ざ":"za","じ":"ji","ず":"zu","ぜ":"ze","ぞ":"zo",
    "だ":"da","ぢ":"ji","づ":"zu","で":"de","ど":"do",
    "ば":"ba","び":"bi","ぶ":"bu","べ":"be","ぼ":"bo",
    "ぱ":"pa","ぴ":"pi","ぷ":"pu","ぺ":"pe","ぽ":"po",
    "きゃ":"kya","きゅ":"kyu","きょ":"kyo",
    "しゃ":"sha","しゅ":"shu","しょ":"sho",
    "ちゃ":"cha","ちゅ":"chu","ちょ":"cho",
    "にゃ":"nya","にゅ":"nyu","にょ":"nyo",
    "ひゃ":"hya","ひゅ":"hyu","ひょ":"hyo",
    "みゃ":"mya","みゅ":"myu","みょ":"myo",
    "りゃ":"rya","りゅ":"ryu","りょ":"ryo",
    "ぎゃ":"gya","ぎゅ":"gyu","ぎょ":"gyo",
    "じゃ":"ja","じゅ":"ju","じょ":"jo",
    "びゃ":"bya","びゅ":"byu","びょ":"byo",
    "ぴゃ":"pya","ぴゅ":"pyu","ぴょ":"pyo",
}

# Explicit Katakana → Romaji mapping
KATAKANA_ROMAJI = { 
    chr(ord(kana)-0x60): v for kana, v in HIRAGANA_ROMAJI.items()
}

# Reverse mappings
ROMAJI_HIRAGANA = {v:k for k,v in HIRAGANA_ROMAJI.items()}
ROMAJI_KATAKANA = {v:k for k,v in KATAKANA_ROMAJI.items()}

# Detect if input is Katakana
def is_katakana(text):
    return all('ァ' <= c <= 'ン' or c in "ー" for c in text)

def preprocess_japanese_keep_tsu(text):
    result = ""
    i = 0
    while i < len(text):
        c = text[i]
        # Replace long vowel mark with previous vowel
        if c == 'ー':
            if result:
                result += result[-1]
            i += 1
            continue
        result += c
        i += 1
    return result

def japanese_to_romaji_keep_tsu(text):
    text = preprocess_japanese_keep_tsu(text)
    romaji = ""
    i = 0
    mapping = KATAKANA_ROMAJI if is_katakana(text) else HIRAGANA_ROMAJI
    while i < len(text):
        if text[i] in {"っ","ッ"}:
            if i+1 < len(text):
                next_romaji = mapping.get(text[i+1], text[i+1])
                if next_romaji:
                    romaji += next_romaji[0]
            i += 1
            continue
        if i+1 < len(text) and text[i:i+2] in mapping:
            romaji += mapping[text[i:i+2]]
            i += 2
        elif text[i] in mapping:
            romaji += mapping[text[i]]
            i += 1
        else:
            romaji += text[i]
            i += 1
    return romaji

def romaji_to_japanese(romaji, target_script="hiragana"):
    result = ""
    i = 0
    mapping = ROMAJI_KATAKANA if target_script=="katakana" else ROMAJI_HIRAGANA
    while i < len(romaji):
        for l in [3,2,1]:
            part = romaji[i:i+l]
            if part in mapping:
                result += mapping[part]
                i += l
                break
        else:
            result += romaji[i]
            i += 1
    return result

# ==========================
#  Malakor Engine
# ==========================
class MalakorEngine:
    vowels = "aeiou"
    consonants = "bcdfghjklmnpqrstvwxyz"

    @staticmethod
    def is_vowel(c: str) -> bool:
        return c.lower() in MalakorEngine.vowels

    def split_syllables(self, word: str):
        word_lower = word.lower()
        syll_list = []
        if len(word) <= 3 or word_lower.endswith("y"):
            return [word_lower]
        pos = 0
        L = len(word_lower)
        while pos < L:
            start = pos
            while pos < L and word_lower[pos] in self.consonants:
                pos += 1
            if pos < L and self.is_vowel(word_lower[pos]):
                pos += 1
            while pos < L and (pos+1>=L or not self.is_vowel(word_lower[pos+1])):
                pos += 1
            syll_list.append(word_lower[start:pos])
        return syll_list

    def en_to_malakor(self, word: str, connector="la"):
        sylls = self.split_syllables(word)
        malakor_sylls = []
        for syl in sylls:
            if not syl:
                continue
            cluster = ""
            remainder = syl
            if len(syl) <=3 or syl.endswith("y"):
                cluster = syl[0]
                remainder = syl[1:]
            else:
                for l in range(min(3,len(syl)),0,-1):
                    if all(c in self.consonants for c in syl[:l]):
                        cluster = syl[:l]
                        remainder = syl[l:]
                        break
                if not cluster:
                    cluster = syl[0]
                    remainder = syl[1:]
                if not remainder:
                    remainder = cluster
            malakor_sylls.append(f"{cluster} {connector} g{remainder}")
        return " / ".join(malakor_sylls)

    def malakor_to_en(self, text: str):
        text = text.lower().strip()
        parts = [w.strip() for w in text.split("/") if w.strip()]
        english_words = []
        for w in parts:
            tokens = w.split()
            i = 0
            built = ""
            while i < len(tokens):
                if i+2 < len(tokens) and tokens[i+1] in {"la","ra"} and tokens[i+2].startswith("g"):
                    cluster = tokens[i][:-1] if tokens[i].endswith("a") else tokens[i]
                    rest = tokens[i+2][1:]
                    built += cluster+rest
                    i += 3
                else:
                    built += tokens[i]
                    i +=1
            english_words.append(built)
        return " ".join(english_words)

# ==========================
#  Terminal App
# ==========================
def main():
    malakor = MalakorEngine()
    print("🍊 Japanese Malakor Terminal (input Japanese → output same script)")
    print("0 → Romaji → Malakor")
    print("1 → Malakor → Romaji")
    print("2 → Japanese → Malakor (output Japanese)")
    print("3 → Malakor → Japanese")
    print("Type 'exit' to quit")
    while True:
        try:
            mode = input("\nMode (0-3): ").strip()
            if mode.lower() == "exit":
                print("Bye 🍊")
                break
            if mode not in {"0","1","2","3"}:
                print("Invalid mode")
                continue
            text = input("Input: ")

            target_script = "katakana" if is_katakana(text) else "hiragana"

            if mode=="0":
                print("→", malakor.en_to_malakor(text))
            elif mode=="1":
                print("→", malakor.malakor_to_en(text))
            elif mode=="2":
                romaji = japanese_to_romaji_keep_tsu(text)
                malakor_text = malakor.en_to_malakor(romaji, connector="ra")
                back_romaji = malakor.malakor_to_en(malakor_text)
                jp = romaji_to_japanese(back_romaji, target_script=target_script)
                print("→", jp)
            elif mode=="3":
                romaji = malakor.malakor_to_en(text)
                jp = romaji_to_japanese(romaji, target_script=target_script)
                print("→", jp)

        except Exception as e:
            print("Error:", e)

if __name__=="__main__":
    main()
