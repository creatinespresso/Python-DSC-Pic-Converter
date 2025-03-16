# modules/format_png.py

from PIL import Image
from .base_module import ImageFormatBase

class FormatPNG(ImageFormatBase):
    def get_params(self):
        return {
            "PARAM_COMPRESS_LEVEL": {
                "type": "int",
                "default": 6,
                "min": 0,
                "max": 9
            }
        }

    def convert(self, input_path, output_path, options):
        """
        Konvertiert ein beliebiges Bild nach PNG.
        options: z.B. {"PARAM_COMPRESS_LEVEL": 6}
        """
        with Image.open(input_path) as img:
            # PNG kann RGBA
            compress_level = options.get("PARAM_COMPRESS_LEVEL", 6)

            # Pillow: pnginfo oder save-Option 'compress_level'
            img.save(output_path, "PNG", compress_level=compress_level)
