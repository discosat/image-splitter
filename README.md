# Image Splitter

A Python CLI tool for extracting **metadata** and **raw image data** from a combined `dtp_data.bin` file. The tool automatically creates an output directory containing:

* The original input file
* `metadata.json`
* `image.raw`
* A preview PNG (optional)

This helps keep all extracted data organized and reproducible.

---

## Installation

### Option 1: Standard Python installation

```bash
git clone https://github.com/discosat/image-splitter.git
cd image-splitter
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Option 2: Using uv

If you have [uv](https://github.com/astral-sh/uv) installed:

```bash
git clone https://github.com/discosat/image-splitter.git
cd image-splitter
uv run image_splitter.py --help
```

---

## Usage

The tool extracts the files into an automatically created output directory named:

```
output_YYYYMMDD_HHMMSS
```

You can also supply a custom output directory.

---

## Running the tool

### Using Python

```bash
python image_splitter.py <input_file> [--outdir <folder>] [--force] [--no-preview]
```

### Using uv

```bash
uv run image_splitter.py <input_file> [--outdir <folder>] [--force] [--no-preview]
```

---

## Arguments

### **Positional**

* **`<input_file>`** — Path to the combined dtp data file (e.g. `dtp_data.bin`).

### **Optional arguments**

| Argument            | Description                                                 |
| ------------------- | ----------------------------------------------------------- |
| `--outdir <folder>` | Specify output directory. Default: `output_YYYYMMDD_HHMMSS` |
| `--force`           | Overwrite output directory if it already exists             |
| `--no-preview`      | Skip generating the preview PNG image                       |

### Legacy / Removed arguments

> The previous `-m / -o` options have been removed.
> Output file names are now automatically generated inside the output folder.

---

## Output Directory Structure

Example:

```
output_20251122_143443/
├── dtp_data.bin
├── metadata.json
├── image.raw
└── preview_2056x2464_1ch.png
```

---

## Examples

### Basic usage

```bash
python image_splitter.py dtp_data.bin
```

### Custom output directory

```bash
python image_splitter.py dtp_data.bin --outdir results_sat_03
```

### Overwrite existing directory

```bash
python image_splitter.py dtp_data.bin --outdir output --force
```

### Using uv

```bash
uv run image_splitter.py dtp_data.bin --no-preview
```

---

## Notes

* Preview generation normalizes raw data into 8‑bit PNG.
* Pillow now automatically infers image mode (`L`, `RGB`, etc.), so the script does not specify the deprecated `mode=` argument.
* Metadata is parsed from the protobuf definition in `metadata_pb2.py`.

---

## License

MIT License. See `LICENSE` for details.
