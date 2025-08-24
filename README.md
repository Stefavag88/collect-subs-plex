# Subtitle Collector for Plex

This script automates collecting and renaming subtitles for Plex.  
It expects a structure like this:

```text
/YourMediaFolder
├─ Subs/
│ ├─ Episode1/
│ │ ├─ some-random-name.eng.srt
│ │ └─ otherfile.greek.forced.srt
│ ├─ Episode2/
│ │ └─ whatever.srt
│ └─ ...
```


After running, the subtitles are moved into the media folder itself:
```text
/YourMediaFolder
├─ Episode1.en.srt
├─ Episode1.el.forced.srt
├─ Episode2.srt
└─ ...
```

Plex will now correctly detect and match them.

---

## Features
- Looks inside `./Subs/[EpisodeName]/*.srt`
- Renames each file to match the episode folder name
- Detects language codes (`en`, `el`, `pt-BR`, etc.)
- Preserves flags like `forced` and `sdh`
- Moves subs into the chosen directory (`./` by default)
- Avoids overwriting by adding `(1)`, `(2)`, etc.

---

## Requirements
- Python 3.7 or higher

---

## Usage

1. Place the script inside the folder that contains your `Subs/` directory.  
2. Run with:

```bash
python collect_subs.py
```

By default, it works on the current directory (./).

You can also specify another target folder:
python collect_subs.py /path/to/media

## Examples

Input:
```text
Subs/
  Ep1/
    track1.eng.srt
    track2.greek.forced.srt
  Ep2/
    something.srt
```

Output:
```text
Ep1.en.srt
Ep1.el.forced.srt
Ep2.srt
```
## Notes

If the script can’t detect a language from the filename, it will just produce EpisodeName.srt.

Existing files are never overwritten — duplicates get (1), (2) appended.

Works on Windows, macOS, and Linux.

## License

MIT — free to use, modify, and share.