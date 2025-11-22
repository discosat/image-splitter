import argparse
import json
import shutil
import struct
from datetime import datetime
from pathlib import Path

import numpy as np
from google.protobuf import json_format
from PIL import Image

import metadata_pb2 as metadata_pb2


def load_combined_file(filename: str):
    with open(filename, "rb") as f:
        data = f.read()

    metadata_size = struct.unpack("<I", data[:4])[0]
    metadata_bytes = data[4 : 4 + metadata_size]
    image_bytes = data[4 + metadata_size :]

    print("metadata bytes ", len(metadata_bytes))
    print("image_bytes ", len(image_bytes))

    return metadata_bytes, image_bytes


def parse_metadata(metadata_bytes: bytes, output_path: Path):
    msg = metadata_pb2.Metadata()
    msg.ParseFromString(metadata_bytes)
    json_string = json_format.MessageToJson(msg)

    with open(output_path, "w") as file:
        file.write(json_string)

    return json.loads(json_string)


def save_image_data(image_bytes: bytes, image_len: int, output_file: Path):
    with open(output_file, "wb") as f:
        f.write(image_bytes[:image_len])
    print(f"Raw image data written to {output_file}")


def save_preview(image_bytes: bytes, metadata: dict, output_dir: Path):
    height = metadata["height"]
    width = metadata["width"]
    channels = metadata["channels"]

    if bpp == 8:
        dtype = np.uint8
    elif bpp == 16:
        dtype = np.uint16
    elif bpp == 12:
        dtype = np.uint16
    else:
        raise ValueError(
            f"Bits per pixel value needs to be one of [8, 12, 16]. Got: {bpp}"
        )

    print("Parsed metadata:", metadata)

    # Convert raw data → numpy
    img = np.frombuffer(image_bytes[:size], dtype=dtype)

    expected_size = height * width * channels
    if img.size != expected_size:
        raise ValueError(
            f"Raw data size mismatch: expected {expected_size}, got {img.size}"
        )

    img = img.reshape((height, width, channels))

    img_8bit = ((img - img.min()) / (img.max() - img.min()) * 255).astype(np.uint8)

    if channels == 1:
        pil_img = Image.fromarray(img_8bit.squeeze())
    elif channels == 3:
        pil_img = Image.fromarray(img_8bit)
    elif channels == 4:
        pil_img = Image.fromarray(img_8bit)
    else:
        raise ValueError(f"Unsupported channel count: {channels}")

    outname = output_dir / f"preview_{height}x{width}_{channels}ch.png"
    pil_img.save(outname)
    print(f"Preview saved to {outname}")


def ensure_output_dir(path: Path, force: bool):
    if path.exists():
        if not force:
            raise FileExistsError(
                f"Output directory {path} already exists. Use --force to overwrite."
            )
        shutil.rmtree(path)

    path.mkdir(parents=True, exist_ok=True)
    return path


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Split combined binary file into metadata + raw image."
    )
    parser.add_argument("filename", help="Input dtp_data.bin file")

    parser.add_argument(
        "--outdir",
        default=None,
        help="Output directory (default: output_YYYYMMDD_HHMMSS)",
    )

    parser.add_argument(
        "--force",
        action="store_true",
        help="Overwrite existing output directory",
    )

    parser.add_argument(
        "--no-preview",
        action="store_true",
        help="Skip generating preview image",
    )

    args = parser.parse_args()

    # Determine output directory
    if args.outdir:
        outdir = Path(args.outdir)
    else:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        outdir = Path(f"output_{timestamp}")

    ensure_output_dir(outdir, args.force)

    # Copy original file
    orig_path = Path(args.filename)
    shutil.copy(orig_path, outdir / orig_path.name)

    # Load and split
    metadata_bytes, image_bytes = load_combined_file(args.filename)

    # Save metadata
    meta_path = outdir / "metadata.json"
    metadata = parse_metadata(metadata_bytes, meta_path)

    # Write raw image data
    raw_path = outdir / "image.raw"
    save_image_data(image_bytes, metadata["size"], raw_path)

    # Preview
    if not args.no_preview:
        save_preview(image_bytes[: metadata["size"]], metadata, outdir)

    print(f"\nAll output saved in: {outdir.resolve()}")
