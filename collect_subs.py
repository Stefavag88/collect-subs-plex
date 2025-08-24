#!/usr/bin/env python3
import os
import re
import shutil
import sys

# Map many common tokens -> standardized language tags
LANG_MAP = {
    "en": "en", "eng": "en", "english": "en",
    "el": "el", "ell": "el", "gr": "el", "gre": "el", "greek": "el",
    "es": "es", "spa": "es", "spanish": "es",
    "fr": "fr", "fra": "fr", "fre": "fr", "french": "fr",
    "it": "it", "ita": "it", "italian": "it",
    "pt": "pt", "por": "pt", "portuguese": "pt",
    "ptbr": "pt-BR", "pt-br": "pt-BR", "brazilian": "pt-BR",
    "de": "de", "ger": "de", "deu": "de", "german": "de",
    "nl": "nl", "dut": "nl", "nld": "nl", "dutch": "nl",
    "pl": "pl", "pol": "pl", "polish": "pl",
    "ru": "ru", "rus": "ru", "russian": "ru",
    "tr": "tr", "tur": "tr", "turkish": "tr",
    "ro": "ro", "ron": "ro", "rum": "ro", "romanian": "ro",
    "hu": "hu", "hun": "hu", "hungarian": "hu",
    "cs": "cs", "ces": "cs", "cze": "cs", "czech": "cs",
    "sk": "sk", "slk": "sk", "slo": "sk", "slovak": "sk",
    "sl": "sl", "slv": "sl", "slovenian": "sl",
    "sr": "sr", "srp": "sr", "serbian": "sr",
    "mk": "mk", "mac": "mk", "mkd": "mk", "macedonian": "mk",
    "bg": "bg", "bul": "bg", "bulgarian": "bg",
    "uk": "uk", "ukr": "uk", "ukrainian": "uk",
    "ar": "ar", "ara": "ar", "arabic": "ar",
    "he": "he", "iw": "he", "heb": "he", "hebrew": "he",
    "fa": "fa", "fas": "fa", "per": "fa", "persian": "fa", "farsi": "fa",
    "zh": "zh", "zho": "zh", "chi": "zh", "chs": "zh", "sc": "zh", "cht": "zh", "tc": "zh", "chinese": "zh",
    "ja": "ja", "jpn": "ja", "japanese": "ja",
    "ko": "ko", "kor": "ko", "korean": "ko",
    "vi": "vi", "vie": "vi", "vietnamese": "vi",
    "th": "th", "tha": "th", "thai": "th",
    "hi": "hi", "hin": "hi", "hindi": "hi",
}

# Tokens that indicate flags
FLAG_TOKENS = {
    "forced": "forced",
    "sdh": "sdh",
    "cc": "sdh",
    "hearing": "sdh",
}

TOKEN_SPLIT_RE = re.compile(r"[.\-_\s\[\]\(\)]+", re.UNICODE)

def detect_lang_and_flags(filename_no_ext: str):
    tokens = [t for t in TOKEN_SPLIT_RE.split(filename_no_ext.lower()) if t]
    lang = None
    flags = []

    # join tokens like 'pt' 'br' -> 'pt-br'
    joined = set()
    for i in range(len(tokens) - 1):
        joined.add(f"{tokens[i]}-{tokens[i+1]}")
        joined.add(f"{tokens[i]}{tokens[i+1]}")

    for cand in list(joined) + tokens:
        if cand in LANG_MAP:
            lang = LANG_MAP[cand]
            break

    seen = set()
    for t in tokens:
        if t in FLAG_TOKENS:
            flag = FLAG_TOKENS[t]
            if flag not in seen:
                flags.append(flag)
                seen.add(flag)

    return lang, flags

def unique_name(dest_dir: str, base_name: str) -> str:
    name, ext = os.path.splitext(base_name)
    candidate = base_name
    i = 1
    while os.path.exists(os.path.join(dest_dir, candidate)):
        candidate = f"{name}({i}){ext}"
        i += 1
    return candidate

def main():
    # use param or default to current directory
    if len(sys.argv) > 1:
        cwd = os.path.abspath(sys.argv[1])
    else:
        cwd = os.getcwd()

    subs_root = os.path.join(cwd, "Subs")
    if not os.path.isdir(subs_root):
        print(f"Error: 'Subs' folder not found inside {cwd}")
        return

    for episode_dir in sorted(os.listdir(subs_root)):
        ep_path = os.path.join(subs_root, episode_dir)
        if not os.path.isdir(ep_path):
            continue

        srt_files = [f for f in os.listdir(ep_path) if f.lower().endswith(".srt")]
        if not srt_files:
            continue

        for idx, srt_name in enumerate(sorted(srt_files)):
            src = os.path.join(ep_path, srt_name)
            base_no_ext = os.path.splitext(srt_name)[0]

            lang, flags = detect_lang_and_flags(base_no_ext)

            parts = [episode_dir]
            if lang:
                parts.append(lang)
            for fl in flags:
                parts.append(fl)

            target_base = ".".join(parts) + ".srt"
            dest_name = unique_name(cwd, target_base)
            dst = os.path.join(cwd, dest_name)

            print(f"Moving {os.path.relpath(src, cwd)} -> {dest_name}")
            shutil.move(src, dst)

    print("Done.")

if __name__ == "__main__":
    main()
