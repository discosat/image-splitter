import struct
import json
import argparse
import numpy as np
from PIL import Image
from google.protobuf import json_format
import metadata_pb2 as metadata_pb2


def load_combined_file(filename: str):
    with open(filename, "rb") as f:
        data = f.read()

    # First 4 bytes = metadata size (little-endian unsigned int)
    metadata_size = struct.unpack("<I", data[:4])[0]
    print(f"Metadata size: {metadata_size} bytes")

    metadata_bytes = data[4:4 + metadata_size]
    image_bytes = data[4 + metadata_size:]

    print("metadata bytes ", len(metadata_bytes))
    print("image_bytes ", len(image_bytes))

    return metadata_bytes, image_bytes


def parse_metadata(metadata_bytes: bytes, output_file="metadata.json"):
    msg = metadata_pb2.Metadata()
    msg.ParseFromString(metadata_bytes)

    json_string = json_format.MessageToJson(msg)

    with open(output_file, "w") as file:
        file.write(json_string)

    print(f"Metadata written to {output_file}")
    return json.loads(json_string)


def save_image_data(image_bytes: bytes, image_len: int, output_file="image.raw"):
    with open(output_file, "wb") as f:
        f.write(image_bytes[:image_len])
    print(f"Raw image data written to {output_file}")


def save_preview(image_bytes: bytes, metadata: dict):
    height = metadata["height"]
    width = metadata["width"]
    channels = metadata["channels"]
    size = metadata["size"]
    bpp = metadata["bitsPixel"]

    if bpp == 8:
        dtype = np.uint8
    elif bpp == 16:
        dtype = np.uint16
    elif bpp == 12:
        dtype = np.uint16
    else:
        raise ValueError(f"Bits per pixel value needs to be one of [8, 12, 16]. Got: {bpp}")
 
    print("Parsed metadata:", metadata)

    # Convert raw data → numpy
    img = np.frombuffer(image_bytes[:size], dtype=dtype)

    expected_size = height * width * channels
    if img.size != expected_size:
        raise ValueError(f"Raw data size mismatch: expected {expected_size}, got {img.size}")

    img = img.reshape((height, width, channels))

    # Normalize to 8-bit for preview
    img_8bit = ((img - img.min()) / (img.max() - img.min()) * 255).astype(np.uint8)

    # Choose mode
    if channels == 1:
        pil_img = Image.fromarray(img_8bit.squeeze(), mode="L")
    elif channels == 3:
        pil_img = Image.fromarray(img_8bit, mode="RGB")
    elif channels == 4:
        pil_img = Image.fromarray(img_8bit, mode="RGBA")
    else:
        raise ValueError(f"Unsupported channel count: {channels}")

    outname = f"image_preview_{height}x{width}_{channels}ch.png"
    pil_img.show()
    pil_img.save(outname)
    print(f"Image preview saved as {outname}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Split combined binary file into metadata + raw image, save JSON metadata, and create a preview image."
    )
    parser.add_argument("filename", help="Input combined binary file")
    parser.add_argument("-m", "--meta", default="metadata.json", help="Output metadata JSON file (default: metadata.json)")
    parser.add_argument("-o", "--output", default="image.raw", help="Output raw image file (default: image.raw)")
    parser.add_argument("--no-preview", action="store_true", help="Skip generating preview image")

    args = parser.parse_args()

    # Load combined file
    metadata_bytes, image_bytes = load_combined_file(args.filename)

    # Write metadata
    metadata = parse_metadata(metadata_bytes, args.meta)

    # Write raw image data
    save_image_data(image_bytes, metadata["size"], args.output)

    # Optionally show/save preview
    if not args.no_preview:
        save_preview(image_bytes, metadata)
