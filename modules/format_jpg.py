# modules/format_jpg.py

from PIL import Image
from .base_module import ImageFormatBase

class FormatJPG(ImageFormatBase):
    def get_params(self):
        return {
            "PARAM_QUALITY": {
                "type": "int",
                "default": 80,
                "min": 0,
                "max": 100
            },
            "PARAM_OPTIMIZE": {
                "type": "bool",
                "default": True
            }
        }

    def convert(self, input_path, output_path, options):
        """
        Konvertiert ein beliebiges Bild nach JPG.
        options: Dictionary mit Parametern (z.B. {"PARAM_QUALITY": 90, "PARAM_OPTIMIZE": True})
        """
        with Image.open(input_path) as img:
            # Standard: RGB, falls Bild nicht bereits RGB ist
            if img.mode not in ("RGB", "RGBA"):
                img = img.convert("RGB")

            quality = options.get("PARAM_QUALITY", 80)
            optimize = options.get("PARAM_OPTIMIZE", True)

            # Speichern als JPG
            img.save(output_path, "JPEG", quality=quality, optimize=optimize)
