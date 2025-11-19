# ==========================
# Japanese → Malakor with consonant + vowel group
# ==========================

SMALL_TSU = {"っ","ッ"}
LONG_VOWEL = "ー"

# Consonant groups
SOUND_GROUPS = {
    "a": ["あ","い","う","え","お","ア","イ","ウ","エ","オ"],
    "k": ["か","き","く","け","こ","カ","キ","ク","ケ","コ"],
    "s": ["さ","し","す","せ","そ","サ","シ","ス","セ","ソ"],
    "t": ["た","ち","つ","て","と","タ","チ","ツ","テ","ト"],
    "n": ["な","に","ぬ","ね","の","ナ","ニ","ヌ","ネ","ノ"],
    "h": ["は","ひ","ふ","へ","ほ","ハ","ヒ","フ","ヘ","ホ"],
    "m": ["ま","み","む","め","も","マ","ミ","ム","メ","モ"],
    "y": ["や","ゆ","よ","ヤ","ユ","ヨ"],
    "r": ["ら","り","る","れ","ろ","ラ","リ","ル","レ","ロ"],
    "w": ["わ","を","ワ","ヲ"],
    "g": ["が","ぎ","ぐ","げ","ご","ガ","ギ","グ","ゲ","ゴ"],
    "z": ["ざ","じ","ず","ぜ","ぞ","ザ","ジ","ズ","ゼ","ゾ"],
    "d": ["だ","ぢ","づ","で","ど","ダ","ヂ","ヅ","デ","ド"],
    "b": ["ば","び","ぶ","べ","ぼ","バ","ビ","ブ","ベ","ボ"],
    "p": ["ぱ","ぴ","ぷ","ぺ","ぽ","パ","ピ","プ","ペ","ポ"]
}

# Vowel groups
VOWEL_GROUPS = {
    "あ": ["あ","か","が","さ","ざ","た","だ","な","は","ば","ぱ","ま","や","ら","わ",
          "ア","カ","ガ","サ","ザ","タ","ダ","ナ","ハ","バ","パ","マ","ヤ","ラ","ワ"],
    "い": ["い","き","ぎ","し","じ","ち","ぢ","に","ひ","び","ぴ","み","り",
          "イ","キ","ギ","シ","ジ","チ","ヂ","ニ","ヒ","ビ","ピ","ミ","リ"],
    "う": ["う","く","ぐ","す","ず","つ","づ","ぬ","ふ","ぶ","ぷ","む","ゆ","る",
          "ウ","ク","グ","ス","ズ","ツ","ヅ","ヌ","フ","ブ","プ","ム","ユ","ル"],
    "え": ["え","け","げ","せ","ぜ","て","で","ね","へ","め","れ",
          "エ","ケ","ゲ","セ","ゼ","テ","デ","ネ","ヘ","メ","レ"],
    "お": ["お","こ","ご","そ","ぞ","と","ど","の","ほ","ぼ","ぽ","も","よ","ろ","を",
          "オ","コ","ゴ","ソ","ゾ","ト","ド","ノ","ホ","ボ","ポ","モ","ヨ","ロ","ヲ"]
}

# Digraphs
DIGRAPHS = [
    "きゃ","きゅ","きょ","しゃ","しゅ","しょ","ちゃ","ちゅ","ちょ",
    "にゃ","にゅ","にょ","ひゃ","ひゅ","ひょ","みゃ","みゅ","みょ",
    "りゃ","りゅ","りょ","ぎゃ","ぎゅ","ぎょ","じゃ","じゅ","じょ",
    "びゃ","びゅ","びょ","ぴゃ","ぴゅ","ぴょ",
    "キャ","キュ","キョ","シャ","シュ","ショ","チャ","チュ","チョ",
    "ニャ","ニュ","ニョ","ヒャ","ヒュ","ヒョ","ミャ","ミュ","ミョ",
    "リャ","リュ","リョ","ギャ","ギュ","ギョ","ジャ","ジュ","ジョ",
    "ビャ","ビュ","ビョ","ピャ","ピュ","ピョ"
]

# Split syllables
def split_syllables_jp(text):
    sylls = []
    i = 0
    while i < len(text):
        if i+1 < len(text) and text[i:i+2] in DIGRAPHS:
            sylls.append(text[i:i+2])
            i += 2
        else:
            sylls.append(text[i])
            i += 1
    return sylls

# Get consonant group
def get_consonant_group(syl):
    for group, chars in SOUND_GROUPS.items():
        if syl[0] in chars:
            return group
    return "a"

# Get vowel group
def get_vowel_group(syl):
    for group, chars in VOWEL_GROUPS.items():
        if syl[0] in chars:
            return group
    return "あ"

# Malakor transform: consonant group + ら + vowel group
def jpmal_transform(syl):
    if syl in SMALL_TSU or syl == LONG_VOWEL:
        return syl
    cons = get_consonant_group(syl)
    vow = get_vowel_group(syl)
    # Keep original case (Katakana/Hiragana)
    return syl[0] + "ら" + vow

# Full Japanese → Malakor
def malakor_jp(text):
    sylls = split_syllables_jp(text)
    result = ""
    for syl in sylls:
        result += jpmal_transform(syl)
    return result

# ==========================
# Test examples
# ==========================
examples = ["あー","きー","ひゃー","もっち","ぼっジー","キャー","シュッ","ぴょー","ぱっぷ","とうきょ"]
for e in examples:
    print(e, "→", malakor_jp(e))
