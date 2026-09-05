import struct
from pathlib import Path

from tools.extract_logo_png import extract_png

SVG_PATH = Path(__file__).resolve().parent.parent / "brand_assets" / "softly_by_belle_logo.svg"


def test_extract_png_matches_source_dimensions(tmp_path):
    output_path = tmp_path / "logo.png"

    extract_png(SVG_PATH, output_path)

    data = output_path.read_bytes()
    assert data[:8] == b"\x89PNG\r\n\x1a\n"
    width, height = struct.unpack(">II", data[16:24])
    assert (width, height) == (986, 802)
