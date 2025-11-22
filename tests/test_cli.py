import subprocess
import sys

import pytest

from image_splitter import cli, metadata_pb2

# ------------------------
# Fixtures
# ------------------------


@pytest.fixture
def dummy_metadata_bytes():
    """Return a serialized Metadata protobuf."""
    msg = metadata_pb2.Metadata()
    msg.height = 2
    msg.width = 2
    msg.channels = 1
    msg.size = 4
    msg.bits_pixel = 8
    return msg.SerializeToString()


@pytest.fixture
def dummy_image_bytes():
    """Return a simple 4-byte raw image."""
    return b"\x01\x02\x03\x04"


@pytest.fixture
def dummy_bin_file(tmp_path, dummy_metadata_bytes, dummy_image_bytes):
    """Create a dummy .bin file with metadata + image."""
    metadata_len = len(dummy_metadata_bytes).to_bytes(4, "little")
    file_bytes = metadata_len + dummy_metadata_bytes + dummy_image_bytes
    file_path = tmp_path / "dummy.bin"
    file_path.write_bytes(file_bytes)
    return file_path


# ------------------------
# CLI Integration Test
# ------------------------


def test_cli_runs(tmp_path, dummy_bin_file):
    outdir = tmp_path / "output"
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "image_splitter.cli",
            str(dummy_bin_file),
            "--outdir",
            str(outdir),
        ],
        capture_output=True,
        text=True,
    )

    assert result.returncode == 0
    assert (outdir / "metadata.json").exists()
    assert (outdir / "image.raw").exists()


# ------------------------
# Unit Tests
# ------------------------


def test_load_combined_file_creates_correct_splits(
    dummy_bin_file, dummy_metadata_bytes, dummy_image_bytes
):
    meta_bytes, img_bytes = cli.load_combined_file(dummy_bin_file)
    assert meta_bytes == dummy_metadata_bytes
    assert img_bytes == dummy_image_bytes


def test_parse_metadata_creates_json_file(tmp_path, dummy_metadata_bytes):
    out_file = tmp_path / "metadata.json"
    meta_dict = cli.parse_metadata(dummy_metadata_bytes, out_file)
    assert out_file.exists()
    assert meta_dict["height"] == 2
    assert meta_dict["width"] == 2
    assert meta_dict["channels"] == 1
    assert meta_dict["bitsPixel"] == 8
    assert meta_dict["size"] == 4


def test_save_image_data_writes_file(tmp_path, dummy_image_bytes):
    out_file = tmp_path / "image.raw"
    cli.save_image_data(dummy_image_bytes, len(dummy_image_bytes), out_file)
    assert out_file.exists()
    assert out_file.read_bytes() == dummy_image_bytes


def test_save_preview_creates_image_file(tmp_path, dummy_image_bytes):
    metadata = {"height": 2, "width": 2, "channels": 1, "size": 4, "bitsPixel": 8}
    cli.save_preview(dummy_image_bytes, metadata, tmp_path)
    previews = list(tmp_path.glob("preview_*.png"))
    assert len(previews) == 1
    assert previews[0].exists()


def test_ensure_output_dir_creates_directory(tmp_path):
    outdir = tmp_path / "out"
    result = cli.ensure_output_dir(outdir, force=False)
    assert result.exists()
    assert result.is_dir()


def test_ensure_output_dir_overwrite(tmp_path):
    outdir = tmp_path / "out"
    outdir.mkdir()
    (outdir / "file.txt").write_text("hello")
    result = cli.ensure_output_dir(outdir, force=True)
    assert result.exists()
    assert result.is_dir()
    assert list(result.iterdir()) == []


def test_ensure_output_dir_error(tmp_path):
    outdir = tmp_path / "out"
    outdir.mkdir()
    with pytest.raises(FileExistsError):
        cli.ensure_output_dir(outdir, force=False)
