# Smart File Organizer

A fast, **zero-dependency** command-line tool that automatically sorts messy folders — Downloads, Desktop, anywhere — into clean subfolders by **type**, **extension** or **date**. Safe by default, with a full **undo**.

<p>
  <img src="https://img.shields.io/badge/Python-3.10+-141417?style=flat-square&logo=python&logoColor=6e56f7" />
  <img src="https://img.shields.io/badge/dependencies-none-141417?style=flat-square" />
  <img src="https://img.shields.io/badge/tested-pytest-141417?style=flat-square&logo=pytest&logoColor=6e56f7" />
  <img src="https://img.shields.io/badge/license-MIT-141417?style=flat-square" />
</p>

> **Demo**
>
> <!-- Replace with a real terminal recording / screenshot -->
> ![Organizer demo](https://placehold.co/800x400/0a0a0b/6e56f7?text=Smart+File+Organizer)

---

## ✨ Features

- 🗂 **Three modes** — group by category, by extension, or by month (`YYYY-MM`)
- 🛡 **Safe by default** — `--dry-run` previews every move before touching a file
- ↩️ **Undo anything** — each run writes a manifest you can reverse instantly
- ⚙️ **Custom rules** — bring your own categories via a simple JSON file
- 🔁 **Recursive mode** + automatic name-collision handling (`file (1).png`)
- 🪶 **No dependencies** — pure Python standard library

## 🚀 Quick start

```bash
git clone https://github.com/Ansagan359/smart-file-organizer.git
cd smart-file-organizer

# Preview what would happen (nothing is moved)
python -m organizer ~/Downloads --dry-run

# Actually organize it
python -m organizer ~/Downloads
```

Or install it as a command:

```bash
pip install .
organizer ~/Downloads
```

## 🧭 Usage

```
organizer [path] [options]

positional:
  path                  Folder to organize (default: current directory)

options:
  -m, --mode {category,extension,date}   How to group files (default: category)
  -r, --recursive                        Include sub-folders
  -n, --dry-run                          Preview without moving anything
  -c, --config FILE                      Custom rules JSON
      --undo MANIFEST                    Undo a previous run
  -v, --version                          Show version
```

### Examples

```bash
# Group the Desktop by file type
organizer ~/Desktop

# Group photos by the month they were created
organizer ~/Pictures --mode date

# Use your own categories
organizer ~/Downloads --config examples/rules.json

# Undo the last run
organizer --undo "organizer-manifest-20260629-141200.json"
```

## ⚙️ Custom rules

Pass any JSON mapping of `category → [extensions]`:

```json
{
  "Pictures": ["jpg", "png", "webp"],
  "Docs": ["pdf", "docx", "md"],
  "Music": ["mp3", "flac"]
}
```

Anything not matched lands in an `Other/` folder.

## 🗂 Project structure

```
smart-file-organizer/
├── organizer/
│   ├── __main__.py     # python -m organizer
│   ├── cli.py          # argument parsing
│   ├── core.py         # planning & executing moves
│   ├── rules.py        # default + custom category rules
│   └── manifest.py     # undo support
├── tests/              # pytest suite
├── examples/rules.json
├── pyproject.toml
└── README.md
```

## 🧪 Tests

```bash
pip install -e ".[dev]"
pytest
```

## 📄 License

[MIT](LICENSE) © Ansagan
