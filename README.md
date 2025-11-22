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
pip install .
```

### Option 2: Using uv

If you have [uv](https://github.com/astral-sh/uv) installed:

```bash
git clone https://github.com/discosat/image-splitter.git
cd image-splitter
uv run image_splitter.cli --help
```

> After installation with `pip install .` , the CLI can also be run globally as `image-splitter` from anywhere.

---

## Usage

The tool extracts the files into an automatically created output directory named:

```
output_YYYYMMDD_HHMMSS
```

You can also supply a custom output directory.

### Running the tool

#### Globally (after pip install)

```bash
image-splitter <input_file> [--outdir <folder>] [--force] [--no-preview]
```

#### Using Python directly

```bash
python -m image_splitter.cli <input_file> [--outdir <folder>] [--force] [--no-preview]
```

#### Using uv

```bash
uv run image_splitter.cli <input_file> [--outdir <folder>] [--force] [--no-preview]
```

---

## Arguments

### Positional

* **`<input_file>`** — Path to the combined dtp data file (e.g. `dtp_data.bin`).

### Optional arguments

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
image-splitter dtp_data.bin
```

### Custom output directory

```bash
image-splitter dtp_data.bin --outdir results_sat_03
```

### Overwrite existing directory

```bash
image-splitter dtp_data.bin --outdir output --force
```

### Skip preview

```bash
image-splitter dtp_data.bin --no-preview
```

### Using Python directly

```bash
python -m image_splitter.cli dtp_data.bin --outdir ~/Downloads/joe
```

---

## Development & Testing

This project includes automated tests using `pytest`.

### Run tests locally

```bash
pytest -v tests/
```

### GitHub Actions

* Tests are automatically run on every pull request and merge to `main`.
* Branch protection is configured to prevent merging if tests fail.

### Mock Data for Tests

The tests include helper fixtures to generate dummy `.bin` files with valid metadata and image data, so you can run tests without real satellite data.

---

## Versioning

This project uses [Semantic Release](https://python-semantic-release.readthedocs.io/) to automatically bump versions based on **conventional commits**.

* `fix:` → Patch version bump
* `feat:` → Minor version bump
* `BREAKING CHANGE:` → Major version bump

The version is stored in:

```
image_splitter/__init__.py
```

> No automatic PyPI release is done; version is updated locally and committed via the workflow.

---

## Notes

* Preview generation normalizes raw data into 8‑bit PNG.
* Pillow automatically infers image mode (`L`, `RGB`, etc.), so the script does not specify the deprecated `mode=` argument.
* Metadata is parsed from the protobuf definition in `metadata_pb2.py`.
* After `pip install .`, the CLI is available globally as `image-splitter`.

---

## License

MIT License. See `LICENSE` for details.
