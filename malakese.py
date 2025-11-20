# ==========================
# JPMal - Pure Japanese Malakor
# ==========================

SMALL_TSU = {"っ", "ッ"}
LONG_VOWEL = "ー"

# Digraphs (hiragana + katakana)
DIGRAPHS = [
    # hiragana
    "きゃ","きゅ","きょ","しゃ","しゅ","しょ","ちゃ","ちゅ","ちょ",
    "にゃ","にゅ","にょ","ひゃ","ひゅ","ひょ","みゃ","みゅ","みょ",
    "りゃ","りゅ","りょ","ぎゃ","ぎゅ","ぎょ","じゃ","じゅ","じょ",
    "びゃ","びゅ","びょ","ぴゃ","ぴゅ","ぴょ",
    # katakana
    "キャ","キュ","キョ","シャ","シュ","ショ","チャ","チュ","チョ",
    "ニャ","ニュ","ニョ","ヒャ","ヒュ","ヒョ","ミャ","ミュ","ミョ",
    "リャ","リュ","リョ","ギャ","ギュ","ギョ","ジャ","ジュ","ジョ",
    "ビャ","ビュ","ビョ","ピャ","ピュ","ピョ",
]

# G-row for simple vowels (hiragana and katakana)
GROW_HIRA = {"あ":"が","い":"ぎ","う":"ぐ","え":"げ","お":"ご"}
GROW_KATA = {"あ":"ガ","い":"ギ","う":"グ","え":"ゲ","お":"ゴ"}  # note keys are hiragana vowels; values katakana

# Digraph -> corresponding g-digraph (both scripts)
DIGRAPH_G_MAP = {
    # hiragana
    "きゃ":"ぎゃ","きゅ":"ぎゅ","きょ":"ぎょ",
    "しゃ":"じゃ","しゅ":"じゅ","しょ":"じょ",
    "ちゃ":"ぢゃ","ちゅ":"ぢゅ","ちょ":"ぢょ",
    "ひゃ":"びゃ","ひゅ":"びゅ","ひょ":"びょ",
    "ぎゃ":"ぎゃ","ぎゅ":"ぎゅ","ぎょ":"ぎょ",
    "じゃ":"じゃ","じゅ":"じゅ","じょ":"じょ",
    "びゃ":"びゃ","びゅ":"びゅ","びょ":"びょ",
    "ぴゃ":"ぴゃ","ぴゅ":"ぴゅ","ぴょ":"ぴょ",
    # katakana
    "キャ":"ギャ","キュ":"ギュ","キョ":"ギョ",
    "シャ":"ジャ","シュ":"ジュ","ショ":"ジョ",
    "チャ":"ヂャ","チュ":"ヂュ","チョ":"ヂョ",
    "ヒャ":"ビャ","ヒュ":"ビュ","ヒョ":"ビョ",
    "ギャ":"ギャ","ギュ":"ギュ","ギョ":"ギョ",
    "ジャ":"ジャ","ジュ":"ジュ","ジョ":"ジョ",
    "ビャ":"ビャ","ビュ":"ビュ","ビョ":"ビョ",
    "ピャ":"ピャ","ピュ":"ピュ","ピョ":"ピョ",
}

# helper sets
HIRAGANA_VOWELS = set("あいうえお")
KATAKANA_VOWELS = set("アイウエオ")
SMALL_YA = {"ゃ","ゅ","ょ","ャ","ュ","ョ"}

# -------------------------
# Utilities
# -------------------------
def is_katakana_char(ch: str) -> bool:
    return '\u30A0' <= ch <= '\u30FF'  # Katakana block

def split_syllables(text: str):
    """Split into syllables: prefer digraphs (2-char) then single kana."""
    out = []
    i = 0
    L = len(text)
    while i < L:
        if i+1 < L and text[i:i+2] in DIGRAPHS:
            out.append(text[i:i+2])
            i += 2
        else:
            out.append(text[i])
            i += 1
    return out

def detect_script(syl: str) -> str:
    """Return 'katakana' or 'hiragana' based on first character."""
    if syl and is_katakana_char(syl[0]):
        return "katakana"
    return "hiragana"

def base_vowel_of_syllable(syl: str) -> str:
    """
    Return a canonical vowel char in hiragana: 'あ','い','う','え','お'
    for the syllable's vowel sound.
    """
    # if digraph ending with small ya/yu/yo -> map to vowels a/u/o
    last = syl[-1]
    if last in {"ゃ","ャ"}:
        return "あ"
    if last in {"ゅ","ュ"}:
        return "う"
    if last in {"ょ","ョ"}:
        return "お"
    # otherwise if last is vowel (hiragana or katakana) map katakana -> hiragana
    if last in HIRAGANA_VOWELS:
        return last
    if last in KATAKANA_VOWELS:
        # map katakana vowel to hiragana vowel by unicode offset
        # simple mapping:
        kat_to_hira = {"ア":"あ","イ":"い","ウ":"う","エ":"え","オ":"お"}
        return kat_to_hira.get(last, "あ")
    # fallback: try first char vowel
    if syl[0] in HIRAGANA_VOWELS:
        return syl[0]
    if syl[0] in KATAKANA_VOWELS:
        kat_to_hira = {"ア":"あ","イ":"い","ウ":"う","エ":"え","オ":"お"}
        return kat_to_hira.get(syl[0], "あ")
    return "あ"

def g_for_vowel(vowel_hira: str, script: str) -> str:
    """Return the g-equivalent kana in the given script for the vowel group."""
    if script == "katakana":
        # GROW_KATA values are katakana; need mapping keyed by hiragana vowel
        return GROW_KATA.get(vowel_hira, "ガ")
    return GROW_HIRA.get(vowel_hira, "が")

# -------------------------
# Core transform
# -------------------------
def jpmal_syllable(syl: str) -> str:
    """Transform a single syllable into JPMal according to rule A."""
    # small tsu or long vowel remain as-is
    if syl in SMALL_TSU or syl == LONG_VOWEL:
        return syl

    script = detect_script(syl)

    # digraph special-case: use DIGRAPH_G_MAP if exists
    if syl in DIGRAPH_G_MAP:
        # form: <first-kana> + ra + g-digraph (preserve script)
        first = syl[0]
        ra = "ラ" if script == "katakana" else "ら"
        gdig = DIGRAPH_G_MAP[syl]
        return first + ra + gdig

    # else general case
    first = syl[0]
    ra = "ラ" if script == "katakana" else "ら"
    # find vowel group and then g equivalent
    vowel_hira = base_vowel_of_syllable(syl)   # 'あ','い','う','え','お'
    g_kana = g_for_vowel(vowel_hira, script)   # 'が' or 'ガ' etc.
    return first + ra + g_kana

def jpmal(text: str) -> str:
    parts = split_syllables(text)
    out = []
    for p in parts:
        out.append(jpmal_syllable(p))
    return "".join(out)

# -------------------------
# Quick tests (examples you gave)
# -------------------------
if __name__ == "__main__":
    examples = [
        'ありがとう',
    ]
    for ex in examples:
        print(f"{ex:8} → {jpmal(ex)}")
