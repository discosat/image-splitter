# Image Splitter

A simple Python CLI tool to split a combined binary file into metadata and raw image, save metadata as JSON, and generate a preview image.

---

## Installation

### Option 1: Installation with normal Python

Clone the repository and create a virtual environment:

```bash
git clone https://github.com/discosat/image-splitter.git
cd image-splitter
python -m venv .venv
source .venv/bin/activate   # On Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Option 2: Installation using uv

If you have [uv](https://github.com/astral-sh/uv) installed, you can simply run:

```bash
git clone https://github.com/discosat/image-splitter.git
cd image-splitter
uv run image_splitter.py --help
```

---

## Usage

### Option 1: Using Python

You must include the `.py` extension:

```bash
python image_splitter.py <input_file> [-m <metadata.json>] [-o <image.raw>] [--no-preview]
```

### Option 2: Using uv

```bash
uv run image_splitter.py <input_file> [-m <metadata.json>] [-o <image.raw>] [--no-preview]
```

### Arguments

* `<input_file>` — input binary file
* `-m, --meta` — output JSON metadata file (default: `metadata.json`)
* `-o, --output` — output raw image file (default: `image.raw`)
* `--no-preview` — skip generating a preview image

### Example

```bash
python image_splitter.py joe.bin -m meta.json -o raw.bin
```

Or with uv:

```bash
uv run image_splitter.py joe.bin -m meta.json -o raw.bin
```
