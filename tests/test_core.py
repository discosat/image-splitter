import struct
import tempfile

from image_splitter import cli as image_cli


def test_load_combined_file_creates_correct_splits():
    # Create dummy binary: 4 bytes metadata length + metadata + image
    metadata = b"abc"
    image = b"123456"
    metadata_len = struct.pack("<I", len(metadata))
    combined = metadata_len + metadata + image

    with tempfile.NamedTemporaryFile() as f:
        f.write(combined)
        f.flush()

        meta_bytes, img_bytes = image_cli.load_combined_file(f.name)
        assert meta_bytes == metadata
        assert img_bytes == image


def test_parse_metadata_creates_json_file(tmp_path):
    # Use a dummy protobuf message
    from image_splitter import metadata_pb2

    msg = metadata_pb2.Metadata()
    msg.height = 10
    msg.width = 10
    msg.channels = 1
    msg.size = 100
    msg.bits_pixel = 8
    data = msg.SerializeToString()

    out_path = tmp_path / "meta.json"
    parsed = image_cli.parse_metadata(data, out_path)

    assert out_path.exists()
    assert parsed["height"] == 10
    assert parsed["width"] == 10
