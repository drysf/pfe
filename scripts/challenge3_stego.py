"""Defi 3 - Steganographie LSB (Least Significant Bit).

Cache et extrait un message dans les bits de poids faible des pixels
d'une image PNG. La passphrase obtenue au defi 2 sert d'autorisation.

Usage:
  python challenge3_stego.py generate          # cree assets/carte_postale.png
  python challenge3_stego.py extract <fichier> # extrait le message
"""
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

from common import FLAG3, STEGO_PASSPHRASE, SOCKET_HOST, SOCKET_PORT, SOCKET_TOKEN

ASSETS = Path(__file__).resolve().parent.parent / "assets"
IMG_PATH = ASSETS / "carte_postale.png"

DELIMITER = "<<<EOF>>>"

PAYLOAD = (
    f"Passphrase: {STEGO_PASSPHRASE} | {FLAG3} | "
    f"Connecte-toi en TCP sur {SOCKET_HOST}:{SOCKET_PORT} "
    f"et envoie la commande 'AUTH {SOCKET_TOKEN}' pour debloquer la suite."
)


def _bits(data: bytes):
    for byte in data:
        for i in range(7, -1, -1):
            yield (byte >> i) & 1


def _bytes_from_bits(bits):
    out = bytearray()
    byte = 0
    for i, b in enumerate(bits):
        byte = (byte << 1) | b
        if i % 8 == 7:
            out.append(byte)
            byte = 0
    return bytes(out)


def hide(image_path: Path, message: str, output: Path):
    img = Image.open(image_path).convert("RGB")
    pixels = list(img.getdata())
    payload = (message + DELIMITER).encode("utf-8")
    bits = list(_bits(payload))
    if len(bits) > len(pixels) * 3:
        raise ValueError("Image trop petite pour le message.")
    new_pixels = []
    bit_iter = iter(bits)
    for r, g, b in pixels:
        new_rgb = []
        for chan in (r, g, b):
            try:
                new_rgb.append((chan & ~1) | next(bit_iter))
            except StopIteration:
                new_rgb.append(chan)
        new_pixels.append(tuple(new_rgb))
    img.putdata(new_pixels)
    img.save(output, "PNG")


def extract(image_path: Path) -> str:
    img = Image.open(image_path).convert("RGB")
    bits = []
    delim_bits = "".join(f"{b:08b}" for b in DELIMITER.encode("utf-8"))
    for r, g, b in img.getdata():
        for chan in (r, g, b):
            bits.append(chan & 1)
            if len(bits) % 8 == 0 and len(bits) >= len(delim_bits):
                tail = "".join(map(str, bits[-len(delim_bits):]))
                if tail == delim_bits:
                    decoded = _bytes_from_bits(bits).decode("utf-8", errors="replace")
                    return decoded[: -len(DELIMITER)]
    return _bytes_from_bits(bits).decode("utf-8", errors="replace")


def make_carrier(path: Path):
    """Cree une image PNG 'carte postale' assez grande pour le payload."""
    width, height = 600, 400
    img = Image.new("RGB", (width, height), (30, 41, 59))
    draw = ImageDraw.Draw(img)
    try:
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 28)
        small = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 16)
    except OSError:
        font = ImageFont.load_default()
        small = ImageFont.load_default()
    draw.rectangle([(20, 20), (width - 20, height - 20)], outline=(56, 189, 248), width=3)
    draw.text((40, 40), "Carte postale de Sophie", fill=(56, 189, 248), font=font)
    draw.text((40, 100), "Greetings from MegaCorp HQ !", fill=(226, 232, 240), font=small)
    draw.text((40, 140), "Tu trouveras de quoi t'amuser dans les pixels...", fill=(148, 163, 184), font=small)
    draw.text((40, 340), "(stego: LSB sur les 3 canaux RGB)", fill=(71, 85, 105), font=small)
    img.save(path, "PNG")


def generate():
    ASSETS.mkdir(exist_ok=True)
    carrier = ASSETS / "_carrier.png"
    make_carrier(carrier)
    hide(carrier, PAYLOAD, IMG_PATH)
    carrier.unlink()
    print(f"[OK] Image stegano ecrite: {IMG_PATH}")


if __name__ == "__main__":
    if len(sys.argv) >= 2 and sys.argv[1] == "generate":
        generate()
    elif len(sys.argv) >= 3 and sys.argv[1] == "extract":
        print(extract(Path(sys.argv[2])))
    else:
        print(__doc__)
